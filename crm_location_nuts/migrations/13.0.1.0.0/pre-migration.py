# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

_field_renames = [
    ("crm.lead", "crm_lead", "region", "nuts2_id"),
    ("crm.lead", "crm_lead", "substate", "nuts3_id"),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, _field_renames)
