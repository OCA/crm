# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models
from odoo.tools.safe_eval import safe_eval


class CrmLead(models.Model):
    """Added the phonecall related details in the lead."""

    _inherit = "crm.lead"

    phonecall_ids = fields.One2many(
        comodel_name="crm.phonecall", inverse_name="opportunity_id", string="Phonecalls"
    )
    phonecall_count = fields.Integer(compute="_compute_phonecall_count")

    def _compute_phonecall_count(self):
        """Calculate number of phonecalls."""
        phonecall_data = self.env["crm.phonecall"]._read_group(
            domain=[("opportunity_id", "in", self.ids)],
            groupby=["opportunity_id"],
            aggregates=["opportunity_id:count"],
        )
        mapped_data = {p[0].id: p[1] for p in phonecall_data}
        for lead in self:
            count = mapped_data.get(lead.id, 0)
            lead.phonecall_count = count

    def button_open_phonecall(self):
        self.ensure_one()
        action_dict = self.env["ir.actions.act_window"]._for_xml_id(
            "crm_phonecall.crm_case_categ_phone_incoming0"
        )
        action_dict["context"] = safe_eval(action_dict.get("context", "{}"))
        action_dict["context"].update(
            {
                "default_opportunity_id": self.id,
                "search_default_opportunity_id": self.id,
                "default_partner_id": self.partner_id.id,
                "default_duration": 1.0,
            }
        )
        return action_dict
