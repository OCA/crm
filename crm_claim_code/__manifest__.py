# Copyright 2015 Tecnativa - Pedro M. Baeza <pedro.baeza@tecnativa.com>
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# Copyright 2017 Tecnativa - Vicent Cubells <vicent.cubells@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Sequential Code for Claims",
    "version": "11.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.avanzosc.es",
    "license": "AGPL-3",
    "depends": [
        "crm_claim",
    ],
    "data": [
        "views/crm_claim_view.xml",
        "data/claim_sequence.xml",
    ],
    'installable': True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
