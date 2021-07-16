# Copyright 2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = ["res.partner", "mailchimp.mixin"]
