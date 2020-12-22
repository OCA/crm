# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from functools import reduce

from odoo import _, api, fields, models


class CrmPhonecall(models.Model):
    """Model for CRM phonecalls."""

    _name = "crm.phonecall"
    _description = "Phonecall"
    _order = "id desc"
    _inherit = ["mail.thread", "utm.mixin", "mail.activity.mixin"]

    date_action_last = fields.Datetime(string="Last Action", readonly=True)
    date_action_next = fields.Datetime(string="Next Action", readonly=True)
    create_date = fields.Datetime(string="Creation Date", readonly=True)
    team_id = fields.Many2one(
        comodel_name="crm.team",
        string="Sales Team",
        index=True,
        help="Sales team to which Case belongs to.",
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Responsible",
        default=lambda self: self.env.user,
    )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Contact")
    company_id = fields.Many2one(comodel_name="res.company", string="Company")
    description = fields.Text()
    state = fields.Selection(
        [
            ("open", "Confirmed"),
            ("cancel", "Cancelled"),
            ("pending", "Pending"),
            ("done", "Held"),
        ],
        string="Status",
        track_visibility="onchange",
        default="open",
        help="The status is set to Confirmed, when a case is created.\n"
        "When the call is over, the status is set to Held.\n"
        "If the callis not applicable anymore, the status can be set "
        "to Cancelled.",
    )
    email_from = fields.Char(string="Email", help="These people will receive email.")
    date_open = fields.Datetime(string="Opened", readonly=True)
    name = fields.Char(string="Call Summary", required=True)
    active = fields.Boolean(required=False, default=True)
    duration = fields.Float(help="Duration in minutes and seconds.")
    tag_ids = fields.Many2many(
        comodel_name="crm.lead.tag",
        relation="crm_phonecall_tag_rel",
        column1="phone_id",
        column2="tag_id",
        string="Tags",
    )
    partner_phone = fields.Char(string="Phone")
    partner_mobile = fields.Char("Mobile")
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High")],
        string="Priority",
        default="1",
    )
    date_closed = fields.Datetime(string="Closed", readonly=True)
    date = fields.Datetime(default=lambda self: fields.Datetime.now())
    opportunity_id = fields.Many2one(comodel_name="crm.lead", string="Lead/Opportunity")
    direction = fields.Selection(
        [("in", "In"), ("out", "Out")], default="out", required=True
    )

    @api.onchange("partner_id")
    def on_change_partner_id(self):
        """Contact number details should be change based on partner."""
        if self.partner_id:
            self.partner_phone = self.partner_id.phone
            self.partner_mobile = self.partner_id.mobile

    def write(self, values):
        """Override to add case management: open/close dates."""
        if values.get("state"):
            if values.get("state") == "done":
                values["date_closed"] = fields.Datetime.now()
                self.compute_duration()
            elif values.get("state") == "open":
                values["date_open"] = fields.Datetime.now()
                values["duration"] = 0.0
        return super().write(values)

    def compute_duration(self):
        """Calculate duration based on phonecall date."""
        phonecall_dates = self.filtered("date")
        phonecall_no_dates = self - phonecall_dates
        for phonecall in phonecall_dates:
            if phonecall.duration <= 0 and phonecall.date:
                duration = fields.Datetime.now() - phonecall.date
                values = {"duration": duration.seconds / 60.0}
                phonecall.write(values)
            else:
                phonecall.duration = 0.0
        phonecall_no_dates.write({"duration": 0.0})
        return True

    def get_values_schedule_another_phonecall(self, vals):
        res = {
            "name": vals.get("name"),
            "user_id": vals.get("user_id") or self.user_id.id or False,
            "description": self.description or False,
            "date": vals.get("schedule_time") or self.date,
            "team_id": vals.get("team_id") or self.team_id.id or False,
            "partner_id": self.partner_id.id or False,
            "partner_phone": self.partner_phone,
            "partner_mobile": self.partner_mobile,
            "priority": self.priority,
            "opportunity_id": self.opportunity_id.id or False,
            "campaign_id": self.campaign_id.id,
            "source_id": self.source_id.id,
            "medium_id": self.medium_id.id,
        }
        if vals.get("tag_ids"):
            res.update({"tag_ids": [(6, 0, vals.get("tag_ids"))]})
        return res

    def schedule_another_phonecall(self, vals, return_recordset=False):
        """Action :('schedule','Schedule a call'), ('log','Log a call')."""
        phonecall_dict = {}
        for call in self:
            values = call.get_values_schedule_another_phonecall(vals)
            new_id = self.create(values)
            if vals.get("action") == "log":
                call.write({"state": "done"})
            phonecall_dict[call.id] = new_id
        if return_recordset:
            return reduce(lambda x, y: x + y, phonecall_dict.values())
        else:
            return phonecall_dict

    @api.onchange("opportunity_id")
    def on_change_opportunity(self):
        """Based on opportunity, changed contact, tags, partner, team."""
        if self.opportunity_id:
            self.team_id = self.opportunity_id.team_id.id
            self.partner_phone = self.opportunity_id.phone
            self.partner_mobile = self.opportunity_id.mobile
            self.partner_id = self.opportunity_id.partner_id.id
            self.tag_ids = self.opportunity_id.tag_ids.ids

    def redirect_phonecall_view(self):
        """Redirect on the phonecall related view."""
        model_data = self.env["ir.model.data"]
        # Select the view
        tree_view = model_data.get_object_reference(
            "crm_phonecall", "crm_case_phone_tree_view"
        )
        form_view = model_data.get_object_reference(
            "crm_phonecall", "crm_case_phone_form_view"
        )
        search_view = model_data.get_object_reference(
            "crm_phonecall", "view_crm_case_phonecalls_filter"
        )
        value = {}
        for call in self:
            value = {
                "name": _("Phone Call"),
                "view_type": "form",
                "view_mode": "tree,form",
                "res_model": "crm.phonecall",
                "res_id": call.id,
                "views": [
                    (form_view and form_view[1] or False, "form"),
                    (tree_view and tree_view[1] or False, "tree"),
                    (False, "calendar"),
                ],
                "type": "ir.actions.act_window",
                "search_view_id": search_view and search_view[1] or False,
            }
        return value

    def convert_opportunity(
        self,
        opportunity_summary=False,
        partner_id=False,
        planned_revenue=0.0,
        probability=0.0,
    ):
        """Convert lead to opportunity."""
        partner = self.env["res.partner"]
        opportunity = self.env["crm.lead"]
        opportunity_dict = {}
        default_contact = False
        for call in self:
            if not partner_id:
                partner_id = call.partner_id.id or False
            if partner_id:
                address_id = partner.address_get().get("contact", False)
                if address_id:
                    default_contact = address_id.id
            opportunity_id = opportunity.create(
                {
                    "name": opportunity_summary or call.name,
                    "planned_revenue": planned_revenue,
                    "probability": probability,
                    "partner_id": partner_id or False,
                    "mobile": default_contact and default_contact.mobile,
                    "team_id": call.team_id.id or False,
                    "description": call.description or False,
                    "priority": call.priority,
                    "type": "opportunity",
                    "phone": call.partner_phone or False,
                    "email_from": default_contact and default_contact.email,
                    "campaign_id": call.campaign_id.id,
                    "source_id": call.source_id.id,
                    "medium_id": call.medium_id.id,
                    "tag_ids": [(6, 0, call.tag_ids.ids)],
                }
            )
            vals = {
                "partner_id": partner_id,
                "opportunity_id": opportunity_id.id,
                "state": "done",
            }
            call.write(vals)
            opportunity_dict[call.id] = opportunity_id
        return opportunity_dict

    def action_make_meeting(self):
        """Open meeting's calendar view to schedule a meeting on phonecall."""
        partner_ids = [self.env["res.users"].browse(self.env.uid).partner_id.id]
        res = {}
        for phonecall in self:
            if phonecall.partner_id and phonecall.partner_id.email:
                partner_ids.append(phonecall.partner_id.id)
            res = self.env["ir.actions.act_window"].for_xml_id(
                "calendar", "action_calendar_event"
            )
            res["context"] = {
                "default_phonecall_id": phonecall.id,
                "default_partner_ids": partner_ids,
                "default_user_id": self.env.uid,
                "default_email_from": phonecall.email_from,
                "default_name": phonecall.name,
            }
        return res

    def action_button_convert2opportunity(self):
        """Convert a phonecall into an opp and redirect to the opp view."""
        opportunity_dict = {}
        for call in self:
            opportunity_dict = call.convert_opportunity()
            return opportunity_dict[call.id].redirect_lead_opportunity_view()
        return opportunity_dict
