1. Open the CRM settings and configure:
    - Force Project: If set, all tasks created from leads will be assigned to this project without asking the user.
    - Archive Lead: If enabled, the lead will be archived after converting it to a task.

    ![crm_settings](../static/description/crm_settings.png)

2. Navigate to *CRM \> Sales \> My pipeline*
3. Open an existing lead or create a new one.
4. Depending on the Archive Lead setting:
    - Enabled → The button will be labeled "Convert to Task".

    ![convert_to_task](../static/description/convert_to_task.png)

    - Disabled → The button will be labeled "Create Task".

    ![create_task](../static/description/create_task.png)

5. When clicking the button (either Create Task or Convert to Task), two scenarios are possible:
    - Force Project set → The task is created immediately and linked to the configured project.
    - No Force Project set → A popup appears allowing you to select a project.
Click Create Task in the popup to proceed.

6. After creation, you will be redirected to the new task form view.
All relevant lead information, including attachments and messages, will be copied to the task.
