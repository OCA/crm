In Odoo standard source code, leads' currency is defined as a computed, non-stored
field, which follows this workflow:

- if the lead's company is set, then the company currency is used

- if the lead's company is not set, then the user's company currency is used

Since the field is not stored, it leads to 2 main issues:

1) Changing a company's currency will change the currency on all the existing leads
   linked to that company, but not the amounts. Eg:
    - you have a lead linked to a company in EUR
    - the lead's expected revenue is 1000 EUR
    - you change the company currency to USD
    - the lead's expected revenue becomes 1000 USD

2) If a lead is not linked to a specific company, then 2 users that are logged in with
   2 different companies and different currencies will see the lead's amounts with
   different currencies. Eg:
    - you have a lead where the company is not set
    - accessing the lead with a user whose main company is in EUR will display an 
      expected revenue of 1000 EUR
    - accessing the lead with a user whose main company is in USD will display an 
      expected revenue of 1000 USD

This module stores the field in the DB to keep data consistency, and will only update
the lead's currency only if the lead's company itself is updated. The behavior for
computing the lead's currency will remain the same (currency is retrieved from the
lead's company or the current user's company), but the issues are fixed:

1) Changing a company's currency **will not change the currency on existing leads**,
   only on the ones created after the currency has been updated. Eg:
    - you have a lead linked to a company in EUR
    - the lead's expected revenue is 1000 EUR
    - you change the company currency to USD
    - the lead's expected revenue is still 1000 EUR
    - a newly created lead's expected revenue will be in USD, not EUR

2) If a lead is not linked to a specific company, then 2 users that are logged in with
   2 different companies and different currencies will see the **lead's amounts with
   the same currency** (computed from the company of the first user that triggers the
   recomputation). Eg:
    - you have a lead where the company is not set
    - accessing the lead with a 1st user whose main company is in EUR will display an 
      expected revenue of 1000 EUR
    - accessing the lead with a 2nd user whose main company is in USD will display an 
      expected revenue of 1000 EUR, because the currency was set from the previous
      user's company
