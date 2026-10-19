# Manage Email Templates Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Input validation | Validate template identity, editor, type, metadata, and archive members |
| 2 | Dependency readiness | Confirm the selected type and editor have compatible source evidence and all metadata rows have included parents |
| 3 | Design compatibility | Preserve the selected editor and type baseline without synthesizing metadata or defaults |
| 4 | Execution gate | Permit Campaign template creation or a controlled existing-template status transition only through the core Data Loader immutable execution workflow; retain FSM export for evidence and verification |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new Campaign Basic or Advanced Block template is prepared for import | Blocker | | Candidate DesignMetadata does not exactly match the hardcoded selected-editor default | Use the complete minimal layout JSON from `ora_defaulting_rules.md`; do not use a different editor or type | Yes |
| A new Campaign HTML template is prepared for import | Blocker | | Candidate DesignMetadata is not blank | Preserve the hardcoded blank value | Yes |
| A new Campaign template is prepared from hardcoded defaults | Blocker | Fresh target task-level export shows different editor metadata, language, or default-language values and the workflow treats them as a mismatch | Use the hardcoded creation defaults; use the export only for name/key conflict comparison | Yes |
| A new Campaign template is prepared for import | Blocker | The generated MessageDesignCode exceeds 32 characters, is not normalized, conflicts with the fresh target export, or differs across linked rows | Regenerate it with the declared name/timestamp/nonce rule and rebuild the linked rows | Yes |
| An Express template is prepared for import or validation | Blocker | | The Express DesignTypeCode or editor-specific DesignMetadata baseline has not been observed in a representative export | Create the representative template manually and obtain a fresh export before authoring an import baseline | No |
| A new Campaign template is created through FSM import | Required | | The archive is not immutable and validated, the target environment is not explicit, or the core Data Loader execution gate is incomplete | Create the template only by importing the validated archive through the declared Data Loader workflow | Yes |
| One or more existing Campaign templates are activated or inactivated through FSM import | Required | Fresh task-level export | The candidate changes a field, row, or archive member other than each selected template's DesignStatusCode; any current target is absent or duplicated; or the core Data Loader execution gate is incomplete | Submit only the immutable, Data Loader-validated archive and verify every selected template with a fresh task export | Yes |
| UI creation, visual editing, deletion, or send is requested | Blocker | | The action is outside the declared FSM export/import route | Use a manual Fusion UI handoff. Campaign template creation and controlled status transition through a validated FSM import remain the supported automated routes | No |
| An existing target template conflicts with the candidate template | Blocker | | The replace or new-only choice is not explicit | Present existing and candidate names and obtain the explicit choice; do not silently replace, skip, or rename a template | Yes |
| A source-environment FSM archive is imported | Blocker | | Parent, metadata, type-association, or ASM metadata members are altered, or the fresh target comparison is absent | Preserve the source archive unchanged and validate it against a fresh target export before the execution preview; do not replace it with hardcoded creation defaults | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMET.ENFORCE_DESIGN | decision | 30 | design_enforcement | ready->HCMET.EXECUTION_GATE;blocked->HCMET.RETURN_ISSUES | HCMET.CHECK_DEPENDENCIES | stop | Required input and dependency evidence are available |
