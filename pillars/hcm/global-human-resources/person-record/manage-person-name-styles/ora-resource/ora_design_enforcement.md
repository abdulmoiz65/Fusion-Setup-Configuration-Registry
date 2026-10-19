# Manage Person Name Styles Design Enforcement

## Purpose

Defines the mandatory Name Style country, component, source-order, and route
design gates evaluated before preview or routing. It does not perform lookups,
apply defaults, or infer missing setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record |
| 2 | Validate country and structure | Confirm one country context, supported fields, and required last-name component |
| 3 | Validate dependencies | Resolve supplied components and order parent rows before child rows |
| 4 | Confirm route | Require the reviewed FSM source and Core Data Loader for create or ordinary field edit; reject deletion and component removal |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Every request | Blocking | find_manage_person_name_styles | Identity is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| COUNTRY | Read, create, or ordinary field edit of a country-specific style | Blocking | resolve_country_context | A supplied country or legislation is unresolved or ambiguous | Supply one exact country or legislation | Lookup fix |
| COMPONENT | A Name Component is supplied | Blocking | resolve_name_style_component | Component is not one enabled compatible PER_NAME_STYLE_ATTRIBUTES code | Resolve the component through Common Lookups | Lookup fix |
| STRUCTURE | Child setup rows are requested | Blocking | validate_parent_before_child | Parent row is absent, follows a child row, or a required last-name component is removed | Correct the scoped source rows | Input fix |
| ROUTE | Create or edit is requested | Blocking |  | The request bypasses the reviewed FSM ZIP and Core Data Loader | Use the approved Core Data Loader FSM create or edit route | No |
| DELETE_UNSUPPORTED | Whole-style deletion or child-component removal, including an edit that removes existing components | Blocking |  | Requested effect deletes a style or component; FSM imports do not delete existing records | Stop with unsupported-operation response; do not plan, preview, approve, or execute deletion through any route | No |

| NAME_STYLE_SAFETY | Create or ordinary field edit | Warning |  | Delivered components are removed, unsupported components are used, or an existing style is not considered | Reuse delivered setup where suitable and preserve required delivered components | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_person_name_styles | Exact read or edit target | Parent style and expanded nameSetups | ora_reference_lookups.md |
| resolve_country_context | Country-specific read, create, or edit | CountryName and LegislationCode | ora_reference_lookups.md |
| resolve_name_style_component | Component is supplied | Stored component code | ora_reference_lookups.md |
| validate_parent_before_child | Create or edit source is prepared | Validated FSM package, keys, and row order | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNS.ENFORCE | decision | 5 | design_enforcement | passed->PNS.ROUTE;not_required->PNS.ROUTE;blocked->PNS.ERROR | PNS.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
