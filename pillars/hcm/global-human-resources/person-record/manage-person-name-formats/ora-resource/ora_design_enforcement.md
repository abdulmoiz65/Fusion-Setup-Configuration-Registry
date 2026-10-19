# Manage Person Name Formats Design Enforcement

## Purpose

Defines the mandatory Name Format scope, reference, token, route, and preview
design gates evaluated before routing. It does not perform lookups, apply
defaults, or infer mask tokens.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm format scope | Resolve one country-scoped format and exclude unrelated source rows |
| 2 | Resolve component tokens | Resolve every supplied component or separator label to one stored token |
| 3 | Confirm mutation control | Require the declared Data Loader route and approved immutable preview |
| 4 | Confirm reconciliation | Require post-load evidence for the requested state |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| SCOPE | A source is prepared | Blocking |  | Source includes unrelated rows or baseline create rows | Rebuild the scoped XLSX source | Source rebuild |
| FORMAT_REFERENCE | A format target or country scope is required | Blocking | find_manage_person_name_formats | Country, format type, name type, or exact format is missing, inactive, or ambiguous | Resolve one exact current format scope | Lookup fix |
| COMPONENT_TOKEN | Create or edit supplies components or separators | Blocking | resolve_name_format_component_token | A label has no unique proven token in the applicable contract | Resolve every label to one supported stored token | Lookup fix |
| REPLACEMENT_COMPONENT | Create or edit supplies `<$preferred$$fallback$>` | Blocking | resolve_name_format_component_token | The replacement component does not contain exactly two independently proven core tokens in preferred-then-fallback order, or it contains nesting, punctuation, or separators | Rebuild the replacement component from the two resolved tokens | Source rebuild |
| LITERAL_SEPARATOR | A human-readable layout contains whitespace, a comma, or another literal character | Blocking | resolve_name_format_component_token | Whitespace is not mapped to `$SPA$`, a comma is not mapped to `$COM$`, or another character lacks one exact proven separator token | Resolve each literal before rebuilding the source | Lookup fix |
| FORMAT_MASK | A FormatMask source value is prepared | Blocking |  | The value contains an unescaped pipe | Backslash-escape every pipe and revalidate the complete mask | Source rebuild |
| MUTATION_ROUTE | Create, edit, or delete | Blocking |  | REST, FSM, CSV, or another mutation route is proposed | Use only Core Data Loader with business object NameFormat | No |
| APPROVAL | A mutation is ready for submission | Blocking |  | The immutable preview is absent, stale, or unapproved | Revalidate and approve the exact preview | Re-preview |
| VERIFY | After load | Blocking | find_manage_person_name_formats | Reconciliation does not prove the requested state | Report failed or unknown; do not replay automatically | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_person_name_formats | Target, country scope, or reconciliation evaluation | Exact format identity, scope, ordered components, and current values | ora_reference_lookups.md |
| resolve_name_format_component_token | Create or edit supplies components or separators | One proven stored token for every ordered label | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PNF.ENFORCE | decision | 5 | design_enforcement | passed->PNF.ROUTE;not_required->PNF.ROUTE;blocked->PNF.ERROR | PNF.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
