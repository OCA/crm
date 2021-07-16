# Copyright 2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
try:
    from mailchimp3.helpers import get_subscriber_hash
except ImportError:
    get_subscriber_hash = False


# SQL to create mailchimp_list_model .
STATEMENT_LIST_MODEL = """\
INSERT INTO mailchimp_list_model
    (name, list_id, model, create_date, create_uid, write_date, write_uid)
 SELECT
     ml.name || ' partner',
     ml.id, 'res.partner',
     ml.create_date, ml.create_uid, CURRENT_TIMESTAMP, ml.write_uid
 FROM mailchimp_list ml
"""

# Merge field list_id should refer to mailchimp_list_model now.
STATEMENT_MERGE_FIELD = """\
UPDATE mailchimp_merge_field target
 SET list_model_id = subquery.model_id
 FROM (
     SELECT mf.id AS field_id, mm.id as model_id, mm.list_id
     FROM mailchimp_merge_field mf
     JOIN mailchimp_list_model mm ON mf.list_id = mm.list_id
 ) AS subquery
 WHERE target.id = subquery.field_id
"""

STATEMENT_MERGE_FIELD_CODE = """\
UPDATE mailchimp_merge_field
 SET code = NULL
 WHERE code = '' OR code like '%/%'
"""

STATEMENT_SUBSCRIBER = """\
INSERT INTO mailchimp_subscriber
    (name, list_id, res_model, res_id, mailchimp_id, email, state,
     create_date, create_uid, write_date, write_uid)
 SELECT
     ml.name || ' - ' || rp.name,
     mp.mailchimp_list_id,
     'res.partner',
     mp.res_partner_id,
     rp.mailchimp_id,
     rp.email,
     'active',
     CURRENT_TIMESTAMP, rp.create_uid, CURRENT_TIMESTAMP, rp.write_uid
 FROM mailchimp_list_res_partner_rel mp
 JOIN res_partner rp ON mp.res_partner_id = rp.id
 JOIN mailchimp_list ml ON mp.mailchimp_list_id = ml.id
 WHERE NOT ml.name like '%demo%'
"""

STATEMENT_INTEREST = """\
INSERT INTO mailchimp_subscriber_interest
    (subscriber_id, interest_id, state,
     create_date, create_uid, write_date, write_uid)
 SELECT
     sub.id,
     rel.mailchimp_interest_id,
     'active',
     CURRENT_TIMESTAMP, sub.create_uid, CURRENT_TIMESTAMP, sub.write_uid
 FROM mailchimp_interest_res_partner_rel rel
 JOIN mailchimp_subscriber sub ON rel.res_partner_id = sub.res_id
"""


def migrate_mailchimp_structure(cr):
    """Create mailchimp_models for partner model and relink merge field to these."""
    cr.execute(STATEMENT_LIST_MODEL)
    cr.execute(STATEMENT_MERGE_FIELD)
    cr.execute(STATEMENT_MERGE_FIELD_CODE)


def migrate_subscribers(cr):
    """We have to fill the mailchimp_id for partners previously subscribed."""
    cr.execute(STATEMENT_SUBSCRIBER)
    cr.execute(STATEMENT_INTEREST)


def migrate(cr, version):
    """Migrate partners and merge fields to streamlined datamodel."""
    migrate_mailchimp_structure(cr)
    migrate_subscribers(cr)
