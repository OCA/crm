- Go to **CRM > Configuration > Stages**.
- On the desired stage (e.g. *Qualified*), check **Create Analytic Account**
  and select an **Analytic Plan**.
- Move a lead/opportunity to that stage.
- An analytic account is automatically created and linked to the
  opportunity in the **Analytic Account** field (below the phone number).
- If the lead already has an analytic account, no new account is created.
- The analytic account's ``code`` is generated from the ``CRM Lead Analytic
  Account`` sequence (**Settings > Technical > Sequences & Identifiers**),
  which can be freely reconfigured (prefix, padding, next number, etc.).
