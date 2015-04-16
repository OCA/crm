.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Membership withdrawal
=====================

This module was written to extend the functionality of membership to support
tracking of members signup and withdrawal. Also, allows to select a withdrawal
reason from a configurated list of reasons


Installation
============

To install this module, go to Settings > Local Modules and install it as usual.


Configuration
=============

Go to Association > Configuration > Member withdrawal reason, to configure
all available reasons you want


Usage
=====

When a member signs up because changes its Membership State to 'Free Member'
or 'Paid Member' and its Signup date is empty, then is automatically filled
with today date.

User has to set withdrawal date and select a withdrawal reason manually. These
fields are not related with Membership Lines or Membership State


Known issues / Roadmap
======================

None


Credits
=======

Icon
----

* Original source : https://thenounproject.com/term/add-group/79375 by Mundo (https://thenounproject.com/DMundo), 2014
* Modified by Antonio Espinosa using GIMP image editor, 2015

Contributors
------------

* Antonio Espinosa <antonioea@antiun.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
