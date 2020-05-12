# Copyright 2004-2016 Odoo SA (<http://www.odoo.com>)
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class CrmLead(models.Model):
    """Added the phonecall related details in the lead."""

    _inherit = "crm.lead"

    phonecall_ids = fields.One2many(
        comodel_name='crm.phonecall',
        inverse_name='opportunity_id',
        string='Phonecalls',
    )
    phonecall_count = fields.Integer(
        compute='_compute_phonecall_count',
    )

    @api.multi
    def _compute_phonecall_count(self):
        """Calculate number of phonecalls."""
        for lead in self:
            lead.phonecall_count = self.env[
                'crm.phonecall'].search_count(
                [('opportunity_id', '=', lead.id)])

    @api.multi
    def button_open_phonecall(self):
        self.ensure_one()
        action = self.env.ref('crm_phonecall.crm_case_categ_phone_incoming0')
        action_dict = action.read()[0] if action else {}
        action_dict['context'] = safe_eval(
            action_dict.get('context', '{}'))
        action_dict['context'].update({
            'default_opportunity_id': self.id,
            'search_default_opportunity_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_duration': 1.0,
        })
        return action_dict
