# Copyright 2015-2017 Odoo S.A.
# Copyright 2017 Tecnativa - Vicent Cubells
# Copyright 2018 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from psycopg2.extensions import AsIs

from odoo import fields, models, tools


class CrmClaimReport(models.Model):
    """ CRM Claim Report"""

    _name = "crm.claim.report"
    _auto = False
    _description = "CRM Claim Report"

    user_id = fields.Many2one(comodel_name="res.users", string="User", readonly=True)
    team_id = fields.Many2one(comodel_name="crm.team", string="Team", readonly=True)
    nbr_claims = fields.Integer(string="# of Claims", readonly=True)
    company_id = fields.Many2one(
        comodel_name="res.company", string="Company", readonly=True
    )
    create_date = fields.Datetime(readonly=True, index=True)
    claim_date = fields.Datetime(string="Claim Date", readonly=True)
    delay_close = fields.Float(
        string="Delay to close",
        digits=(16, 2),
        readonly=True,
        group_operator="avg",
        help="Number of Days to close the case",
    )
    stage_id = fields.Many2one(
        comodel_name="crm.claim.stage",
        string="Stage",
        readonly=True,
        domain="[('team_ids','=',team_id)]",
    )
    categ_id = fields.Many2one(
        comodel_name="crm.claim.category", string="Category", readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", readonly=True
    )
    priority = fields.Selection(
        selection=[("0", "Low"), ("1", "Normal"), ("2", "High")], string="Priority"
    )
    type_action = fields.Selection(
        selection=[
            ("correction", "Corrective Action"),
            ("prevention", "Preventive Action"),
        ],
        string="Action Type",
    )
    date_closed = fields.Datetime(string="Close Date", readonly=True, index=True)
    date_deadline = fields.Date(string="Deadline", readonly=True, index=True)
    delay_expected = fields.Float(
        string="Overpassed Deadline",
        digits=(16, 2),
        readonly=True,
        group_operator="avg",
    )
    email = fields.Integer(string="# Emails", readonly=True)
    subject = fields.Char(string="Claim Subject", readonly=True)

    def _select(self):
        select_str = """
            SELECT
            min(c.id) AS id,
            c.date AS claim_date,
            c.date_closed AS date_closed,
            c.date_deadline AS date_deadline,
            c.user_id,
            c.stage_id,
            c.team_id,
            c.partner_id,
            c.company_id,
            c.categ_id,
            c.name AS subject,
            count(*) AS nbr_claims,
            c.priority AS priority,
            c.type_action AS type_action,
            c.create_date AS create_date,
            avg(extract(
                'epoch' FROM (
                    c.date_closed-c.create_date)))/(3600*24)
                    AS delay_close,
            (
                SELECT count(id)
                FROM mail_message
                WHERE model='crm.claim'
                AND res_id=c.id) AS email,
            extract(
                'epoch' FROM (
                    c.date_deadline - c.date_closed))/(3600*24)
                    AS delay_expected
        """
        return select_str

    def _from(self):
        from_str = """
            crm_claim c
        """
        return from_str

    def _group_by(self):
        group_by_str = """
            GROUP BY c.date, c.user_id, c.team_id, c.stage_id, c.categ_id,
                c.partner_id, c.company_id, c.create_date, c.priority,
                c.type_action, c.date_deadline, c.date_closed, c.id
        """
        return group_by_str

    def init(self):
        """ Display Number of cases And Team Name
        @param cr: the current row, from the database cursor,
         """

        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS (
                %s
                from
                %s
                %s)
            """,
            (
                AsIs(self._table),
                AsIs(self._select()),
                AsIs(self._from()),
                AsIs(self._group_by()),
            ),
        )
