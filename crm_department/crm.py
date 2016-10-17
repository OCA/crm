# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Joël Grand-guillaume (Camptocamp)
#    Contributor: Yannick Vaucher (Camptocamp)
#    Contributor: Eficent
#    Copyright 2011 Camptocamp SA
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


class CrmSalesTeam(models.Model):
    _inherit = 'crm.team'

    department_id = fields.Many2one(
        'hr.department',
        'Department',
        default=lambda s: s.env.user.employee_ids[0].department_id or None)


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    department_id = fields.Many2one('hr.department', 'Department')

    def on_change_user(self, cr, uid, ids, user_id, context=None):
        """
        Updates res dictionary with the department
        corresponding to the User Employee, consistent with the default value
        """
        res = super(CrmLead, self).on_change_user(
            cr, uid, ids, user_id, context=context)
        res.setdefault('value', {})
        user = self.pool['res.users'].browse(cr, uid, user_id, context=context)
        if user.employee_ids:
            dptm_id = user.employee_ids[0].department_id.id or None
            res['value']['department_id'] = dptm_id
        return res
