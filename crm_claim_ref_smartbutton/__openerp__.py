# -*- coding: utf-8 -*-
##############################################################################
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

{
    "name": "Smart-button for referenced claims",
    "version": "1.0",
    "depends": [
        "crm_claim",
    ],
    "author": "AvanzOSC, "
              "Serv. Tecnol. Avanzados - Pedro M. Baeza, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "contributors": [
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
    ],
    "data": [
        'security/ir.model.access.csv',
    ],
    "category": "Customer Relationship Management",
    "installable": True,
    "uninstall_hook": "uninstall_hook",
}
