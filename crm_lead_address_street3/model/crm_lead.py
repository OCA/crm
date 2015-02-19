# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Romain Deheele
#    Copyright 2015 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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
from openerp import models, fields


class crm_lead(models.Model):
    """Add third field in lead address"""

    _inherit = "crm.lead"

    def _lead_create_contact(self, cr, uid, lead, name, is_company,
                             parent_id=False, context=None):
        partner_obj = self.pool['res.partner']
        partner = super(crm_lead, self).\
            _lead_create_contact(cr, uid, lead, name, is_company,
                                 parent_id=parent_id, context=context)
        partner_obj.write(cr, uid, [partner], {'street3': lead.street3},
                          context=context)
        return partner

    street3 = fields.Char('Street 3')
