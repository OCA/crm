# Copyright 2015 Serv. Tec. Avanzados - Pedro M. Baeza (http://www.serviciosbaeza.com)
# Copyright 2015 AvanzOsc (http://www.avanzosc.es)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Sequential Code for Leads / Opportunities",
    "version": "12.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "Tecnativa, "
              "AvanzOSC, "
              "Odoo Community Association (OCA)",
    "website": "http://www.odoomrp.com",
    "license": "AGPL-3",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <ajuaristo@gmail.com>",
        "Mathias Markl <mathias.markl@mukit.at>",
    ],
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
