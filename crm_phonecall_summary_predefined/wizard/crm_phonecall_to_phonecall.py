# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class CrmPhonecall2phonecall(models.TransientModel):

    _inherit = "crm.phonecall2phonecall"

    name = fields.Char(
        related="summary_id.name", store=True, required=False, readonly=True,
    )
    summary_id = fields.Many2one(
        comodel_name="crm.phonecall.summary",
        string="Summary",
        required=True,
        ondelete="restrict",
    )

    @api.model
    def default_get(self, fields):
        """Function gets default values."""
        res = super().default_get(fields)
        for phonecall in self.env["crm.phonecall"].browse(
            self.env.context.get("active_id")
        ):
            res["summary_id"] = getattr(phonecall, "summary_id").id
        return res

    def get_vals_action_schedule(self):
        res = super().get_vals_action_schedule()
        res.update({"summary_id": self.summary_id.id})
        return res
