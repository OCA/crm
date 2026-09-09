Standard CRM builds the customer (`res.partner`) out of a lead only through the
*Convert to Opportunity* wizard, which is reachable from leads alone. Every
other way of getting an opportunity bypasses it:

- creating an opportunity manually from the pipeline,
- the website contact form, when the sales team it targets does not use leads
  (`crm.team.use_leads`), which makes `website_crm` create an opportunity
  directly.

Those opportunities keep their contact details denormalized on the record
(`contact_name`, `partner_name`, `email_from`, `phone`, address) and never get
a customer. Worse, the standard opportunity form hides all of those fields
except the email and the phone, so the company name and the contact name a
website visitor typed are stored but unreachable from the interface.

This module:

- shows the contact and address fields on opportunities as long as no customer
  is assigned, and
- adds a **Create Customer** button to the status bar of those
  opportunities, which opens the
  standard `crm.lead2opportunity.partner` wizard. Nothing is decided behind the
  user's back: the wizard is the usual one, so it still offers to create a new
  customer or link an existing one, and still proposes merging the duplicate
  leads and opportunities it detects.
