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
{
    'name': 'Partner City Autocomplete',
    'version': '2.0',
    'category': 'Customer Relationship Management',
    'sequence': 10,
    'summary': 'Partner Localisation and Fiscal Position',
    'description': """ 
This module allows you to import the cities with zip and country.
When you fill in a zip, the city will be automatically filtered based on this zip.
When you select the city, the country will be add automatically.
When the country is set,the related tax position for this country is add automatically.

2.0 : When you do install the module, this version adds the possibility to import, Zip codes and cities for Belgium and France. An option also allows you to import all other countries based on a CSV file.
    """,
    'author': 'BHC',
    'images': ['images/city.png','images/country.png','images/fiscal_position.png','images/customer.png','images/Install_data1.png','images/Install_data2.png',],
    'website': 'www.bhc.be',
    'depends': ['base','account'],
    'data': ['security/ir.model.access.csv','res_country_view.xml','installer.xml'],
    'installable': True,
}