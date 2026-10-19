# Benefit Provider Design Enforcement

Require `Organization`, Organization and OrgUnitClassification rows, matching LOV-derived classification names, blank ClassificationCode, valid location mapping, and Status `A` when omitted. Exclude `OrgInformation`. Stop before immutable archive preparation on any failed gate.
