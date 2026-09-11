Leads sometimes stop moving: nobody calls the customer back, and nobody marks
the lead as won or lost either. This module lets you define **escalation
rules** that watch for those leads and warn a manager automatically.

A rule answers three questions:

- **When?** Either the lead got no follow-up for a given delay, or it is
  neither won nor lost a given delay after its creation. The delay is
  expressed in minutes, hours or days.
- **Who?** The sales team leader of the lead, or one specific user.
- **What?** A to-do activity is scheduled on the lead for that person, an
  email is sent, and the lead can optionally be reassigned to them.

Anything a salesperson does on the lead - a message, a planned or completed
activity such as a call or a meeting, a stage change or a change of
salesperson - counts as a follow-up and restarts the clock, so nobody gets
notified twice for the same standstill.

Several rules can run side by side, with their own delays, sales teams and
recipients.

## Relation to the native rotting feature

Odoo 19 can already highlight stale records: `crm.stage.rotting_threshold_days`
together with `is_rotting` on the mail tracking duration mixin. That mechanism
measures the time since the last **stage change**, per stage, with a
granularity of one day, and it only colours the record in the interface.

This module answers a different question: it measures the time since the last
**follow-up** of any kind, with a granularity of one minute, per rule rather
than per stage, and it notifies somebody about it.
