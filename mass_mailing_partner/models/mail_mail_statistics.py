# -*- coding: utf-8 -*-
# © 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class MailMailStatistics(models.Model):
    _inherit = "mail.mail.statistics"

    partner_id = fields.Many2one(
        string="Partner", comodel_name='res.partner', readonly=True)

    @api.model
    def partner_id_from_obj(self, model, res_id):
        partner_id = False
        obj = self.env[model].browse(res_id)
        if obj.exists():
            if model == 'res.partner':
                partner_id = res_id
            elif 'partner_id' in obj._fields:
                partner_id = obj.partner_id.id
        return partner_id

    @api.multi
    def partner_link(self):
        for stat in self.filtered(lambda r: r.model and r.res_id):
            partner_id = self.partner_id_from_obj(stat.model, stat.res_id)
            if partner_id != stat.partner_id.id:
                stat.partner_id = partner_id
        return True

    @api.model
    def create(self, vals):
        stat = super(MailMailStatistics, self).create(vals)
        stat.partner_link()
        return stat
