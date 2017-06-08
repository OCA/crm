# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L.
# © 2016 Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, tools


class CrmOpportunityReport(models.Model):
    _inherit = "crm.opportunity.report"

    substage_id = fields.Many2one(
        comodel_name="crm.case.substage", string="Substage")

    def init(self, cr):
        super(CrmOpportunityReport, self).init(cr)
        cr.execute("SELECT pg_get_viewdef('crm_opportunity_report', true)")
        view_def = cr.fetchone()[0]
        # Inject the new field in the expected SQL
        sql = "SELECT "
        index = view_def.find(sql) + len(sql)
        if index >= 0:
            sql = "    c.substage_id,\n"
            view_def = view_def[:index] + sql + view_def[index:-1]
            tools.drop_view_if_exists(cr, 'crm_opportunity_report')
            cr.execute(
                "CREATE OR REPLACE VIEW crm_opportunity_report AS (%s)" %
                view_def)
