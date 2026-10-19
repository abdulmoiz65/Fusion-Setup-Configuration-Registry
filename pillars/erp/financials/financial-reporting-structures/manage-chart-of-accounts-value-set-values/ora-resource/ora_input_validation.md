# Value Set Value Input Validation

## Required Groups

| Group | Required Fields | Failure Behavior |
|---|---|---|
| Base candidate | ValueSetCode; Values[].Value; Description; SummaryFlag; AllowPostingFlag; AllowBudgetingFlag | Ask one consolidated question before authentication or package handoff |
| Natural Account candidate | A proved Structure Instance association or explicit standalone declaration; reviewed AccountType for every row | Ask for an explicit declaration when standalone Natural Account usage is claimed; stop until every AccountType suggestion is accepted or corrected |
| File candidate | Base candidate plus EnabledFlag in CSV position 6 | Reject the affected file rows |
| Parent lookup | Exactly one matching ValueSetCode; MaximumLength from 1 through 150 | Stop before package generation |
| Live execution | Valid package plus explicit create/update intent | Return preview only when live intent is absent |

## Validation Rules

| Rule ID | Field | Severity | Invalid When | Required Handling |
|---|---|---|---|---|
| MVS.002 | ValueSetCode | Error | Blank | Stop |
| MVS.003 | Values | Error | Empty | Stop |
| MVS.004 | Value-set resolution | Error | Parent GET returns no exact match, multiple exact matches, or invalid MaximumLength | Stop before package handoff |
| MVS.005 | Value | Error | Repeated inside the batch | Reject the complete batch |
| MVS.006 | Flags | Error | Required flag isn't Y/N or an unambiguous equivalent | Report row and field |
| MVS.010 | Value | Error | Blank or longer than MaximumLength | Report exact and maximum lengths |
| MVS.011 | Value | Error | Contains `"`, `=`, `[`, `]`, or `,` | Reject the row |
| MVS.012 | Value | Error | Starts with `@`, `\`, `{`, `}`, `,`, `=`, `<`, `(`, `)`, `.`, `+`, vertical bar (U+007C), space, `-`, `'`, or `_` | Reject the row |
| MVS.013 | Value | Error | Contains an Essbase or GL reserved word such as DEFAULT, ALL, CALC, DIM, MBR, MISSING, HISTORY, YEAR, PERIOD, TOTAL, QTD, YTD, PTD, ACTUAL, currency codes, or N/A | Reject the row |
| MVS.015 | AccountType | Error | Supplied but not A/L/E/O/R or a named equivalent; or omitted when Natural Account usage is proved or declared | Reject the row; require user review of every description-derived suggestion |
| MVS.016 | ThirdPartyControlAccount | Error | Not N, Y, R, CUSTOMER, or SUPPLIER | Reject the row |
| MVS.017 | Description | Error | Blank, longer than 240 characters, or contains double quote | Reject the row |
| MVS.018 | Dates | Error | Invalid date, unsupported format, or End Date precedes Start Date | Accept YYYY-MM-DD or YYYY/MM/DD and write YYYY/MM/DD |
| MVS.019 | SummaryFlag, AllowPostingFlag, and AllowBudgetingFlag | Error | SummaryFlag is `Y` and either AllowPostingFlag or AllowBudgetingFlag is `Y` for the same value | Reject the complete batch; a summary value must have both Allow Posting and Allow Budgeting set to `N` |
| MVS.020 | FBDI columns | Error | Unknown populated column after 101 or imported workbook validation state | Reject before ZIP generation |
| MVS.021 | Value | Error | Matches a segment name in the same COA, case-insensitive | Reject after the selected COA context is available |
| MVS.022 | Value | Error | Conflicts with generated member ID `segment_sequence-value` | Reject; for sequence 2, value `2-100` is invalid |
| MVS.023 | Value | Error | Conflicts with an accounting-period member in `segment_sequence-value` format | Reject; if period `1-01` exists, value `01` under sequence 1 conflicts |

## Reserved Lexicons

Match reserved words case-insensitively at token boundaries. For a reserved
entry whose first and last characters are alphanumeric, a boundary is any
character other than `A-Z`, `0-9`, or `_`. For symbolic entries such as
`#MISSING`, match the literal text.

Essbase reserved words:

