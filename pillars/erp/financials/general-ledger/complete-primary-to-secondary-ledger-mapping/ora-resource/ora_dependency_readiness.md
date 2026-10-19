# Complete Primary to Secondary Ledger Mapping Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Environment and release identity | Confirm the target environment and current Fusion release before accepting any export |
| 2 | Scoped package | Acquire a valid current export for this exact task and accounting-configuration scope |
| 3 | Parent relationship | Resolve the exact primary-to-secondary relationship and its current lifecycle tuple |
| 4 | Structural and rate prerequisites | Resolve directional COA mapping only when COAs differ and rate type only when currencies differ |
| 5 | Optional conversion prerequisites | Resolve BSV value-set/value evidence or preserve and hand off custom journal policy only when explicitly selected |
| 6 | Package graph | Validate all ten CSV members, both 133-column aliases, actual headers, semantic parent keys, and ASM_SETUP_CSV_METADATA.xml before authoring |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| scoped_package | Exact current task package | Yes | Always | Blocked until validated | Validated project package, else fresh direct export, else signed-in UI download | acquire_scoped_mapping_package | Prevent stale, wrong-release, wrong-scope, or partial authoring | Supply or approve acquisition of an exact current export | Baseline ZIP; environment; release; task; scope; checksum; headers; manifest graph |
| relationship | Existing primary-to-secondary relationship | Yes | Always | Lookup | Scoped package relationship and ledger aliases | resolve_primary_secondary_relationship | Establishes the exact parent and comparison values | Provide exact primary and secondary ledger names | Parent tuple; categories; level; structures; currencies; OrgIdTrans |
| coa_mapping | Directional COA mapping | Conditional | Structure instances differ | Lookup | Scoped Financial Reporting Structures mapping-task export | resolve_directional_coa_mapping | Name4 must identify the correct source-to-target direction | Select an exact existing mapping | Name4; source structure; target structure |
| rate_type | Conversion rate type | Conditional | Currencies differ | Lookup | Current Fusion rate-type LOV | find_conversion_rate_type_exact | Different-currency mapping cannot proceed without a rate policy | Choose the exact rate type; do not assume Corporate | AlcDefaultConvRateTypeTrans; canonical display |
| balancing_value_set | Source balancing value set | Conditional | Controlled BSV conversion is explicitly selected | Lookup | Current populated GL_MANAGE_CHARTS_OF_ACCOUNTS_STRUCTURE_INSTANCES or GL_MANAGE_CHARTS_OF_ACCOUNTS task export; trigger the task-level export when no usable existing package contains the source COA | derive_balancing_value_set | Segment values must be resolved in the exact export-derived semantic balancing-role value set | Confirm the requested BSV design; FSCR reuses a current matching export or triggers the named task export and reports exact member/key defects | ValueSetCode; balancing SegmentCode and ColumnName; structure and export receipt |
| balancing_values | Exact effective balancing values | Conditional | BSV conversion rows are explicitly selected | Lookup | Current code-keyed value-set child endpoint | find_balancing_segment_value_exact | Prevent wrong-value-set, expired, or ambiguous conversion rows | Supply each exact source value | SourceSegmentValue; Meaning; effective state |
| existing_rules | Existing journal conversion rules | Conditional | Relationship already has rules or custom policy is requested | Verify | Scoped package | resolve_existing_conversion_rules | Existing rows must survive and custom policy is UI-controlled | Review the catch-all disclosure or complete custom rules in the UI | Existing semantic keys; parent aliases; flags |
| preview_approval | Accountable package approval | Yes | A package delta is ready | Blocked until explicit approval | Diff receipt signed by an accountable reviewer |  | Mapping can change subsequent accounting behavior | Approve the exact checksum-bound preview | Approval identity; timestamp; preview checksum |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Exact scoped evidence is present and current | Yes; read-only lookup or local derivation only |
| Lookup | Business value is present but authoritative code or related attributes are unresolved | Yes; read-only lookup only |
| UI handoff | Optional custom journal, tree, replication, DFF, or unsupported field behavior lacks an exact portable contract | No direct CSV authoring; baseline may continue preserved or disabled, but Review readiness waits for UI completion and re-export |
| Blocked | Package, relationship, conditional mapping/rate/value, or approval evidence is missing or ambiguous | No |
| Preserve | Dependency member or row exists only for package closure | No create; preserve byte and semantic content |

## Package Acquisition and Shape

| Rule | Contract |
|---|---|
| Acquisition order | Use a validated project package; otherwise obtain a fresh direct export; if completed export bytes are unavailable, use the signed-in UI download; block with FSM_EXPORT_UNAVAILABLE when none succeeds |
| Freshness checks | Confirm environment, release, task, scope, Completed state, zero export errors, retrievable bytes, checksum, actual headers, and expected graph; Completed alone is not proof of a usable ZIP |
| Required CSV members | GL_LEDGER.csv 24 columns; ORA_GL_PRIMARY_LEDGER_CONFIG.csv 24; GL_PRIMARY_LEDGER.csv 133; GL_SECONDARY_LEDGER.csv 133; ORA_GL_JOURNAL_CONFIG_DETAIL.csv 15; ORA_LEGAL_ENTITY_BAL_SEG_VAL_DEF.csv 16; GL_LEDGER_SEG_VAL_ASSIGNMENT.csv 31; ORA_GL_LEDGER_RELATIONSHIP.csv 57; ORA_GL_JOUNAL_CONVERSION_RULES.csv 39; ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv 43; actual current export headers remain authoritative |
| Required manifest | ASM_SETUP_CSV_METADATA.xml; preserve Oracle member names, including the JOUNAL typo, logical paths, field graph, node order, task/release/scope metadata, and header order |
| Mapping-owned members | ORA_GL_LEDGER_RELATIONSHIP.csv; conditional parent updates or supported rows in ORA_GL_JOUNAL_CONVERSION_RULES.csv; conditional GL_LEDGER_SEG_VAL_ASSIGNMENT.csv; conditional ORA_PRIMARY_BALANCING_SEGMENT_VALUE_CONVERSION_RULES.csv |
| Dependency closure | Root aliases, both 133-column ledger aliases, journal config detail, and legal-entity BSV definition remain present and unchanged unless a separately supported task owns a change |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| GLMAP.DEPENDENCIES | decision | 20 | resolve_dependency | ready->GLMAP.LOOKUPS;blocked->GLMAP.RETURN_ISSUES | GLMAP.VALIDATE | stop | Validated intake exists |
