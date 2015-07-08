# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
from lxml import etree
from openerp import models, api


class MailWizardInvite(models.TransientModel):
    _inherit = 'mail.wizard.invite'

    @api.model
    def mail_restrict_follower_selection_get_domain(self):
        parameter_name = 'mail_restrict_follower_selection.domain'
        return self.env['ir.config_parameter'].get_param(
            '%s.%s' % (parameter_name,
                       self.env.context.get('default_res_model')),
            self.env['ir.config_parameter'].get_param(
                parameter_name, default='[]')
        )

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(MailWizardInvite, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        arch = etree.fromstring(result['arch'])
        for field in arch.xpath('//field[@name="partner_ids"]'):
            field.attrib['domain'] = self\
                .mail_restrict_follower_selection_get_domain()
        result['arch'] = etree.tostring(arch)
        return result
