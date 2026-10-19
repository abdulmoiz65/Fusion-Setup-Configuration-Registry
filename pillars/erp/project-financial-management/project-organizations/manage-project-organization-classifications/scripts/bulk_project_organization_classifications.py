"""Task-local bulk HDL preparation; no authentication, export, submission or approval."""
from __future__ import annotations

from datetime import datetime
import hashlib
import io
import json
from pathlib import Path
import zipfile

import validate_project_organization_classifications_hdl as single

GATES = ["data_loader_preflight", "task_hook_preview", "immutable_artifact_approval",
         "submit_once", "persist_request_id", "terminal_load_success", "post_load_rest_verification"]


def normalize_bulk_request(request):
    if (not isinstance(request, dict) or set(request) != {"target_environment", "organizations"}
            or not isinstance(request["organizations"], list) or not request["organizations"]):
        raise ValueError("Bulk request requires target_environment and a nonempty organizations array.")
    single.text(request["target_environment"], "target_environment", 2048)
    names = set()
    for row in request["organizations"]:
        if not isinstance(row, dict):
            raise ValueError("Each organization must be an object.")
        update = row.get("update_existing_pto_permissions", False)
        if type(update) is not bool:
            raise ValueError("update_existing_pto_permissions must be Boolean.")
        item = {k: v for k, v in row.items() if k != "update_existing_pto_permissions"}
        name, _, permissions, _ = single.normalize_request(item)
        if name in names:
            raise ValueError("Duplicate organization name in bulk request: " + name)
        if update and not permissions:
            raise ValueError(name + ": explicit existing PTO update requires supplied permissions.")
        names.add(name)
    return request


def plan_bulk_request(request, evidence):
    normalize_bulk_request(request)
    if (not isinstance(evidence, dict) or evidence.get("TargetEnvironment") != request["target_environment"]
            or not isinstance(evidence.get("RunId"), str) or not evidence["RunId"]
            or not isinstance(evidence.get("Organizations"), list)
            or len(evidence["Organizations"]) != len(request["organizations"])):
        raise ValueError("One ordered target-bound current-run baseline is required per organization.")
    rows, identities, refs = [], set(), set()
    for index, (row, proof) in enumerate(zip(request["organizations"], evidence["Organizations"]), 1):
        if (not isinstance(proof, dict) or proof.get("TargetEnvironment") != request["target_environment"]
                or proof.get("ValidationRunId") != evidence["RunId"]):
            raise ValueError(row["organization_name"] + ": baseline target/run binding differs.")
        try:
            collected = datetime.fromisoformat(proof["CollectedAt"])
            if collected.tzinfo is None:
                raise ValueError("Missing timezone")
        except (KeyError, TypeError, ValueError):
            raise ValueError(row["organization_name"] + ": baseline collection timestamp is required.") from None
        item = {k: v for k, v in row.items() if k != "update_existing_pto_permissions"}
        state = single.resolve_classification_state(item, proof)
        if state["organization_id"] in identities or proof["EvidenceRef"] in refs:
            raise ValueError("Duplicate selected parent or reused organization baseline in bulk request.")
        identities.add(state["organization_id"]); refs.add(proof["EvidenceRef"])
        if state["existing_targets"]["PTO"] and not row.get("update_existing_pto_permissions", False):
            # Creation permissions never implicitly update an existing PTO.
            item.pop("pto_permissions", None)
        elif row.get("update_existing_pto_permissions", False) and not state["existing_targets"]["PTO"]:
            raise ValueError(row["organization_name"] + ": existing PTO update requested but REST proves PTO absent.")
        try:
            plan = single.plan_request(item, proof)
        except ValueError as exc:
            raise ValueError(row["organization_name"] + ": " + str(exc)) from exc
        rows.append({"index": index, "request": item, "plan": plan})
    missing = any(row["plan"]["missing"] for row in rows)
    updates = any(row["plan"]["permission_changes"] for row in rows)
    return {"status": "ADD_MISSING" if missing else "UPDATE_PERMISSIONS" if updates else "ALREADY_CONFIGURED",
            "target": request["target_environment"], "run_id": evidence["RunId"], "organizations": rows}


def allocate_bulk_mappings(request, evidence):
    """Propose new keys only; the workflow must persist/register them before generation."""
    plan = plan_bulk_request(request, evidence)
    proposed, keys = [], set()
    for row in plan["organizations"]:
        item = row["plan"]
        if not item["components"]:
            continue
        ids = single.allocate_source_ids(item["components"])
        ids.update(row["request"].get("source_system_ids", {}))
        for key in ids.values():
            if key in keys:
                raise ValueError("Duplicate component source key across organizations.")
            keys.add(key)
        proposed.append({"Binding": single.mapping_binding(item), "SourceSystemIds": ids,
                         "Persisted": False})
    return proposed


