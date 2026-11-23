from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    group_show_form_view = fields.Boolean(
        "Enable form view for phone calls",
        help="By default form is disabled for calls, with this group it is enabled.",
        implied_group="crm_phonecall.group_show_form_view",
        default=True,
    )
