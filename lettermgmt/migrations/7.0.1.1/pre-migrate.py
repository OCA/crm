# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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


def migrate(cr, previous_version):
    if previous_version == '7.0.0.1':
        # probably nobody used this version anyway
        raise NotImplementedError(
            'Migrating from the previous community version is not supported '
            'yet')
    if previous_version == '6.1.1.0':
        # migration from letter_mgmt_v6
        cr.execute('alter table res_letter rename column date to snd_rec_date')
        cr.execute('alter table res_letter rename column ref_data to orig_ref')
        cr.execute(
            'alter table res_letter rename column partner_id to '
            'recipient_partner_id')
