# coding: utf-8
# © 2016 6IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class AddCall(models.TransientModel):
    _name = 'add.call'

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        required=True,
    )

    date = fields.Date('Date')

    lead_ids = fields.Many2many(
        'crm.lead',
        string='Leads',
        default=lambda self: self._default_leads(),
    )

    def _default_lead_ids(self):
        return self.env['crm.lead'].browse(self._context.get('active_ids'))

    @api.multi
    @api.depends('lead_ids')
    def action_add_call(self):
        obj_phone = self.env['crm.phonecall']
        obj_lead = self.env['crm.lead']
        for lead in self.lead_ids:
            obj_phone.create({
                'date': self.date,
                'name': lead.name,
                'partner_id': lead.partner_id.id,
                'user_id': self.salesperson_id.id,
                'partner_mobile': lead.mobile,
                'partner_phone': lead.phone,
                'opportunity_id': lead.id,
                'state': "open",
            })

            obj_lead.browse(lead.id).write({
                'user_id': self.salesperson_id.id
            })
        return True
