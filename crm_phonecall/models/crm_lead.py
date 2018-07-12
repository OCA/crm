# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    phonecall_ids = fields.One2many(
        comodel_name='crm.phonecall',
        inverse_name='opportunity_id',
        string='Phonecalls',
    )
    phonecall_count = fields.Integer(
        compute='_compute_phonecall_count',
        string="Phonecalls",
    )

    @api.multi
    def _compute_phonecall_count(self):
        for lead in self:
            lead.phonecall_count = self.env[
                'crm.phonecall'].search_count(
                [('opportunity_id', '=', lead.id)])
