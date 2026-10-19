# Design Enforcement

Require least privilege, clear job/abstract/duty/data-role classification, documented role inheritance, approved duty and privilege mappings, explicit data-security scope, and avoidance of duplicate roles. Treat seeded roles and privileges as protected by default. Require an applicable SoD review before a scope-changing design is ready.

| Finding | Result |
|---|---|
| Missing role classification, inheritance, or data-security scope | Block planning or preview. |
| Duplicate-role risk or undocumented duty/privilege mapping | Return design issue; do not invent a resolution. |
| Seeded-role or privilege change without current Oracle support and approval | Block. |
| Excessive privilege or unresolved SoD concern | Return for approved remediation. |
