from openupgradelib import openupgrade

_field_renames = [
    ("crm.stage", "crm_stage", "openupgrade_legacy_13_0_probability", "probability"),
]


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(
        env.cr, "crm_stage", "openupgrade_legacy_13_0_probability"
    ):
        openupgrade.rename_fields(env, _field_renames)
