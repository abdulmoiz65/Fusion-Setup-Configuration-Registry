# Manage Extended Lookup Codes Design Enforcement

## Purpose

Defines the mandatory Extended Lookup Code design gates evaluated before
preview or routing. It does not perform lookups, apply defaults, or create a
missing parent lookup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm business key | Resolve the complete scoped key or create-availability evidence |
| 2 | Confirm parent scope | Resolve one enabled current parent and its exact legislation scope |
| 3 | Validate source | Keep only the selected current XLSX rows and the supported source-key mode; remove unused template columns |
| 4 | Confirm mutation control | Require the declared Data Loader route and approved immutable preview |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Create, edit, delete, or duplicate check | Blocking | find_extended_lookup_codes | The business key is incomplete, its scope is implicit, or the result is ambiguous | Correct the complete scoped key and resolve all required pages | Lookup fix |
| INTERNAL_ID | Every operation | Blocking | find_extended_lookup_codes | A caller-supplied or saved ExtendedLookupCodeId is treated as authority | Discard it and resolve the business key fresh; retain a fresh ID only within the current edit, delete, or translation DAT | Lookup fix |
| PARENT | Create, edit, or delete | Blocking | resolve_extended_lookup_parent_scope | The parent lookup is missing, disabled, ambiguous, or scope-incompatible | Resolve one enabled current parent tuple; never create it implicitly | Lookup fix |
| SOURCE | Create, edit, or delete | Blocking |  | XLSX source is stale, incomplete, unsafe, or contains unrelated changes | Rebuild the smallest selected-row source and revalidate it | Source rebuild |
| SOURCE_KEY_MODE | Base create | Blocking |  | SourceSystemOwner or SourceSystemId is absent or blank, only one is present, or a caller-supplied pair lacks validated provenance | Add the deterministic FDOS pair or preserve a complete validated caller pair; never submit a keyless MERGE | Source rebuild |
| XLSX_CONTRACT | Create, edit, or delete | Blocking |  | The editable source is not an XLSX generated from current Core Data Loader metadata, or a hand-authored DAT is proposed as the approval source | Regenerate the XLSX through Core Data Loader and review it before internal DAT conversion | Source rebuild |
| DAT_CONTRACT | Create, edit, or delete | Blocking |  | The internally generated header is not the live `ExtendedLookupCode` or `ExtendedLookupCodeTranslation` DAT contract, it includes `RestAction`, or its ZIP member is not named after the exact top-level discriminator | Regenerate internally through Core Data Loader from the frozen XLSX, use the native DAT record verb, and emit `ExtendedLookupCode.dat` or `ExtendedLookupCodeTranslation.dat` as applicable | Source rebuild |
| DAT_VERB | Create, edit, or delete | Blocking |  | Internal conversion does not use `MERGE` for create or edit, or `DELETE` for delete | Rebuild through Core Data Loader before preview | Source rebuild |
| MINIMAL_SOURCE | Create, edit, or delete | Blocking |  | The source retains unused GUID, source-reference, or DFF columns, or omits a requested DFF value | Build the smallest current-template source with only requested values and required keys | Source rebuild |
| MUTATION_ROUTE | Create, edit, or delete | Blocking |  | REST, FSM, CSV, or another mutation route is proposed | Use only Core Data Loader with business object ExtendedLookupCode | No |
| APPROVAL | Create, edit, or delete | Blocking |  | Preview or approval is missing, stale, or not bound to both the frozen XLSX and generated ZIP fingerprints | Regenerate and approve the exact immutable preview | Re-preview |
| VERIFY | After load | Blocking | find_extended_lookup_codes | Reconciliation does not prove the requested state | Report failed or unknown; do not replay automatically | No |

| LOOKUP_NAMING | Create or edit | Warning |  | Name is unclear, inconsistent, or duplicated | Use concise, business-recognizable, consistently capitalized names | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_extended_lookup_codes | Identity, current-run ID, uniqueness, or reconciliation evaluation | Complete business key, exact scope, current values, and match cardinality | ora_reference_lookups.md |
| resolve_extended_lookup_parent_scope | Create, edit, or delete | One enabled current parent tuple and exact LegislationCode | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| XLOOK.ENFORCE | decision | 5 | design_enforcement | passed->XLOOK.ROUTE;not_required->XLOOK.ROUTE;blocked->XLOOK.ERROR | XLOOK.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
