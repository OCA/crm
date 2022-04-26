# -*- coding: utf-8 -*-
# © 2015 Vauxoo: Yanina Aular <yani@vauxoo.com>, Osval Reyes <osval@vauxoo.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CrmClaim(models.Model):

    """
        CRM Claim
    """
    _inherit = 'crm.claim'

    claim_type = fields.Many2one('crm.claim.type', help="Claim classification")

    stage_id = fields.Many2one(
        'crm.claim.stage',
        string='Stage',
        track_visibility='onchange',
        domain="[ '&',"
               "'|',('team_ids', '=', team_id), "
               "('case_default', '=', True), "
               "'|',('claim_type', '=', claim_type)"
               ",('claim_common', '=', True)]")
