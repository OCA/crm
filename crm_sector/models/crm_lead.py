# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, exceptions, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sector_id = fields.Many2one(comodel_name='res.partner.sector',
                                string='Main Sector', oldname='sector')

    secondary_sector_ids = fields.Many2many(
        comodel_name='res.partner.sector', string="Secondary Sectors",
        domain="[('id', '!=', sector_id)]")

    @api.one
    @api.constrains('sector_id', 'secondary_sector_ids')
    def _check_sectors(self):
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
