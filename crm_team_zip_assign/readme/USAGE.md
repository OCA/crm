## Setting up CRM Teams

1.  Go to CRM → Configuration → Sales Teams
2.  Edit or create a CRM team
3.  Enable "Active ZIP Assignment" checkbox
4.  Set "ZIP Assignment Priority" (higher number = higher priority)
5.  Configure geographic coverage:
    -   Select "Countries" where this team operates (required)
    -   Select "States" within those countries (required)
6.  Add ZIP patterns in the "ZIP Patterns" tab
7.  (Optional) Set a "Pre-Zip Match Condition" using Odoo domain syntax
    to restrict assignment to partners matching specific criteria (e.g.,
    only companies, only certain types, etc.)

### Geographic Coverage

-   **Countries**: Teams will only be considered for partners located in
    the selected countries
-   **States**: Teams will only be considered for partners in the
    selected states
-   **Domain Filtering**: State selection is automatically filtered
    based on selected countries

### Pre-Zip Match Condition

You can further restrict team assignment by specifying a domain
condition in the "Pre-Zip Match Condition" field. This uses Odoo's
domain syntax (e.g., \[('is_company', '=', True)\]). Only partners
matching this condition will be considered for ZIP pattern matching for
this team.

### Pre-Zip Match Condition Examples

Some example domain conditions:

-   \[('is_company', '=', True)\] — Only assign to partners that are
    companies
-   \[('type', '=', 'contact')\] — Only assign to contacts
-   \[('industry_id', '!=', False)\] — Only assign to partners with an
    industry set

You can combine multiple conditions, e.g. \[('is_company', '=', True),
('country_id', '=', ref('base.us'))\]

### ZIP Pattern Examples

All patterns are validated in real-time to ensure they are valid Python
regular expressions:

-   `^1[0-5].*` - ZIP codes starting with 10-15
-   `^2[0-9].*` - ZIP codes starting with 20-29
-   `^751.*` - ZIP codes starting with 751
-   `.*123$` - ZIP codes ending with 123
-   `^[1-3].*` - ZIP codes starting with 1, 2, or 3
-   `^(10|20|30).*` - ZIP codes starting with 10, 20, or 30

### Pattern Validation

The system validates regex patterns when they are entered:

-   Invalid patterns will show an error message immediately
-   Error messages include the specific regex error for debugging
-   Only valid patterns can be saved to the database

## Partner Configuration

Partners have an "Exclude from ZIP Assignment" checkbox to prevent
automatic assignment.

Teams can have a "Pre-Zip Match Condition" to restrict assignment to
partners matching specific criteria before ZIP pattern matching is
performed.

## Usage

### Automatic Assignment

Partners are automatically assigned to CRM teams when:

-   A partner is created with complete geographic information (ZIP,
    country, state)
-   A partner's ZIP code is modified
-   A partner's country or state is changed
-   A partner's company is changed
-   The exclusion flag is modified

For each team, if a "Pre-Zip Match Condition" is set, the partner must
match this condition before ZIP pattern matching is performed. If not
set, all partners are considered for ZIP matching.

### Manual Assignment

You can also trigger assignment manually:

-   Use the contextual action available in partner views
-   This is useful for reassigning existing partners after updating team
    configurations or after addon installation

### Assignment Requirements

For automatic assignment to work, partners must have:

-   A ZIP code
-   A country
-   A state
-   A company
-   "Exclude from ZIP Assignment" must be unchecked