```text
DEFAULT ALL AND ASSIGN AVERAGE CALC CALCMBR COPYFORWARD CROSSDIM CURMBRNAME
DIM DIMNAME DIV DYNAMIC EMPTYPARM EQ EQOP EXCEPT EXP EXPERROR FLOAT FUNCTION
GE GEN GENRANGE GROUP GT ID IDERROR INTEGER LE LEVELRANGE LOOPBLOCK LOOPPARMS
LT MBR MBRNAME MBRONLY MINUS MISSING #MISSING MUL MULOP NE NON NONINPUT NOT OR
PAREN PARENPARM PERCENT PLUS RELOP SET SKIPBOTH SKIPMISSING SKIPNONE SKIPZERO
TO TOLOCALRATE TRAILMISSING TRAILSUM UMINUS UPPER VARORXMBR XMRONLY XMBRONLY
$$$UNIVERSE$$$ #MI
```

GL reserved words and currency/period keywords:

```text
ACTUAL ADP AED AFA AFN ALLOCATED AMD ANG AOA AOK AON ARA ARS ATS AUD AWG AZM
AZN BAM BASE BBD BDT BEF BEGINNINGBALANCECR BEGINNINGBALANCEDR BGL BGN BHD BIF
BMD BND BOB BOV BRC BRL BSD BTN BUK BWP BYB BYN BYR BZD CAD CD CDF CHE CHF CHW
CLF CLP CNY CONVERTED COP COU CRC CSD CSK CUP CVE CYP CZK DAY DEM DJF DKK DOP
DZD ECS ECV EEK EGP ENDINGBALANCECR ENDINGBALANCEDR ENTERED EOD ERN ESB ESP
ETB EUR FIM FJD FKP FRF GBP GEK GEL GHC GHS GIP GMD GNF GRD GTQ GWP GYD
HISTORY HKD HNL HRD HRK HTG HUF IDR IEP ILS INR IQD IRR ISK ITL JMD JOD JPY
KES KGS KHR KMF KPW KRW KWD KYD KZT LAK LBP LKR LRD LSL LTL LUC LUF LUL LVL
LVR LYD MAD MDL MGA MGF MKD MMK MNT MONTH MOP MRO MRU MS25 MS26 MTL MUR MVR
MWK MXN MXP MXV MYR MZM MZN NAD NGN NIC NIO NLG NOK NPR NZD OMR PAB PATD PEI
PEN PERIOD PERIODACTIVITYCR PERIODACTIVITYDR PGK PHP PKR PLN PLZ PTA PTD PTE PYG
QAR QATD QTD QUARTER RMB ROL RON RSD RUB RUR RWF SAR SBD SCR SDD SDG SDP SEASON
SEK SGD SHP SIT SKK SLL SOS SRD SRG SSP STAT STD STN SUR SVC SYP SZL THB TJR
TJS TMM TMT TND TOP TOTAL TOTALFORALLOCATIONS TPE TRL TRY TTD TWD TZS UAH UAK
UF UGS UGX UKS USD USN USS UYI UYP UYU UYW UZS VEB VEF VES VND VUV WEEK WST
XAF XAG XAU XB5 XBA XBB XBC XBD XCD XDR XEU XFO XFU XGL1 XOF XPD XPF XPO
XPT XTS XXX YATD YDD YEAR YER YTD YUD YUM YUN ZAL ZAR ZBIQA_C1 ZBIQA_C2
ZBIQA_C3 ZBIQA_C4 ZMK ZMW ZRN ZRZ ZWD ZWL ZWR DAILY ACTIVITY N/A
```

`DAILY ACTIVITY` is one multiword token and `N/A` is one literal token.

## Description Rules

Always reject a blank Description, a Description longer than 240 characters, or
one containing `"`.
When `GL_DISPLAY_SEGMENT_VALUE` is `Y` or `YES`, also:

- Reject any Essbase reserved word from the lexicon above.
- Reject a Description starting with `(`, `)`, `\`, `*`, `|`, `@`, `=`, `_`,
  `<`, `+`, `,`, `.`, `{`, `}`, `-`, `"`, or `'`.

If the `GL_DISPLAY_SEGMENT_VALUE` state isn't available through the fresh UI
context, disclose that the FBDI process remains the server-side authority for
the conditional Description rules; do not call a profile REST resource.

## Complete-Batch Gate

Do not generate or submit a ZIP while any row is invalid. Save the prepared
candidate only when every row passes. Preserve every reported source row so the
user can correct the input without remapping it.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MVS.VALIDATE_BASE | step | 1 | validate_input | valid->MVS.RESOLVE_VALUE_SET;invalid->MVS.FAILED | none | stop | Create/update candidate supplied |
| MVS.VALIDATE_CLASSIFIED | step | 4 | validate_input | valid->MVS.READY_FOR_DATA_LOADER;invalid->MVS.FAILED | MVS.CLASSIFY | stop | Segment-usage classification completed |
