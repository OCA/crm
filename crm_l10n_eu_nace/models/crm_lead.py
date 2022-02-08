from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    nace_id = fields.Many2one(
        comodel_name="res.partner.nace", string="Main NACE", index=True
    )
    secondary_nace_ids = fields.Many2many(
        comodel_name="res.partner.nace", string="Secondary NACE"
    )

    def _prepare_customer_values(self, name, is_company, parent_id=False):
        """Propagate NACE activity to created partner."""
        result = super()._prepare_customer_values(name, is_company, parent_id)
        if self.nace_id:
            result["nace_id"] = self.nace_id.id
        if self.secondary_nace_ids:
            result["secondary_nace_ids"] = [
                (4, id_) for id_ in self.secondary_nace_ids.ids
            ]
        return result
