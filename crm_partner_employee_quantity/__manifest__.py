# Copyright 2026 Binhex -  Adasat Torres de León
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Partner Employee Quantity",
    "summary": "Show partner employee quantity in CRM leads",
    "version": "18.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Binhex, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["crm", "partner_employee_quantity"],
    "data": ["views/crm_lead_view.xml"],
}
