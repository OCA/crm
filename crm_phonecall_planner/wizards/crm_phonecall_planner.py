# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from __future__ import division
from datetime import datetime, timedelta
from logging import getLogger
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval

_logger = getLogger(__name__)


class CrmPhonecallPlan(models.TransientModel):
    _name = "crm.phonecall.planner"
    _description = "Phonecall planner"
    _inherit = [
        "utm.mixin",
    ]

    name = fields.Char(
        "Call Summary",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
    )
    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="Sales Team",
    )
    tag_ids = fields.Many2many(
        comodel_name="crm.lead.tag",
        string="Tags",
    )
    res_partner_domain = fields.Char(
        "Partners filter",
        help="Filter the parters that will get a scheduled call.",
    )
    duration = fields.Float(
        string="Call duration",
        default=lambda self: self._default_duration(),
        required=True,
        help="Leave this free time between phone calls.",
    )
    start = fields.Datetime(
        default=lambda self: self._default_start(),
        required=True,
        help="Schedule calls from this moment. The time you select will be "
             "used as the plan starting time for each day in the range.",
    )
    end = fields.Datetime(
        default=lambda self: self._default_end(),
        required=True,
        help="Schedule calls until this moment. The time you select will be "
             "used as the plan ending time for each day in the range.",
    )
    repeat_calls = fields.Boolean(
        help="Allow repeated calls for the same partner, campaign, medium "
             "and source combination?",
    )
    days_gap = fields.Integer(
        default=1,
        required=True,
        help="Schedule one call each X days to the same partner."
    )
    planned_calls = fields.Many2many(
        comodel_name="crm.phonecall",
    )

    @api.model
    def _default_duration(self):
        return 7 / 60  # 7 minutes

    @api.model
    def _default_start(self):
        return fields.Datetime.now()

    @api.model
    def _default_end(self):
        return self._default_start() + timedelta(days=30, hours=8)

    @api.constrains("start", "end")
    def _constrains_plan_dates(self):
        for one in self:
            if one.start > one.end:
                raise ValidationError(
                    _("Starting date must be less than ending date"))

    @api.multi
    def action_accept(self):
        """Generate phonecall plan according to given criteria."""
        self.ensure_one()
        Phonecall = self.env["crm.phonecall"]
        Partner = self.env["res.partner"]
        # Prepare all required time variables
        start = self.start
        end = self.end
        call_duration = timedelta(hours=self.duration)
        now = start - call_duration
        repetition_gap = timedelta(days=self.days_gap)
        tomorrow = timedelta(days=1) - call_duration
        oldest_call_to_partner = u"""
            SELECT res_partner.id
            FROM res_partner
            LEFT JOIN crm_phonecall
            ON res_partner.id = crm_phonecall.partner_id
            WHERE res_partner.id IN ({})
            GROUP BY res_partner.id
            ORDER BY COUNT(crm_phonecall.id), MAX(crm_phonecall.date)
            LIMIT 1
        """
        # Get preexisting calls
        utm_domain = [
            ("campaign_id", "=", self.campaign_id.id),
            ("source_id", "=", self.source_id.id),
            ("medium_id", "=", self.medium_id.id),
        ]
        existing_calls = Phonecall.search(
            utm_domain + [
                ("partner_id", "!=", False),
            ],
            order="date",
        )
        # Get partners to plan
        partner_domain = safe_eval(self.res_partner_domain or "[]") + [
            ("phonecall_calendar_ids", "!=", False),
        ]
        forbidden_partners = existing_calls.mapped("partner_id")
        partners = Partner.search(partner_domain)
        # And now the hot chili...
        while partners and now <= end:
            now += call_duration
            _logger.debug(
                "Plannig phonecalls for %s",
                fields.Datetime.to_string(now),
            )
            # Should we continue tomorrow?
            if not start.time() <= now.time() <= end.time():
                _logger.info(
                    "Finished plannig phonecalls for %s with %d calls so far",
                    fields.Date.to_string(now.date()),
                    len(self.planned_calls),
                )
                now = datetime.combine(now.date(), start.time()) + tomorrow
                continue
            # Know partners that we cannot call right now
            if self.repeat_calls:
                forbidden_partners = Phonecall.search(utm_domain + [
                    ("partner_id", "in", partners.ids),
                    ("date", ">",
                     fields.Datetime.to_string(now - repetition_gap)),
                ]).mapped("partner_id")
            # Know partners we can call right now
            available_partners = Partner.with_context(now=now).search([
                ("id", "in", partners.ids),
                ("id", "not in", forbidden_partners.ids),
                ("phonecall_available", "=", True),
            ])
            # Continue when nobody is available
            if not available_partners:
                continue
            # Just pick the first one and continue
            if not self.repeat_calls:
                winner = available_partners[:1]
                self._schedule_call(winner, now)
                partners -= winner
                continue
            # Get a partner with no calls, or with the oldest one
            self.env.cr.execute(
                oldest_call_to_partner.format(
                    ",".join(["%s"] * len(available_partners)),
                ),
                available_partners.ids,
            )
            winner = Partner.browse(self.env.cr.fetchone()[0])
            self._schedule_call(winner, now)
        _logger.info("Total planned phonecalls: %d", len(self.planned_calls))
        return {
            "name": "Generated calls",
            "type": "ir.actions.act_window",
            "res_model": "crm.phonecall",
            "views": [[False, "tree"], [False, "calendar"], [False, "form"]],
            "domain": [("id", "in", self.planned_calls.ids)],
        }

    @api.multi
    def _schedule_call(self, partner, when):
        _logger.debug(
            "Planning a call for %s at %s",
            partner.display_name,
            fields.Datetime.to_string(when),
        )
        self.planned_calls |= self.env["crm.phonecall"].create({
            "campaign_id": self.campaign_id.id,
            "date": when,
            "duration": self.duration,
            "medium_id": self.medium_id.id,
            "partner_mobile": partner.mobile,
            "name": self.name,
            "partner_id": partner.id,
            "partner_phone": partner.phone,
            "source_id": self.source_id.id,
            "tag_ids": [(6, 0, self.tag_ids.ids)],
            "team_id": self.team_id.id,
            "user_id": self.user_id.id,
        })