def generate_bulk_dats(request, evidence):
    plan = plan_bulk_request(request, evidence)
    if plan["status"] == "ALREADY_CONFIGURED":
        return plan, {}
    new_components = any(row["plan"]["components"] for row in plan["organizations"])
    ledger = evidence.get("PersistedMappings", [])
    if new_components and (evidence.get("PersistedMappingsComplete") is not True or not isinstance(ledger, list)):
        raise ValueError("Complete persisted bulk source-key ledger is required.")
    groups = {role: {"classes": [], "infos": [], "info_header": None, "organizations": []}
              for role in ("PEO", "PTO")}
    keys = set()
    for row, raw in zip(plan["organizations"], evidence["Organizations"]):
        item = row["plan"]
        if not item["missing"] and not item["permission_changes"]:
            continue
        proof = {**raw, "PersistedMappings": ledger,
                 "PersistedMappingsComplete": evidence.get("PersistedMappingsComplete", False)}
        reference = proof.get("ParentReference")
        if not isinstance(reference, dict) or reference.get("Attribute") != "OrganizationId":
            raise ValueError(item["name"] + ": bulk rows require the REST-resolved numeric OrganizationId parent reference.")
        try:
            content = single.generate_dat(row["request"], proof)
        except ValueError as exc:
            raise ValueError(item["name"] + ": " + str(exc)) from exc
        metadata = {}
        roles = set()
        for line in content.splitlines():
            fields = line.split("|")
            op, component = fields[:2]
            if op == "METADATA":
                metadata[component] = fields[2:]
                continue
            values = dict(zip(metadata[component], fields[2:]))
            key = values["SourceSystemId"]
            if key in keys:
                raise ValueError("Duplicate source key across PEO/PTO archives: " + key)
            keys.add(key)
            role = "PEO" if values["ClassificationCode"] == single.CODES["PEO"] else "PTO"
            group = groups[role]; roles.add(role)
            if component == "OrgUnitClassification":
                group["classes"].append(line)
            elif component == "OrgInformation":
                header = metadata[component]
                if group["info_header"] not in (None, header):
                    raise ValueError("PTO permission column layouts differ. For one PTO ZIP, explicitly supply the same update fields, including all three for updates mixed with new PTOs; otherwise use compatible batches. Omitted existing values are never filled.")
                group["info_header"] = header
                group["infos"].append(line)
            else:
                raise ValueError("Bulk child generation must not mutate the Organization parent.")
        for role in roles:
            groups[role]["organizations"].append({"request_index": row["index"],
                "organization_id": item["organization_id"], "name": item["name"],
                "baseline_ref": item["classification_baseline_ref"],
                "validation_run_id": item["validation_run_id"],
                "baseline_collected_at": item["baseline_collected_at"],
                "baseline_as_of_date": item["baseline_as_of_date"],
                "missing": [role] if role in item["missing"] else [],
                "permission_changes": item["permission_changes"] if role == "PTO" else {}})
    outputs = {}
    for role, group in groups.items():
        if not group["classes"] and not group["infos"]:
            continue
        lines = ["|".join(["METADATA", "Organization", *single.ROOT])]
        if group["classes"]:
            lines += ["|".join(["METADATA", "OrgUnitClassification",
                               *single.headers("OrganizationId")["OrgUnitClassification"]]), *group["classes"]]
        if group["infos"]:
            lines += ["|".join(["METADATA", "OrgInformation", *group["info_header"]]), *group["infos"]]
        content = "\n".join(lines) + "\n"
        errors = validate_bulk_text(content, role)
        if errors:
            raise ValueError("; ".join(errors))
        outputs[role] = {"content": content, "organizations": group["organizations"],
                         "classification_rows": len(group["classes"]), "information_rows": len(group["infos"])}
    return plan, outputs


