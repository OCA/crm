# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Restricted Summary for Phone Calls",
    "summary": "Allows to choose from a defined summary list",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "https://github.com/OCA/crm",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "post_init_hook": "convert_names_to_many2one",
    "depends": [
        "crm_phonecall",
        "sales_team",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/crm_phonecall_summary_view.xml",
        "views/crm_phonecall_view.xml",
    ],
    "images": [
        "images/summary_picker.png",
        "images/summary_editor.png",
    ],
}
