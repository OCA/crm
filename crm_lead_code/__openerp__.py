# -*- coding: utf-8 -*-
# © 2015 Tecnativa - Pedro M. Baeza (https://www.tecnativa.com)
# © 2015 AvanzOsc (http://www.avanzosc.es)
# © 2016 Atul Arvind (http://tech.heliconia.in)


{
    "name": "Sequential Code for Leads / Opportunities",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Tecnativa - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "website": "http://www.odoomrp.com",
    "license": "AGPL-3",
    "depends": [
        "crm",
    ],
    "data": [
        "views/crm_lead_view.xml",
        "data/lead_sequence.xml",
    ],
    'installable': True,
    "pre_init_hook": "create_code_equal_to_id",
    "post_init_hook": "assign_old_sequences",
}
