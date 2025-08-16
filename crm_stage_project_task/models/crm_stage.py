from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class CrmStage(models.Model):
    _inherit = "crm.stage"

    check_task_state = fields.Boolean(
        string="Validate Task Completion",
        help="All stage tasks must be Done/Canceled before pipeline progression",
    )
    task_template_ids = fields.One2many(
        "crm.task.template",
        "stage_id",
    )

    @api.constrains("task_template_ids")
    def _check_task_template_ids(self):
        if not self.env.company.stage_project_id:
            raise ValidationError(_("'CRM State Default Project' value is not set!"))
