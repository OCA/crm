# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.models import BaseModel
from .models.base_model import registered_dbs
from . import models


def uninstall_hook(cr, registry):
    # Undo monkey-patching to restore functionality
    registered_dbs.remove(cr.dbname)
    if not registered_dbs:
        BaseModel.fields_view_get = BaseModel.base_fields_view_get
