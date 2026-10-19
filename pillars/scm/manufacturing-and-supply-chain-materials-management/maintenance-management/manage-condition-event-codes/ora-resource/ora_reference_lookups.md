# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| cec_condition_event_type | Create or type change | Provided Condition Event Type Code | Match the supplied type code exactly against approved source data | Validated Condition Event Type Code | Stop when missing or ambiguous |
| cec_category | Category supplied | Provided Condition Event Category Code | Match the supplied category against lookup ORA_MNT_EVENTCODE_CATEGORY | Validated Condition Event Category Code | Stop when unsupported or ambiguous |
| cec_existing_row | Update or end-date | Provided Condition Event Code and Type Code | Match both values exactly against supplied source data | Target row identity and current values | Stop when zero or multiple rows match |
