When a lead is matched to a partner, Odoo looks the partner up by email. This
module makes it look up a **company by VAT (TIN)** first, and only falls back
to the native email lookup when the lead has no VAT or no company carries it.

It builds on `crm_lead_vat`, which adds the VAT field to leads.
