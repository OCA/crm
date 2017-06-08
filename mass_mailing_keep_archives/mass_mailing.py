# -*- coding: utf-8 -*-
from openerp import models, api, fields


class MassMailing(models.Model):
    _inherit = "mail.mass_mailing"

    keep_archives = fields.Boolean('Keep Archives')


class MailComposeMessage(models.Model):
    _inherit = "mail.compose.message"

    @api.model
    def get_mail_values(self, wizard, res_ids):
        """ Override method to add keep_archives functionalty """
        res = super(MailComposeMessage, self).get_mail_values(
            wizard, res_ids)
        # use only for allowed models in mass mailing
        if wizard.composition_mode == 'mass_mail' and \
                (wizard.mass_mailing_name or wizard.mass_mailing_id) and \
                wizard.model in [item[0] for item in self.env[
                    'mail.mass_mailing']._get_mailing_model()]:
            mass_mailing = wizard.mass_mailing_id
            # opcion solo desde mass mailing, no para composiciones que creen
            # mass mailings
            if mass_mailing:
                for res_id in res_ids:
                    res[res_id].update({
                        'auto_delete': not mass_mailing.keep_archives,
                    })
        return res
