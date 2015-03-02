# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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
    'name': 'Newsletters',
    'version': '1.0',
    'description': """
With this addon, you can send HTML-formatted mass emails to your customers.
While it was developed with primarily newsletters in mind, it works for
arbitrary objects and arbitrary content.

Preparations
------------

Under Sales/Configuration/Newsletter types, review the default one or create a
new one. You'll have to fill in a name, a model, a domain expression on that
model, an email template (have a look a the default newsletter type's email
template to see how this might look like) and the address that should show up
as the sender's address.

If you fill in a group in the type's groups-field, only users which are a
member of said group are allowed to send a newsletter of this type. See below
for details.

Finally, click 'Show recipient objects' to check the list of records that will
receive a newsletter of this type. We work with dynamic selections here, so
this list ist not fixed and will be evaluated every time you send a newsletter.

Usage
-----

After a newsletter type is configured, the handling is pretty straightworfard:
Go to Sales/Newsletters/Newsletters and create a new one. Choose the type you
configured before and fill in a subject.
    
Often, a template will be chosen that enforces a certain layout for different
subsections of your text. That's why the text is broken up into an intro, an
outro and topics with optional heading in between. This way, you can put most
of the layout into the template and leave only the interesting layout to your
users.

A note on images: If you upload an image via the editor, it will be embedded
as dataurl into the resulting email. This is good for your customers' privacy,
but bad for bandwidth, so take care to chose reasonable image sizes.

It is mandatory that you click on 'Preview' before you are allowed to finally
send the newsletter. The sending process uses OpenERP's standard email queue.

Security
--------
There are three groups defined:

newsletter editor
  A user who can create a newsletter and add/edit topics

newsletter sender
  A user who may send newsletters. Note that if a newsletter type is
  restricted to certain groups, the user has to be a newsletter sender and
  be a member of one of the groups given in the newsletter type

newsletter manager
  A user who may edit newsletter types

Note that the groups are listed in order of inheritance, so a newsletter sender
always also is an editor and a manager is a sender as well as an editor.
    """,
    'author': "Therp BV,Odoo Community Association (OCA)",
    'website': 'http://www.therp.nl',
    "category": "Newsletter",
    "depends": [
        'email_template',
        'web_ckeditor4',
        ],
    'css': [
        ],
    'data': [
        'data/ir_module_cateogry.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/email_template.xml',
        'data/newsletter_type.xml',
        'view/newsletter.xml',
        'view/menu.xml',
        'view/email_template_preview_view.xml',
        'view/newsletter_type.xml',
        ],
    'js': [
        'static/src/js/newsletter.js',
        ],
    'installable': False,
    'auto_install': False,
    'application': True,
}
