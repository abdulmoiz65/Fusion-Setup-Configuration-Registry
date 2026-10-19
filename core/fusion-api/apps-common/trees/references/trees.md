# Functional rules

## Model and source parameters

A structure defines sources and hierarchy rules. A tree instantiates it; versions
contain nodes. Adding a node associates an existing source record, not a new
business record. Node IDs differ from ordered source primary-key tuples and
from display names. Single nodes represent values, ranges represent intervals,
and referenced-tree nodes point to another version under the same structure.
Range/reference creation is currently blocked pending a complete action contract.

Validate proposed source-member primary-key values through the relevant existing
source-object resolver before mutation. That check establishes the source record;
it does not use a generated TreeNodeId. After a successful node action, validate
the generated TreeNodeId with the structure-specific post-create endpoint listed
in contracts.md. A read-back failure is recorded separately from the action
result and does not turn a known-successful create into a retry.

Level labels follow data sources; Group labels allow discretionary assignment;
Depth labels follow depth automatically. Depth and level can differ. None means
no labeling. Resolve ragged and skip-level permissions from structure evidence.
A label definition, tree-label association and node label reference are distinct.

Tree parameters override structure defaults. Bound Value is constant, Variable
binds dynamic context, and View Criteria selects source filtering. Resolve all
mandatory parameters and source values under those effective filters. The
helper does not evaluate ADF view criteria.

For Position Tree creation, the requester supplies every tree-level Data Source
Parameter as an explicit FndTreeDataSourceParamsVO tuple: DataSourceId,
ParameterId and ParameterValue. Before a create, compare the complete normalized
tuple collection to each existing tree with the exact TreeStructureCode. A match
permits the planned create. If no such tree exists, preserve an `assumed_correct`
result. If one exists and none match, persist the exception diagnostic and stop
before creating the tree, version or nodes. This user-supplied rule is distinct
from source-parameter validation performed after the new version exists for a
sequenced node action.

## Structure readiness

Use an existing active, audited structure. Obtain authoritative exported structure
and source configuration from the routed project/pillar workflow. The supplied
contracts establish no structure-discovery endpoint. Missing evidence is a gap,
not permission to invent one.

Structure audit checks accessible source VOs and valid registered keys, compatible
attribute types, label sources when enabled, set/date attributes when restricted,
and compatible node and row/column flattening tables. These are readiness
requirements, not instructions for direct SaaS database access or repair.
Structure changes can affect dependent statuses; deleting a structure can remove
dependent objects. Structure mutation is outside this route.

## Version validation

Each result is pass, fail, not applicable or unknown. Unknown flags are never
assumed false. Evaluate the final graph, including requested new parents.

| Check | Meaning |
| --- | --- |
| Effective Date | Start precedes end. |
| Root Node | A nonempty version needs one root unless multiple roots are allowed. |
| Maximum Depth | Respect each source limit; unlimited has no numeric cap. |
| Duplicate Node | Source plus full key tuple must be unique unless duplicates are allowed. |
| Available Node | Source values and referenced versions exist. |
| Node Relationship | Parent/child sources follow registered relationships. |
| SetID Restricted Node | When enabled, node source set equals tree set. |
| Label Enabled Node | Enabled schemes require labels on final nodes. |
| Date Restricted Node | When enabled, source dates cover the full version interval, possibly extending beyond it. |
| Multiple Active Version | Overlap is forbidden only when the structure disallows multiple active versions. |
| Range Based Node | Ranges require source permission. |
| Terminal Node | Leaf sources permit use as leaves. |
| Usage Limit | Use All Values requires complete source coverage. |

Local integrity checks additionally cover cycles, parent membership, exact IDs,
mandatory parameters and label compatibility. Do not present these as Oracle's
named validators. The helper automates normalized checks; prerequisite validation
and server audit still require independent evidence. Drafts may be incomplete;
report creation separately from readiness for audit/activation.

## User-specified defaults

TreeVersionId is system generated: omit on standalone/nested creates even if
metadata marks it mandatory. Disclose any supplied ID omission; do not convert
create into update. Existing-version actions require the resolved identifier.

Missing/null/blank create start dates default to the plan date in its timezone;
end dates default independently to 4712-12-31. Preserve valid explicit dates;
reject malformed nonblank ones. No date defaults on PATCH or undated resources.
Freeze approved values; --as-of is only a reproducible offline fixture option.
New versions default to DRAFT. For Draft version creates only,
ChangedSinceValidation defaults to `"Y"` when omitted, null or blank;
LevelCount and NodeCount independently default to `0` when omitted or null.
Explicit ChangedSinceValidation must be a one-character string; explicit counts
must be non-negative integers. Preserve valid explicit values and reject invalid
values before a Fusion call. These defaults apply to both nested fndTrees version
creates and standalone fndTreeVersions creates, never PATCH. UI Active-to-Draft
editing and keep-active options do not establish REST behavior.

## Audit, activation and flattening

Audit must succeed before activation. No complete REST/ESS contract is established
here. Hand off to Manage Trees and Tree Versions, Actions > Audit and activation
after success; collect operator evidence rather than claiming automatic completion.

Manage All Trees Operations Centrally in Scheduled Processes provides Copy Tree
Version With Nodes (source structure/code/version name and duplicate version name),
Audit and Validate Tree Version (optional Set Active Status), and Flatten Tree
Version (optional Force Flattening). Incremental row/column flattening is default.
Row flattening materializes descendants; column flattening materializes ancestry.
Do not invent job IDs or invoke ESS without a separately documented routed skill.
