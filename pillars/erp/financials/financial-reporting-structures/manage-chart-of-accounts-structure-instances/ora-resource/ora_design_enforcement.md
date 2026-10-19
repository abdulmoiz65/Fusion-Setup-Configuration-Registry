# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Validate | Enforce mandatory COA and task field rules |
| 2 | Default | Apply only documented values and record source |
| 3 | Lookup | Compare existing object before create |
| 4 | Readiness | Block package with unresolved technical values |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| COAINS.001 | Always | Error | find_chart_of_accounts, get_chart_of_accounts | Equivalent object differs | Obtain update-or-new decision | No |
| COAINS.002 | Structure | Error | FSM label metadata | Primary Balancing or Natural Account label absent | Use valid exported code | Yes |
| COAINS.003 | Future-use segment | Error | FSM export | Required, Displayed, or default absent | Correct design | Yes |
| COAINS.005 | Always | Error | Complete same-task FSM export | Populated CSV files or ASM_SETUP_CSV_METADATA.xml are absent | Run complete export before defaulting or package generation; use template-only only as a supplement | Yes |
| COAINS.006 | Future-use segment | Error | Approved structure design | A future/reserved segment is proposed without approved exception | Do not add the segment; if approved, enforce Required, Displayed, and Default Value | No |
| COAINS.007 | Segment values and sequences are available | Error | Segment sequences and associated value-set values | A segment value exactly matches a generated member ID in segment_sequence-value form, such as value 2-100 for segment sequence 2 | Change the conflicting value before cube-ready approval | No |
| COAINS.008 | An instance segment default is supplied | Error | Referenced value-set datatype | DefaultType is blank, the referenced datatype is unresolved, a numeric default is not stored in DefaultValueNumber, a nonnumeric default is not stored in DefaultValue, or both default-value fields are populated | Correct the default type and populate only the datatype-compatible default-value field | Yes |
| COAINS.009 | Instance package is requested | Error | find_chart_of_accounts, find_value_set | The structure identity or any inherited or override value set is unresolved, incompatible, or ambiguous | Stop before instance export, package generation, preview, or import until all structure and value-set prerequisites are verified | Yes |
| COAINS.010 | User requests COA creation without structural details | Error | none | COA identity, confirmation or revision of the proposed Company, Cost Center, Account, and Intercompany baseline, segment lengths, or user-designed additional segments is absent | Present the baseline as a proposal and request the missing design facts. Do not derive additional segments, values, hierarchies, or artifacts. | No |
| COAINS.011 | Any live import | Critical | none | A direct FSM endpoint or another import adapter is selected instead of core.data-loader | Submit the approved immutable FSM ZIP through core.data-loader only. | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| COAINS.007 | compare_generated_member_ids | Before cube-ready approval | Segment sequence and every associated segment value | Developer-provided gl_detect_essbase_conf_pkg.pkb |
| COAINS.008 | find_value_set | Before preview when an instance segment default is supplied | ValueSetCode, ValueDataType, DefaultType, DefaultValue, and DefaultValueNumber | KFFSegmentInstanceVO.xml and referenced value-set metadata |
