# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CrmCaseSubstage(models.Model):
    _name = 'crm.case.substage'

    name = fields.Char(required=True)
    stage_id = fields.Many2one(
        comodel_name="crm.case.stage", required=True, string="Stage",
        translate=True)
