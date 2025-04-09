Now, to actually generate the phone call planning:

1.  Go to *CRM \> Phone Calls \> Planner*.
2.  Fill the fields under *Call details*. Those fields will be saved
    literally in the generated phone calls.
3.  Fill the fields under *Criteria*. Those fields are used to filter
    the partners and the preexisting calls. The UTM fields will also be
    saved literally in the generated phone calls.
4.  Fill the fields under *Times*. See note below.
5.  Fill the fields under *Repetition*. See note below.
6.  Press *Generate planning*.
7.  Wait a little bit (this is usually a long process).
8.  You will get to the list of planned phone calls. Start calling!

## Note about *Times* section

The *Start* and *End* times behave in a special way:

- Their *date* part is used to know the start and end dates for the
  planning.
- Their *time* part is used to know the time at which we will plan calls
  *each day under the date range*.

The *Call duration* field indicates the time spacing you want to leave
between one call and the next one.

So, for instance, if you select start on *2017-09-01 09:00:00*, end on
*2017-09-03 10:00:00* and duration of *1:00*, it will try to generate
these phone calls:

- 2017-09-01 09:00:00
- 2017-09-01 10:00:00
- 2017-09-02 09:00:00
- 2017-09-02 10:00:00
- 2017-09-03 09:00:00
- 2017-09-03 10:00:00

## Note about *Repetition* section

If you choose not to repeat calls, the planner will try to schedule one
single phone call for each **criteria combination** (*Partner +
Campaign + Source + Medium*) under the specified conditions in the
*Times* section (see note above).

If you choose instead to repeat calls after some amount of days (*Days
gap*), the planner will:

1.  Try to find a partner that matches the **criteria combination** and
    has never been called; then schedule a call for him.
2.  If all matching partners have already been called, then search for
    matching partners that have not been called in the specified *Days
    gap*; then schedule a call for the one with least total scheduled
    calls.
3.  If there is still no match, then schedule nothing and continue.
