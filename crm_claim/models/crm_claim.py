# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, api, fields, models
from odoo.tools import html2plaintext

APPLICABLE_MODELS = [
    "account.invoice",
    "event.registration",
    "hr.applicant",
    "res.partner",
    "product.product",
    "purchase.order",
    "purchase.order.line",
    "sale.order",
    "sale.order.line",
]


class CrmClaim(models.Model):
    _name = "crm.claim"
    _description = "Claim"
    _order = "priority,date desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    @api.model
    def _get_default_stage_id(self):
        """ Gives default stage_id """
        team_id = self.env["crm.team"]._get_default_team_id()
        return self.stage_find(team_id.id, [("sequence", "=", "1")])

    @api.model
    def _get_default_team(self):
        return self.env["crm.team"]._get_default_team_id()

    @api.model
    def _selection_model(self):
        return [
            (x, _(self.env[x]._description)) for x in APPLICABLE_MODELS if x in self.env
        ]

    name = fields.Char(string="Claim Subject", required=True)
    active = fields.Boolean(default=True)
    description = fields.Text()
    resolution = fields.Text()
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    write_date = fields.Datetime(string="Update Date", readonly=True)
    date_deadline = fields.Date(string="Deadline")
    date_closed = fields.Datetime(string="Closed", readonly=True)
    date = fields.Datetime(string="Claim Date", index=True, default=fields.Datetime.now)
    model_ref_id = fields.Reference(
        selection="_selection_model", string="Model Reference"
    )
    categ_id = fields.Many2one(comodel_name="crm.claim.category", string="Category")
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High")], default="1"
    )
    type_action = fields.Selection(
        selection=[
            ("correction", "Corrective Action"),
            ("prevention", "Preventive Action"),
        ],
        string="Action Type",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        track_visibility="always",
        default=lambda self: self.env.user,
    )
    user_fault = fields.Char(string="Trouble Responsible")
    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="Sales Team",
        index=True,
        default=_get_default_team,
        help="Responsible sales team. Define Responsible user and Email "
        "account for mail gateway.",
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Company",
        default=lambda self: self.env.company,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    email_cc = fields.Text(
        string="Watchers Emails",
        help="These email addresses will be added to the CC field of all "
        "inbound and outbound emails for this record before being sent. "
        "Separate multiple email addresses with a comma",
    )
    email_from = fields.Char(
        string="Email", help="Destination email for email gateway."
    )
    partner_phone = fields.Char(string="Phone")
    stage_id = fields.Many2one(
        comodel_name="crm.claim.stage",
        string="Stage",
        track_visibility="onchange",
        default=_get_default_stage_id,
        domain="['|', ('team_ids', '=', team_id), ('case_default', '=', True)]",
    )
    cause = fields.Text(string="Root Cause")

    def stage_find(self, team_id, domain=None, order="sequence"):
        """ Override of the base.stage method
            Parameter of the stage search taken from the lead:
            - team_id: if set, stages must belong to this team or
              be a default case
        """
        if domain is None:  # pragma: no cover
            domain = []
        # collect all team_ids
        team_ids = []
        if team_id:
            team_ids.append(team_id)
        team_ids.extend(self.mapped("team_id").ids)
        search_domain = []
        if team_ids:
            search_domain += ["|"] * len(team_ids)
            for team_id in team_ids:
                search_domain.append(("team_ids", "=", team_id))
        search_domain.append(("case_default", "=", True))
        # AND with the domain in parameter
        search_domain += list(domain)
        # perform search, return the first found
        return (
            self.env["crm.claim.stage"].search(search_domain, order=order, limit=1).id
        )

    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """This function returns value of partner address based on partner
           :param email: ignored
        """
        if self.partner_id:
            self.email_from = self.partner_id.email
            self.partner_phone = self.partner_id.phone

    @api.onchange("categ_id")
    def onchange_categ_id(self):
        if self.stage_id:
            self.team_id = self.categ_id.team_id

    @api.model
    def create(self, values):
        ctx = self.env.context.copy()
        if values.get("team_id") and not ctx.get("default_team_id"):
            ctx["default_team_id"] = values.get("team_id")
        return super(CrmClaim, self.with_context(context=ctx)).create(values)

    def copy(self, default=None):
        default = dict(
            default or {},
            stage_id=self._get_default_stage_id(),
            name=_("%s (copy)") % self.name,
        )
        return super(CrmClaim, self).copy(default)

    # -------------------------------------------------------
    # Mail gateway
    # -------------------------------------------------------
    @api.model
    def message_new(self, msg, custom_values=None):
        """ Overrides mail_thread message_new that is called by the mailgateway
            through message_process.
            This override updates the document according to the email.
        """
        if custom_values is None:
            custom_values = {}
        desc = html2plaintext(msg.get("body")) if msg.get("body") else ""
        defaults = {
            "name": msg.get("subject") or _("No Subject"),
            "description": desc,
            "email_from": msg.get("from"),
            "email_cc": msg.get("cc"),
            "partner_id": msg.get("author_id", False),
        }
        if msg.get("priority"):
            defaults["priority"] = msg.get("priority")
        defaults.update(custom_values)
        return super(CrmClaim, self).message_new(msg, custom_values=defaults)
