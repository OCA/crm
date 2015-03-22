Newsletters
===========
With this addon, you can send HTML-formatted mass emails to your customers.
While it was developed with primarily newsletters in mind, it works for
arbitrary objects and arbitrary content.

This is something else than the mass_mailing module, which is geared very much
on marketing campaigns with appropriate language and measuring tools.

Installation
============

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

Configuration
=============

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

Usage
=====

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

For further information, please visit:

 * https://www.odoo.com/forum/help-1

Known issues / Roadmap
======================

 * a glue module between this and mass_mailing would be nice

=======
Credits
=======

Contributors
------------

* Holger Brunn <hbrun@therp.nl>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
