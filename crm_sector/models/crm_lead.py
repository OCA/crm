# -*- coding: utf-8 -*-
# © 2015 Antiun Ingenieria S.L. - Javier Iniesta
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    sector_id = fields.Many2one(comodel_name='res.partner.sector',
                                string='Main Sector')

    secondary_sector_ids = fields.Many2many(
        comodel_name='res.partner.sector', string="Secondary Sectors",
        domain="[('id', '!=', sector_id)]")

    @api.one
    @api.constrains('sector_id', 'secondary_sector_ids')
    def _check_sectors(self):
        if self.sector_id in self.secondary_sector_ids:
            raise exceptions.UserError(_('The secondary sectors must be '
                                       'different from the main sector.'))

    @api.multi
    def _lead_create_contact(self, name, is_company,
                             parent_id=False):
        """Propagate sector to created partner.
        """
        partner = super(CrmLead, self)._lead_create_contact(
            name, is_company, parent_id)
        partner.write({
            'sector_id': self.sector_id.id,
            'secondary_sector_ids': [(6, 0, self.secondary_sector_ids.ids)],
        })
        return partner
