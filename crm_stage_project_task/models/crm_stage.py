from odoo import fields, models


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
    has_default_project = fields.Boolean(compute="_compute_has_default_project")

    def _compute_has_default_project(self):
        self.write({"has_default_project": bool(self.env.company.stage_project_id)})
