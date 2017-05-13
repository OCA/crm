# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestNewsletter(TransactionCase):
    def test_newsletter(self):
        newsletter = self.env['newsletter.newsletter'].create({
            'type_id': self.env.ref('newsletter.newsletter_type_default').id,
            'subject': 'testnewsletter',
            'text_intro_html': 'hello world',
        })
        action = newsletter.action_show_recipient_objects()
        self.assertEqual(
            action['res_model'],
            self.env.ref('newsletter.newsletter_type_default').model.model,
        )
        action = newsletter.action_preview()
        self.assertEqual(newsletter.state, 'testing')
        self.env[action['res_model']].with_context(**action['context'])\
            .create({
                'newsletter_test_recipient': 'test@test.com',
                'model_id':
                self.env.ref('newsletter.model_newsletter_newsletter').id,
            })\
            .newsletter_test_send()
        self.assertTrue(self.env['mail.mail'].search([
            ('email_to', '=', 'test@test.com'),
        ]))
        newsletter.action_send()
        self.assertTrue(self.env['ir.cron'].search([
            ('model', '=', 'newsletter.newsletter'),
            ('function', '=', '_cronjob_send_newsletter'),
            ('args', '=', str((newsletter.ids,))),
        ]))
        newsletter._cronjob_send_newsletter()
        self.assertEqual(newsletter.state, 'sent')
