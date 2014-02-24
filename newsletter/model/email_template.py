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

from mako.template import Template as MakoTemplate
from urllib import quote as quote
from openerp.osv.orm import Model
from openerp.osv import fields


class email_template(Model):
    _inherit = 'email.template'

    def render_template(self, cr, uid, template, model, res_id, context=None):
        result = super(email_template, self).render_template(cr, uid, template,
                model, res_id, context)
        if (model == 'newsletter.newsletter' and res_id
            and context.get('newsletter_res_id')):
            
            newsletter = self.pool.get(model).browse(cr, uid, res_id,
                    context=context)
            user = self.pool.get('res.users').browse(cr, uid, uid,
                    context=context)


            result = MakoTemplate(result).render_unicode(
                object=self.pool.get(newsletter.type_id.model.model).browse(
                    cr, uid, context.get('newsletter_res_id'), context),
                user=user,
                # context kw would clash with mako internals
                ctx=context,
                quote=quote,
                format_exceptions=True)

        return result

class email_template_preview(Model):
    _inherit = 'email_template.preview'

    def render_template(self, cr, uid, template, model, res_id, context=None):
        return email_template.render_template(self.pool.get('email.template'),
                cr, uid, template, model, res_id, context)
