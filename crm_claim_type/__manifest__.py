# Copyright 2015 Vauxoo: Yanina Aular <yani@vauxoo.com>,
# Copyright 2015 Vauxoo: Osval Reyes <osval@vauxoo.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Claim Types",
    "category": "Customer Relationship Management",
    "summary": "Claim types for CRM",
    "author": "Vauxoo, "
    "Ursa Information Systems, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/crm",
    "license": "AGPL-3",
    "version": "13.0.1.0.0",
    "depends": ["crm_claim"],
    "data": [
        "data/crm_claim_type.xml",
        "data/crm_claim_stage.xml",
        "security/ir.model.access.csv",
        "views/crm_claim.xml",
        "views/crm_claim_stage.xml",
        "views/crm_claim_type.xml",
    ],
    "demo": ["demo/crm_claim.xml", "demo/crm_claim_stage.xml"],
    "installable": True,
    "auto_install": False,
}
