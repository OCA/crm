# -*- coding: utf-8 -*-
# © 2015 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# © 2015 Javier Iniesta <javieria@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields, _
from openerp.exceptions import Warning as UserError


class PartnerMailListWizard(models.TransientModel):
    _name = "partner.mail.list.wizard"
    _description = "Create contact mailing list"

    mail_list_id = fields.Many2one(comodel_name="mail.mass_mailing.list",
                                   string="Mailing List")
    partner_ids = fields.Many2many(
        comodel_name="res.partner", relation="mail_list_wizard_partner",
        default=lambda self: self.env.context.get("active_ids"))

    @api.multi
    def add_to_mail_list(self):
        contact_obj = self.env['mail.mass_mailing.contact']
        for partner in self.partner_ids:
            if not partner.email:
                raise UserError(_("Partner '%s' has no email.") % partner.name)
            criteria = [('email', '=', partner.email),
                        ('list_id', '=', self.mail_list_id.id)]
            contact_test = contact_obj.search(criteria)
            if contact_test:
                continue
            contact_vals = {
                'email': partner.email,
                'name': partner.name,
                'list_id': self.mail_list_id.id
            }
            contact_obj.create(contact_vals)
