# Activity Profile Options Defaulting and Precedence Rules

Oracle-published defaults describe delivered behavior; they are not configured
values or mutation instructions. Never create a value merely because a
documentation page shows a default.

## Oracle Documentation Sources

| Source | Used For |
|---|---|
| https://docs.oracle.com/en/cloud/saas/sales/fasqa/why-can-t-i-find-my-activities-using-find-or-advanced-search-in-the-classic-ui.html | All Records I Can See default |
| https://docs.oracle.com/en/cloud/saas/sales/oasal/set-up-activity-notifications.html | Activity notification defaults |

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| ZMM_ACTIVITY_ENABLE_ALL_RECORDS | No | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_TASKS_EXTERNAL_NOTIFICATION | No | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_EXTERNAL_NOTIFICATION | Yes | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_DISABLE_EMAIL_APPT_NOTIF | No | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_DISABLE_EMAIL_TASK_NOTIF | No | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_DISABLE_LIST_APPT_NOTIF | No | Comparing configured behavior with Oracle's documented delivery | No | |
| ZMM_ACTIVITY_DISABLE_LIST_TASK_NOTIF | No | Comparing configured behavior with Oracle's documented delivery | No | |
| Absent configured row | Not configured; allow lower-precedence configured or Fusion-delivered behavior | Reviewing an exact Site, Product, or User scope | No | resolve_exact_activity_profile_option_and_dependencies |
| Deleted configured row | Lower-precedence configured value or Fusion-delivered behavior | Previewing Remove or Delete | No | resolve_exact_activity_profile_option_and_dependencies |
| Absent from FSM export | Not a default and not proof of absence | Reconciling Inventory or Review | No | resolve_exact_activity_profile_option_and_dependencies |

## Application Rules

- Preserve current configured state unless the user requests a specific CRUD
  operation and approves its complete immutable preview.
- Use live validation and exact dependency resolvers to obtain the stored code
  or identifier. Never translate a display default into a stored value without
  one exact active match.
- For Create, require explicit child-row absence; do not silently persist an
  inherited or delivered value.
- For Delete, preview the fallback behavior without manufacturing a replacement
  row.
- Defaults are informational and do not contribute an apply-default Task Node.
