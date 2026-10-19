"""Strict, side-effect-free CPQ approval intent extraction.

The caller must supply registration obtained through authenticated metadata
discovery, never registration copied from an editable approval envelope. This
module extracts intent; it does not grant approval or authorize an upload.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import stat
import unicodedata
import zipfile
from dataclasses import dataclass, field
from typing import Any, Mapping


INITIALIZE = "cpqSetupAssistantInitialize"
ASSISTANT = "setupAssistants"
COMPANY = "CompanyProfiles"
ADMIN = "CPQUsers"
CPQ_ROOTS = frozenset({INITIALIZE, ASSISTANT})
CPQ_SECTIONS = frozenset({INITIALIZE, ASSISTANT, COMPANY, ADMIN})
# Retired registrations must not quietly fall back to generic authorization.
CPQ_LEGACY_ROOTS = frozenset({
    "cpqSetupAssistantSubmit", "cpqSetupAssistantAdministrator", "cpqCompanyProfile",
})
MAX_ARCHIVE_BYTES = 16 * 1024 * 1024
MAX_MEMBERS = 32
MAX_OPERATIONS = 10000
_ATTRIBUTE = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
_SOURCE_REFERENCE = re.compile(r"SourceRef(?:TableName|[0-9]{3})\Z")
_COMMENT = re.compile(
    r"COMMENT Data for Business Object: ([A-Za-z][A-Za-z0-9_]*)"
    r" Version: V[0-9]+ Created on: [0-9-]+\Z"
)


class ContractError(ValueError):
    """An unsupported or ambiguous CPQ source; messages contain no row values."""


def canonical_bytes(value: Any) -> bytes:
    """The version-1 manifest serialization (reject non-JSON and nonfinite data)."""
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


@dataclass(frozen=True)
class Registration:
    """Immutable projection of an authenticated live business-object schema."""

    root: str
    sections: tuple[tuple[str, tuple[str, ...]], ...]
    fingerprint: str

    @classmethod
    def from_schema(cls, schema: Any) -> Registration:
        sections = tuple(
            (section.discriminator, tuple(section.attribute_names))
            for section in schema.sections
        )
        # Bind more than header names: component and attribute metadata can
        # affect routing, identity fields, mandatory values, and derivation.
        material = {
            "businessObjectId": schema.business_object_id,
            "root": schema.discriminator,
            "sections": sections,
            "components": schema.components,
            "attributes": schema.attributes,
            "schemaSource": schema.schema_source,
            "ucmContentId": schema.ucm_content_id,
        }
        return cls(schema.discriminator, sections, digest(material))


@dataclass(frozen=True)
class Operation:
    member: str
    line: int
    section: str
    # Exclude raw business values from incidental repr/debug output.
    fields: tuple[tuple[str, str], ...] = field(repr=False)

    def as_manifest(self) -> dict[str, Any]:
        return {
            "member": self.member, "line": self.line, "directive": "MERGE",
            "section": self.section, "fields": [list(pair) for pair in self.fields],
        }


@dataclass(frozen=True)
class ParsedArchive:
    stage: str
    artifact_sha256: str
    registration_fingerprints: tuple[str, ...]
    operations: tuple[Operation, ...] = field(repr=False)

    def as_manifest(self) -> dict[str, Any]:
        return {
            "schemaVersion": "cpq-dat-intent-v1",
            "stage": self.stage,
            "artifactSha256": self.artifact_sha256,
            "registrationFingerprints": list(self.registration_fingerprints),
            "operations": [operation.as_manifest() for operation in self.operations],
        }


def archive_members(content: bytes) -> tuple[tuple[str, bytes], ...]:
    """Read every member in archive order without extracting to the filesystem."""
    if not content or len(content) > MAX_ARCHIVE_BYTES:
        raise ContractError("CPQ archive is empty or exceeds the size limit.")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            infos = archive.infolist()
            if not infos or len(infos) > MAX_MEMBERS:
                raise ContractError("CPQ archive has an unsupported member count.")
            if sum(info.file_size for info in infos) > MAX_ARCHIVE_BYTES:
                raise ContractError("CPQ archive exceeds the expanded size limit.")
            names: set[str] = set()
            result: list[tuple[str, bytes]] = []
            for info in infos:
                name = info.filename
                # No ignored files: nested members, directories, hidden metadata,
                # encrypted entries and links must not alter loader interpretation.
                if (
                    not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*\.dat", name)
                    or name != info.orig_filename
                    or name.casefold() in names
                    or info.flag_bits & 1
                    or stat.S_IFMT(info.external_attr >> 16) not in (0, stat.S_IFREG)
                ):
                    raise ContractError("CPQ archive contains an unsupported or duplicate member.")
                names.add(name.casefold())
                result.append((name, archive.read(info)))
            return tuple(result)
    except (zipfile.BadZipFile, NotImplementedError, RuntimeError, OSError) as error:
        raise ContractError("CPQ archive cannot be read safely.") from error


def _attribute(raw: str) -> str:
    name, separator, _label = raw.partition("=")
    if not _ATTRIBUTE.fullmatch(name):
        raise ContractError("CPQ metadata contains an invalid attribute name.")
    if separator and not _SOURCE_REFERENCE.fullmatch(name):
        raise ContractError("CPQ metadata contains an unsupported attribute mapping.")
    return name


def _lines(content: bytes) -> list[str]:
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ContractError("CPQ DAT members must be UTF-8.") from error
    text = text.replace("\r\n", "\n")
    if any(
        character != "\n" and unicodedata.category(character) in {"Cc", "Cf", "Zl", "Zp"}
        for character in text
    ):
        raise ContractError("CPQ DAT members contain unsupported control characters.")
    return text.split("\n")


def _parse_member(
    name: str, content: bytes, registration: Registration,
) -> tuple[Operation, ...]:
    if registration.root not in CPQ_ROOTS:
        raise ContractError("Mixed or unsupported business objects in a CPQ archive.")
    allowed_sections = dict(registration.sections)
    if len(allowed_sections) != len(registration.sections):
        raise ContractError("CPQ registration has duplicate sections.")
    headers: dict[str, tuple[str, ...]] = {}
    operations: list[Operation] = []
    for line_number, line in enumerate(_lines(content), start=1):
        if not line:
            continue
        comment = _COMMENT.fullmatch(line)
        if comment:
            if comment.group(1) != registration.root:
                raise ContractError("CPQ template comment does not match its registration.")
            continue
        parts = line.split("|")
        if len(parts) < 3 or parts[0] not in {"METADATA", "MERGE"}:
            raise ContractError("CPQ DAT contains an unsupported or malformed directive.")
        directive, section = parts[:2]
        if section not in CPQ_SECTIONS or section not in allowed_sections:
            raise ContractError("CPQ DAT section is outside the registered stage contract.")
        if directive == "METADATA":
            attributes = tuple(_attribute(raw) for raw in parts[2:])
            if (
                section in headers or len(set(attributes)) != len(attributes)
                or not set(attributes).issubset(allowed_sections[section])
            ):
                raise ContractError("CPQ DAT has duplicate or unregistered metadata.")
            headers[section] = attributes
            continue
        header = headers.get(section)
        if header is None or len(parts[2:]) != len(header):
            raise ContractError("CPQ DAT row has no header or an inconsistent column count.")
        operations.append(Operation(name, line_number, section, tuple(zip(header, parts[2:]))))
        if len(operations) > MAX_OPERATIONS:
            raise ContractError("CPQ DAT exceeds the operation limit.")
    if not operations:
        raise ContractError("CPQ DAT must contain at least one operation.")
    if registration.root == INITIALIZE and set(headers) != {INITIALIZE}:
        raise ContractError("Initialization cannot contain another CPQ section.")
    if registration.root == ASSISTANT and INITIALIZE in headers:
        raise ContractError("Child or submission sources cannot contain initialization.")
    return tuple(operations)


def _stage(operation: Operation) -> str:
    values = dict(operation.fields)
    section = operation.section
    expected_action = "POST" if section in {INITIALIZE, ADMIN} else "PATCH"
    if values.get("RestAction") != expected_action:
        raise ContractError("CPQ operation requires its exact registered REST action.")
    if section == INITIALIZE:
        permitted = {"InitializationRequestId", "Content-Type", "REST-Framework-Version", "RestAction"}
        if any(value and key not in permitted for key, value in operation.fields):
            raise ContractError("Initialization contains an unsupported business value.")
        # Some published registrations have no correlation attribute. Others
        # expose transport columns as optional. Do not invent any of these from
        # the client's HTTP defaults; live metadata determines required columns.
        if values.get("Content-Type") not in (None, "", "application/vnd.oracle.adf.action+json"):
            raise ContractError("Initialization contains an unsupported content type.")
        if values.get("REST-Framework-Version") not in (None, "", "9"):
            raise ContractError("Initialization contains an unsupported REST framework version.")
        return "initialize"
    # Supported pillar transport contract; live registration must independently
    # expose each supplied column. Never populate absent columns/defaults.
    if values.get("Content-Type") not in (None, "", "application/json", "application/vnd.oracle.adf.resource+json"):
        raise ContractError("CPQ row contains an unsupported content type.")
    if values.get("REST-Framework-Version") not in (None, "", "9"):
        raise ContractError("CPQ row contains an unsupported REST framework version.")
    if section == ASSISTANT:
        if not values.get("Status"):
            if any(value and key not in {"Name", "RestAction", "Content-Type", "REST-Framework-Version"}
                   for key, value in operation.fields):
                raise ContractError("Child-import parent must be routing-only.")
            return "children"
        if values.get("Status") != "SUBMITTED":
            raise ContractError("Parent mutations may only submit the Setup Assistant.")
        if any(value and key not in {"Name", "Status", "RestAction", "Content-Type", "REST-Framework-Version"} for key, value in operation.fields):
            raise ContractError("Final submission contains an extra business change.")
        return "submit"
    if section == ADMIN:
        if any(not values.get(key, "").strip() for key in ("FirstName", "LastName", "Email")):
            raise ContractError("Each new CPQ administrator requires first name, last name and email.")
        if any(values.get(key) for key in ("CPQUserId", "Id", "PartyNumber", "UserName")):
            raise ContractError("New CPQ administrators must not supply generated identities.")
    elif section == COMPANY:
        if values.get("IsDataExisting"):
            raise ContractError("Company discovery-only state must not be supplied for mutation.")
        # The state verifier separately binds the registered identity/routing
        # fields to the discovered company; do not invent an identifier here.
        routing = {"CompanyProfileId", "CustomId", "Id", "Name", "RestAction", "Content-Type", "REST-Framework-Version"}
        if not any(value and key not in routing and not _SOURCE_REFERENCE.fullmatch(key)
                   for key, value in operation.fields):
            raise ContractError("A Company Profile update requires a business change.")
    return "children"


def parse_archive(content: bytes, registrations: Mapping[str, Registration]) -> ParsedArchive:
    """Extract every operation and require exactly one supported mutation stage.

    ``registrations`` maps every exact member name to its independently resolved
    live schema. Filename, comment, and editable preflight claims are not a
    replacement for authoritative registration resolution.
    """
    members = archive_members(content)
    if set(registrations) != {name for name, _ in members}:
        raise ContractError("Every CPQ archive member requires an authoritative registration.")
    operations: list[Operation] = []
    fingerprints: list[str] = []
    for name, payload in members:
        registration = registrations[name]
        fingerprints.append(registration.fingerprint)
        operations.extend(_parse_member(name, payload, registration))
        if len(operations) > MAX_OPERATIONS:
            raise ContractError("CPQ archive exceeds the operation limit.")
    stages = {_stage(operation) for operation in operations}
    if len(stages) != 1:
        raise ContractError("An archive cannot combine CPQ mutation stages.")
    stage = stages.pop()
    if stage != "children" and len(operations) != 1:
        raise ContractError("Initialization and final submission require exactly one operation.")
    if stage == "children" and not any(op.section in {COMPANY, ADMIN} for op in operations):
        raise ContractError("Child import must contain child operations.")
    administrators = [dict(op.fields)["Email"].casefold() for op in operations if op.section == ADMIN]
    if len(set(administrators)) != len(administrators):
        raise ContractError("A child import must not contain duplicate administrators.")
    if sum(op.section == COMPANY for op in operations) > 1:
        raise ContractError("A child import may update only the discovered Company Profile once.")
    return ParsedArchive(stage, hashlib.sha256(content).hexdigest(), tuple(fingerprints), tuple(operations))
