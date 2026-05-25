This module extends the CRM functionality to support **multi-team
stages**.

**Features:**

-   Adds a many2many field `team_ids` on CRM stages, allowing a stage to
    be shared by multiple sales teams.

**Use cases:**

-   A company with multiple sales teams sharing some stages but also
    having exclusive ones.
-   Cleaner kanban views per team, avoiding irrelevant stages.
