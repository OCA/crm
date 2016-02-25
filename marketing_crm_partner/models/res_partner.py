# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = [_name, "crm.tracking.mixin"]
