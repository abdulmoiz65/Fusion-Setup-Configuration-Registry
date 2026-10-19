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
| Structures key and relationship validation | Relevant listed FND_VS/FND_KF EDM pages |
| Design review | Attached COA Best Practices document |
| Technical defaults | Attached COA Attributes workbook |
| Default segment design | COA Best Practices: use Company, Cost Center, Account, and Intercompany as the default corporate structure |
| Segment governance and scope | COA Best Practices: centralize COA control, avoid redundant segments, and prefer fewer meaningful segments |
| Segment order and separators | COA Best Practices: Company, Cost Center, Account, Intercompany order; . or - is preferred for usability when the business has no stated delimiter |
| Future segments | COA Best Practices advises against future or reserved segments because they degrade user experience |
| Intercompany design | COA Best Practices: use an intercompany segment for multiple legal entities and align its values to the company segment |
| Vague COA request baseline | User-provided rule: propose Company, Cost Center, Account, and Intercompany, then require user confirmation or revision |
| User-owned additional segment design | User-provided rule: never derive additional segments; collect them from the user or an approved design source |
| Missing COA identity | User-provided rule: configuration without a COA must trigger a follow-up asking which COA owns it |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Vague chart-of-accounts creation request | Required follow-up | Explain the proposed Company, Cost Center, Account, and Intercompany baseline and ask for the COA name, confirmation or revision, and additional segments | Do not state that the baseline is approved or create-ready before the user confirms it |
| Additional segments | Design owner decision | Explain that the user or approved design source must identify every segment beyond the basic proposed set | Do not invent future, reserve, affiliate, department, product, location, or other segments |
| Configuration without a COA | Required follow-up | Ask which COA owns the supplied configuration | Do not infer COA Name or StructureCode from the configuration, environment, files, or conversation history |

## Output Rules

| Situation | What Happens |
|---|---|
| Request says only create or add a chart of accounts | Return a follow-up that proposes the basic four segments and asks for the COA name, confirmation or revision, and any additional segments. |
| User provides a partial segment design | Preserve the supplied segments, identify missing required business meanings, and ask the user to complete or approve the design. Do not derive optional or additional segments. |
| User provides configuration without identifying the COA | Return a follow-up asking for the COA Name or StructureCode and stop before artifact generation or Fusion activity. |
