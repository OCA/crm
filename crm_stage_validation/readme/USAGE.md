This guide explains how to use the CRM Stage Validation module to enforce data quality in your sales pipeline.

## How Validation Works

When a user attempts to move a lead/opportunity to a stage that has validation rules configured, the system will:

1. Check if all required fields are filled
2. If any required field is empty, display a validation error
3. Block the stage change until all required fields are completed

## Working with Validated Stages

**Moving a Lead/Opportunity**

1. Open a lead/opportunity in the CRM
2. Try to move it to a stage with validation rules (drag-and-drop in kanban or change stage in form)
3. If validation fails, you will see an error message like:
   > "Lead/Opportunity [Name] can't be moved to the stage [Stage Name] until the following fields are set: [Field Names]."
4. Fill in the required fields
5. Try moving the lead/opportunity again

**Bulk Operations**

When moving multiple leads/opportunities at once:
* Each record is validated individually
* All validation errors are displayed together
* No records are moved until all validations pass

## Validation Error Messages

The validation error message includes:
* The name of the lead/opportunity that failed validation
* The name of the target stage
* A list of all fields that need to be filled

**Example Error Message:**

> Lead/Opportunity "Big Deal Corp" can't be moved to the stage "Proposition" until the following fields are set: Expected Closing, Expected Revenue.

## Usage Examples

**Example 1: Requiring Expected Revenue at Proposition Stage**

1. Configure the "Proposition" stage to require "Expected Revenue"
2. User tries to move a lead to "Proposition" without filling expected revenue
3. System displays: "Lead/Opportunity can't be moved to the stage Proposition until the following fields are set: Expected Revenue."
4. User fills in the expected revenue
5. Lead is successfully moved to "Proposition"

**Example 2: Multiple Required Fields**

1. Configure the "Negotiation" stage to require "Expected Closing" and "Contact Name"
2. User tries to move an opportunity to "Negotiation" with only contact name filled
3. System displays the validation error for "Expected Closing"
4. User fills in the expected closing date
5. Opportunity is successfully moved to "Negotiation"

**Example 3: Batch Move Validation**

1. User selects 5 opportunities in kanban view
2. User drags them to a stage requiring "Expected Revenue"
3. 2 opportunities don't have expected revenue filled
4. System displays validation errors for those 2 opportunities
5. User fills in the missing data
6. Retries the batch move successfully

## Tips

* Start with key fields that are essential for your sales process
* Don't over-configure - too many required fields can slow down your team
* Use validation strategically at milestone stages (Qualification, Proposition, Negotiation)
* Review your validation rules periodically to ensure they match your current process
* Train your team on the validation requirements to avoid frustration

