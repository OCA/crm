# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Phonecall planner",
    "summary": "Schedule phone calls according to some criteria",
    "version": "15.0.1.0.2",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["crm_phonecall", "partner_phonecall_schedule"],
    "data": ["security/ir.model.access.csv", "wizards/crm_phonecall_planner_view.xml"],
}
