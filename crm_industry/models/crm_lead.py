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
