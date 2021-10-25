# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Secondary phone number on lead",
    "summary": "Adds a secondary phone number on lead",
    "license": "AGPL-3",
    "version": "14.0.1.0.0",
    "author": "BizzAppDev, Odoo Community Association (OCA)",
    "maintainers": ["bizzappdev"],
    "category": "Customer Relationship Management",
    "depends": ["crm"],
    "website": "https://github.com/OCA/crm",
    "external_dependencies": {"python": ["phonenumbers"]},
    "data": ["views/crm_lead.xml"],
}
