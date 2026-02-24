# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


def create_code_equal_to_id(env):
    env.cr.execute(
        "SELECT column_name FROM information_schema.columns "
        "WHERE table_name = 'crm_claim' AND column_name = 'code'"
    )
    if not env.cr.fetchone():
        env.cr.execute("ALTER TABLE crm_claim ADD COLUMN code character varying;")
        env.cr.execute("UPDATE crm_claim SET code = id;")


def assign_old_sequences(env):
    env.cr.execute("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'crm_claim' AND column_name = 'code'
    """)
    sequence_model = env["ir.sequence"]
    claims = env["crm.claim"].search([], order="id")
    for claim in claims:
        claim.code = sequence_model.next_by_code("crm.claim")
