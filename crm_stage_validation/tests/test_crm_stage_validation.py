# Copyright 2025 Marcel Savegnago - Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, fields
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

from odoo.addons.base.tests.common import DISABLED_MAIL_CONTEXT


class TestCrmStageValidation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env["base"].with_context(**DISABLED_MAIL_CONTEXT).env
        cls.stage = cls.env["crm.stage"]
        cls.crm_lead = cls.env["crm.lead"]
        cls.ir_model_fields = cls.env["ir.model.fields"]
        # Get some fields to use in the stages
        cls.lead_field = cls.ir_model_fields.search(
            [("model", "=", "crm.lead"), ("name", "=", "date_deadline")]
        )
        cls.stage_lead_default = cls.stage.create(
            {
                "name": "CRM Stage Default",
            }
        )
        cls.stage_lead_validated = cls.stage.create(
            {
                "name": "CRM Stage Validated",
                "validate_field_ids": [(6, 0, [cls.lead_field.id])],
            }
        )
        cls.lead = cls.crm_lead.create(
            {
                "name": "Test Lead",
                "stage_id": cls.stage_lead_default.id,
            }
        )

    def get_validate_message(self, lead, stage):
        validate_message = False
        field_ids = stage.sudo().validate_field_ids
        field_names = [x.name for x in field_ids]
        values = lead.sudo().read(field_names)
        fields_list = [
            field.field_description for field in field_ids if not values[0][field.name]
        ]
        fields_str = ", ".join(fields_list)
        if fields_str:
            validate_message = _(
                "Lead/Opportunity %(lead)s can't be moved to the stage %(stage)s "
                "until the following fields are set: %(fields)s."
                % {
                    "lead": lead.name,
                    "stage": stage.name,
                    "fields": fields_str,
                }
            )
        return validate_message

    def test_crm_stage_validation(self):
        validate_message = self.get_validate_message(
            self.lead, self.stage_lead_validated
        )
        with self.assertRaisesRegex(ValidationError, validate_message):
            self.lead.write({"stage_id": self.stage_lead_validated.id})
        self.lead.write({"date_deadline": fields.Date.today()})
        self.lead.write({"stage_id": self.stage_lead_validated.id})
        self.assertEqual(self.lead.stage_id, self.stage_lead_validated)
