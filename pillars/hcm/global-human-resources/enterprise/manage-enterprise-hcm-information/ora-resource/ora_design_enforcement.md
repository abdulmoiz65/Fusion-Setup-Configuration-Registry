# Manage Enterprise HCM Information Design Enforcement

## Purpose

Defines the mandatory Enterprise classification and EFF design gates evaluated
before preview or routing. It does not perform lookups, apply defaults, or
invent parent identifiers.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record |
| 2 | Resolve classification parent | Follow the Enterprise enterpriseEFF envelope and resolve the ENTERPRISE classification row |
| 3 | Validate context | Confirm the EFF context and segment from current describe metadata |
| 4 | Validate source structure | Build the Organization, freshly resolved existing OrgUnitClassification, and changed OrgInformation rows with their resolved row identities and one logical-object effective date |
| 5 | Validate segment value | Require one typed value compatible with the resolved segment contract |
| 6 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_enterprise | The effective Enterprise parent is absent or unresolved | Supply one effective date covered by the Enterprise row | Lookup fix |
| CLASSIFICATION_PARENT | An OrgInformation EFF row is built | Blocking | resolve_enterprise_classification | ENTERPRISE classification parent is absent, ambiguous, or not linked to OrgInformation | Resolve the classification parent from enterpriseEFF; do not guess it | Lookup fix |
| EFF_STRUCTURE | An OrgInformation EFF segment is supplied | Blocking | resolve_enterprise_context | Existing-row identity, SequenceNumber, flexfield code, EFF category, context, segment, or classification-parent link is missing | Rebuild the source with resolved row identity, EFF controls, and parent links | Source rebuild |
| MULTIROW_KEY | A multirow context is supplied | Blocking | resolve_enterprise_context | A configured unique-key segment is missing or duplicated | Complete the context user key | Input fix |
| SEGMENT_VALUE | A proposed EFF segment value is supplied | Blocking | validate_enterprise_segment_value | The value is missing, ambiguous, type-incompatible, or mapped to the wrong target attribute | Resolve one typed value for the declared target attribute | Lookup fix |
| DELETE_ROW | Date-effective delete | Blocking | resolve_enterprise_delete_history | Complete delete or ZAP is requested, the current history row is missing or ambiguous, or it is the first date-effective row | Confirm the displayed eligible current row or refuse the delete | Input fix |
| DESIGN | A context or segment value is required | Blocking |  | The value is inferred rather than configured or exactly resolved | Supply or resolve one approved business value | Input fix |

| ENTERPRISE_NAMING | Edit | Warning |  | Enterprise name is not the official organization name or contains environment identifiers | Use a simple, recognizable official name | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_enterprise | Every request | Effective Enterprise identity, range, and current parent values | ora_reference_lookups.md |
| resolve_enterprise_classification | An OrgInformation EFF row is built | One ENTERPRISE classification parent and effective values | ora_reference_lookups.md |
| resolve_enterprise_context | A context or segment is requested | Context collection, segment contract, type, cardinality, and value-set contract | ora_reference_lookups.md |
| validate_enterprise_segment_value | A proposed segment value is supplied | One typed stored value for the declared target attribute | ora_reference_lookups.md |
| resolve_enterprise_delete_history | Date-effective delete | Complete history, one current row, effective range, and internal eligibility | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ENT.DESIGN | decision | 10 | design_enforcement | passed->ENT.ROUTE;not_required->ENT.ROUTE;blocked->ENT.ERROR | ENT.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
