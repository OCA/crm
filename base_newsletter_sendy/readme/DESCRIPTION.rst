This module allows ecommerce customers to subscribe a newsletter which is provided by `Sendy <https://sendy.co/>`_. Sendy is a self-hosted newsletter system independent of Odoo.

For configuration there are three parameters to be set in Settings -> Activate the developer mode -> Settings -> Technical -> System Parameters:

* sendy_api_key
* sendy_list
* sendy_url

.. image:: images/01_api_key.png

During checkout customers can subscribe by activating the marked checkbox.

.. image:: images/02_e-commerce_checkout.png

At a contact record in the backoffice: Sales & Purchases -> Newsletter (via Sendy)

.. image:: images/03_customer_record.png
