# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - David Vidal
# Copyright 2018 Tecnativa S.L. - Cristina Martin R.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """Populate marketing fields in partner."""
        res = super()._prepare_customer_values(partner_name, is_company, parent_id)
        # We use self.env['utm.mixin'] for not losing possible overrides
        # see https://github.com/odoo/odoo/blob/
        # 51833e4735fb0b761d3cd2867dfd166813469e70/addons/utm/models/utm_mixin.py#L52
        for _key, field, _cookie in self.env["utm.mixin"].tracking_fields():
            res[field] = self[field].id
        return res
