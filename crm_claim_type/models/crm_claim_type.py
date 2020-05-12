# Copyright 2015 Vauxoo: Yanina Aular <yani@vauxoo.com>,
#                        Osval Reyes <osval@vauxoo.com>
# Copyright 2017 Bhavesh Odedra <bodedra@ursainfosystems.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmClaimType(models.Model):
    """
        CRM Claim Type
    """
    _name = 'crm.claim.type'
    _description = "Claim Type"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Text(translate=True)
