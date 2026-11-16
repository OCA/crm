This module provides a read-only access to the CRM documents introduced by
the `crm` standard module, through the *Readonly* option of the *Sales*
privilege of the user form.

Users holding the group can browse leads/opportunities and the CRM menus
(pipeline, activities, reporting) without any create, write or unlink
right.

The *Readonly* option is shared with the other Sales applications through
the `sales_team_readonly` module: it also grants read access to the
documents of the other installed modules using it (e.g. `sale_readonly`).
