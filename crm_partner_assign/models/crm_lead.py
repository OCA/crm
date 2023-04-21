# Copyright 2023 Moduon Team S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

from odoo import api, fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    partner_contact_assigned_id = fields.Many2one(
        comodel_name="res.partner",
        domain="[('is_company', '=', False)]",
        string="Assigned Partner Contact",
        tracking=True,
        help="Partner Contact this case has been assigned to.",
        check_company=True,
    )
    partner_assigned_id = fields.Many2one(
        comodel_name="res.partner",
        string="Assigned Partner",
        help="Partner this case has been assigned to.",
        related="partner_contact_assigned_id.commercial_partner_id",
        store=True,
        readonly=True,
        check_company=True,
    )
    date_partner_assign = fields.Date(
        compute="_compute_date_partner_assign",
        string="Partner Assignment Date",
        readonly=False,
        store=True,
        copy=True,
        help="Last date this case was assigned to a partner",
    )

    @api.depends("partner_assigned_id")
    def _compute_date_partner_assign(self):
        for lead in self:
            if not lead.partner_assigned_id:
                lead.date_partner_assign = False
            else:
                lead.date_partner_assign = fields.Date.context_today(lead)

    def _merge_get_fields(self):
        fields_list = super()._merge_get_fields()
        fields_list += [
            "partner_assigned_id",
            "partner_contact_assigned_id",
            "date_partner_assign",
        ]
        return fields_list
