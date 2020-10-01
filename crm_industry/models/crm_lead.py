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
                        "The secondary industries must be different from the main "
                        "industry."
                    )
                )

    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """Propagate industries in the creation of partner.
        """
        values = super(CrmLead, self)._create_lead_partner_data(
            name, is_company, parent_id
        )
        values.update(
            {
                "industry_id": self.industry_id.id,
                "secondary_industry_ids": [(6, 0, self.secondary_industry_ids.ids)],
            }
        )
        return values