def validate_bulk_text(content, role):
    """Structural check only; regenerate and compare to governed per-parent evidence."""
    if role not in {"PEO", "PTO"}:
        return ["Bulk archive role must be PEO or PTO."]
    metadata, rows, errors = {}, {}, []
    for number, line in enumerate(content.splitlines(), 1):
        if not line.strip():
            continue
        fields = line.split("|")
        if len(fields) < 3 or fields[0] not in {"METADATA", "MERGE"}:
            errors.append(f"Line {number}: unsupported instruction."); continue
        op, component, values = fields[0], fields[1], fields[2:]
        if component not in single.headers("OrganizationId"):
            errors.append("Unsupported component."); continue
        if op == "METADATA":
            if component in metadata:
                errors.append("Duplicate component metadata.")
            metadata[component] = values
        elif component not in metadata or len(values) != len(metadata[component]):
            errors.append("Row/header mismatch.")
        else:
            rows.setdefault(component, []).append(dict(zip(metadata[component], values)))
    expected = single.headers("OrganizationId")
    classes, infos = rows.get("OrgUnitClassification", []), rows.get("OrgInformation", [])
    wanted = {"Organization"} | ({"OrgUnitClassification"} if classes else set()) | ({"OrgInformation"} if infos else set())
    if rows.get("Organization") or set(metadata) != wanted or not (classes or infos):
        errors.append("Bulk file needs child rows and metadata-only parent anchor.")
    for component in wanted - {"OrgInformation"}:
        if metadata.get(component) != expected[component]:
            errors.append("Unsupported bulk header.")
    info_header = metadata.get("OrgInformation", [])
    prefix = expected["OrgInformation"][:-len(single.SEGMENTS)]
    segments = [s for s in single.SEGMENTS if s in info_header]
    if infos and (not segments or info_header != prefix + segments
                  or (classes and info_header != expected["OrgInformation"])):
        errors.append("PTO columns must be full for new PTOs or consistent supplied columns for updates.")
    if role == "PEO" and (infos or not classes):
        errors.append("PEO ZIP must contain only PEO classification rows.")
    if role == "PTO" and not infos:
        errors.append("PTO ZIP requires information rows.")
    if errors:
        return errors
    keys, class_parents, info_parents, bindings = set(), set(), set(), {}
    for component, records in (("OrgUnitClassification", classes), ("OrgInformation", infos)):
        for row in records:
            try:
                for key, value in row.items(): single.text(value, key, 2048)
                single.dates(row)
                parent = single.identity(row["OrganizationId"])
                binding = (row["SourceSystemOwner"], row["EffectiveStartDate"], row["EffectiveEndDate"])
                if parent in bindings and bindings[parent] != binding:
                    raise ValueError("Conflicting owner/date binding for one parent.")
                bindings[parent] = binding
                if row["SourceSystemId"] in keys:
                    raise ValueError("Duplicate component source key.")
                keys.add(row["SourceSystemId"])
                parents = class_parents if component == "OrgUnitClassification" else info_parents
                if parent in parents:
                    raise ValueError("Duplicate classification/information row for a parent.")
                parents.add(parent)
                if component == "OrgUnitClassification":
                    category = "PA_PROJECT_ORG" if role == "PTO" else "NO_EFF_CATEGORY"
                    if row["ClassificationCode"] != single.CODES[role] or row["CategoryCode"] != category or row["Status"] != "A":
                        raise ValueError("Wrong classification role/category/status.")
                else:
                    fixed = {"ClassificationCode": "PA_PROJECT_ORG", "SequenceNumber": "1",
                        "FLEX:PER_ORGANIZATION_INFORMATION_EFF": single.CONTEXT,
                        "EFF_CATEGORY_CODE": "PA_PROJECT_ORG", "OrgInformationContext": single.CONTEXT}
                    if any(row[k] != v for k, v in fixed.items()) or any(row[k] not in {"Y", "N"} for k in segments):
                        raise ValueError("Invalid PTO context or permissions.")
            except (ValueError, KeyError) as exc:
                errors.append(str(exc))
    if role == "PTO" and not class_parents <= info_parents:
        errors.append("Every new PTO classification needs one matching information row.")
    return errors


def write_bulk_archives(outputs, plan, output_dir, project_root):
    """Create up to two checksum-bound ZIPs, refusing overwrite; never submit."""
    if not outputs:
        return []
    project = Path(project_root).resolve(strict=True)
    folder = Path(output_dir)
    if not folder.is_dir() or any(p.is_symlink() for p in (folder, *folder.parents)):
        raise ValueError("Use an existing nonsymlink task artifact directory.")
    relative = folder.resolve().relative_to(project)
    if not relative.parts or relative.parts[0] != "artifacts":
        raise ValueError("Bulk outputs must be under the selected project's artifacts directory.")
    prepared, manifest = {}, []
    for role, item in outputs.items():
        errors = validate_bulk_text(item["content"], role)
        if errors:
            raise ValueError("; ".join(errors))
        path = folder / (role + "-Organization.zip")
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as package:
            member = zipfile.ZipInfo(single.MEMBER, (1980, 1, 1, 0, 0, 0))
            package.writestr(member, item["content"].encode())
        data = stream.getvalue(); prepared[path] = data
        manifest.append({"role": role, "archive": str(path.resolve().relative_to(project)),
            "sha256": hashlib.sha256(data).hexdigest(), "target": plan["target"],
            "task_code": single.TASK_CODE, "run_id": plan["run_id"],
            "organizations": item["organizations"], "classification_rows": item["classification_rows"],
            "information_rows": item["information_rows"], "required_gates": list(GATES)})
    prepared[folder / "bulk-classification-manifest.json"] = json.dumps(manifest, indent=2).encode()
    if any(p.exists() for p in prepared):
        raise ValueError("Bulk archive or manifest already exists; no overwrite is permitted.")
    created = []
    try:
        for path, data in prepared.items():
            with path.open("xb") as output:
                created.append(path); output.write(data)
    except OSError:
        for path in created: path.unlink()
        raise
    return manifest
