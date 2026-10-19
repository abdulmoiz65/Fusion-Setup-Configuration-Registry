# Markdown-guided profile preparation

## Scope and execution

This is the initial profile-only route: Participant Eligibility with Person Type
and Department criteria. Other criteria and all populated supporting tabs are
not yet validated for this route; stop and identify the unsupported content.
Never discard rows or supporting tabs without an explicit user scope instruction.
This is not full parity with the former adapter. Supporting-object and evaluation
coverage remain migration work. No new runtime Python file is installed.

The recipe below is executable Python in Markdown, run transiently by the agent.
It is not a no-code workflow. Tests execute this same recipe; do not substitute
untested generated code, monkey-patch parent modules, or rewrite the source
workbook to ANE. It uses existing parent APIs without modifying their source.

Load the unchanged parent `scripts/eligibility.py` via importlib; bind its
`excel_to_plan_copy_xml` namespace as `xml`. Read the explicit user workbook
with `xml.workbook_io._read_workbook`. Require exactly one visible sheet named
Participant Eligibility. Check all other sheets for setup data using the parent
sheet parsers; absent/blank tabs are valid. Select only the authorized scope.
Pass the selected sheet's rows to `validate_rows` below.

Load the parent Oracle template using `xml.load_template` with its logical
`assets/plan-copy/BEN_ELIGY_PRFL.xml` path. For actual preparation use the
parent `FusionLookupResolver` configured for the selected target; no mock or
saved cross-environment values are allowed. Follow the parent's exact-match,
EMP-only person type, date-effective department and ambiguity policies.

<!-- executable-profile-recipe -->
```python
import copy
import re
import xml.etree.ElementTree as ET

DUPLICATE = "The eligibility profile name you entered is already in use. The name must be unique within the enterprise"

def validate_rows(xml, rows):
    header, cols = xml._find_header(rows)
    seen = set()
    current = None
    required = {"profile_type": {"participant", "prtp"},
                "profile_usage": {"opportunity marketplace", "ora opp market place"},
                "assignment_to_use": {"specific assignment", "aps"}}
    for number, row in enumerate(rows[header + 1:], header + 2):
        if not any(str(v).strip() for v in row):
            continue
        name = xml._cell(row, cols["profile_name"]).strip()
        if name:
            if name.casefold() in seen:
                raise ValueError(DUPLICATE)
            seen.add(name.casefold())
            current = name
        if current is None:
            raise ValueError(f"Row {number}: criterion before profile")
        for field, allowed in required.items():
            value = xml._cell(row, cols[field])
            if (name or value.strip()) and xml._normalized(value) not in allowed:
                raise ValueError(f"Row {number}: invalid {field}: {value!r}")
    profiles = xml.parse_profiles(rows)
    if not profiles:
        raise ValueError("Participant Eligibility must contain a profile")
    for profile in profiles:
        xml._mapped_profile_value("status", profile.status)
    return profiles

def render_profiles(xml, template, profiles, resolver):
    # This initial route deliberately covers Person Type and Department only.
    # Broader criteria/supporting objects must follow a separately validated expansion.
    mappings = xml.load_lookup_mappings()
    source = xml._direct_child(template, "EligibilityProfileVORow")
    output = copy.deepcopy(template)
    for child in list(output):
        if xml._local_name(child.tag) == "EligibilityProfileVORow":
            output.remove(child)
    for profile in profiles:
        if xml._normalized(profile.assignment_to_use) not in {"aps", "specific assignment"}:
            raise ValueError("Specific assignment required")
        if xml._normalized(profile.profile_type) not in {"prtp", "participant"}:
            raise ValueError("Participant required")
        if xml._normalized(profile.profile_usage) not in {"ora opp market place", "opportunity marketplace"}:
            raise ValueError("Opportunity Marketplace required")
        row = copy.deepcopy(source)
        for child in list(row):
            if xml._is_criterion_container(child):
                row.remove(child)
            elif re.fullmatch(r"Elig.*Flag", xml._local_name(child.tag)):
                child.attrib.pop("null", None)
                child.text = "N"
        fields = {"ViewInstanceName":"EligibilityProfile", "GroupingKey":profile.name,
                  "Name":profile.name, "EligibilityProfileName":profile.name,
                  "Description":profile.description, "StatCd":xml._mapped_profile_value("status", profile.status),
                  "ProfileType":"PRTP", "BnftCagrPrtnCd":"ORA_OPP_MARKET_PLACE", "AsmtToUseCd":"APS"}
        for key, value in fields.items():
            xml._set_element(row, key, value)
        containers = {}
        for criterion in profile.criteria:
            key = xml._normalized(criterion.kind)
            if key not in {"person type", "department"}:
                raise ValueError(f"Criterion not yet validated for Markdown route: {criterion.kind}")
            spec = xml.CRITERION_SPECS[key]
            values = xml._criterion_xml_values(criterion, lookup_mappings=mappings,
                      lookup_resolver=resolver, package_reference_names={})
            original = xml._direct_child(source, spec.container)
            if key not in containers:
                container = copy.deepcopy(original)
                for child in list(container):
                    if xml._local_name(child.tag) == spec.row:
                        container.remove(child)
                containers[key] = container
                row.append(container)
            child = copy.deepcopy(xml._matching_template_row(original, spec.row, values))
            for field, value in values.items():
                xml._set_element(child, field, value)
            parts = [profile.name] + [child.findtext(field) for field in spec.grouping_elements]
            if not all(parts):
                raise ValueError("Missing criterion grouping value")
            xml._set_element(child, "GroupingKey", ",".join(parts))
            xml._set_element(child, "EligibilityProfileName", profile.name)
            if spec.sequence_element:
                xml._set_element(child, spec.sequence_element, criterion.sequence)
            if spec.exclude_element:
                xml._set_element(child, spec.exclude_element, criterion.exclude)
            containers[key].append(child)
            xml._set_element(row, spec.flag, "Y")
        output.append(row)
    return output
```

## Mapping and package preparation

Use the unchanged parent `excel_to_plan_copy_map_xml` namespace to load the
maintained mapping contract and Oracle map template and call
`convert_plan_copy_map(template, profiles, contract, resolver)`. Use the same
validated profiles and target configuration, but create a fresh resolver instance
for mapping: profile XML resolution caches display fields, whereas mappings
require additional ID fields. Reusing that cache can omit PersonTypeId. Reject missing source/target identifiers.
Never invent IDs or reuse the example values from a prior import.

For the initial profile-only route, use empty VO roots for the eight supporting
batches: PostalZipRangeVO, ServiceAreaVO, AgeFactorVO, CompensationLevelFactorVO,
LengthOfServiceFactorVO, CombinedAgeLosFactorVO, HoursWorkedFactorVO,
FullTimeEquivalentFactorVO. Do this only after proving that supporting content
is absent or explicitly excluded by the user. Serialize with the parent renderer;
call existing `excel_to_plan_copy_package.build_eligibility_import_package`
with all ten XML byte streams and `validate_import_package` on the result.
Write a new project artifact directory; never overwrite an approved package.

Compare every profile header and criterion to the source: names, description,
status, PRTP, OM usage, APS, value, sequence, exclusion, criterion flags/counts,
null helper IDs and mappings. Preserve parent XML templates and flag contracts.
Record hashes, target, source workbook and selected scope in the run record.
Then follow `markdown-import-workflow.md`; package preparation is not approval.
