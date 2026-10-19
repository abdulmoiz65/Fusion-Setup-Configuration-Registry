# Manage Procurement Agents Client-Side Design Enforcement

## Source Basis

- Oracle Fusion Cloud Procurement 26C Procurement Agents and Flexfields for Procurement Agents documentation
- Oracle Fusion Cloud Procurement 26C Implement Procurement guidance
- Procurement-agent Redwood, REST, and UI acceptance-criteria exports supplied by the developer

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm implementation access | Confirm the implementer and end user have the required roles and privileges before enabling the client action |
| 2 | Validate client values | Validate operation, identifiers, status, capability flags, access-level codes, and DFF shape without making a network request |
| 3 | Check duplicates when evidence is available | Compare the proposed parent Agent and Procurement BU only when a current client-side candidate collection is already supplied; do not prompt for that collection |
| 4 | Apply least privilege | Retain only explicitly approved capabilities and the minimum documented access level required for each enabled capability |
| 5 | Review flexfields | When a DFF value is supplied, map it through the registered child section, retain no more than one DFF item for the parent assignment, and do not request separate enablement confirmation. Where the live attribute header binds a context, use that header binding and leave the context-selector columns blank. |
| 6 | Produce a client preview | Show normalized form values, client-side validation results, and defaults; a separate execution workflow owns any later environment verification or mutation |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new procurement agent is proposed | Error | | Supplied client-side candidate evidence contains the same resolved parent Agent and Procurement BU pair | Select a different pair when duplicate; absence of a candidate collection is not a prompt or blocker | Yes |
| Any capability is enabled | Error | | The corresponding access level is broader than the approved business need or is outside the documented values for that document type | Start at None and increase only to the approved View, Modify, or Full level | Yes |
| A capability is disabled | Error | | Its associated access-level code remains broader than None | Reset the related access-level code to None | Yes |
| An update proposal is prepared | Error | | Parent Agent or Procurement BU display value is absent, preventing surrogate-key derivation | Supply the parent display values; the selected Data Loader route derives the surrogate key | Yes |
| DFF is included | Error | | The DFF has more than one item, contains an unparseable value, cannot inherit parent linkage, or has no header-bound context | Retain one supplied DFF item, map it through the registered child section, propagate linkage from the parent record, and leave context-selector columns blank when the header binds the context; do not request a duplicate DFF attribute name or enablement confirmation | Yes |
| A client preview is ready | Error | | The preview omits applied defaults, access-policy results, or duplicate-check result | Regenerate the client preview before handing it to the separate execution workflow | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PAG.ENFORCE_CREATE | decision | 30 | design_enforcement | passed->PAG.READY_CREATE;blocked->PAG.HANDLE_ISSUES | PAG.APPLY_DEFAULTS | stop | A client-side create candidate has been validated and defaulted |
| PAG.ENFORCE_UPDATE | decision | 40 | design_enforcement | passed->PAG.READY_UPDATE;blocked->PAG.HANDLE_ISSUES | PAG.VALIDATE_INPUT | stop | A client-side update or DFF maintenance proposal has been validated |
