.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Customizable unsubscribe link on mass mailing emails
====================================================

With this module you can set a custom unsubscribe link append at bottom of mass
mailing emails.


Configuration
=============

To configure unsubscribe label go to Setting > Technical > Parameters > System parameters
and add a 'mass_mailing.unsubscribe.label' parameter with html to set at bottom
of mass emailing emails. Including '%(url)s' variable where unsubscribe link

For example:
```
<small>You can unsubscribe <a href="%(url)s">here</a></small>

```

Additionally, you can disable this link if you set this parameter to 'False'


Known issues / Roadmap
======================

* This custom html is not translatable, so you can define the same text in
several languages


Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/crm/issues/new?body=module:%20mass_mailing_custom_unsubscribe%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Rafael Blasco <rafabn@antiun.com>
* Antonio Espinosa <antonioea@antiun.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.