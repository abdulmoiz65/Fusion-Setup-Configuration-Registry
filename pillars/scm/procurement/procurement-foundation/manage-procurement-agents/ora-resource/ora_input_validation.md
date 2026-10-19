# Manage Procurement Agents Client-Side Input Validation

## Source Basis

- Oracle Fusion Cloud Procurement 26C Procurement Agents documentation
- Procurement-agent Redwood, REST, and UI acceptance-criteria exports supplied by the developer

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Intent Create or Update | Block client-side validation | Request exactly one supported operation | Always | |
| Create parent identity | Agent and Procurement BU display values | Block before preparation | Supply the parent record's display values; the selected Data Loader route resolves them through business-object derivation queries | Intent is Create | |
| Update parent identity | Agent and Procurement BU display values | Block before update preparation | Supply the existing parent record's display values; the selected Data Loader route derives the surrogate key | Intent is Update | |
| DFF parent linkage | No child-level identity input | Do not prompt for Agent, Procurement BU, or AssignmentId on the DFF item | Copy the parent record's resolved linkage into the prepared DFF loader row | DFF is supplied with a parent create or update | |
| DFF value acceptance | One supplied DFF value | Omit the DFF row; do not request a duplicate DFF attribute name or enabled-attribute evidence | Map the supplied value to the sole writable flexfield column in the registered DFF child section and normalize it by data type | A DFF item is supplied with a parent create or update | |
| DFF context binding | No context input | Block only if the live DFF header has no bound context | Use the context embedded in the live attribute header; for `procurementAgents`, `_Procurement__Agents__BI__DFF(PO_AGENT_ASSIGNMENTS=Global Data Elements)` binds the value to `Global Data Elements`. Leave `FLEX:PO_AGENT_ASSIGNMENTS`, `__FLEX_Context`, and `__FLEX_Context_DisplayValue` blank. | A DFF item is supplied with a parent create or update | |
| DFF date value | ISO date or Data Loader timestamp | Block only when the value cannot be parsed as a date or timestamp | Convert an ISO date such as `2026-09-30` to `2026/09/30 00:00:00`; preserve a supplied valid timestamp after normalizing it to `YYYY/MM/DD HH24:MI:SS` | A DFF date attribute is supplied | |
| Required create access policy | All required Allowed flags and all required access-level Code fields | Block before design review | Supply every documented required boolean and access-level code explicitly | Intent is Create | |
| Procurement-agent status | Status | Block before design review | Supply Active or Inactive explicitly | Intent is Create | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A create form has parent Agent and Procurement BU display values | Continue to documented defaults and least-privilege rules | Resolve parent identifiers through the selected Data Loader route | |
| An update form has parent Agent and Procurement BU display values | Continue to client-side design enforcement | Derive the parent surrogate key through the selected Data Loader route | |
| A DFF item is supplied with a parent record | Continue without requesting child-level identity fields | Propagate the parent linkage during loader-row preparation | |
| A DFF value is supplied | Continue without an additional DFF attribute or enablement prompt | Use the registered child-section flexfield column and normalize the supplied value by data type | |
| A DFF value is supplied and the live header includes a context in parentheses | Continue without a context prompt | Write only the flexfield value and leave the context-selector columns blank; the header-bound context is authoritative | |
| A DFF date is supplied as an ISO date | Continue after deterministic normalization | Write the loader value as `YYYY/MM/DD HH24:MI:SS` before archive validation | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Parent Agent and Procurement BU are nonblank display values | Reject missing values only; do not prompt for numeric IDs | Intent is Create or Update | |
| DFF parent linkage is derived | Do not request or validate child-level Agent, Procurement BU, or AssignmentId input | DFF is supplied with a parent record | |
| DFF value is accepted from the supplied item | Map the supplied value directly to the registered child-section flexfield column; do not request a duplicate DFF attribute name or enabled-attribute evidence | One DFF item is supplied and the child section has one writable flexfield column | |
| DFF context is header-bound | Never copy the context display label into `FLEX:`, `__FLEX_Context`, or `__FLEX_Context_DisplayValue` columns | A registered DFF attribute name contains a parenthesized context binding | |
| DFF date is loader-normalized | Convert parseable ISO dates to `YYYY/MM/DD HH24:MI:SS`; reject unparseable values rather than passing them through | A DFF date attribute is supplied | |
| Status is Active or Inactive | Reject any other status value | Status is supplied | |
| Allowed flags are booleans | Reject values other than true or false | A documented Manage*AllowedFlag is supplied | |
| Access-level codes are valid for their document type | Require None, View, Full, or Modify only where Oracle documents that value for the specific code | An access-level code is supplied | |
| DFF collection has at most one item | Reject more than one DFF item for one procurement-agent assignment | DFF is supplied | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAG.VALIDATE_INPUT | decision | 10 | validate_input | create_valid->PAG.APPLY_DEFAULTS;update_valid->PAG.ENFORCE_UPDATE;invalid->PAG.HANDLE_ISSUES | none | stop | Before a procurement-agent create, update, or DFF maintenance proposal |
