# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2006 - 2015 BHC SPRL www.bhc.be
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

import datetime
from lxml import etree
import math
import pytz
import re
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
import time
import openerp
from openerp import SUPERUSER_ID, api
from openerp import tools
from openerp.osv import fields, osv, expression
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round

import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)

class format_address(object):
    def fields_view_get_address(self, cr, uid, arch, context={}):
        user_obj = self.pool.get('res.users')
        fmt = user_obj.browse(cr, SUPERUSER_ID, uid, context).company_id.country_id
        fmt = fmt and fmt.address_format
        layouts = {
            '%(city)s %(state_code)s\n%(zip)s': """
                <div class="address_format">
                    <field name="city" placeholder="City" style="width: 50%%"/>
                    <field name="state_id" class="oe_no_button" placeholder="State" style="width: 47%%" options='{"no_open": true}'/>
                    <br/>
                    <field name="zip" placeholder="ZIP"/>
                </div>
            """,
            '%(zip)s %(city)s': """
                <div class="address_format">
                    <field name="zip" placeholder="ZIP" style="width: 40%%"/>
                    <field name="city" placeholder="City" style="width: 57%%"/>
                    <br/>
                    <field name="state_id" class="oe_no_button" placeholder="State" options='{"no_open": true}'/>
                </div>
            """,
            '%(zip)s %(city2)s': """
                <div class="address_format">
                    <field name="zip" placeholder="ZIP" style="width: 40%%"/>
                    <field name="city" placeholder="City" style="width: 57%%"/>
                    <br/>
                    <field name="state_id" class="oe_no_button" placeholder="State" options='{"no_open": true}'/>
                </div>
            """,
            '%(city)s\n%(state_name)s\n%(zip)s': """
                <div class="address_format">
                    <field name="city" placeholder="City"/>
                    <field name="state_id" class="oe_no_button" placeholder="State" options='{"no_open": true}'/>
                    <field name="zip" placeholder="ZIP"/>
                </div>
            """
        }
        for k,v in layouts.items():
            if fmt and (k in fmt):
                doc = etree.fromstring(arch)
                for node in doc.xpath("//div[@class='address_format']"):
                    tree = etree.fromstring(v)
                    node.getparent().replace(node, tree)
                arch = etree.tostring(doc)
                break
        return arch


class Country(osv.osv):
    _inherit = 'res.country'
    _columns = {
        'pos_fis': fields.many2one('account.fiscal.position','Fiscal Position',),
    }
Country()

class fiscal(osv.osv):
    _inherit = 'account.fiscal.position'
    _columns = {
        'country': fields.one2many('res.country','pos_fis','Country',),
    }
fiscal()

    
class zip_city(osv.osv):
    _name = "zip.city"
    _columns = {
        'zip': fields.char('Zip',size=128),
        'name': fields.char('City',size=128, required=True),
        'country':fields.many2one('res.country','Country'),
    }
zip_city() 

class partner(osv.osv):
    _inherit="res.partner"
    _columns={
              'city2': fields.many2one('zip.city','City',domain="[('zip','=',zip)]"),
              }
    def _display_address(self, cr, uid, address, without_company=False, context=None):
        # get the information that will be injected into the display format
        # get the address format
        address_format = address.country_id and address.country_id.address_format or \
              "%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'state_code': address.state_id and address.state_id.code or '',
            'state_name': address.state_id and address.state_id.name or '',
            'country_code': address.country_id and address.country_id.code or '',
            'country_name': address.country_id and address.country_id.name or '',
            'company_name': address.parent_id and address.parent_id.name or '',
            'city2': address.city2 and address.city2.name or '',
        }
        for field in self._address_fields(cr, uid, context=context):
            args[field] = getattr(address, field) or ''
        if without_company:
            args['company_name'] = ''
        elif address.parent_id:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args
    
    def onchange_zip(self,cr,uid,ids,zip):
        res={}
        res['city']=''
        res['city2']=False
        res['country_id']=False
        res['property_account_position'] = False
        return {'value': res}
    
    def onchange_city(self,cr,uid,ids,city2):
        res={}
        if not city2:
            res['city']=''
            return {'value': res}
        else:
            idss=self.pool.get('zip.city').browse(cr,uid,city2)
            res['city']=idss.name
            if idss.country and idss.country.id:
                res['country_id']=idss.country.id
                fis=self.pool.get('res.country').browse(cr,uid,idss.country.id).pos_fis.id
                if fis:
                    res['property_account_position'] = fis
            return {'value': res}
        return {}
    
    def onchange_country(self, cr, uid, ids, country, context=None):
        value = {}
        if country:
            fis=self.pool.get('res.country').browse(cr,uid,country).pos_fis.id
            if fis:
                value['property_account_position'] = fis
            else:
                value['property_account_position'] = False
        else:
            value['property_account_position'] = False
        return {'value': value}
    
partner()