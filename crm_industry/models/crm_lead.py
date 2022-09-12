# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    industry_id = fields.Many2one(
        comodel_name="res.partner.industry", string="Main Industry"
    )

    secondary_industry_ids = fields.Many2many(
        comodel_name="res.partner.industry",
        string="Secondary Industries",
        domain="[('id', '!=', industry_id)]",
    )

    @api.constrains("industry_id", "secondary_industry_ids")
    def _check_industries(self):
        for lead in self:
            if lead.industry_id in lead.secondary_industry_ids:
                raise exceptions.UserError(
                    _(
                        "The secondary industries must be different from the"
                        " main industry."
                    )
                )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """Propagate industries in the creation of partner."""
        values = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )
        main, secondary = self.industry_id, self.secondary_industry_ids
        values.update(
            {
                "industry_id": main.id,
                "secondary_industry_ids": [(6, 0, secondary.ids)],
            }
        )
        return values

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.industry_id:
                self.industry_id = self.partner_id.industry_id
            if self.partner_id.secondary_industry_ids:
                self.secondary_industry_ids = self.partner_id.secondary_industry_ids

    @api.model
    def create(self, vals):
        if vals.get("partner_id"):
            customer = self.env["res.partner"].browse(vals["partner_id"])
            if customer.industry_id and not vals.get("industry_id"):
                vals.update({"industry_id": customer.industry_id.id})
            if customer.secondary_industry_ids and not vals.get(
                "secondary_industry_ids"
            ):
                vals.update(
                    {
                        "secondary_industry_ids": [
                            (6, 0, customer.secondary_industry_ids.ids)
                        ]
                    }
                )
        return super().create(vals)
