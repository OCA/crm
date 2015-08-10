.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3

Smart-button for referenced claims
==================================

This module adds an smart-button in the models that can be referenced in a
claim with the number of linked claims and a shortcut to them.

Usage
=====

Go to any record that can be referenced in a claim, and you will see in a
smart-button called "linked claims" a number indicating the number of
claims that reference this record. Clicking on the button, it will navigate
to a list of these claims.

If you click *New* on the claim list, the created claim will be automatically
linked to the referenced record.

Known issues / Roadmap
======================

* The check for seeing if the opened model is one of the possible referenced
  models is done on each view request, so this hits very little, but a bit,
  the overall performance of the system.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/crm/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/OCA/crm/issues/new?body=module:%20crm_claim_ref_smartbutton%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.


Credits
=======

Contributors
------------

* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Oihane Crucelaegui <oihanecrucelaegi@avanzosc.es>

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
