from odoo import api, fields, models

from odoo.addons.project.models.project_task import CLOSED_STATES


class ProjectTask(models.Model):
    _inherit = "project.task"

    lead_id = fields.Many2one("crm.lead")
    lead_stage_id = fields.Many2one("crm.stage")
    crm_task_template_id = fields.Many2one("crm.task.template")

    def _has_closed_states(self) -> bool:
        """
        Has all task closed states

        Returns:
            bool: If all tasks have a closed state,
                returns True, otherwise returns False.
        """
        for record in self:
            if record.state not in CLOSED_STATES:
                return False
        return True

    @api.model
    def _attach_subtask_to_lead(self, parent_id: int) -> dict:
        """
        Attach subtasks to a CRM lead if the parent has a lead_id set

        Arguments:
            parent_id (int): project task record id
        Returns:
            dict: vals dict with lead record id and crm stage record id
        """
        if parent_id:
            parent = self.browse([parent_id]).exists()
            if parent and parent.lead_id:
                return {
                    "lead_id": parent.lead_id.id,
                    "lead_stage_id": parent.lead_stage_id.id,
                }
        return {}

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.update(**self._attach_subtask_to_lead(vals.get("parent_id", False)))
        return super().create(vals_list)
