Go to **Settings > CRM > Lead Escalation > Manage Escalation Rules**, or to
**CRM > Configuration > Lead Escalation Rules**, and create a rule:

1. Choose the trigger: *No follow-up* or *Not won nor lost*.
2. Set the delay, in minutes, hours or days.
3. Choose who to notify: the *Sales Team Leader* of the lead, or a specific
   user. Other modules may add more recipients to that list.
4. Tick **Assign Lead to Recipient** to also make that person the salesperson
   of the lead.
5. Optionally restrict the rule to some sales teams, to leads or to
   opportunities only.

Rules are checked by the scheduled action **CRM: Escalate Leads**, which runs
every 5 minutes. That interval is the precision of the shortest delays: raise
it if you only use delays counted in days.
