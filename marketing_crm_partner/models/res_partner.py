# -*- coding: utf-8 -*-
# © 2016 Tecnativa S.L. - Jairo Llopis
# © 2016 Tecnativa S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models


class ResPartner(models.Model):
    _name = "res.partner"
    _inherit = [_name, "utm.mixin"]
