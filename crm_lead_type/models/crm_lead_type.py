# Copyright (C) 2020 Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class CRMLeadType(models.Model):
    _name = "crm.lead.type"
    _description = "CRM Lead Type"

    name = fields.Char("Name")
