# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime
import simplejson
import time
import werkzeug
from dateutil.relativedelta import relativedelta
from lxml import etree
from openerp import api, models, tools
from openerp.http import request
from openerp.addons.base.ir.ir_qweb import QWebContext


class EmailTemplate(models.Model):
    _inherit = 'email.template'

    @api.model
    def generate_email_batch(self, template_id, res_ids, fields=None):
        result = super(EmailTemplate, self).generate_email_batch(
            template_id, res_ids, fields=fields)
        this = self.browse(template_id)
        for record_id, this in self.get_email_template_batch(
            template_id, res_ids
        ).iteritems():
            if this.model_id.model == 'newsletter.newsletter' and\
               self.env.context.get('newsletter_res_id') and\
               this.body_type == 'qweb' and\
               (not fields or 'body_html' in fields):
                for record in self.env[this.model].browse(record_id):
                    result[record_id]['body_html'] = self.env['ir.qweb']\
                        ._model.render_node(
                            etree.fromstring(
                                result[record_id]['body_html'],
                                etree.HTMLParser()
                            ),
                            self
                            ._generate_email_batch_get_newsletter_qcontext({
                                'object': self.env[record.type_id.model.model]
                                .browse(self.env.context['newsletter_res_id']),
                                'newsletter': record,
                            }),
                        )
                    result[record_id]['body'] = tools.html_sanitize(
                        result[record_id]['body_html']
                    )
        return result

    def _generate_email_batch_get_newsletter_qcontext(self, values=None):
        return QWebContext(
            self.env.cr, self.env.uid,
            dict(
                env=self.env,
                request=request,
                debug=request.debug if request else False,
                json=simplejson,
                quote_plus=werkzeug.url_quote_plus,
                time=time,
                datetime=datetime,
                relativedelta=relativedelta,
                **(values or {})
            ),
            loader=lambda name: self.env['ir.qweb'].read_template(name),
            context=self.env.context
        )
