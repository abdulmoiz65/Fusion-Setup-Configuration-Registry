# Educational Establishments Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Supplied configuration | Preserve local intake and confirmed mappings; identify missing required fields without comparable-configuration discovery |
| 2 | Approved value authority | For configuration readiness, confirm proposed establishments and fields come from the approved source |
| 3 | Complete current evidence | For exact claims, bind a fresh complete read to the authenticated target and request |
| 4 | Create-only FSM provider | Require the approved local package receipt and mandatory core.data-loader handoff |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| supplied_configuration_capture | Supplied establishment configuration | Yes | A review proposal is requested | Verify | Local normalized user input and actual file-mapping review status | capture_educational_establishment_supplied_configuration | All supplied reference values must survive normalization | Retain exact missing values and uncertain field mappings in preliminary review; leave optionals omitted | proposal_scope; proposed_values; assumption_ledger; exclusions |
| approved_value_authority | Approved establishment source | Yes | Configuration-ready new controlled values are proposed | Verify | User-identified approved source retained in the request record | | The skill must not invent institutions or derive them from employee data | Identify the approved source and confirmed review status | source_reference; source_owner; review_status |
| complete_educational_establishment_evidence | Complete current Educational Establishments evidence | Yes | Exact duplicate review, or configuration readiness is requested | Verify | Workflow-approved complete task export or equivalent complete read | find_complete_educational_establishment_evidence | Exact duplicate classification requires complete current evidence | Supply a fresh complete authenticated-target artifact | evidence_path; target_identity; evidence_fingerprint; completeness_status; valid_through |
| create_import_provider | Approved Educational Establishments create-only FSM provider | Yes | Create or import is requested | Verify | Approved proposal, value-authority, and provider-row fingerprints, complete fresh current evidence, reviewed same-task baseline, exact provider rows, and immutable package receipt | verify_educational_establishment_fsm_import_contract | The local builder owns package preparation and core.data-loader owns Task Hook, preview, approval, upload, and initiation | Resolve every package gate; never substitute direct REST, HDL, HSDL, browser automation, or an internal service | package_path; package_sha256; provider_rows_fingerprint; readiness_fingerprint; data_loader_route |
| unsupported_mutation | Unsupported Educational Establishments mutation | Yes | Update, merge, delete, end-date, replace, employee education change, or direct write is requested | Blocked | Create-only FSM contract | | Existing keys are duplicate locks and employee records are outside this task | Change the request to create-only controlled reference values or route it to the owning skill | blocker_reference |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Approved source authority and complete current evidence are exact and fresh for review, or every create-only FSM gate is ready | Lookup yes; create only through core.data-loader |
| Proposal-ready | Supplied object ownership is unambiguous; missing required values, uncertain field mappings, and incomplete approved-value or exact evidence are retained visibly | Preliminary review-only proposal; no configuration-ready, exact or create claim |
| Needs evidence | Source authority or complete current evidence is absent, stale, incomplete, or ambiguous | No |
| Blocked | Evidence is incomplete, the package contract fails, or an unsupported mutation/provider is requested | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EE.CHECK_DEPENDENCIES | decision | 2 | resolve_dependency | ready->EE.CHECK_EXACT_EXISTING;proposal_only->EE.ENFORCE_DESIGN;import_ready->EE.VALIDATE_FSM_IMPORT;evidence_unavailable->EE.RETURN_BLOCKED;source_unapproved->EE.RETURN_BLOCKED;unsupported_mutation->EE.RETURN_UNSUPPORTED;blocked->EE.RETURN_BLOCKED | EE.CAPTURE_CONFIGURATION | stop | A supplied-configuration Educational Establishments proposal, exact review, or create-only import request is being resolved |

## Sources

- [GROW-8154 FDD v3 AC1-AC7](https://confluence.oraclecorp.com/confluence/pages/viewpage.action?pageId=21882990113)

- [HCM Tool FSCR taxonomy](https://fabuddy-apps.oraclecorp.com/hcm-product-setup-tree/hcm-tool-fscr-taxonomy/)
- [GROW-8154](https://jira.oraclecorp.com/jira/browse/GROW-8154)
