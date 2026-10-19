# AutoInvoice Grouping Rule Reference Lookups

The class code has a source-backed local seed contract. Line-ordering and grouping-column identity resolve inside the FSM import hook; no supported public read-only setup GET was established. Do not invent a REST route. Sources: SRC-CODE-CLASS-EDIT-UIVO, SRC-CODE-CLASS-LOOKUP-VVO, SRC-CODE-CLASS-SEED, SRC-CODE-AMIMPL, SRC-CODE-ORDER-VO, SRC-CODE-GROUPBY-COLUMN-VO, SRC-CODE-GROUPBY-SEED.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|
| resolve_grouping_transaction_class | A class child is requested | GROUPING_TRX_TYPE system seed: C Credit Memo; D Debit Memo; I Invoice | Trim and match a business label case-insensitively or match exact code; only three enabled system codes | Class11: C, D or I | Reject off-domain or ambiguous input before package build |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_line_ordering_rule_by_name | LineOrderingRuleName supplied | Supplied exact rule name | TBD - no supported public preflight GET; FSM importData resolves against RA_LINE_ORDERING_RULES | Name, OrderingRuleId | Exact Name alternate key | OrderingRuleId filled internally by FSM import | Missing name removes affected root row and reports an error; multiple-match behavior not observed |
| resolve_grouping_column_name | Group-by child requested | Supplied exact FromColumnName | TBD - no supported public preflight GET; FSM importData resolves against RA_GROUP_BY_COLUMNS with COLUMN_ID under 1000 | FromColumnName, ColumnId | Exact FromColumnName alternate key | ColumnId filled internally by FSM import | Missing name removes affected child row and reports an error; multiple-match behavior not observed |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| No public preflight route for a reference | Use current pod export or task UI to confirm a candidate; FSM import remains authoritative after separately approved preview. |
| Optional UI grouping choices | The UI query offers 87 base optional seed rows and seven additional rows when consolidated-invoice opt-in is enabled; source seed alone does not prove target-pod availability. |
| Missing or ambiguous reference | Block candidate or report the exact FSM import diagnostic; do not substitute another name. |
