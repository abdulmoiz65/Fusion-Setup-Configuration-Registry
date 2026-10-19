# Candidate Pool Package Design Enforcement

## Archive invariants

- The target process row must be `TypeCode=POOL` and must not reuse the source process code.
- A generated settings row and every generated setting-item row must join the target Pool process and its generated parent setting code exactly.
- The target process-routing row must retain the source-backed reusable Pool phase identity and canonical terminal-state behavior.
- Retain `ASM_SETUP_CSV_METADATA.xml` and all expected CSV members. Members outside the target Pool graph remain header-only.
- Every translation parent must resolve to the target Pool process row.

## Task nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| POOL.VALIDATE_ARCHIVE | decision | 50 | design_enforcement | valid->POOL.HANDOFF;invalid->POOL.HANDLE_ISSUES | POOL.BUILD_ARCHIVE | stop | Before immutable approval preparation |
