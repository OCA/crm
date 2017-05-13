# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, tools


class EmailTemplatePreview(models.Model):
    _inherit = 'email_template.preview'

    newsletter_test_recipient = fields.Char('Test recipient')

    @api.multi
    def newsletter_test_send(self):
        self.ensure_one()
        mail_values = self.env['email.template'].generate_email(
            self.env.context.get('template_id'), int(self.res_id)
        )
        mail_values['email_to'] = self.newsletter_test_recipient
        mail_values.pop('email_cc', None)
        mail_values.pop('email_bcc', None)
        mail_values['auto_delete'] = not tools.config['test_enable']
        self.env['mail.mail'].create(mail_values).send()
