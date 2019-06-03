To configure this module, you need to:

#. go to `Settings / Mailchimp / Settings` and fill in your mailchimp credentials (this will import audiences)
#. here, you'll also find the URL to configure as webhook for mailchimp. For now, only unsubscribe is supported.
#. go to `Settings / Mailchimp / Audiences` and review the merge fields in audiences. For every merge field, fill in python code that generates this field's value (ie: for FNAME, you probably need partner.name)
#. when you're happy with your settings, you might want to activate the cronjob `Push partner data to mailchimp`, which will push partners to mailchimp periodically. It will only update partners changed in the last 24 hours, so in case you change the interval of the job, you need to adapt the arguments to the amount of seconds of your interval.
