# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import IntegrityError
from openerp import api, fields, models, SUPERUSER_ID


class CRMPhonecall(models.Model):
    _inherit = "crm.phonecall"

    name = fields.Char(
        related="summary_id.name",
        store=True,
        required=False,
        readonly=True)
    summary_id = fields.Many2one(
        comodel_name="crm.phonecall.summary",
        string="Summary",
        required=True,
        ondelete="restrict")

    def _set_default_value_on_column(self, cr, column_name, context=None):
        """Default values when creating the field."""
        if column_name != "summary_id":
            return super(CRMPhonecall, self)._set_default_value_on_column(
                cr, column_name, context)

        # Ensure crm.phonecall.summary is installed before continuing
        summary = self.pool["crm.phonecall.summary"]
        if not summary._table_exist(cr):
            summary._auto_init(cr, context)

        # Proper default value per row
        self._init_summary_id(cr, SUPERUSER_ID)

    @api.model
    def _init_summary_id(self):
        """Convert old string names to new Many2one."""
        summary = self.env["crm.phonecall.summary"]
        for s in self.search([("summary_id", "=", False)]):
            try:
                with self.env.cr.savepoint():
                    s.summary_id = summary.create({
                        "name": s.name,
                    })
            except IntegrityError:
                s.summary_id = summary.search([("name", "=", s.name)])

    @api.model
    def _prepare_another_phonecall_vals(
            self, call, schedule_time, call_summary, user_id=False,
            section_id=False, categ_id=False):
        res = super(CRMPhonecall, self)._prepare_another_phonecall(
            call, schedule_time, call_summary, user_id=user_id,
            section_id=section_id, categ_id=categ_id)
        summary_id = (self.env.context and
                      self.env.context.get('summary_id', False) or False)
        res['summary_id'] = summary_id
        return res
