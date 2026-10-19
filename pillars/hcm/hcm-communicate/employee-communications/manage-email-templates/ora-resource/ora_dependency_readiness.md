# Manage Email Templates Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM export privilege | Confirm that the task-level FSM export process can be created and retrieved for semantic verification |
| 2 | Template type mapping | Resolve the selected Campaign type and editor from the hardcoded task defaults |
| 3 | Editor-compatible metadata | Apply the hardcoded Campaign editor default for the selected editor |
| 4 | Parent and dependent relationship | Confirm every metadata row resolves to one included MessageDesignCode before import preview |
| 5 | Creation-conflict evidence | Use one fresh target export to check the visible DesignName and generated MessageDesignCode conflicts |
| 6 | Status-transition baseline | Confirm every selected existing Campaign template, its current status, and a fresh target export before changing only their DesignStatusCode values |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| HCM-ET-001 | FSM export privilege | Yes | Export or semantic verification | Verify | Task-level FSM export | | The export process must be available to obtain current evidence | Stop and route privilege issues to the security owner | Export process availability |
| HCM-ET-002 | Template type mapping | Yes | Standard Campaign creation preview | Verify | `ora_defaulting_rules.md` hardcoded Campaign constants | | Campaign type and editor codes must match the selected UI values | Stop; do not infer Express values | Matching DesignTypeCode and DesignEditorTypeCode |
| HCM-ET-003 | Editor-compatible metadata | Yes | Standard Campaign creation preview | Verify | `ora_defaulting_rules.md` hardcoded Campaign constants | | The selected editor must use its declared static metadata and language values; target-template metadata is not a creation baseline | Stop; do not substitute Agent-specific, target-template, or another editor's values | Matching complete DesignMetadata, MessageLanguage, and DefaultLanguageFlag |
| HCM-ET-004 | Parent and dependent relationship | Yes | Import preview | Verify | CSV package validation | | Every metadata row must resolve to one included MessageDesignCode | Stop; rebuild the linked package | Valid parent and metadata row relationship |
| HCM-ET-007 | Creation-conflict evidence | Yes | Standard Campaign creation preview | Verify | One fresh target export and `ora_defaulting_rules.md` MessageDesignCode generator | | A new template must have a unique visible name and 32-character-or-shorter key without asking the requester for technical input | Use the same export for the name check and generator; the generator retries nonces and fails closed on an unresolved key collision | One unique DesignName and generated MessageDesignCode |
| HCM-ET-005 | Target template comparison | Yes | Standard Campaign creation or cross-environment import | Verify | Fresh target task-level export | | Existing target names or keys require an explicit resolution; they do not redefine standard-creation editor defaults | For standard creation, resolve the name/key conflict before preview. For cross-environment import, select Import only new templates or Replace existing templates before building the immutable candidate | Existing and candidate template groups |
| HCM-ET-006 | Status-transition baseline | Yes | Existing Campaign template activation or inactivation | Verify | Fresh target task-level export and immutable archive comparison | | Every target, current state, and sole changed field must be unambiguous | Stop when any target is absent, duplicated, stale, or any field other than a selected row's DesignStatusCode changes | Exact MessageDesignCode; current and requested status for every selected template |

## Dependency Classification

| Result Category | When Used | Can Continue? |
|---|---|---|
| Verify | A documented prerequisite must be confirmed from the specified evidence | Only after confirmation |
| Blocked | A required prerequisite or hardcoded Campaign default is absent or mismatched | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| HCMET.CHECK_DEPENDENCIES | decision | 20 | resolve_dependency | ready->HCMET.ENFORCE_DESIGN;blocked->HCMET.RETURN_ISSUES | HCMET.VALIDATE_INPUT | stop | Input validation passed |
