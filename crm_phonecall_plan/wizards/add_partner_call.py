# coding: utf-8
# © 2016 6IT
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _


class AddPartnerCall(models.TransientModel):
    _name = 'add.partner_call'

    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        required=True,
    )

    date = fields.Date('Date')

    partner_ids = fields.Many2many(
        'res.partner',
        string='Partners',
        default=lambda self: self._default_partner_ids(),
    )

    def _default_partner_ids(self):
        return self.env['res.partner'].browse(self._context.get('active_ids'))

    @api.multi
    @api.depends('partner_ids')
    def action_add_call(self):
        obj_phone = self.env['crm.phonecall']
        for partner in self.partner_ids:
            obj_phone.create({
                'date': self.date,
                'name': _('To fill !!!'),
                'partner_id': partner.id,
                'partner_phone': partner.phone,
                'partner_mobile': partner.mobile,
                'user_id':  self.salesperson_id.id,
                'state': "open",
            })
        return True
