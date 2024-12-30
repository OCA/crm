# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models
from odoo.tools.misc import clean_context


class CrmLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many("project.task", "lead_id")
    task_count = fields.Integer("#Task", compute="_compute_task_count")

    @api.depends("task_ids")
    def _compute_task_count(self):
        domain = [("lead_id", "!=", False)]
        data = self.env["project.task"].read_group(
            domain, fields=["lead_id"], groupby=["lead_id"]
        )
        result = {d.get("lead_id")[0]: d.get("lead_id_count") for d in data}
        for lead in self:
            lead.task_count = result.get(lead.id, 0)

    def action_tasks(self):
        self.ensure_one()
        ctx = clean_context(self.env.context.copy())
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "project.action_view_task"
        )
        ctx.update({"default_lead_id": self.id})
        action.update({"context": ctx, "domain": [("lead_id", "=", self.id)]})
        return action
