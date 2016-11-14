# -*- coding: utf-8 -*-
# © 2016 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Populate marketing fields in partner."""
        new_context = {"default_%s" % field: lead[field]
                       for _key, field, cookie in self.tracking_fields()}
        return (super(CRMLead, self.with_context(**new_context))
                ._lead_create_contact(lead, name, is_company, parent_id))
