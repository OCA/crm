# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from collections import defaultdict
from datetime import timedelta

from markupsafe import Markup

from odoo import Command, api, fields, models
from odoo.exceptions import ValidationError
from odoo.fields import Domain

_logger = logging.getLogger(__name__)

ESCALATION_BATCH_SIZE = 1000


class CrmLeadEscalationRule(models.Model):
    _name = "crm.lead.escalation.rule"
    _description = "CRM Lead Escalation Rule"
    _order = "sequence, id"
    _check_company_auto = True

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one(
        "res.company",
        default=lambda self: self.env.company,
        ondelete="cascade",
        help="Leave empty to apply the rule in every company.",
    )
    trigger = fields.Selection(
        [
            ("no_followup", "No follow-up"),
            ("not_closed", "Not won nor lost"),
        ],
        required=True,
        default="no_followup",
        help="No follow-up: the delay runs from the last time somebody worked "
        "on the lead.\n"
        "Not won nor lost: the delay runs from the creation of the lead.",
    )
    delay_value = fields.Integer(required=True, default=3, aggregator=False)
    delay_unit = fields.Selection(
        [
            ("minutes", "Minutes"),
            ("hours", "Hours"),
            ("days", "Days"),
        ],
        required=True,
        default="days",
    )
    team_ids = fields.Many2many(
        "crm.team",
        string="Sales Teams",
        check_company=True,
        help="Leave empty to apply the rule to every sales team.",
    )
    lead_type = fields.Selection(
        [
            ("all", "Leads and Opportunities"),
            ("lead", "Leads"),
            ("opportunity", "Opportunities"),
        ],
        required=True,
        default="all",
    )
    assigned_only = fields.Boolean(
        string="Assigned Leads Only",
        default=True,
        help="Only escalate leads that already have a salesperson.",
    )
    recipient_type = fields.Selection(
        [
            ("team_leader", "Sales Team Leader"),
            ("user", "Specific User"),
        ],
        string="Notify",
        required=True,
        default="team_leader",
    )
    recipient_user_id = fields.Many2one(
        "res.users",
        string="Recipient",
        domain=[("share", "=", False)],
        check_company=True,
        ondelete="restrict",
    )
    assign_recipient = fields.Boolean(
        string="Assign Lead to Recipient",
        help="Make the notified user the salesperson of the escalated lead.",
    )
    mail_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        domain=[("model", "=", "crm.lead")],
        ondelete="restrict",
        default=lambda self: self.env.ref(
            "crm_lead_escalation.mail_template_crm_lead_escalation",
            raise_if_not_found=False,
        ),
        help="Leave empty to only schedule an activity, without sending an email.",
    )
    delay_display = fields.Char(compute="_compute_delay_display")

    _delay_value_positive = models.Constraint(
        "CHECK(delay_value > 0)",
        "The escalation delay must be strictly positive.",
    )

    def _get_delay_unit_label(self):
        """Translatable, lowercase label of the delay unit."""
        self.ensure_one()
        return {
            "minutes": self.env._("minutes"),
            "hours": self.env._("hours"),
            "days": self.env._("days"),
        }[self.delay_unit]

    @api.depends("delay_value", "delay_unit")
    def _compute_delay_display(self):
        for rule in self:
            rule.delay_display = self.env._(
                "%(value)s %(unit)s",
                value=rule.delay_value,
                unit=rule._get_delay_unit_label(),
            )

    @api.constrains("recipient_type", "recipient_user_id")
    def _check_recipient_user_id(self):
        for rule in self:
            if rule.recipient_type == "user" and not rule.recipient_user_id:
                raise ValidationError(
                    self.env._(
                        "Rule %s must define the user to notify.", rule.display_name
                    )
                )

    def _get_delay(self):
        self.ensure_one()
        return timedelta(**{self.delay_unit: self.delay_value})

    def _get_date_field(self):
        """Field holding the moment the escalation delay runs from."""
        self.ensure_one()
        return "last_followup_date" if self.trigger == "no_followup" else "create_date"

    def _get_recipient_domain(self):
        """Extra conditions making sure the rule can resolve a recipient.

        Leads that can never resolve one would otherwise come back on every
        run and, once they fill a whole batch, starve the queue.
        """
        self.ensure_one()
        if self.recipient_type == "team_leader":
            return Domain("team_id.user_id", "!=", False)
        return Domain([])

    def _get_lead_domain(self):
        """Leads this rule has to escalate right now."""
        self.ensure_one()
        deadline = self.env.cr.now() - self._get_delay()
        domain = Domain(
            [
                ("active", "=", True),
                ("won_status", "=", "pending"),
                ("escalation_rule_ids", "not in", self.ids),
                (self._get_date_field(), "<=", deadline),
            ]
        )
        domain &= self._get_recipient_domain()
        if self.assigned_only:
            domain &= Domain("user_id", "!=", False)
        if self.team_ids:
            domain &= Domain("team_id", "in", self.team_ids.ids)
        if self.lead_type != "all":
            domain &= Domain("type", "=", self.lead_type)
        if self.company_id:
            domain &= Domain(
                "company_id",
                "in",
                [False] + self.company_id.child_ids.ids + self.company_id.ids,
            )
        return domain

    def _get_recipient(self, lead):
        """User notified for ``lead``, empty recordset when there is none."""
        self.ensure_one()
        if self.recipient_type == "user":
            recipient = self.recipient_user_id
        else:
            recipient = lead.team_id.user_id
        return recipient.filtered(lambda user: user.active and not user.share)

    def _notify_recipient(self, leads, recipient):
        """Warn ``recipient`` about ``leads``, in their own language."""
        self.ensure_one()
        rule = self.with_context(lang=recipient.lang)
        note = Markup("<p>%s</p>") % rule.env._(
            "This lead has not moved forward for %(delay)s %(unit)s.",
            delay=rule.delay_value,
            unit=rule._get_delay_unit_label(),
        )
        # The escalation activity itself must not count as a follow-up.
        activities = leads.with_context(
            crm_lead_escalation=True, lang=recipient.lang
        ).activity_schedule(
            "mail.mail_activity_data_todo",
            user_id=recipient.id,
            summary=rule.name,
            note=note,
        )
        if not activities:
            _logger.warning(
                "Escalation rule %s could not schedule activities on leads %s.",
                self.display_name,
                leads.ids,
            )
        if self.mail_template_id and recipient.partner_id:
            self.mail_template_id.sudo().with_context(
                lang=recipient.lang
            ).send_mail_batch(
                leads.ids,
                email_values={
                    "recipient_ids": [Command.link(recipient.partner_id.id)],
                },
                email_layout_xmlid="mail.mail_notification_light",
            )

    def _escalate_batch(self, leads, recipient):
        """Escalate the ``leads`` sharing the same ``recipient``."""
        self.ensure_one()
        if self.assign_recipient:
            to_assign = leads.filtered(lambda lead: lead.user_id != recipient)
            # Skip the follow-up reset: the reassignment is the escalation
            # itself, not somebody working on the lead.
            to_assign.with_context(crm_lead_escalation=True).user_id = recipient
        self._notify_recipient(leads, recipient)

    def _escalate(self, leads):
        """Escalate ``leads``, already selected by ``_get_lead_domain``."""
        self.ensure_one()
        leads_by_recipient = defaultdict(list)
        orphan_ids = []
        for lead in leads:
            recipient = self._get_recipient(lead)
            if recipient:
                leads_by_recipient[recipient].append(lead.id)
            else:
                orphan_ids.append(lead.id)
        if orphan_ids:
            _logger.warning(
                "Escalation rule %s found no recipient for leads %s. They are "
                "marked as escalated so that they do not block the queue.",
                self.display_name,
                orphan_ids,
            )
        escalated_ids = list(orphan_ids)
        for recipient, lead_ids in leads_by_recipient.items():
            batch = self.env["crm.lead"].browse(lead_ids)
            try:
                # One unrenderable template or one unreadable lead must not
                # roll back the escalations of every other recipient.
                with self.env.cr.savepoint():
                    self._escalate_batch(batch, recipient)
            except Exception:
                _logger.exception(
                    "Escalation rule %s failed to notify %s about leads %s.",
                    self.display_name,
                    recipient.display_name,
                    lead_ids,
                )
                continue
            escalated_ids += lead_ids
        escalated = self.env["crm.lead"].browse(escalated_ids)
        escalated.escalation_rule_ids = [Command.link(self.id)]
        return escalated

    @api.model
    def _cron_escalate_leads(self, limit=ESCALATION_BATCH_SIZE):
        lead_model = self.env["crm.lead"]
        for rule in self.search([("active", "=", True)]):
            leads = lead_model.search(rule._get_lead_domain(), limit=limit)
            if not leads:
                continue
            rule._escalate(leads)
            if (
                self.env.context.get("ir_cron_progress_id")
                and self.env["ir.cron"]._commit_progress(len(leads)) <= 0
            ):
                break
