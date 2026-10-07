Assign the *Readonly* option under the *Sales* privilege in the user form
(Settings / Users). The option is mutually exclusive with the standard
*User: ...* and *Administrator* options of the same privilege.

What the user gets:

* read access to all leads/opportunities, whatever their salesperson;
* a CRM application menu with *My Pipeline*, *My Activities* and the
  *Reporting* menus (forecast, pipeline and leads analyses, activities),
  all in read-only mode;
* the *Leads* menu as soon as the *Leads* setting (`crm.group_use_lead`)
  is enabled, exactly like standard sales users;
* the read-only access to the other Sales applications using the shared
  *Readonly* option (e.g. quotations and sales orders with
  `sale_readonly`).

What the user does not get:

* any write access: action buttons requiring write access (e.g. *Mark Won*,
  *Convert to Opportunity*) raise an access error when clicked;
* the *Configuration* menus, reserved to sales administrators.
