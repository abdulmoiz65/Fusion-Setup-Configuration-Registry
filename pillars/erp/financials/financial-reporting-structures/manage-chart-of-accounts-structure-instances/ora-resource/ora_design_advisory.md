# Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Functional | Listed Oracle COA, value-set, future-segment, import, LOV, and REST pages | Behavior and sequencing |
| Metadata | Listed FND_VS and FND_KF EDM pages | Field meaning, keys, and relationships |
| Implementation | COA Attributes workbook and COA Best Practices document | Defaults and design review |

## Source Mapping

| Rule or Decision | Source Evidence |
|---|---|
| Export-first default derivation and source order | User requirement; same-task FSM export; listed Oracle docs and EDM |
| Structure attributes, required labels, inheritance, future segments | Listed COA structure and future-segment pages |
| Value-set format and value attributes | Listed value-set, values/hierarchies, and import pages |
| Structure instances key and relationship validation | Relevant listed FND_VS/FND_KF EDM pages |
| Design review | Attached COA Best Practices document |
| Technical defaults | Attached COA Attributes workbook |
| Default segment design | COA Best Practices: use Company, Cost Center, Account, and Intercompany as the default corporate structure |
| Segment governance and scope | COA Best Practices: centralize COA control, avoid redundant segments, and prefer fewer meaningful segments |
| Future segments | COA Best Practices advises against future or reserved segments because they degrade user experience |
| Intercompany design | COA Best Practices: use an intercompany segment for multiple legal entities and align its values to the company segment |
