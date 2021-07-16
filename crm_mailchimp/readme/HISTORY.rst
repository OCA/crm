Changes in version 13.0.2.0.0
=============================

- The datamodel has been changes significantly to support other models then
  res.partner as a source of email addresses to subscribe. Specifically it will
  be possible to support crm.lead subscriptions;
- New or changed subscribers will be pushed to mailchimp as soon as they happen,
  but only if relevant fields (email, or used in merge field code) changed;
- Data deleted on the mailchimp side (interests, categories, merge fields) will
  be deleted on the Odoo side as well;
- There is now a check to prevent multiple records (might be from the same or
  different models) to subscribe to Mailchimp with a same email address;
- Merge fields will now have a default False / NULL value for the code field, and
  will be ignored when pushing data to mailchimp as long as they are not filled.
