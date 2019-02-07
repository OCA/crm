# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def init_lead_ref(cr, registry):
    _logger.info("Initialize leads reference")
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        leads = env['crm.lead'].search([])
        for lead in leads:
            lead.ref = lead._get_next_ref()
    return
