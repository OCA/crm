# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - David Vidal
# Copyright 2018 Tecnativa S.L. - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _lead_create_contact(self, name):
        """Populate marketing fields in partner."""
        vals = {
            field: self[field].id
            for key, field, cook in self.env['utm.mixin'].tracking_fields()}
        partner = super(
            CRMLead, self)._lead_create_contact(name)
        partner.write(vals)
        return partner
