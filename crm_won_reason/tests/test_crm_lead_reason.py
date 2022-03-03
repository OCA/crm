# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo.tests import Form
from odoo.tests.common import TransactionCase


class TestCrmLeadReason(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.crm_lead_model = cls.env["crm.lead"]
        cls.lead_reason = cls.env["crm.lost.reason"]
        cls.won_reason = cls.lead_reason.create(
            {"name": "won reason 1", "reason_type": "won"}
        )
        cls.lost_reason = cls.lead_reason.create(
            {"name": "lost reason 1", "reason_type": "lost"}
        )
        cls.unspecified_reason = cls.lead_reason.create({"name": "too expensive"})

    def test_won_reason(self):
        crm_lead = self.crm_lead_model.create({"name": "Testing lead won reason"})

        wizard_model = self.env["crm.lead.won"].with_context(
            active_id=crm_lead.id, active_model="crm.lead"
        )
        wizard_form = Form(wizard_model)
        wizard_form.won_reason_id = self.won_reason
        wizard_id = wizard_form.save()["id"]
        wizard_record = wizard_model.browse(wizard_id)
        wizard_record.with_context(active_ids=crm_lead.id).action_win_reason_apply()
        self.assertTrue(crm_lead.stage_id.is_won)
        self.assertEqual(crm_lead.won_reason_id.name, self.won_reason.name)

    def test_lost_reason(self):
        crm_lead = self.crm_lead_model.create({"name": "Testing lead lost reason"})
        crm_lead.action_set_lost(lost_reason=self.lost_reason)
        self.assertFalse(crm_lead.stage_id.is_won)
        self.assertEqual(crm_lead.lost_reason.name, self.lost_reason.name)

    def test_unspecified_reason(self):
        crm_lead = self.crm_lead_model.create(
            {"name": "Testing lead unspecified reason"}
        )
        crm_lead.action_set_lost(lost_reason=self.unspecified_reason)
        self.assertFalse(crm_lead.stage_id.is_won)
        self.assertEqual(crm_lead.lost_reason.name, self.unspecified_reason.name)
