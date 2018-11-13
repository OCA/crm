# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """
    The objective of this hook is to help in migration if you came
    from v9 using openupgrade.
    """
    migration_from_openupgrade_v9(cr)


def migration_from_openupgrade_v9(cr):
    cr.execute("""SELECT column_name
    FROM information_schema.columns
    WHERE table_name='crm_stage'
        AND column_name='openupgrade_legacy_10_0_type'""")
    if cr.fetchone():
        logger.info("table crm_stage, column openupgrade_legacy_10_0_type: "
                    "renaming to lead_type")
        cr.execute('ALTER TABLE "crm_stage" RENAME '
                   '"openupgrade_legacy_10_0_type" TO "lead_type"')
        cr.execute('DROP INDEX IF EXISTS '
                   '"crm_stage_openupgrade_legacy_10_0_type_index"')
