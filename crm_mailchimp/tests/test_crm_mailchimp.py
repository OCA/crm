# Copyright 2019-2021 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# from mailchimp3.mailchimpclient import MailChimpError
from mock import Mock, patch
from werkzeug.exceptions import NotFound

from odoo import exceptions
from odoo.tests.common import TransactionCase

from odoo.addons.website.tools import MockRequest

from ..controllers.main import Mailchimp as MailchimpController

# from odoo.tools.misc import mute_logger


class TestCrmMailchimp(TransactionCase):
    def setUp(self):
        super(TestCrmMailchimp, self).setUp()
        self.list = self.env.ref("crm_mailchimp.list_demo")
        self.category = self.env.ref("crm_mailchimp.interest_category_demo")
        self.interest0 = self.env.ref("crm_mailchimp.interest_demo0")
        self.interest1 = self.env.ref("crm_mailchimp.interest_demo1")
        self.interest2 = self.env.ref("crm_mailchimp.interest_demo2")
        self.user_demo = self.env.ref("base.user_demo")
        self.user_subscriber = self.env.ref("crm_mailchimp.user_subscriber")

    def _setup_mock_mailchimp(self, mock_MailChimp):
        mock_client = Mock()
        mock_MailChimp.return_value = mock_client
        self.list_data = {
            "id": self.list.mailchimp_id,
            "name": self.list.name,
        }
        mock_client.lists.all.return_value = {
            "lists": [self.list_data],
        }
        mock_client.lists.get.return_value = self.list_data
        self.field_data = {
            "merge_id": "42",
            "name": "A field",
            "tag": "tag",
        }
        mock_client.lists.merge_fields.all.return_value = {
            "merge_fields": [self.field_data],
        }
        mock_client.lists.merge_fields.get.return_value = self.field_data
        self.category_data = {
            "id": self.category.mailchimp_id,
            "title": self.category.name,
        }
        mock_client.lists.interest_categories.all.return_value = {
            "categories": [self.category_data],
        }
        mock_client.lists.interest_categories.interests.all.return_value = {
            "interests": [
                {"id": interest.mailchimp_id, "name": interest.name}
                for interest in self.interest0 + self.interest1 + self.interest2
            ],
        }
        mock_client.lists.members.create_or_update.return_value = {
            "id": "the mailchimp id",
        }
        mock_client.lists.members.create.return_value = {
            "id": "the mailchimp id",
        }
        return mock_client

    @patch("odoo.addons.crm_mailchimp.models.mailchimp_list.MailChimp")
    def test_crm_mailchimp_settings(self, mock_MailChimp):
        ir_config_parameter = self.env["ir.config_parameter"]
        self._setup_mock_mailchimp(mock_MailChimp)
        # we want to test creating this here initially via the config wizard
        self.list.unlink()
        ir_config_parameter.set_param("crm_mailchimp.username", "/")
        ir_config_parameter.set_param("crm_mailchimp.apikey", "/")
        settings_wizard = self.env["mailchimp.settings"].create({})
        self.assertEqual(settings_wizard.username, "/")
        self.assertEqual(settings_wizard.apikey, "/")
        settings_wizard.write({"username": "a user", "apikey": "a key"})
        settings_wizard.execute()
        self.assertEqual(
            ir_config_parameter.get_param("crm_mailchimp.username"), "a user",
        )
        self.assertEqual(
            ir_config_parameter.get_param("crm_mailchimp.apikey"), "a key",
        )
        # must have created our fake list from above
        created_list = self.env["mailchimp.list"].search(
            [("name", "=", self.list_data["name"])]
        )
        self.assertTrue(created_list)
        # and the merge field + category
        self.assertTrue(created_list.interest_category_ids)
        self.assertTrue(
            created_list.mapped("interest_category_ids.interest_ids.display_name")
        )
        # Fake list must have models (well, at least one).
        self.assertTrue(created_list.model_ids)
        # Models must have merge fields.
        for list_model in created_list.model_ids:
            self.assertTrue(list_model.merge_field_ids)

    @patch("odoo.addons.crm_mailchimp.models.mailchimp_list.MailChimp")
    def test_crm_mailchimp_backend(self, mock_MailChimp):
        # mock_client = self._setup_mock_mailchimp(mock_MailChimp)
        self._setup_mock_mailchimp(mock_MailChimp)
        self.assertTrue(bool(self.user_demo))
        partner = self.user_demo.partner_id
        # Subscribe the demo user (or rather the partner).
        subscriber = self._subscribe_partner(partner)
        # change of email address
        partner.write({"email": "test2@test.com"})
        self.assertEqual(partner.email, subscriber.email)
        # with mute_logger("odoo.addons.crm_mailchimp.models.mailchimp_list"):
        #     self.list.action_push()
        # partner.write({"email": "test3@test.com"})
        # self.list.action_push()
        # removal from mailchimp

    def test_crm_mailchimp_rules(self):
        """Check access to interests and lists."""
        demo_list = self.env.ref("crm_mailchimp.list_demo")
        interest_model = self.env["mailchimp.interest"]
        interest_domain = [("category_id.list_id", "=", demo_list.id)]
        interests = interest_model.search(interest_domain)
        # demo user (mailchimp user) sees all interests
        self.assertEqual(
            interest_model.with_user(self.user_demo).search(interest_domain), interests,
        )
        # subscriber only if she has the good group
        self.assertEqual(
            interest_model.with_user(self.user_subscriber).search(interest_domain),
            interests,
        )
        self.env.cache.invalidate()
        # Specify that only system users can see the demo list.
        demo_list.write({"group_ids": [(6, 0, [self.env.ref("base.group_system").id])]})
        self.assertFalse(
            interest_model.with_user(self.user_subscriber).search(interest_domain)
        )

    @patch("odoo.addons.crm_mailchimp.models.mailchimp_list.MailChimp")
    def test_crm_mailchimp_controllers(self, mock_MailChimp):
        """Test the controller for the webhooks called by Mailchimp."""
        controller = MailchimpController()
        webhook_key = self.env["mailchimp.settings"]._get_webhook_key()
        with MockRequest(self.env):
            # Request without arguments is a test and should return an empty string.
            response = controller.hook(webhook_key)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_data(as_text=True), "")
            # Request with a wrong webhook key should result in AccessDenied exception.
            with self.assertRaises(exceptions.AccessDenied):
                response = controller.hook("wrong key")
            # Request with wrong type of actions should result in NotFound exception.
            with self.assertRaises(NotFound):
                response = controller.hook(
                    webhook_key,
                    **{
                        "type": "not_existing_type",
                        "data[action]": "unsub",
                        "data[email]": self.user_demo.email,
                        "data[list_id]": self.list.mailchimp_id,
                    }
                )
            # Request for non-existing partner should result in NotFound exception.
            with self.assertRaises(NotFound):
                response = controller.hook(
                    webhook_key,
                    **{
                        "type": "unsubscribe",
                        "data[action]": "unsub",
                        "data[email]": "unknown@unknown.com",
                    }
                )
            # correct request
            self._setup_mock_mailchimp(mock_MailChimp)
            partner = self.user_demo.partner_id
            self._subscribe_partner(partner)
            self.assertEqual(partner.subscription_count, 1)
            response = controller.hook(
                webhook_key,
                **{
                    "type": "unsubscribe",
                    "data[action]": "unsub",
                    "data[email]": self.user_demo.email,
                    "data[list_id]": self.list.mailchimp_id,
                }
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(partner.subscription_count, 0)

    def _subscribe_partner(self, partner):
        """Subscribe a partner to the demo list and return subscriber record."""
        subscriber_model = self.env["mailchimp.subscriber"]
        subscriber = subscriber_model.create(
            {"list_id": self.list.id, "res_model": partner._name, "res_id": partner.id}
        )
        subscriber.write({"interest_ids": [(0, 0, {"interest_id": self.interest1.id})]})
        return subscriber
