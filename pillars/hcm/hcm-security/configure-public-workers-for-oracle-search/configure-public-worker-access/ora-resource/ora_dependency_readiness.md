# Configure Public Worker Access Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Configuration Name availability | Confirm no exact Name match before a create, or exactly one exact unchanged Name match before an update or delete. |
| 2 | Profile option | Optionally verify ORA_PER_PUBLIC_WORKER_ACCESS_ENABLED when the user requests the current mode |
| 3 | Profile option change | Route any requested profile-option value change to hcm.hcm-security.hcm-security-common.manage-profile-options |
| 4 | Rule Builder and search index | Deploy the DFF and publish its search-index metadata before advanced-filter validation |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| PWA-CONFIGURATION-NAME | Configuration Name availability | Yes | A PWA configuration is created, updated, or deleted | Verify | publicWorkerAccess through core.fusion-api.rest-api-client | verify_pwa_configuration_name_availability | A create must not duplicate an existing configuration Name, and an update or delete must identify exactly one existing configuration by its unchanged Name | Supply a unique Name for a create or the exact existing Name for an update or delete. A rename is unsupported by this task. | Configuration Name availability and existing-configuration evidence |
| PWA-PROFILE | Public Worker Access profile option | No | The user asks to view or confirm the current PWA mode | Verify | ora_reference_lookups.md | verify_public_worker_access_profile_option | The returned values can explain the current mode but are not a prerequisite for package preparation | Pass profileOptionCode ORA_PER_PUBLIC_WORKER_ACCESS_ENABLED exactly when the lookup is requested | Effective and site-level ProfileOptionValue and verification status |
| PWA-PROFILE-CHANGE | Public Worker Access profile-option change | Yes | A change to ORA_PER_PUBLIC_WORKER_ACCESS_ENABLED is requested | Route | hcm.hcm-security.hcm-security-common.manage-profile-options |  | Configure Public Worker Access does not change profile-option values | Route the requested value change to hcm.hcm-security.hcm-security-common.manage-profile-options; continue PWA package preparation independently of optional profile verification | Requested value-change scope and handoff status |
| PWA-MODE | PWA profile option mode | No | A profile-option lookup is requested | Verify | ora_reference_lookups.md | verify_public_worker_access_profile_option | N, Y, and M describe the returned mode; package design remains governed by its applicable role, criterion, and package rules | Present the returned value when available; do not require it before selecting the design | Effective and site-level N, Y, or M values and verification status |
| PWA-DFF-INDEX | Search-index attribute publication | Yes | An advanced filter uses a DFF attribute | Verify | Manage Search Indexes result and completed ESS request | verify_dff_search_index_publication | Rule Builder rejects invalid or unpublished DFF attributes | Publish the selected DFF attribute before package creation or update | Published attribute and request ID |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | A create has zero exact configuration-Name matches, or an update or delete has exactly one exact unchanged Name match | Yes; read-only lookup only |
| Blocked | A create duplicates an existing configuration Name, an update or delete has zero or multiple exact matches, or a rename is requested | No; provide a unique Name, the exact existing Name, or use a separately supported rename route |
| Verify | A documented prerequisite must be confirmed | No |
| Blocked | A required prerequisite is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWA.CHECK_DEPENDENCIES | decision | 3 | resolve_dependency | satisfied->PWA.RESOLVE_REFERENCES;blocked->PWA.BLOCKED | PWA.VERIFY_CONFIGURATION_NAME | stop | Configuration Name availability and input validation passed for a Data Loader package |
