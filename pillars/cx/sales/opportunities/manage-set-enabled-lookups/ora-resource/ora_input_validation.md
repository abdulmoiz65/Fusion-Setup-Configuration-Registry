# Manage Set Enabled Lookups Input Validation

## FSM Task Identity Policy

Require exact task code/name, selected task `SKILL.md`, target environment, and
immutable archive SHA-256 throughout review, export, package preparation, and
validation.

- Review, export, and package preparation do not require Data Loader task context.
- Every Core Data Loader mutation handoff requires a persisted project
  `TaskContextPath`, exact `TaskName`, and positive `TaskSequence`.
- The selected context entry must resolve to this task's exact skill path,
  `TaskCode`, `TaskName`, offering, and functional area.

The persisted context may come from a project setup-task plan without creating
an Oracle Run Book. Never hand-author, infer, or synthesize it solely to satisfy
Data Loader.

Use these task-scoped rules for the exact `FND_MANAGE_SET_ENABLED_LOOKUPS`
adapter. It owns only `MOO_SETID_ASSESS_OVRRIDE_RSN` and
`MOO_SETID_REVN_CATEGORY`. The source contract is the enclosing task skill,
Oracle's [Set-ID-Enabled Predefined Data for Opportunities](https://docs.oracle.com/en/cloud/saas/sales/fabus/business-units-and-opportunity-attributes.html),
and the Common Features [Set-Enabled Lookup Code](https://docs.oracle.com/en/cloud/saas/applications-common/26d/farca/api-set-enabled-lookups-lookup-codes-adf.html)
contract.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Request envelope | TargetEnvironment, Operation, RequestMode, and ExecutionRoute for a mutation | Block lookup, export, package review, or preview | Select one target; use SingleLookup for Inventory, Read, or direct REST and Package for Export, Import, or FSM package work | Every request |  |
| Single lookup identity | LookupType, SetSelectionDecision, and one of SetId, SetCode, BUOrgId, or OrganizationCode; confirmed Common Set is a valid decision but not an inferred selector | Block lookup and preview | Ask whether Common Set should be used or a different exact Set ID or Set Code should be selected; resolve confirmed Common Set through the read-only set resolver | SingleLookup | resolve_set_enabled_lookup_parent |
| Single code identity | LookupCode | Block lookup and preview | Supply the exact code | SingleLookup Read, Create, Update, Disable, or Delete |  |
| Single create definition | Meaning; optional Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, and Tag | Block preview | Supply a user-facing meaning and only intended mutable fields | SingleLookup Create |  |
| Single update definition | At least one of Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, or Tag | Block preview | Supply at least one intended mutable field | SingleLookup Update |  |
| Export task identity and persisted Data Loader task context | TaskCode fixed to FND_MANAGE_SET_ENABLED_LOOKUPS, exact target environment, and release | Block export routing | Select the exact task and target; no single set selector or LookupCode is required | Package Export |  |
| FSM baseline and final package | Fresh completed same-target export, exact task identity and persisted Data Loader task context, baseline and final package paths and SHA-256 values, exact ASM metadata identity, member inventory, exported headers, and final row counts | Block package review or Data Loader handoff | Export the exact task, preserve its contract, build the smallest delta, and reopen and hash the final immutable ZIP | Package Import or FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| FSM changed child codes | For every reviewed business child-code change: RowOperation, LookupType, LookupCode, exact set identity, proposed fields, current-state lock and impact; validate unchanged support parents separately | Block package review or Data Loader handoff | Resolve each changed child independently; one or both owned types may be changed, with unchanged parent linkage and unrelated baseline rows preserved | Package Import or FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| Direct REST preview | Exact method, returned item link when one exists, body or bodyless Delete, Upsert-Mode value for Create, before and after state, impact, verification GET, fingerprint, and separate approval | Block REST handoff | Build one immutable preview from fresh parent, set, and code evidence and approve that exact preview | SingleLookup explicitly selected REST or eligible SingleLookup/Package REST_FALLBACK Create, Update, or Disable | resolve_set_enabled_lookup_state |

| Final fallback receipt | REST_FALLBACK; same-target task/type/row/set CSV failure, applicable recovery outcomes, unchanged reviewed intent and complete prior-submission reconciliation | Block fallback; retain the original blocker | Apply omitted-parent recovery first. Submitted imports need a later explicit results request, all related jobs terminal, status/errors/ProcessLog and fresh unchanged row states | REST_FALLBACK Create, Update, or Disable | verify_set_lookup_rest_fallback |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Operation is outside Inventory, Read, Create, Update, Disable, Delete, Export, or Import | Reject before lookup or package validation | Every request |  |
| RequestMode is SingleLookup for Export or Import, or Package for Inventory, Read, or requester-selected direct REST other than REST_FALLBACK | Reject the incompatible mode; do not apply single-selector rules to package-only work | Every request |  |
| LookupType is not MOO_SETID_ASSESS_OVRRIDE_RSN or MOO_SETID_REVN_CATEGORY | Reject before lookup; route a named Opportunity type to its exact adapter and never infer a type from a display label | SingleLookup and every changed package row | resolve_set_enabled_lookup_parent |
| More than one single-request set selector is supplied and equivalence isn't proven | Reject the conflicting identity before lookup | SingleLookup with multiple selectors | resolve_lookup_reference_set |
| A set is required but SetSelectionDecision is absent, or Common Set was inferred from an empty selector, product default, environment convention, or prior example | Stop and ask whether to use Common Set or a different exact Set ID/Set Code; never continue with an assumed Common Set | Every SingleLookup request and every new changed package row | resolve_lookup_reference_set |
| SetId is not an integer, SetCode is blank after trimming, or the selected-environment lookup returns no exact set | Reject before code lookup or preview; request one valid exact set identity and never substitute Common Set or a close match. Do not reject a live-resolved integer solely because it is zero | Every SingleLookup request and every changed package row | resolve_lookup_reference_set |
| SetId and SetCode resolve to different sets, a confirmed Common Set choice resolves to a non-Common set, or the resolved set differs from the business-unit/organization assignment or package-row identity | Reject the conflicting set scope and show the sanitized mismatched identities; require the user to reconfirm Common Set or provide one different exact set | Every SingleLookup request and every changed package row | resolve_lookup_reference_set |
| LookupCode is blank, longer than 30 characters, contains a path separator or control character, or has surrounding whitespace | Reject the exact code; never silently normalize it | Every code-specific single request and every changed package row |  |
| Meaning is blank or longer than 80 characters | Reject the value and show the constraint | Create, or any row that supplies Meaning |  |
| Description is longer than 240 characters or Tag is longer than 150 characters | Reject the value and show the constraint | A changed row or REST body supplies the field |  |
| EnabledFlag is not Y or N | Reject the value | A changed row or REST body supplies EnabledFlag |  |
| StartDateActive or EndDateActive isn't an ISO 8601 date, or EndDateActive precedes StartDateActive | Reject the date or range | A changed row or REST body supplies an active date |  |
| DisplaySequence isn't an integer | Reject the proposed value; don't infer or renumber a sequence | A changed row or REST body supplies DisplaySequence |  |
| A mutation changes LookupType, LookupCode, SetId, SetCode, ReferenceGroupName, ModuleId, audit, seed, or returned resource identity | Reject the immutable-identity change before package or REST preview | Every Update, Disable, or Delete and every package delta | resolve_set_enabled_lookup_state |
| A mutation supplies an unrecognized field or changes a field outside Meaning, Description, EnabledFlag, StartDateActive, EndDateActive, DisplaySequence, or Tag | Reject the unsupported mutation field | Every REST body or package row delta |  |
| Create doesn't prove an exact missing code, Update doesn't name a mutable delta, or Disable proposes a change other than EnabledFlag=N | Reject the operation/state mismatch | Every changed row or direct REST request | resolve_set_enabled_lookup_state |
| Delete uses FSM, or a package row encodes Delete | Reject before package preparation; Delete is direct-REST-only | Delete or every package delta |  |
| Create, Update, or Disable has no explicit route | Default to FSM; never infer direct REST | Mutation route selection |  |
| Direct REST is neither explicitly selected nor eligible through the documented final REST_FALLBACK, the method or body doesn't match the operation, an existing-item operation lacks the returned item link, Create doesn't set Upsert-Mode=false, or the preview/approval binding is incomplete | Reject the REST handoff | Direct REST Create, Update, Disable, or Delete | resolve_set_enabled_lookup_state |
| A package uses a task code other than FND_MANAGE_SET_ENABLED_LOOKUPS or changes a lookup type owned by another task adapter | Reject readiness for the unsupported change; unchanged unrelated rows from the exact full-task baseline must remain preserved and are not adapter-owned mutations | Package Export, Import, Create, Update, or Disable | verify_set_lookup_package_readiness |
| A mutation baseline isn't a fresh successful export from the exact target, release, and task identity and persisted Data Loader task context | Reject package readiness; refresh the export | FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| ASM_SETUP_CSV_METADATA.xml is missing, duplicate, unreadable, encrypted, unsafe, or doesn't contain exactly one FND_MANAGE_SET_ENABLED_LOOKUPS identity | Reject package readiness without rewriting the ZIP | Package Import or FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| Baseline or final member names, headers, header order, metadata, or unrelated rows differ outside the reviewed row delta | Reject package readiness and report the exact difference | Package Import or FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| A reviewed changed child-code row lacks an owned type, exact resolvable set, supported operation, current-state lock, intended delta or impact | Reject the complete package; report invalid child changes and validate unchanged support parents through the separate linkage checks | Package Import or FSM Create, Update, or Disable | verify_set_lookup_package_readiness |
| PackagePath, PackageSha256, task identity and persisted Data Loader task context, or the artifact disagree before preview, or Task Hook finalData.archiveSha256 or approval evidence disagrees after Data Loader issues it | Block the current Data Loader stage and restart its validation and preview lifecycle | FSM handoff, Data Loader preview lifecycle, or approved upload, using only evidence available at that stage | verify_set_lookup_package_readiness |

| Successful export omits owned seeded parents/codes | Preserve exact baseline contract and unrelated rows; include one unchanged fresh live parent linkage per affected type plus reviewed child changes | Native FSM Create, Update, Disable or Import | verify_set_lookup_package_readiness |
| Changed child has no matching support parent or its resolved SetCode/join differs | Block handoff; parent linkage is a disclosed unchanged support row, not a requested parent mutation | Native FSM mutation or Import | verify_set_lookup_package_readiness |
| REST_FALLBACK bypasses identity/input/catalog/auth/set/assignment/context/approval constraints, explicit FSM-only scope, usable/repairable CSV, or pending/uncertain/partial submissions | Reject fallback before preview; require same-target exhaustion and full reconciliation without inventing facts or retrying an import | REST_FALLBACK | verify_set_lookup_rest_fallback |
| A fallback batch duplicates type/code/set identities, changes order/scope after review, sends read-only SetCode/audit/parent fields, or lacks its own exact-preview approval | Block REST submission; prepare one immutable ordered preview and approve it immediately before execution | REST_FALLBACK | resolve_set_enabled_lookup_state |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OPP.SET_LOOKUP.VALIDATE | step | 1 | validate_input | valid->OPP.SET_LOOKUP.RESOLVE_PARENT;missing->OPP.SET_LOOKUP.RETURN_MISSING;invalid->OPP.SET_LOOKUP.RETURN_MISSING;failed->OPP.SET_LOOKUP.RETURN_FAILED | none | stop | Every Manage Set Enabled Lookups request; require an explicit Common Set confirmation or different set selection and reject malformed, unknown, or conflicting set identities |
