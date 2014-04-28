# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2014 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from operator import attrgetter
from openerp.osv import orm


class crm_claim(orm.Model):
    _inherit = 'crm.claim'

    def _merge_get_default_main(self, cr, uid, claims, context=None):
        return sorted(claims, key=attrgetter('date'))[0]

    def merge(self, cr, uid, ids, merge_in_id=None, context=None):
        """ Merge claims together.

        :param merge_in_ids: the other claims will be merged into this one
            if None, the oldest claim will be selected.
        """
        claims = self.browse(cr, uid, ids, context=context)
        if merge_in_id is None:
            merge_in_id = self._merge_get_default_main(cr, uid, claims,
                                                       context=context).id
        pass
