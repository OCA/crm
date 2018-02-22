# -*- coding: utf-8 -*-
# Copyright 2016 Pedro M. Baeza <pedro.baeza@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.osv import osv
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError


class BasePartnerMergeAutomaticWizard(models.TransientModel):
    _inherit = "base.partner.merge.automatic.wizard"

    # The field is named this way to not be automatically added as a "group by"
    # option, which is performed in the code through the name of the field
    fuzzy_name_group_by = fields.Boolean(
        string='Similar name',
        help="WARNING: This option is significantly slower than the others, "
             "because the match cannot be performed in group.")
    max_fuzzy_name_difference = fields.Integer(
        string="Max. characters difference", default=2)

    def _register_hook(self, cr):
        cr.execute(
            """
            SELECT *
            FROM pg_extension
            WHERE extname = 'fuzzystrmatch'
            """)
        if not cr.fetchall():
            try:
                # Try to install the extension
                cr.execute("CREATE EXTENSION fuzzystrmatch")
            except:
                raise UserError(
                    _("PostgreSQL extension 'fuzzystrmatch' is not present on "
                      "your DB and can't be auto-installed. Please install "
                      "it."))
        return super(BasePartnerMergeAutomaticWizard,
                     self)._register_hook(cr)

    def _compute_selected_groupby(self, this):
        if this.fuzzy_name_group_by:
            try:
                return super(BasePartnerMergeAutomaticWizard,
                             self)._compute_selected_groupby(this)
            except osv.except_osv:
                # There are no groups
                return []
        return super(BasePartnerMergeAutomaticWizard,
                     self)._compute_selected_groupby(this)

    @api.multi
    def _process_query(self, query):
        if self.fuzzy_name_group_by:
            partner_obj = self.env['res.partner']
            line_obj = self.env['base.partner.merge.line']
            groups = self._compute_selected_groupby(self)
            models = self.compute_models()
            counter = 0
            # Reuse WHERE part of the built query
            index_where = query.find('WHERE')
            if index_where > 0:
                index_group_by = query.find('GROUP BY')
                if index_group_by > 0:
                    where_query = query[index_where + 5:index_group_by]
                else:
                    where_query = query[index_where + 5:]
                self.env.cr.execute(
                    "SELECT id FROM res_partner "
                    "WHERE active = True AND (%s)" % where_query)
                partners = partner_obj.browse(
                    [x[0] for x in self.env.cr.fetchall()])
            else:
                partners = partner_obj.search([])
            while partners:
                partner = partners[0]
                partners -= partner
                if not partner.exists():
                    # It has been removed while processing
                    continue  # pragma: no cover
                query = (
                    "SELECT id "
                    "FROM res_partner "
                    "WHERE levenshtein("
                    "  %s, "
                    "  substring(name for 100))"
                    "  <= %s "
                    "AND id != %s")
                for field in groups:
                    query += " AND %s = '%s'" % (
                        field, getattr(partner, field))
                self.env.cr.execute(
                    query, (partner.name[:100],
                            self.max_fuzzy_name_difference, partner.id))
                match_partner_ids = [x[0] for x in self.env.cr.fetchall()]
                if match_partner_ids:
                    partners -= partner_obj.browse(match_partner_ids)
                    if models and self._partner_use_in(
                            match_partner_ids, models):
                        continue
                    counter += 1
                    values = {
                        'wizard_id': self.id,
                        'min_id': partner.id,
                        'aggr_ids': match_partner_ids + partner.ids,
                    }
                    line_obj.create(values)
            self.write({
                'state': 'selection',
                'number_group': counter,
            })
            return
        return super(BasePartnerMergeAutomaticWizard,
                     self)._process_query(query)
