When converting a lead to an opportunity, the native wizard can already attach
the lead's contact to an existing company: pick **Create a new customer** and
fill the **Company** field.

That field is only editable when the lead carries **no company name**, though.
As soon as the lead has one — which is the usual case for leads coming from a
website form or an import — the native wizard leaves no way to do it:

- **Create a new customer** creates a *second* company out of the lead's company
  name, even when that company already exists;
- **Link to an existing customer** links the company, and the lead's contact is
  never created.

This module fills that gap. It adds a sub-question under **Link to an existing
customer**, shown when the lead has a contact name and the selected customer is
a company, to decide what to do with that contact:

- **Create a new contact** on the existing company
- **Link to an existing contact** of that company
- **Do not add a contact** (keep the native behaviour: link the company, and
  leave the lead's contact aside)

If a contact of the company already matches the lead's email, it is
pre-selected, so that no duplicate is created. When the lead has no contact
name, or the selected customer is a person, the native behaviour is kept.

![Screenshot lead to opportunity
wizard](../static/description/crm_lead_to_opportunity_contact-sshot.png)
