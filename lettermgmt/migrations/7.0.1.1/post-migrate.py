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
    if previous_version == '6.1.1.0':
        # migration from letter_mgmt_v6
        cr.execute(
            'update res_letter set sender_partner_id=recipient_partner_id,'
            "recipient_partner_id=null where move='in'")
        cr.execute(
            'update res_letter set recipient_partner_id=u.partner_id '
            "from res_users u where snd_rec_id=u.id and move='in'")
        cr.execute(
            'update res_letter set sender_partner_id=u.partner_id '
            "from res_users u where snd_rec_id=u.id and move='out'")
