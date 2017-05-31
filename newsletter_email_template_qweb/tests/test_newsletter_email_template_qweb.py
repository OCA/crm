# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase


class TestNewsletterEmailTemplateQweb(TransactionCase):
    def setUp(self):
        super(TestNewsletterEmailTemplateQweb, self).setUp()
        self.view = self.env['ir.ui.view'].create({
            'name': 'testview',
            'type': 'qweb',
            'arch': '<t><h2><t t-esc="object.subject"/></h2>'
            '<t t-raw="object.text_intro_html"/>'
            '<div t-foreach="object.topic_ids" t-as="topic">'
            '<h3 t-esc="topic.title"/>'
            '<div t-raw="topic.text_html"/>'
            '</div>'
            '<t t-raw="object.text_outro_html"/></t>',
        })
        self.template = self.env['email.template'].create({
            'name': 'testtemplate',
            'body_type': 'qweb',
            'body_view_id': self.view.id,
            'model_id': self.env['ir.model'].search([
                ('model', '=', 'newsletter.newsletter'),
            ]).id,
        })
        self.newsletter_type = self.env['newsletter.type'].create({
            'name': 'testtype',
            'email_template_id': self.template.id,
            'model': self.env['ir.model'].search([
                ('model', '=', 'res.users'),
            ]).id,
            'email_from': 'test@test.com',
            'domain': [('id', '=', self.env.ref('base.user_root').id)],
        })
        self.newsletter = self.env['newsletter.newsletter'].create({
            'subject': 'testnewsletter',
            'type_id': self.newsletter_type.id,
            'text_intro_html': '<t t-esc="object.name" />',
        })

    def test_newsletter_email_template_qweb(self):
        values = self.env['email.template'].with_context(
            newsletter_res_id=self.env.ref('base.user_root').id,
        ).generate_email(
            self.newsletter.type_id.email_template_id.id, self.newsletter.id
        )
        self.assertEqual(
            '<h2>testnewsletter</h2>Administrator', values['body']
        )
