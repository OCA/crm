# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from mailchimp3.mailchimpclient import MailChimpError
from mock import Mock, patch
from werkzeug.exceptions import NotFound
from odoo import exceptions
from odoo.tests.common import TransactionCase
from odoo.tools.misc import mute_logger
from ..controllers.main import Mailchimp as MailchimpController


class TestCrmMailchimp(TransactionCase):
    def setUp(self):
        super(TestCrmMailchimp, self).setUp()
        self.list = self.env.ref('crm_mailchimp.list_demo')
        self.category = self.env.ref('crm_mailchimp.interest_category_demo')
        self.interest0 = self.env.ref('crm_mailchimp.interest_demo0')
        self.interest1 = self.env.ref('crm_mailchimp.interest_demo1')
        self.interest2 = self.env.ref('crm_mailchimp.interest_demo2')
        self.user_demo = self.env.ref('base.user_demo')
        self.user_subscriber = self.env.ref('crm_mailchimp.user_subscriber')

    def _setup_mock_mailchimp(self, mock_MailChimp):
        mock_client = Mock()
        mock_MailChimp.return_value = mock_client
        self.list_data = {
            'id': self.list.mailchimp_id,
            'name': self.list.name,
        }
        mock_client.lists.all.return_value = {
            'lists': [self.list_data],
        }
        mock_client.lists.get.return_value = self.list_data
        self.field_data = {
            'merge_id': '42',
            'name': 'A field',
            'tag': 'tag',
        }
        mock_client.lists.merge_fields.all.return_value = {
            'merge_fields': [self.field_data],
        }
        mock_client.lists.merge_fields.get.return_value = self.field_data
        self.category_data = {
            'id': self.category.mailchimp_id,
            'title': self.category.name,
        }
        mock_client.lists.interest_categories.all.return_value = {
            'categories': [self.category_data],
        }
        mock_client.lists.interest_categories.interests.all.return_value = {
            'interests': [
                {
                    'id': interest.mailchimp_id,
                    'name': interest.name,
                }
                for interest in
                self.interest0 + self.interest1 + self.interest2
            ],
        }
        return mock_client

    @patch('odoo.addons.crm_mailchimp.models.mailchimp_list.MailChimp')
    def test_crm_mailchimp_settings(self, mock_MailChimp):
        ir_config_parameter = self.env['ir.config_parameter']
        self._setup_mock_mailchimp(mock_MailChimp)
        # we want to test creating this here initially via the config wizard
        self.list.unlink()
        ir_config_parameter.set_param('crm_mailchimp.username', '/')
        ir_config_parameter.set_param('crm_mailchimp.apikey', '/')
        settings_wizard = self.env['mailchimp.settings'].create({})
        self.assertEqual(settings_wizard.username, '/')
        self.assertEqual(settings_wizard.apikey, '/')
        settings_wizard.write({
            'username': 'a user',
            'apikey': 'a key',
        })
        settings_wizard.execute()
        self.assertIn(
            self.env['mailchimp.settings']._get_webhook_key(),
            settings_wizard.webhook_url,
        )
        self.assertEqual(
            ir_config_parameter.get_param('crm_mailchimp.username'),
            'a user',
        )
        self.assertEqual(
            ir_config_parameter.get_param('crm_mailchimp.apikey'),
            'a key',
        )
        # must have created our fake list from above
        created_list = self.env['mailchimp.list'].search([
            ('name', '=', self.list_data['name']),
        ])
        self.assertTrue(created_list)
        # and the merge field + category
        self.assertTrue(created_list.interest_category_ids)
        self.assertTrue(created_list.mapped(
            'interest_category_ids.interest_ids.display_name'
        ))
        self.assertTrue(created_list.merge_field_ids)

    @patch('odoo.addons.crm_mailchimp.models.mailchimp_list.MailChimp')
    def test_crm_mailchimp_backend(self, mock_MailChimp):
        mock_client = self._setup_mock_mailchimp(mock_MailChimp)

        # change of email address
        last_email = self.user_demo.email
        self.assertFalse(self.user_demo.mailchimp_last_email)
        self.user_demo.write({'email': 'test2@test.com'})
        self.assertEqual(self.user_demo.mailchimp_last_email, last_email)
        mock_client.lists.members.create_or_update.side_effect = MailChimpError
        with mute_logger('odoo.addons.crm_mailchimp.models.mailchimp_list'):
            self.list.action_push()
        self.assertFalse(self.user_demo.mailchimp_last_email)
        self.user_demo.write({'email': 'test3@test.com'})
        mock_client.lists.members.create_or_update = Mock()
        self.list.action_push()
        self.assertFalse(self.user_demo.mailchimp_last_email)

        # removal from mailchimp
        self.assertTrue(self.user_demo.mailchimp_list_ids)
        self.assertTrue(self.user_demo.mailchimp_interest_ids)
        self.assertFalse(self.user_demo.mailchimp_deleted_list_ids)
        self.user_demo.write({'mailchimp_list_ids': [(6, 0, [])]})
        self.assertEqual(self.user_demo.mailchimp_deleted_list_ids, self.list)
        self.assertFalse(self.user_demo.mailchimp_interest_ids)
        mock_client.lists.members.delete.side_effect = MailChimpError
        with mute_logger('odoo.addons.crm_mailchimp.models.mailchimp_list'):
            self.list._cron(60)
        self.assertFalse(self.user_demo.mailchimp_deleted_list_ids)

    def test_crm_mailchimp_rules(self):
        interests = self.env['mailchimp.interest'].search([])
        # demo user (mailchimp user) sees all interests
        self.assertEqual(
            self.env['mailchimp.interest'].sudo(self.user_demo).search([]),
            interests,
        )
        # subscriber only if she has the good group
        self.assertEqual(
            self.env['mailchimp.interest'].sudo(
                self.user_subscriber
            ).search([]),
            interests,
        )
        self.env['ir.rule'].clear_caches()
        self.env.ref('crm_mailchimp.list_demo').write({
            'group_ids': [(4, self.env.ref('base.group_system').id)],
        })
        self.assertFalse(
            self.env['mailchimp.interest'].sudo(
                self.user_subscriber
            ).search([]),
        )

    @patch('odoo.addons.crm_mailchimp.controllers.main.request')
    def test_crm_mailchimp_controllers(self, mock_request):
        mock_request.env = self.env
        controller = MailchimpController()
        # test reqeust by mailchimp without parameters
        self.assertEqual(
            controller.hook.original_func(
                controller,
                self.env['mailchimp.settings']._get_webhook_key(),
            ),
            '',
        )
        # wrong key
        with self.assertRaises(exceptions.AccessDenied):
            controller.hook.original_func(controller, 'wrong key')
        # wrong type
        with self.assertRaises(NotFound):
            controller.hook.original_func(
                controller,
                self.env['mailchimp.settings']._get_webhook_key(),
                **{
                    'type': 'not_existing_type',
                    'data[action]': 'unsub',
                    'data[email]': self.user_demo.email,
                    'data[list_id]': self.list.mailchimp_id,
                }
            )
        # nonexisting partner
        with self.assertRaises(NotFound):
            controller.hook.original_func(
                controller,
                self.env['mailchimp.settings']._get_webhook_key(),
                **{
                    'type': 'unsubscribe',
                    'data[action]': 'unsub',
                    'data[email]': 'unknown@unknown.com',
                }
            )
        # correct request
        self.assertTrue(self.user_demo.mailchimp_list_ids)
        self.assertTrue(self.user_demo.mailchimp_interest_ids)
        controller.hook.original_func(
            controller,
            self.env['mailchimp.settings']._get_webhook_key(),
            **{
                'type': 'unsubscribe',
                'data[action]': 'unsub',
                'data[email]': self.user_demo.email,
                'data[list_id]': self.list.mailchimp_id,
            }
        )
        self.assertFalse(self.user_demo.mailchimp_list_ids)
        self.assertFalse(self.user_demo.mailchimp_interest_ids)
