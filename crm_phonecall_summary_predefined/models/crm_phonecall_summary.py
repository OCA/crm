# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class CRMPhonecallSummary(models.Model):
    _name = "crm.phonecall.summary"
    _sql_constraints = [
        ("name_unique", "UNIQUE (name)", "Name must be unique"),
    ]

    name = fields.Char()
    phonecall_ids = fields.One2many(
        "crm.phonecall",
        "summary_id",
        "Phonecalls",
        help="Phonecalls with this summary.")
