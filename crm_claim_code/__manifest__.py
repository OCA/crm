# Copyright 2015-2018 Tecnativa - Pedro M. Baeza
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# Copyright 2017 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Sequential Code for Claims",
    "version": "13.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "AvanzOSC, Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "depends": ["crm_claim"],
    "data": ["views/crm_claim_view.xml", "data/claim_sequence.xml"],
    "installable": True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
