# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CRMPhonecall2Phonecall(models.Model):
    _inherit = "crm.phonecall2phonecall"

    name = fields.Char(
        related="summary_id.name",
        store=True,
        required=False,
        readonly=True)
    summary_id = fields.Many2one(
        comodel_name="crm.phonecall.summary",
        string="Summary",
        required=True,
        ondelete="restrict")

    @api.model
    def default_get(self, fields):
        res = super(CRMPhonecall2Phonecall, self).default_get(fields)
        record_id = (self.env.context and
                     self.env.context.get('active_id', False) or False)
        if record_id:
            phonecall = self.env['crm.phonecall'].browse(record_id)
            if 'summary_id' in fields:
                res.update({'summary_id': phonecall.summary_id.id})
        return res

    def action_schedule(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        # Only consider first wizard, because in all cases there's only one
        this = self.browse(cr, uid, ids, context=context)[0]
        context['summary_id'] = this.summary_id.id
        return super(CRMPhonecall2Phonecall, self).action_schedule(
            cr, uid, ids, context=context)
