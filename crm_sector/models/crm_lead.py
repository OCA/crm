# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, exceptions, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sector_id = fields.Many2one(comodel_name='res.partner.sector',
                                string='Main Sector', oldname='sector')

    secondary_sector_ids = fields.Many2many(
        comodel_name='res.partner.sector', string="Secondary Sectors",
        domain="[('id', '!=', sector_id)]")

    @api.multi
    @api.constrains('sector_id', 'secondary_sector_ids')
    def _check_sectors(self):
        self.ensure_one()
        if self.sector_id in self.secondary_sector_ids:
            raise exceptions.Warning(_('The secondary sectors must be '
                                       'different from the main sector.'))

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        """Propagate sector to created partner.
        """
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id)
        secondary_sector_ids = []
        for sector in lead.secondary_sector_ids:
            secondary_sector_ids.append((4, sector.id, 0))
        self.env['res.partner'].browse(partner_id).write(
            {'sector_id': lead.sector_id.id,
             'secondary_sector_ids': secondary_sector_ids})
        return partner_id

    @api.multi
    def on_change_partner_id(self, partner_id):
        res = super(CrmLead, self).on_change_partner_id(partner_id)
        if partner_id:
            partner = self.env['res.partner'].browse(partner_id)
            if res is None:
                res = {'value': {}}
            res['value']['sector_id'] = partner.sector_id
            res['value']['secondary_sector_ids'] = [
                (6, 0, partner.secondary_sector_ids.ids)]
        return res
