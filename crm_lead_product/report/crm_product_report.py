# Copyright (C) 2017-19 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from psycopg2.extensions import AsIs

from odoo import fields, models, tools


class ActivityReport(models.Model):
    """CRM Lead Analysis"""

    _name = "crm.product.report"
    _auto = False
    _description = "CRM Pipeline by Product Analysis"
    _rec_name = "id"

    active = fields.Boolean(readonly=True)
    campaign_id = fields.Many2one("utm.campaign", "Campaing", readonly=True)
    country_id = fields.Many2one("res.country", "Country", readonly=True)
    company_id = fields.Many2one("res.company", "Company", readonly=True)
    create_date = fields.Datetime(readonly=True)
    date_closed = fields.Datetime("Closed Date", readonly=True)
    date_conversion = fields.Datetime("Conversion Date", readonly=True)
    date_deadline = fields.Datetime("Deadline Date", readonly=True)
    date_open = fields.Datetime("Open Date", readonly=True)
    lost_reason = fields.Many2one("crm.lost.reason", readonly=True)
    name = fields.Char("Lead Name", readonly=True)
    partner_id = fields.Many2one("res.partner", "Partner/Customer", readonly=True)
    partner_name = fields.Char("Contact Name", readonly=True)
    probability = fields.Float(group_operator="avg", readonly=True)
    stage_id = fields.Many2one("crm.stage", "Stage", readonly=True)
    team_id = fields.Many2one("crm.team", "Sales Team", readonly=True)
    type = fields.Selection(
        [("lead", "Lead"), ("opportunity", "Opportunity")],
        help="Type is used to separate Leads and Opportunities",
    )
    user_id = fields.Many2one("res.users", "Salesperson", readonly=True)
    category_id = fields.Many2one("product.category", "Category", readonly=True)
    expected_revenue = fields.Float(readonly=True)
    planned_revenue = fields.Float(readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)
    product_qty = fields.Integer("Product Quantity", readonly=True)
    product_tmpl_id = fields.Many2one(
        "product.template", "Product Template", readonly=True
    )

    def _select(self):
        return """
            SELECT
                l.id,
                l.active,
                l.id as lead_id,
                l.campaign_id,
                l.country_id,
                l.company_id,
                l.create_date,
                l.date_closed,
                l.date_conversion,
                l.date_deadline,
                l.date_open,
                l.lost_reason_id,
                l.name,
                l.partner_id,
                l.partner_name,
                l.probability,
                l.type,
                l.stage_id,
                l.team_id,
                l.user_id,
                ll.category_id,
                ll.expected_revenue,
                ll.planned_revenue,
                ll.product_id,
                ll.product_qty,
                ll.product_tmpl_id
        """

    def _from(self):
        return """
            FROM crm_lead AS l
        """

    def _join(self):
        return """
            JOIN crm_lead_line AS ll ON l.id = ll.lead_id
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                %s
                %s
                %s
            )
        """,
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                AsIs(self._join()),
            ),
        )
