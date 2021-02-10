# Copyright 2021 Eder Brito
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import date, timedelta

from odoo import api, models


class CrmLead(models.Model):

    _inherit = "crm.lead"

    @api.model
    def create(self, vals):

        activity = self.env["mail.activity"]
        crm_model = self.env["ir.model"].search([("model", "=", "crm.lead")])

        res = super(CrmLead, self).create(vals)

        if res.stage_id.create_automated_activity and any(
            res.stage_id.automated_activity_ids
        ):

            for act in res.stage_id.automated_activity_ids:

                deadline = date.today() + timedelta(days=act.days_deadline)

                if act.apply_in in ["create", "create_write"]:

                    activity.sudo().create(
                        [
                            {
                                "res_id": res.id,
                                "res_model": "crm.lead",
                                "res_model_id": crm_model.id,
                                "res_name": res.name,
                                "activity_type_id": act.id,
                                "summary": act.summary,
                                "note": act.note,
                                "date_deadline": deadline,
                                "user_id": self.env.user.id,
                                # 'user_id': act.user_id.id if act.user_id \
                                #  else self.env.user.id,
                            }
                        ]
                    )

        return res

    def write(self, vals):

        activity = self.env["mail.activity"]
        crm_model = self.env["ir.model"].search([("model", "=", "crm.lead")])
        stage_id = self.stage_id.id

        res = super(CrmLead, self).write(vals)

        if "stage_id" in vals:

            if vals["stage_id"] != stage_id:

                if self.stage_id.create_automated_activity and any(
                    self.stage_id.automated_activity_ids
                ):

                    for act in self.stage_id.automated_activity_ids:

                        deadline = date.today() + timedelta(days=act.days_deadline)

                        if act.apply_in in ["write", "create_write"]:

                            activity.sudo().create(
                                [
                                    {
                                        "res_id": self.id,
                                        "res_model": "crm.lead",
                                        "res_model_id": crm_model.id,
                                        "res_name": self.name,
                                        "activity_type_id": act.id,
                                        "summary": act.summary,
                                        "note": act.note,
                                        "date_deadline": deadline,
                                        "user_id": self.env.user.id,
                                        # 'user_id': act.user_id.id if act.user_id \
                                        # else self.env.user.id,
                                    }
                                ]
                            )

            return res
