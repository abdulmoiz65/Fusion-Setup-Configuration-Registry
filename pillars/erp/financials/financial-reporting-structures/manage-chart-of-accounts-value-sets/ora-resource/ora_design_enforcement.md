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
| COAVS.001 | Always | Error | find_value_set | Equivalent object differs | Obtain update-or-new decision | No |
| COAVS.002 | Structure | Error | FSM label metadata | Primary Balancing or Natural Account label absent | Use valid exported code | Yes |
| COAVS.003 | Future-use segment | Error | FSM export | Required, Displayed, or default absent | Correct design | Yes |
| COAVS.005 | Always | Error | Complete same-task FSM export | Populated CSV files or ASM_SETUP_CSV_METADATA.xml are absent | Run complete export before defaulting or package generation; use template-only only as a supplement | Yes |
| COAVS.006 | Intercompany value set | Error | Company value-set design | Intercompany values are not designed to align with company values | Align values before preview | Yes |
| COAVS.007 | SecurityEnabledFlag is Y | Error | Data security object metadata | DataSecurityObjectName is blank, the referenced object does not exist, or its object tag is blank | Supply a ready data security object or set SecurityEnabledFlag to N | Yes |
| COAVS.008 | ValidationType indicates table validation | Error | Table-validation source metadata | A required table-validation field is blank, or supplied table, column, enabled/date, where, or order-by metadata cannot be verified | Correct the table-validation metadata or use the independent validation type | Yes |
| COAVS.009 | COA-driven value-set candidate is absent | Error | find_value_set | A requested COA segment has no validated candidate code, requested MaximumLength, or business classification | Derive SegmentCode_VS where SegmentCode is available; otherwise collect the missing segment design. Do not ask for a separate value-set creation confirmation. | Yes |
| COAVS.010 | User requests COA creation without structural details | Error | none | COA identity, confirmation or revision of the proposed Company, Cost Center, Account, and Intercompany baseline, segment lengths, or user-designed additional segments is absent | Present the baseline as a proposal and request the missing design facts. Do not derive additional segments, values, hierarchies, or artifacts. | No |
| COAVS.011 | Any live import | Critical | none | A direct FSM endpoint or another import adapter is selected instead of core.data-loader | Submit the approved immutable FSM ZIP through core.data-loader only. | Yes |

## Design Lookup Requirements

| Rule ID | Resolver | When Required | Values Needed | Source File |
|---|---|---|---|---|
| COAVS.007 | verify_value_set_security_object | Before preview when SecurityEnabledFlag is Y | DataSecurityObjectName, object existence, and nonblank object tag | KFFSegmentValueSetVO.xml and FND_OBJECTS metadata |
| COAVS.008 | verify_table_validated_value_set_metadata | Before preview when ValidationType indicates table validation | FromClause, required value and ID column metadata, and any supplied enabled/date or clause metadata | ValueSetVO.xml and FND_VS_VT_TABLE_EXT metadata |
