# Jobs FSM bootstrap contract

Use this contract only after a fresh, structurally valid export for
`ORA_IRC_MP_SITE_CONFIGURATION` has been validated and its
`ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT.csv` member has zero data rows.

| Field | Approved bootstrap value |
|---|---|
| CSV member | `ORA_IRC_MP_SITE_CONFIG_AVAIL_CXT.csv` |
| `ObjectTypeCode` | `ORA_OM_SITE` |
| Prohibited inferred values | `ORA_OM_JOB_SITE`, `ORA_IRC_MP_SITE_CONFIG_FILTER` |

This is a task-specific technical contract, not a naming convention. It is
derived from the Recruiting availability-context product contract: the Job
site mapping is `ORA_OM_SITE`; `ORA_OM_JOB_SITE` is not a defined context
object type. Do not use a Gig sample or a root FSM-object name to replace this
value.

For a populated fresh member, the source data remains the primary contract and
must establish only `ORA_OM_SITE`. Record the fresh export fingerprint,
source-row count, branch (`populated_export` or `zero_row_bootstrap`), and
resolved value in preflight validation.
