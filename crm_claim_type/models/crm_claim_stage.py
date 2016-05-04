# -*- coding: utf-8 -*-
# © 2015 Vauxoo
# © 2013 Camptocamp
# © 2009-2013 Akretion
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CrmClaimStage(models.Model):

    _inherit = 'crm.claim.stage'

    claim_type = fields.Many2one(
        'crm.claim.type',
        help="Claim classification"
    )

    claim_common = fields.Boolean(string='Common to All Claim Types',
                                  help="If you check this field,"
                                  " this stage will be proposed"
                                  " by default on each claim type.")
