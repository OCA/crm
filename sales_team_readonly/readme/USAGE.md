To grant a read-only access to the Sales applications, select *Readonly*
under the *Sales* privilege in the user form (Settings / Users).

Selecting another option of the *Sales* privilege replaces it, as the
privilege options are mutually exclusive.

The effective read-only access depends on the installed modules using the
group:

* `sale_readonly` grants access to the quotations, sales orders and their
  details;
* `crm_readonly` grants access to the leads/opportunities, the CRM menus
  and the related analysis.
