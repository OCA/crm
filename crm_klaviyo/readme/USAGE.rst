To use this module, you can ie create an automated action on partner creation,
filtered by the customer flag, and add code similar to the following::

    client = env['klaviyo.account'].get_api()
    client.Profiles.create_profile({
        'type': 'profile',
        'attributes': {
            # this assumes you have partner_firstname installed
            'first_name': record.firstname,
            'last_name': record.lastname,
            'email': record.email,
        }
    });

to push new partners to Klaviyo.
