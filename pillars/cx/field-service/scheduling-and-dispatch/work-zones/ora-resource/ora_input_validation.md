# Workbook Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Workbook source | A readable .xlsx workbook containing a Work Zones worksheet | Stop before validation or preview | Supply the workbook and preserve the Work Zones worksheet | Every request | |
| Work Zone row | Work_Zone_Name, Work_Zone_Label, Status, and Work_Zone_Key; optional Shapes and Translations JSON | Mark the candidate row invalid | Complete the required API fields or remove it from the proposed configuration; use only a JSON array for Translations when supplied | A row is proposed as a Work Zone | |
| Design-evidence row | Geographic Eligibility Boundary, Practical Routing Pool Evidence, Key Definition Governance Controlled, Assignment Model, and Post-Change Validation Plan | Block preview at design enforcement | Complete the yellow design-evidence columns in assets/Work_Zones_Input_Template.xlsx; these fields are not REST payload fields | A row is proposed as a Work Zone | |
| Work Zone key | A nonblank Work_Zone_Key of at most 50 characters | Stop the candidate row | Provide a stable key that meets the workbook property definition | A row is proposed as a Work Zone | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A row has no Work_Zone_Name | Ignore the blank template row | Do not treat it as configuration data | |
| A row has a Work_Zone_Name | Candidate Work Zone | Apply field and design validation before preview | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Work_Zone_Key length | Reject values longer than 50 characters | A candidate Work Zone has a key | |
| Work_Zone_Key comparison | Compare keys case-insensitively | Any two candidate Work Zones have keys | |
| Duplicate Work_Zone_Key | Reject the candidate set when a normalized key appears more than once | Any two candidate Work Zones have keys | |
| Translations JSON | Reject a supplied value that is not a JSON array | A candidate Work Zone has Translations JSON | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| WZ.VALIDATE_WORKBOOK | decision | 1 | validate_input | valid->WZ.ENFORCE_DESIGN;invalid->WZ.RETURN_ISSUES | none | stop | Before validating or previewing any Work Zone configuration from the workbook. |
