# Copyright 2009-2013 Akretion
# Copyright 2013 Camptocamp
# Copyright 2015 Vauxoo
# Copyright 2017 URSA Information Systems
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmClaimStage(models.Model):

    _inherit = "crm.claim.stage"

    claim_type = fields.Many2one("crm.claim.type", help="Claim classification")

    claim_common = fields.Boolean(
        string="Common to All Claim Types",
        help="If you check this field,"
        " this stage will be proposed"
        " by default on each claim type.",
    )
