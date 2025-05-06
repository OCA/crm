# 2025 Moval Agroingeniería
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class RegistryConfiguration(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'res.registry.config.settings'
    _description = 'Configuration of Register Management'

    allow_number_edition = fields.Boolean(
        string='Allow number edition',
        config_parameter='res_registry_config.allow_number_edition',
        help='Allow to edit the register number during creation.',
    )
