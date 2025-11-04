# Copyright 2021 Sygel - Valentin Vinagre
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    salesperson_planner_visit_count = fields.Integer(
        string="Number of Salesperson Visits",
        compute="_compute_salesperson_planner_visit_count",
    )

    def _compute_salesperson_planner_visit_count(self):
        partners = self | self.mapped("child_ids")
        partner_data = self.env["crm.salesperson.planner.visit"].read_group(
            [("partner_id", "in", partners.ids)], ["partner_id"], ["partner_id"]
        )
        mapped_data = {m["partner_id"][0]: m["partner_id_count"] for m in partner_data}
        for partner in self:
            visit_count = mapped_data.get(partner.id, 0)
            for child in partner.child_ids:
                visit_count += mapped_data.get(child.id, 0)
            partner.salesperson_planner_visit_count = visit_count

    def action_view_salesperson_planner_visit(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "crm_salesperson_planner.all_crm_salesperson_planner_visit_action"
        )
        operator = "child_of" if self.is_company else "="
        action["domain"] = [("partner_id", operator, self.id)]
        return action
