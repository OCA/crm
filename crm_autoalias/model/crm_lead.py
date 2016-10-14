# -*- coding: utf-8 -*-
# © 2016 FactorLibre - Hugo Santos <hugo.santos@factorlibre.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api
from uuid import uuid4


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    email_alias = fields.Many2one('mail.alias', 'Alias', readonly=True)
    email_alias_email = fields.Char(string='Alias',
                                    related="email_alias.display_name",
                                    store=True)

    @api.model
    def create(self, vals):
        ir_model = self.env['ir.model']
        mail_alias_model = self.env['mail.alias']
        lead_model_ids = ir_model.search([
            ('model', '=', 'crm.lead')
        ])
        while True:
            alias_name = "{0}-crm".format(uuid4().hex)
            mail_alias_ids = mail_alias_model.search([
                ('alias_name', '=', alias_name)
            ])
            if not mail_alias_ids:
                break
        alias = mail_alias_model.create({
            'alias_name': alias_name,
            'alias_model_id': lead_model_ids[0].id
        })
        vals['email_alias'] = alias.id
        record = super(CrmLead, self).create(vals)
        alias.alias_force_thread_id = record.id
        return record
