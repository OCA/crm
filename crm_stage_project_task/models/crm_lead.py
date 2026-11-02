import logging

from odoo import _, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class CRMLead(models.Model):
    _inherit = "crm.lead"

    task_ids = fields.One2many("project.task", "lead_id")

    def _can_change_stage(self) -> bool:
        """
        Check update stage with tasks
        """
        for record in self:
            if (
                record.stage_id.check_task_state
                and not record.task_ids._has_closed_states()
            ):
                return False
        return True

    def _create_tasks_by_template(self):
        """Create tasks by stage"""
        for record in self:
            # Obtaining templates that have not yet been created
            template_to_create = (
                record.stage_id.task_template_ids - record.task_ids.crm_task_template_id
            )
            if not template_to_create:
                continue
            # Creating tasks based on templates
            tasks = template_to_create.create_crm_tasks(record)
            _logger.info(
                f"Tasks #ID {tasks.ids} were created for CRM lead #ID {record.id}"
            )

    def write(self, vals):
        stage_id = vals.get("stage_id")
        if stage_id:
            # Checking the possibility of changing stage_id
            state = self._can_change_stage()
            if not state:
                raise UserError(
                    _(
                        "Changing the stage is not possible "
                        "because the tasks have not been completed!"
                    )
                )
        result = super().write(vals)
        if stage_id:
            # Creating tasks based on stage
            self._create_tasks_by_template()
        return result
