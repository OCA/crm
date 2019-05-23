# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# Copyright 2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # No need to check existence, as if getting to this, it will exist
    openupgrade.rename_fields(
        env, [
            ('crm.lead', 'crm_lead', 'sector_id', 'industry_id'),
        ],
    )
    # Many2many field
    openupgrade.rename_tables(
        env.cr, [('crm_lead_res_partner_sector_rel',
                  'crm_lead_res_partner_industry_rel')],
    )
    openupgrade.rename_columns(env.cr, {
        'crm_lead_res_partner_industry_rel': [
            ('res_partner_sector_id', 'res_partner_industry_id'),
        ],
    })
