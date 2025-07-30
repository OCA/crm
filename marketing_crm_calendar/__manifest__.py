# Copyright 2025 Juan Alberto Raja <juan.raja@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "CRM Phonecall Calendar Tracking",
    "summary": "Automatically copy campaign fields from calls to calendar events",
    "version": "18.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Sygel, Odoo Community Association (OCA)",
    "depends": [
        "crm_phonecall",
        "crm",
        "calendar",
    ],
    "license": "AGPL-3",
    "website": "https://github.com/OCA/crm",
    "data": [
        "views/calendar_event_views.xml",
    ],
    "installable": True,
    "application": False,
}
