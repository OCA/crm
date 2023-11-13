**No Exception checking in the create function.**

Adding exception checking to the create function would trigger an Odoo Client Error
related to JavaScript (Error: Component is destroyed) when attempting to create a new opportunity
in the pipeline's kanban view and clicking the edit button.
