# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa S.L. - Jairo Llopis
# Copyright 2016 Tecnativa S.L. - Vicent Cubells
# Copyright 2016 Tecnativa S.L. - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _lead_create_contact(self, name, is_company, parent_id=False):
        """Populate marketing fields in partner."""
        vals = {
            field: self[field].id
            for _key, field, cookie in self.tracking_fields()}
        partner = super(
            CRMLead, self)._lead_create_contact(name, is_company, parent_id)
        partner.write(vals)
        return partner
