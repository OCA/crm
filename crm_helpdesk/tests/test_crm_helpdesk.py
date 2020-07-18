# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import TransactionCase
from odoo.modules.module import get_module_resource
from odoo.loglevels import ustr


class TestCrmHelpdesk(TransactionCase):

    def setUp(self):
        super(TestCrmHelpdesk, self).setUp()

        self.helpdesk_user = self.env['res.users'].create({
            'company_id': self.env.ref("base.main_company").id,
            'name': "Helpdesk User",
            'login': "hdu",
            'email': "helpdeskuser@yourcompany.com",
            'groups_id': [(6, 0, [
                self.env.ref('sales_team.group_sale_salesman').id,
                self.env.ref('base.group_partner_manager').id])]
        })

    def test_crm_helpdesk_form(self):
        helpdesk = self.env['crm.helpdesk'].sudo(self.helpdesk_user).create(
            {'name': "Helpdesk 1"})
        helpdesk.partner_id = self.env.ref('base.res_partner_1')

    def test_crm_helpdesk_mail(self):
        # Customer has Questions regarding our products, so he sent an email.
        # Mail script will fetch his question from mail server.
        # Then that mail is processed after reading EML file.
        request_file = open(get_module_resource(
            'crm_helpdesk', 'tests', 'customer_question.eml'), 'rb')
        request_message = request_file.read()
        self.env['crm.helpdesk'].sudo(self.helpdesk_user).\
            message_process('crm.helpdesk', request_message)

        # After getting the mail, the details of new question are checked.
        question = self.env['crm.helpdesk'].\
            sudo(self.helpdesk_user).search(
            [('email_from', '=', 'Mr. John Right <info@customer.com>')],
            limit=1)
        self.assertTrue(question.ids,
                        "Question is not created after getting request")
        self.assertTrue(
            question.name == ustr(
                "Where is download link of user manual of your product ? "),
            "Subject does not match")

        # Now the message is updated according to provide services.
        question = self.env['crm.helpdesk'].\
            sudo(self.helpdesk_user).search(
            [('email_from', '=', 'Mr. John Right <info@customer.com>')],
            limit=1)
        try:
            question.message_update(
                {'subject': 'Link of product', 'body': 'www.odoo.com'})
        except Exception:
            raise
