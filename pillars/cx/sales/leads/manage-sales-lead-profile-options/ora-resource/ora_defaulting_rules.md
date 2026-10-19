# Defaulting and Precedence Rules

Oracle-published defaults describe delivered behavior; they are not configured
values or mutation instructions. Never create a value merely because a
documentation page shows a default.

## Precedence

| Scope | Rule |
|---|---|
| Site | Site-wide configured value and the normal implementation baseline |
| Product | Application-specific configured value; use only when that exact Product level is enabled and updatable |
| User | Exact-user configured value; use only when that User level is enabled and updatable |
| Absent configured row | Report not configured; never replace absence with an exported value or documented default |
| Deleted configured row | Disclose the lower-precedence configured value or Fusion-delivered behavior that can apply after deletion |
| Absent from FSM export | Not a default and not proof of absence; read the exact live child collection |

## Application Rules

- Preserve current configured state unless the user requests a specific CRUD
  operation and approves its complete immutable preview.
- Use live `SqlValidation` and exact dependency resolvers to obtain the stored
  code or identifier contract. Never translate a display default into a stored
  value without one exact active match.
- For Create, require explicit child-row absence; do not silently inherit and
  persist a lower-precedence value.
- For Delete, preview the resulting fallback behavior without manufacturing a
  replacement row.
- Do not add an `apply_default` Task Node. Defaulting remains informational.
