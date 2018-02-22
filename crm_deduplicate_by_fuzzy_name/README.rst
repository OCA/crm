.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

====================================
Deduplicate Contacts by similar name
====================================

This module extends the criteria to match duplicated contacts looking for
similar names according a maximum of different characters.

Installation
============

You need to have the *fuzzystrmatch* Postgres extension installed. You can
add it from a psql command line typing:

.. code-block:: psql

   CREATE EXTENSION fuzzystrmatch;

Usage
=====

To use this module, you need to:

#. Go to *Sales > Tools > Deduplicate Contacts*.
#. Mark "Similar name" in the section "Search duplicates based on duplicated
   data in", and select the maximum number of different characters that you
   are going to allow.
#. This criteria will be used for deduplicating.

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/111/8.0

Known issues / Roadmap
======================

* The similarity is not a transitive operation (it's only symetric and
  reflexive), which means that we cannot set an equivalence relation. This
  makes that the search is perform through a pivot partner, and looking for
  similar names to it, but no subsequent searches are performed for finding
  similar names to the results, or you will probably match everything. Imagine
  you have "Maco", "Mala" and "Rala", and you put a difference of 2 characters,
  "Maco" will match with "Mala", and "Mala" will match with "Rala", but
  "Maco" won't match with "Rala". The current algorithm will match only the
  first two, losing the second similarity.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/crm/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Pedro M. Baeza <pedro.baeza@tecnativa.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
