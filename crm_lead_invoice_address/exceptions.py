# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, exceptions


class CrmLeadInvoiceAddressValidationError(exceptions.ValidationError):
    def __init__(self, msg=None):
        msg = msg or self._value
        super(CrmLeadInvoiceAddressValidationError, self).__init__(msg)


class Need2PartnersError(CrmLeadInvoiceAddressValidationError):
    _value = _("Need partner and contact names to separate invoice address.")
