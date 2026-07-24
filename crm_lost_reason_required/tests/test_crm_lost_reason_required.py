# Copyright 2026 Gray Matter Logic (<https://www.graymatterlogic.com>).
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from lxml import etree

from odoo.addons.base.tests.common import BaseCommon


class TestCrmLostReasonRequired(BaseCommon):
    def test_lost_reason_required_on_wizard_view(self):
        view = self.env.ref("crm.crm_lead_lost_view_form")
        result = self.env["crm.lead.lost"].get_view(view_id=view.id, view_type="form")
        arch = etree.fromstring(result["arch"])
        field = arch.xpath("//field[@name='lost_reason_id']")[0]
        self.assertTrue(
            field.get("required") in ("True", "1", "true"),
            "lost_reason_id must be required on the Mark as Lost wizard",
        )
