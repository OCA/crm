# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c)
#    2015 Serv. Tec. Avanzados - Pedro M. Baeza (http://www.serviciosbaeza.com)
#    2015 AvanzOsc (http://www.avanzosc.es)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{
    "name": "Sequential Code for Claims",
    "version": "1.0",
    "author": "Avanzosc S.L., OdooMRP team, Pedro Baeza",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com",
        "Ana Juaristi <ajuaristo@gmail.com>",
        "Iker Coranti <ikercoranti@avanzosc.com>",
        "Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
    ],
    "category": "Customer Relationship Management",
    "depends": [
        "crm_claim",
    ],
    "data": [
        "views/crm_claim_view.xml",
        "data/claim_sequence.xml",
    ],
    "installable": True,
    "post_init_hook": "assign_old_sequences",
}
