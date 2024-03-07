# Copyright (C) 2017-2024 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(
        env.cr, "crm_lead_line", "expected_revenue"
    ) and not openupgrade.column_exists(env.cr, "crm_lead_line", "prorated_revenue"):
        env.cr.execute(
            """
            ALTER TABLE crm_lead_line
            ADD COLUMN prorated_revenue NUMERIC;
            COMMENT ON COLUMN crm_lead_line.prorated_revenue
            IS 'Prorated Revenue';
        """
        )
        # PostgreSQL already automatically truncates from `double_precision` type to
        # `numeric` type, this is needed as we are converting from Float Odoo field
        # to Monetary Odoo field
        env.cr.execute(
            """
            UPDATE crm_lead_line
            SET prorated_revenue = expected_revenue;
            """
        )
        env.cr.execute(
            """
            ALTER TABLE crm_lead_line
            DROP COLUMN expected_revenue;
            """
        )
    if openupgrade.column_exists(
        env.cr, "crm_lead_line", "planned_revenue"
    ) and not openupgrade.column_exists(env.cr, "crm_lead_line", "expected_revenue"):
        env.cr.execute(
            """
            ALTER TABLE crm_lead_line
            ADD COLUMN expected_revenue NUMERIC;
            COMMENT ON COLUMN crm_lead_line.expected_revenue
            IS 'Expected Revenue';
        """
        )
        # PostgreSQL already automatically truncates from `double_precision` type to
        # `numeric` type, this is needed as we are converting from Float Odoo field
        # to Monetary Odoo field
        env.cr.execute(
            """
            UPDATE crm_lead_line
            SET expected_revenue = planned_revenue;
            """
        )
        env.cr.execute(
            """
            ALTER TABLE crm_lead_line
            DROP COLUMN planned_revenue;
            """
        )
