from datetime import timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for order in self:
            crm_opportunity = order.opportunity_id
            if not crm_opportunity:
                continue
            activities = order.sudo().company_id.crm_recurring_activity_ids
            for item in activities:
                crm_opportunity.activity_schedule(
                    date_deadline=fields.Date.today()
                    + timedelta(days=item.scheduled_days),
                    summary=item.summary,
                    note=item.note,
                    activity_type_id=item.activity_type_id.id,
                    user_id=item.user_id.id,
                )
        return super().action_confirm()
