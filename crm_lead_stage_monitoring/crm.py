# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2014 Camptocamp SA (http://www.camptocamp.com)
#   @author Vincent Renaville 
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
from openerp.osv import orm, fields
from openerp import tools
from openerp.tools.translate import _


class CrmLead(orm.Model):

    _inherit = "crm.lead"

    _columns = {
                'last_activity_stage': fields.date('Current stage date',
                                                    readonly=True)
                }

    def write(self, cr, uid, ids, vals, context=None):
        if vals.get('stage_id'):
            ## Add the last_activity_stage for the current date
            vals['last_activity_stage'] = fields.datetime.now()
        return super(CrmLead, self).write(cr, uid, ids, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        ## Do not duplicate last_activity_stage
        default['last_activity_stage'] = False
        return super(CrmLead, self).copy(cr, uid, id, default, context=context)
