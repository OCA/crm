# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# © 2016 Antonio Espinosa - <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    mass_mailing_contact_ids = fields.One2many(
        string="Mailing lists",
        oldname="mass_mailing_contacts",
        domain=[('opt_out', '=', False)],
        comodel_name='mail.mass_mailing.contact', inverse_name='partner_id')
    mass_mailing_contacts_count = fields.Integer(
        string='Mailing list number',
        compute='_compute_mass_mailing_contacts_count', store=True)
    mass_mailing_stats = fields.One2many(
        string="Mass mailing stats",
        comodel_name='mail.mail.statistics', inverse_name='partner_id')
    mass_mailing_stats_count = fields.Integer(
        string='Mass mailing stats number',
        compute='_compute_mass_mailing_stats_count', store=True)

    @api.one
    @api.constrains('email')
    def _check_email_mass_mailing_contacts(self):
        if self.mass_mailing_contact_ids and not self.email:
            raise ValidationError(
                _("This partner '%s' is subscribed to one or more "
                  "mailing lists. Email must be assigned." % self.name))

    @api.one
    @api.depends('mass_mailing_contact_ids',
                 'mass_mailing_contact_ids.opt_out')
    def _compute_mass_mailing_contacts_count(self):
        self.mass_mailing_contacts_count = len(self.mass_mailing_contact_ids)

    @api.one
    @api.depends('mass_mailing_stats')
    def _compute_mass_mailing_stats_count(self):
        self.mass_mailing_stats_count = len(self.mass_mailing_stats)

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if vals.get('name') or vals.get('email'):
            mm_vals = {}
            if vals.get('name'):
                mm_vals['name'] = vals['name']
            if vals.get('email'):
                mm_vals['name'] = vals['email']
            self.env["mail.mass_mailing.contact"].search([
                ("partner_id", "in", self.ids),
            ]).write(mm_vals)
        return res
