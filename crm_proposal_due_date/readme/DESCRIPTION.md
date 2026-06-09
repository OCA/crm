This module extends the CRM *Opportunity* form with an **Expected Proposal
Submission Date** field (``proposal_due_date``).

Whenever this date is set or changed on an opportunity, an activity of type
*"Remettre la proposition"* is automatically scheduled with the same deadline,
giving the responsible salesperson a visible reminder in their activity feed.
If the date is cleared the corresponding activity is automatically removed.
