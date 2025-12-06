# Copyright 2025 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _track_template(self, changes):
        res = super()._track_template(changes)
        lead = self[0]
        if "stage_id" in changes and lead.stage_id.mail_template_id:
            res["stage_id"] = (
                lead.stage_id.mail_template_id,
                {
                    "auto_delete_keep_log": False,
                    "subtype_id": self.env["ir.model.data"]._xmlid_to_res_id(
                        "mail.mt_note"
                    ),
                    "email_layout_xmlid": "mail.mail_notification_light",
                },
            )
        return res
