# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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

from openerp.osv.orm import Model
from openerp.addons.email_template.email_template import mako_template_env,\
    format_tz


class email_template(Model):
    _inherit = 'email.template'

    def render_template_batch(self, cr, uid, template, model, res_ids,
                              context=None, post_process=False):
        result = {}
        try:
            if model == 'newsletter.newsletter':
                mako_template_env.autoescape = False
                post_process = False
            result = super(email_template, self).render_template_batch(
                cr, uid, template, model, res_ids, context=context,
                post_process=post_process)
        finally:
            if model == 'newsletter.newsletter':
                mako_template_env.autoescape = True

        if model == 'newsletter.newsletter' and res_ids and result and\
                context.get('newsletter_res_id'):
            for res_id, rendered in result.iteritems():
                newsletter = self.pool[model].browse(
                    cr, uid, res_id, context=context)
                user = self.pool['res.users'].browse(
                    cr, uid, uid, context=context)
                template = mako_template_env.from_string(rendered)
                result[res_id] = template.render({
                    'object': self.pool[newsletter.type_id.model.model].browse(
                        cr, uid, context.get('newsletter_res_id'), context),
                    'user': user,
                    'ctx': context,
                    'format_tz': lambda dt, tz=False, fmt=False:
                    format_tz(self.pool, cr, uid, dt, tz, fmt, context),
                })

        return result
