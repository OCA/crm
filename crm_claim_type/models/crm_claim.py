# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2015 Vauxoo
#    Author : Yanina Aular <yani@vauxoo.com>
#             Osval Reyes <osval@vauxoo.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models


class CrmClaim(models.Model):

    """
        CRM Claim
    """
    _inherit = 'crm.claim'

    claim_type = \
        fields.Many2one('crm.claim.type',
                        help="Claim classification")

    stage_id = fields.Many2one('crm.claim.stage',
                               'Stage',
                               track_visibility='onchange',
                               domain="[ '&','|',('section_ids', '=', "
                               "section_id), ('case_default', '=', True), "
                               "'|',('claim_type', '=', claim_type)"
                               ",('claim_common', '=', True)]")
