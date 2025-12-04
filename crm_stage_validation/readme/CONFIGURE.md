This module requires configuration of the fields to validate for each stage.

## Installation

1. Go to the **Apps** menu
2. Remove the "Apps" filter if necessary
3. Search for "CRM Stage Validation"
4. Click **Install**

## Configuration

**Setting up Field Validation for Stages**

1. Go to **CRM > Configuration > Stages**
2. Select a stage you want to configure
3. In the **Stage Validation** section, find the **Fields to Validate** field
4. Select one or more fields that must be filled when a lead/opportunity reaches this stage
5. Save the stage

**Example Configuration**

For a "Proposition" stage, you might require:
* **Expected Closing** - to ensure a deadline is set
* **Expected Revenue** - to track potential revenue
* **Contact Name** - to ensure a contact person is identified

For a "Won" stage, you might require:
* **Expected Revenue** - to ensure the deal value is recorded
* **Partner** - to ensure a customer is linked

## Permissions

The module uses the same access permissions as the base CRM module:
* Users with access to **CRM Configuration** can configure field validation on stages
* All CRM users are subject to the validation rules when moving leads/opportunities

No additional permission configuration is required.

