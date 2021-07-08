# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
try:
    from mailchimp3.helpers import get_subscriber_hash
except ImportError:
    get_subscriber_hash = False

from openupgradelib import openupgrade


def migrate_partner_mailchimp_id(env):
    """We have to fill the mailchimp_id for partners previously subscribed."""
    if not get_subscriber_hash:
        return
    partner_model = env["res.partner"]
    subscribed_partners = partner_model.search(
        [("mailchimp_list_ids", "!=", False), ("email", "!=", False)]
    )
    for partner in subscribed_partners:
        partner.mailchimp_id = get_subscriber_hash(partner.email)


def migrate_merge_field(env):
    """Remove unneeded default from merge_field."""
    merge_field_model = env["mailchimp.merge.field"]
    merge_fields = merge_field_model.search([("code", "=", "'/'")])
    merge_fields.write({"code": False})


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    """Migrate partners and merge fields to streamlined datamodel."""
    migrate_partner_mailchimp_id(env)
    migrate_merge_field(env)
