# -*- coding: utf-8 -*-
# © 2015 Serv. Tec. Avanzados - Pedro M. Baeza (http://www.serviciosbaeza.com)
# © 2015 AvanzOsc (http://www.avanzosc.es)

{
    "name": "Sequential Code for Claims",
    "version": "9.0.1.0.0",
    "category": "Customer Relationship Management",
    "author": "OdooMRP team, "
              "AvanzOSC, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.avanzosc.es",
    "license": "AGPL-3",
    "contributors": [
        "Pedro M. Baeza <pedro.baeza@tecnativa.com>",
        "Ana Juaristi <ajuaristo@gmail.com>",
        "Iker Coranti <ikercoranti@avanzosc.com>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        "Cyril Gaudin <cyril.gaudin@camptocamp.com>",
    ],
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
