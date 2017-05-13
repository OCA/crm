# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class NewsletterNewsletter(models.Model):
    _inherit = 'newsletter.newsletter'

    template_body_type = fields.Selection(
        related=['type_id', 'email_template_id', 'body_type']
    )
