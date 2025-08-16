from odoo import _, api, fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")
    lead_stage_id = fields.Many2one("crm.stage")
    crm_task_template_id = fields.Many2one("crm.task.template")

    def action_open_project_task(self):
        """Action to open task record"""
        self.ensure_one()
        return {
            "name": _("Task: %s", self.name),
            "type": "ir.actions.act_window",
            "res_model": "project.task",
            "view_mode": "form",
            "res_id": self.id,
            "target": "current",
        }

    @api.model_create_multi
    def create(self, vals_list):
        # Attaching subtasks to a CRM lead if the parent has a lead_id set
        for vals in vals_list:
            parent_id = vals.get("parent_id", False)
            if not parent_id:
                continue
            parent = self.browse(parent_id).exists()
            if parent and parent.lead_id:
                vals.update(
                    lead_id=parent.lead_id.id, lead_stage_id=parent.lead_stage_id.id
                )
        return super().create(vals_list)
