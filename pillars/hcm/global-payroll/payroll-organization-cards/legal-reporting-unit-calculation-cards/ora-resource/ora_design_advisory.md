# Legal Reporting Unit Calculation Cards Design Advisory

## Functional-User Operation Advisory

- Ask for business names, requested values, and effective dates—not `dirCardId` or other technical identifiers.
- Resolve the complete object path and effective history before deciding create, update, or correction.
- Explain an existing-data choice in functional terms: Update preserves prior history from the requested date; Correction changes the selected existing slice.
- Create only an absent leaf under resolved existing parents. Never duplicate an existing card or component because a requested child is absent.

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Catalog-backed | Task manifest and effective setup task catalog | Task identity, availability, and CSV export/import support |
| Release catalog description | Release setup task catalog description | High-level scope only |
| User-confirmed parity source | Legal Entity Calculation Cards HAR pattern confirmed by the user as applicable to TRU | Redwood calculationEntries endpoint shape after TRU read-only verification |
| Developer source | Notes, workbook rows, endpoint metadata, or approved contract artifacts | Runtime behavior, field mapping, and validation rules |
| Oracle documentation | Current Oracle documentation only when separately authorized | Product behavior not present in local source |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Task scope | Informational | Legal Reporting Unit Calculation Cards is scoped to tax reporting unit calculation cards based on catalog description | Undocumented statutory rules |
| CSV support | Informational | Catalog flags show export/import and CSV export/import support | Unsupported CSV column definitions |
| Runtime readiness | Blocking advisory | Use calculationEntries parity only after a read-only TRU response verifies sourceType=TRU and field shape | Fabricated endpoints or payload fields |
| Override design | Blocking advisory | Override fields are card-driven by getCardDetails metadata and LOV dataSource | Hard-coded Legal Entity override codes unless the TRU card returns them |

## Output Rules

| Situation | What Happens |
|---|---|
| User asks for implementation advice without source | Explain known catalog facts and list TBD blockers |
| User asks for field-level rule behavior | Use getCardDetails metadata when available; otherwise require source evidence or authorized documentation lookup |
| User asks for direct live execution | Redirect to preview and approval gates |
