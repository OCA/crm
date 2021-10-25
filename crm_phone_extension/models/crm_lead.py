# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    phone_extension = fields.Char("Phone Extension", help="Phone Number Extension.")
