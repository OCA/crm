# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate_crm_helpdesk(cr):
    cr.execute("""
        ALTER TABLE crm_helpdesk
        RENAME COLUMN section_id to team_id""")


def migrate(cr, version):
    """Update database from previous versions, before updating module."""
    if not version:
        return
    migrate_crm_helpdesk(cr)
