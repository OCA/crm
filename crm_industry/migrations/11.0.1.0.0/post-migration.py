# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade
from psycopg2.extensions import AsIs


def fill_crm_lead_industry_id(cr):
    cr.execute(
        """
        UPDATE crm_lead cl
        SET industry_id = rpi.id
        FROM res_partner_industry rpi
        WHERE cl.%s IS NOT NULL AND cl.%s = rpi.%s
            """, (
            AsIs(openupgrade.get_legacy_name('sector_id')),
            AsIs(openupgrade.get_legacy_name('sector_id')),
            AsIs(openupgrade.get_legacy_name('old_sector_id')),
        ),
    )


def fill_crm_lead_industry_secondary(cr):
    cr.execute(
        """
        INSERT INTO crm_lead_res_partner_industry_rel (crm_lead_id,
            res_partner_industry_id)
        SELECT rel.crm_lead_id, rpi.id
        FROM crm_lead_res_partner_sector_rel rel
        LEFT JOIN res_partner_industry rpi
            ON rel.res_partner_sector_id = rpi.%s
        """, (AsIs(openupgrade.get_legacy_name('old_sector_id')),),
    )


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    cr = env.cr
    fill_crm_lead_industry_id(cr)
    fill_crm_lead_industry_secondary(cr)
