# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - David Vidal
# Copyright 2018 Tecnativa S.L. - Cristina Martin R.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _create_lead_partner_data(self, name, is_company, parent_id=False):
        """Populate marketing fields in partner."""
        res = super()._create_lead_partner_data(
            name, is_company, parent_id=parent_id,
        )
        # We use self.env['utm.mixin'] for not losing possible overrides
        # see https://github.com/odoo/odoo/blob/
        # e5c8071484c883bf78478a39ef2120bcd8f2442d/addons/utm/models/utm.py#L51
        for _key, field, _cookie in self.env['utm.mixin'].tracking_fields():
            res[field] = self[field].id
        return res
