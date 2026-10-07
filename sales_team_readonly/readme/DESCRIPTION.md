This module provides the *Readonly* group of the *Sales* privilege of the
user form. It is shared by the modules adding a read-only access to the
documents of the Sales applications (e.g. `sale_readonly`, `crm_readonly`).

The group itself does not grant access to any document: the modules
depending on it attach their own read-only access rights, record rules and
menus to it.
