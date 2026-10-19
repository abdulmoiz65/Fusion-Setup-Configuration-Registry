#!/usr/bin/env python3
"""Benefits eligibility workflow. Default: preview; --approve-upload: approved import.
Subcommands: generate, import, evaluate, convert-profiles, convert-map,
convert-factors, legacy-package.

All Benefits conversion and import components are maintained in this file.
Named source sections run in isolated namespaces to preserve their distinct
constants, dataclasses, and shared callers without duplicate module files.
Only repository core services, reference catalogs, and assets remain external.
"""
import argparse
from dataclasses import dataclass
import functools
import hashlib
import http.client
import json
from pathlib import Path
import re
import ssl
import sys
import time
from types import ModuleType
from typing import Any, Callable
import urllib.error
import urllib.request

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPOSITORY_ROOT = SKILL_ROOT.parents[4]

def _component(name, source):
    module = ModuleType(name)
    module.__file__ = __file__
    sys.modules[name] = module
    exec(compile(source, __file__ + ":" + name, "exec"), module.__dict__)
    return module

# ---- shared core REST client ----
REST_CLIENT_SCRIPTS = REPOSITORY_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts"
if str(REST_CLIENT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(REST_CLIENT_SCRIPTS))

import rest_client_common as rest_client_compat  # noqa: E402


# Keep this task runnable against the REST client currently present on each
# supported branch. Newer branches provide these transport conveniences in
# core; older branches receive the same interface here without changing core.
if not hasattr(rest_client_compat, "RestResponse"):
    @dataclass(frozen=True)
    class _RestResponse:
        status: int
        headers: dict[str, str]
        body: Any


    @dataclass(frozen=True)
    class _PollOutcome:
        value: Any
        state: str
        elapsed_seconds: int


    def _poll_until(
        fetch: Callable[[], Any],
        classify: Callable[[Any], str],
        *,
        wait_seconds: int,
        poll_interval: int,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
        on_observation: Callable[[Any, int], None] | None = None,
    ) -> _PollOutcome:
        started = clock()
        while True:
            value = fetch()
            elapsed = max(0, int(clock() - started))
            if on_observation is not None:
                on_observation(value, elapsed)
            state = classify(value)
            if state not in {"continue", "success", "failure"}:
                raise ValueError(f"Unsupported poll classification: {state}")
            if state != "continue":
                return _PollOutcome(value=value, state=state, elapsed_seconds=elapsed)
            if elapsed >= wait_seconds:
                return _PollOutcome(value=value, state="timeout", elapsed_seconds=elapsed)
            sleep(poll_interval)


    def _normalize_tls_cert_sha256(value: str) -> str:
        normalized = value.strip().replace(":", "").lower()
        if not re.fullmatch(r"[0-9a-f]{64}", normalized):
            raise ValueError(
                "TLS certificate SHA-256 fingerprint must contain 64 hexadecimal digits."
            )
        return normalized


    class _PinnedHTTPSConnection(http.client.HTTPSConnection):
        def __init__(self, host: str, *, tls_cert_sha256: str, **kwargs: Any) -> None:
            kwargs["context"] = ssl._create_unverified_context()
            super().__init__(host, **kwargs)
            self._tls_cert_sha256 = tls_cert_sha256

        def connect(self) -> None:
            super().connect()
            assert self.sock is not None
            actual = hashlib.sha256(self.sock.getpeercert(binary_form=True)).hexdigest()
            if actual != self._tls_cert_sha256:
                self.close()
                raise ssl.SSLCertVerificationError(
                    "Fusion TLS certificate does not match the approved SHA-256 fingerprint."
                )


    class _PinnedHTTPSHandler(urllib.request.HTTPSHandler):
        def __init__(self, tls_cert_sha256: str) -> None:
            super().__init__()
            self._tls_cert_sha256 = tls_cert_sha256

        def https_open(self, request: urllib.request.Request) -> Any:
            connection = functools.partial(
                _PinnedHTTPSConnection,
                tls_cert_sha256=self._tls_cert_sha256,
            )
            return self.do_open(connection, request)


    class _FusionRestSession:
        def __init__(
            self,
            props: dict[str, str],
            args: argparse.Namespace,
            *,
            default_headers: dict[str, str] | None = None,
        ) -> None:
            self.props = props
            self.args = args
            self.default_headers = dict(default_headers or {})
            self.access_token = rest_client_compat.get_token(props, args)

        def request(
            self,
            method: str,
            path: str,
            *,
            json_body: dict[str, Any] | None = None,
            raw_body: bytes | None = None,
            content_type: str | None = None,
            expected: set[int],
            retry_auth: bool = True,
            parse_json: bool = True,
            accept: str = "application/json",
        ) -> _RestResponse:
            if json_body is not None and raw_body is not None:
                raise ValueError("Provide JSON or raw request content, not both.")
            url = rest_client_compat.build_url(self.props, path, {})
            headers = dict(self.default_headers)
            headers["Accept"] = accept
            headers["Authorization"] = f"Bearer {self.access_token}"
            body = raw_body
            if json_body is not None:
                body = json.dumps(json_body).encode("utf-8")
            if content_type:
                headers["Content-Type"] = content_type
            request = urllib.request.Request(url, data=body, headers=headers, method=method)
            try:
                tls_pin = getattr(self.args, "tls_cert_sha256", None)
                if tls_pin is None:
                    response_context = rest_client_compat.authorized_urlopen(
                        self.props, request, timeout=getattr(self.args, "timeout", 60), access_token=self.access_token
                    )
                else:
                    parsed = urllib.parse.urlparse(url)
                    if parsed.scheme != "https":
                        raise ValueError("TLS certificate pinning requires an https:// request.")
                    normalized_pin = _normalize_tls_cert_sha256(tls_pin)
                    response_context = rest_client_compat.authorized_urlopen(
                        self.props, request, timeout=getattr(self.args, "timeout", 60),
                        access_token=self.access_token, handlers=(_PinnedHTTPSHandler(normalized_pin),)
                    )
                with response_context as response:
                    contents = response.read()
                    response_headers = dict(response.headers.items())
                    status = response.status
            except urllib.error.HTTPError as exc:
                contents = exc.read()
                if (
                    retry_auth
                    and method == "GET"
                    and exc.code in {401, 403}
                    and not getattr(self.args, "access_token", None)
                ):
                    self.access_token = rest_client_compat.get_token(
                        self.props, self.args, force_login=True
                    )
                    return self.request(
                        method,
                        path,
                        json_body=json_body,
                        raw_body=raw_body,
                        content_type=content_type,
                        expected=expected,
                        retry_auth=False,
                        parse_json=parse_json,
                        accept=accept,
                    )
                raise rest_client_compat.FusionHttpError(
                    exc.code, url, contents.decode("utf-8", errors="replace")
                ) from exc
            except urllib.error.URLError as exc:
                raise RuntimeError(f"Failed calling {url}: {exc.reason}") from exc

            if status not in expected:
                raise rest_client_compat.FusionHttpError(
                    status, url, f"Unexpected HTTP status {status}"
                )
            if not parse_json:
                parsed_body: Any = contents
            elif not contents.strip():
                parsed_body = {}
            else:
                try:
                    parsed_body = json.loads(contents.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise RuntimeError(
                        f"Fusion returned a non-JSON response from {url}"
                    ) from exc
            return _RestResponse(status=status, headers=response_headers, body=parsed_body)


    rest_client_compat.RestResponse = _RestResponse
    rest_client_compat.PollOutcome = _PollOutcome
    rest_client_compat.poll_until = _poll_until
    rest_client_compat.normalize_tls_cert_sha256 = _normalize_tls_cert_sha256
    rest_client_compat.FusionRestSession = _FusionRestSession

# Embedded component modules historically import this compatibility name.
sys.modules["rest_client_compat"] = rest_client_compat

# ---- excel_to_plan_copy_xml ----
excel_to_plan_copy_xml = _component("excel_to_plan_copy_xml", r'''
#!/usr/bin/env python3
"""Convert an eligibility-profile workbook into Oracle Plan Copy sample XML."""

from __future__ import annotations

import argparse
from collections import OrderedDict
import copy
from dataclasses import dataclass, field
from datetime import date
import io
import json
import os
from pathlib import Path
import re
import sys
import tempfile
from typing import Any, Callable, Iterable, Protocol
import xml.etree.ElementTree as ET
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[6]
LIB_DIR = Path(__file__).resolve().parent
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))
DATA_LOADER_SCRIPTS = REPO_ROOT / "core" / "data-loader" / "scripts"
if str(DATA_LOADER_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(DATA_LOADER_SCRIPTS))

REST_CLIENT_SCRIPTS = REPO_ROOT / "core" / "fusion-api" / "rest-api-client" / "scripts"
if str(REST_CLIENT_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(REST_CLIENT_SCRIPTS))

import xlsx_sample_workbook as workbook_io  # noqa: E402
import rest_client_compat as rest_client_common  # noqa: E402


MAX_TEMPLATE_BYTES = 20 * 1024 * 1024
MAX_ARCHIVE_ENTRIES = 5_000
MAX_ARCHIVE_EXPANDED_BYTES = 100 * 1024 * 1024
MAX_NESTED_ZIP_DEPTH = 4
LOOKUP_PAGE_SIZE = 200
MAX_LOOKUP_PAGES = 100
SKILL_ROOT = Path(__file__).resolve().parents[1]
LOOKUP_MAPPINGS_PATH = SKILL_ROOT / "references" / "criterion-lookup-mappings.json"
ELIGIBILITY_SHEET_NAME = "Participant Eligibility"


class ConversionError(ValueError):
    """Raised when the workbook or sample XML cannot be converted safely."""


@dataclass(frozen=True)
class Criterion:
    kind: str
    sequence: str
    name: str
    exclude: str


@dataclass
class Profile:
    name: str
    description: str
    status: str
    profile_type: str
    profile_usage: str
    assignment_to_use: str
    criteria: list[Criterion] = field(default_factory=list)


@dataclass(frozen=True)
class CriterionSpec:
    flag: str
    container: str
    row: str
    value_elements: tuple[str, ...]
    grouping_elements: tuple[str, ...]
    sequence_element: str | None = "OrdrNum"
    exclude_element: str | None = "ExcldFlag"


@dataclass(frozen=True)
class LookupSpec:
    criterion: str
    endpoint: str
    catalog: str
    source_fields: tuple[str, ...]
    target_fields: tuple[tuple[str, str], ...]
    query: tuple[tuple[str, str], ...]
    required_values: tuple[tuple[str, Any], ...]
    multiple_match_policy: str = "error"
    items_path: tuple[str, ...] = ()
    active_date_fields: tuple[str, str] | None = None


class LookupResolver(Protocol):
    def resolve(self, mapping: LookupSpec, meaning: str) -> dict[str, str]:
        """Resolve a workbook meaning to XML element values from one lookup row."""


CRITERION_SPECS = {
    "age": CriterionSpec(
        "EligAgeFlag",
        "AgeCriteriaVO",
        "AgeCriteriaVORow",
        ("AgeFactorName",),
        ("AgeFactorName",),
    ),
    "assignment status": CriterionSpec(
        "EligEeStatFlag",
        "AssignmentStatusCriteriaVO",
        "AssignmentStatusCriteriaVORow",
        ("AssignmentStatusTypeName",),
        ("AssignmentStatusTypeName",),
    ),
    "bargaining unit": CriterionSpec(
        "EligBrgngUnitFlag",
        "BargainingUnitCriteriaVO",
        "BargainingUnitCriteriaVORow",
        ("BrgngUnitCd",),
        ("BrgngUnitCd",),
    ),
    "business unit": CriterionSpec(
        "EligBuFlag",
        "BusinessUnitCriteriaVO",
        "BusinessUnitCriteriaVORow",
        ("BusinessUnitName",),
        ("EligCriteriaCode", "BusinessUnitName"),
    ),
    "hourly or salaried": CriterionSpec(
        "EligHrlySlrdFlag",
        "HourlyOrSalariedCriteriaVO",
        "HourlyOrSalariedCriteriaVORow",
        ("HrlySlrdCd",),
        ("HrlySlrdCd",),
    ),
    "job function": CriterionSpec(
        "EligJobfuncFlag",
        "JobFunctionCriteriaVO",
        "JobFunctionCriteriaVORow",
        ("CritChar1",),
        ("EligCriteriaCode", "CritChar1"),
    ),
    "labor union member": CriterionSpec(
        "EligLbrMmbrFlag",
        "LaborUnionMemberCriteriaVO",
        "LaborUnionMemberCriteriaVORow",
        ("LbrMmbrFlag",),
        ("LbrMmbrFlag",),
    ),
    "legal employer": CriterionSpec(
        "EligLglEntyFlag",
        "LegalEntityCriteriaVO",
        "LegalEntityCriteriaVORow",
        ("OrganizationName",),
        ("OrganizationName",),
    ),
    "marital status": CriterionSpec(
        "EligMrtlStsFlag",
        "MaritalStatusCriteriaVO",
        "MaritalStatusCriteriaVORow",
        ("MaritalStatus",),
        ("MaritalStatus",),
        sequence_element=None,
    ),
    "manager": CriterionSpec(
        "EligMgrFlag",
        "PeopleManagerCriteriaVO",
        "PeopleManagerCriteriaVORow",
        ("CritChar1",),
        ("EligCriteriaCode", "CritChar1"),
    ),
    "religion": CriterionSpec(
        "EligReligionFlag",
        "ReligionCriteriaVO",
        "ReligionCriteriaVORow",
        ("CritChar1",),
        ("EligCriteriaCode", "CritChar1"),
    ),
    "union": CriterionSpec(
        "EligSupplRoleFlag",
        "UnionCriteriaVO",
        "UnionCriteriaVORow",
        ("CritCharOrganizationName", "OrganizationName"),
        ("EligCriteriaCode", "OrganizationName"),
    ),
    "person type": CriterionSpec(
        "EligPerTypFlag",
        "PersonTypeCriteriaV2VO",
        "PersonTypeCriteriaV2VORow",
        ("UserPersonType", "SystemPersonType"),
        ("UserPersonType", "SystemPersonType"),
    ),
    "tobacco use": CriterionSpec(
        "EligTbcoUseFlag",
        "TobaccoUseCriteriaVO",
        "TobaccoUseCriteriaVORow",
        ("UsesTbcoFlag",),
        ("UsesTbcoFlag",),
    ),
    "gender": CriterionSpec(
        "EligGndrFlag",
        "GenderCriteriaVO",
        "GenderCriteriaVORow",
        ("Sex",),
        ("Sex",),
    ),
    "disabled": CriterionSpec(
        "EligDsbldFlag",
        "DisabilityCriteriaVO",
        "DisabilityCriteriaVORow",
        ("DsbldCd",),
        ("DsbldCd",),
    ),
    "termination reason": CriterionSpec(
        "EligLvgRsnFlag",
        "LeavingReasonCriteriaVO",
        "LeavingReasonCriteriaVORow",
        ("ActionName", "LvgRsnCd"),
        ("ActionName",),
    ),
    "assignment category": CriterionSpec(
        "EligFlTmPtTmFlag",
        "FullTimeOrPartTimeCriteriaVO",
        "FullTimeOrPartTimeCriteriaVORow",
        ("FlTmPtTmCd",),
        ("FlTmPtTmCd",),
    ),
    "salary basis": CriterionSpec(
        "EligPyBssFlag",
        "PayBasisCriteriaVO",
        "PayBasisCriteriaVORow",
        ("SalaryBasisName",),
        ("SalaryBasisName",),
    ),
    "quartile in grade": CriterionSpec(
        "EligQuaInGrFlag",
        "QuartileInGradeCriteriaVO",
        "QuartileInGradeCriteriaVORow",
        ("QuarInGradeCd",),
        ("QuarInGradeCd",),
    ),
    "formula": CriterionSpec(
        "EligyPrflRlFlag",
        "RuleCriteriaVO",
        "RuleCriteriaVORow",
        ("ParticipationandRateEligibilityFormulaName",),
        ("ParticipationandRateEligibilityFormulaName",),
        sequence_element="OrdrToAplyNum",
        exclude_element=None,
    ),
    "department": CriterionSpec(
        "EligOrgUnitFlag",
        "OrganizationCriteriaVO",
        "OrganizationCriteriaVORow",
        ("OrganizationName",),
        ("OrganizationName",),
    ),
    "job family": CriterionSpec(
        "EligJobfamFlag",
        "JobFamilyCriteriaV2VO",
        "JobFamilyCriteriaV2VORow",
        ("JobFamilyName", "JobFamilyCode"),
        ("EligCriteriaCode", "JobFamilyName", "JobFamilyCode"),
    ),
    "collective agreement": CriterionSpec(
        "EligAsntSetFlag",
        "CollectiveAgreementCriteriaV2VO",
        "CollectiveAgreementCriteriaV2VORow",
        (
            "CritCharCollectiveAgreementName",
            "IdentificationCode",
            "CollectiveAgreementName",
        ),
        ("EligCriteriaCode", "CollectiveAgreementName", "IdentificationCode"),
    ),
    "compensation": CriterionSpec(
        "EligCompLvlFlag",
        "CompensationCriteriaVO",
        "CompensationCriteriaVORow",
        ("CompensationFactorName",),
        ("CompensationFactorName",),
    ),
    "length of service": CriterionSpec(
        "EligLosFlag",
        "LengthOfServiceCriteriaVO",
        "LengthOfServiceCriteriaVORow",
        ("LengthOfServiceFactorName",),
        ("LengthOfServiceFactorName",),
    ),
    "age and service": CriterionSpec(
        "EligCmbnAgeLosFlag",
        "CombinedAgeAndLosCriteriaVO",
        "CombinedAgeAndLosCriteriaVORow",
        ("CombinedAgeLosFactorName",),
        ("CombinedAgeLosFactorName",),
    ),
    "combined age and length of service": CriterionSpec(
        "EligCmbnAgeLosFlag",
        "CombinedAgeAndLosCriteriaVO",
        "CombinedAgeAndLosCriteriaVORow",
        ("CombinedAgeLosFactorName",),
        ("CombinedAgeLosFactorName",),
    ),
    "hours worked": CriterionSpec(
        "EligHrsWkdFlag",
        "HoursWorkedCriteriaVO",
        "HoursWorkedCriteriaVORow",
        ("HoursWorkedFactorName",),
        ("HoursWorkedFactorName",),
    ),
    "full time equivalent": CriterionSpec(
        "EligPctFlTmFlag",
        "FullTimeEquivalentCriteriaVO",
        "FullTimeEquivalentCriteriaVORow",
        ("FullTimeEquivalentFactorName",),
        ("FullTimeEquivalentFactorName",),
    ),
    "benefit groups": CriterionSpec(
        "EligBenftsGrpFlag",
        "BenefitsGroupCriteriaVO",
        "BenefitsGroupCriteriaVORow",
        ("BenefitsGroupName",),
        ("BenefitsGroupName",),
    ),
    "postal code range": CriterionSpec(
        "EligPstlCdFlag",
        "PostalZipRangeCriteriaVO",
        "PostalZipRangeCriteriaVORow",
        ("PostalZipRange",),
        ("PostalZipRange",),
    ),
    "postal code ranges": CriterionSpec(
        "EligPstlCdFlag",
        "PostalZipRangeCriteriaVO",
        "PostalZipRangeCriteriaVORow",
        ("PostalZipRange",),
        ("PostalZipRange",),
    ),
    "service area": CriterionSpec(
        "EligSvcAreaFlag",
        "ServiceAreaCriteriaVO",
        "ServiceAreaCriteriaVORow",
        ("ServiceAreaName",),
        ("ServiceAreaName",),
    ),
    "service areas": CriterionSpec(
        "EligSvcAreaFlag",
        "ServiceAreaCriteriaVO",
        "ServiceAreaCriteriaVORow",
        ("ServiceAreaName",),
        ("ServiceAreaName",),
    ),
}


PACKAGE_REFERENCE_LABELS = {
    "age": "Age worksheet",
    "compensation": "Comp derived factors worksheet",
    "benefit groups": "Benefit Groups worksheet",
    "length of service": "Length of Service worksheet",
    "age and service": "Age and Service worksheet",
    "combined age and length of service": "Age and Service worksheet",
    "hours worked": "Hours Worked worksheet",
    "full time equivalent": "Full-Time Equivalent worksheet",
    "postal code range": "Postal Code Ranges worksheet",
    "postal code ranges": "Postal Code Ranges worksheet",
    "service area": "Service Areas worksheet",
    "service areas": "Service Areas worksheet",
}

PROFILE_VALUE_MAPS = {
    "status": {
        "a": "A",
        "active": "A",
        "i": "I",
        "inactive": "I",
    },
    "profile type": {
        "prtp": "PRTP",
        "participant": "PRTP",
    },
    "profile usage": {
        # Enabled BEN_BNFT_CAGR_PRTN seeds used by the ADF Profile Usage LOV.
        # CAGR (Collective agreements) and MUSE (Multiuse) are disabled.
        "bnft": "BNFT",
        "benefits": "BNFT",
        "chklist": "CHKLIST",
        "checklist": "CHKLIST",
        "cmp": "CMP",
        "compensation": "CMP",
        "ehw": "EHW",
        "employee wellness": "EHW",
        "ffs": "FFS",
        "field services": "FFS",
        "global": "GLOBAL",
        "goal": "GOAL",
        "goals management": "GOAL",
        "hwr": "HWR",
        "personal brand": "HWR",
        "performance": "PERFORMANCE",
        "ora emp communication": "ORA_EMP_COMMUNICATION",
        "employee communications": "ORA_EMP_COMMUNICATION",
        "ora opp market place": "ORA_OPP_MARKET_PLACE",
        "opportunity marketplace": "ORA_OPP_MARKET_PLACE",
    },
    "assignment to use": {
        "ane": "ANE",
        "any assignment enterprise": "ANE",
    },
}


def _normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def _exact_text_key(value: str) -> str:
    return value.strip().casefold()


def read_contract_bytes(path: Path) -> bytes:
    """Read loose overrides or a logical section of the bundled contracts."""
    if path.exists():
        return path.read_bytes()
    references = SKILL_ROOT / 'references'
    sections = {
        references / 'criterion-lookup-mappings.json': 'lookup_mappings',
        references / 'plan-copy-map-criteria.json': 'map_rules',
        references / 'plan-copy.openapi.json': 'openapi',
        references / 'eligibility-profile-mapping-reference/mapping-reference.json': 'mapping_catalog',
    }
    section = sections.get(path.resolve())
    if section is None:
        return path.read_bytes()
    bundle = json.loads((references / 'eligibility-contracts.json').read_text(encoding='utf-8'))
    if not isinstance(bundle, dict) or bundle.get('version') != 1 or not isinstance(bundle.get(section), dict):
        raise OSError(f'Invalid eligibility contract section: {section}')
    return (json.dumps(bundle[section], ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def contract_path_exists(path: Path) -> bool:
    if path.exists():
        return True
    references = SKILL_ROOT / 'references'
    if path.resolve() == references / 'eligibility-profile-mapping-reference':
        path = path / 'mapping-reference.json'
    try:
        read_contract_bytes(path)
        return True
    except (OSError, ValueError):
        return False


def load_lookup_mappings(path: Path = LOOKUP_MAPPINGS_PATH) -> dict[str, LookupSpec]:
    """Load the maintained criterion-to-Fusion-lookup declarations."""
    try:
        payload = json.loads(read_contract_bytes(path))
    except OSError as exc:
        raise ConversionError(f"Unable to read criterion lookup mappings {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ConversionError(f"Criterion lookup mappings are not valid JSON: {exc}") from exc

    if not isinstance(payload, dict) or payload.get("version") != 4:
        raise ConversionError("Criterion lookup mappings must use schema version 4.")
    criteria = payload.get("criteria")
    if not isinstance(criteria, dict):
        raise ConversionError("Criterion lookup mappings must contain a criteria object.")

    mappings: dict[str, LookupSpec] = {}
    required = {
        "endpoint",
        "catalog",
        "source_fields",
        "target_fields",
        "query",
        "required_values",
    }
    reserved_query_fields = {"fields", "onlyData", "limit", "offset"}
    for criterion, raw_mapping in criteria.items():
        if not isinstance(criterion, str) or not isinstance(raw_mapping, dict):
            raise ConversionError("Each criterion lookup mapping must be a named object.")
        missing = sorted(required - raw_mapping.keys())
        if missing:
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' is missing: {', '.join(missing)}"
            )
        string_fields = {name: raw_mapping[name] for name in ("endpoint", "catalog")}
        if any(not isinstance(value, str) or not value.strip() for value in string_fields.values()):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' requires non-empty endpoint and "
                "catalog strings."
            )
        raw_sources = raw_mapping["source_fields"]
        if not isinstance(raw_sources, list) or not raw_sources or any(
            not isinstance(value, str) or not value.strip() for value in raw_sources
        ):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' requires a non-empty "
                "source_fields string array."
            )
        source_fields = tuple(dict.fromkeys(value.strip() for value in raw_sources))
        endpoint = string_fields["endpoint"].strip()
        if not endpoint.startswith(("/fscmRestApi/", "/hcmRestApi/")) or "?" in endpoint:
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' must use a query-free Fusion REST path."
            )
        criterion_key = _normalized(criterion)
        if criterion_key in mappings:
            raise ConversionError(f"Duplicate normalized criterion lookup mapping: {criterion}")
        spec = CRITERION_SPECS.get(criterion_key)
        if spec is None:
            raise ConversionError(f"Lookup mapping references unsupported criterion: {criterion}")

        raw_targets = raw_mapping["target_fields"]
        if not isinstance(raw_targets, dict) or not raw_targets:
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' requires a non-empty target_fields object."
            )
        if any(
            not isinstance(element, str)
            or not element.strip()
            or not isinstance(field_name, str)
            or not field_name.strip()
            for element, field_name in raw_targets.items()
        ):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' target_fields must contain "
                "non-empty string pairs."
            )
        normalized_targets = {element.strip(): field_name.strip() for element, field_name in raw_targets.items()}
        if set(normalized_targets) != set(spec.value_elements):
            raise ConversionError(
                f"Lookup mapping for '{criterion}' must target exactly: "
                f"{', '.join(spec.value_elements)}."
            )

        raw_query = raw_mapping["query"]
        if not isinstance(raw_query, dict) or any(
            not isinstance(name, str)
            or not name.strip()
            or not isinstance(value, str)
            or not value.strip()
            for name, value in raw_query.items()
        ):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' query must contain non-empty string pairs."
            )
        if reserved_query_fields.intersection(raw_query):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' cannot override pagination or fields."
            )

        raw_required_values = raw_mapping["required_values"]
        if not isinstance(raw_required_values, dict) or any(
            not isinstance(name, str)
            or not name.strip()
            or isinstance(value, (dict, list))
            or value is None
            for name, value in raw_required_values.items()
        ):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' required_values must contain scalar values."
            )
        multiple_match_policy = raw_mapping.get("multiple_match_policy", "error")
        if (
            not isinstance(multiple_match_policy, str)
            or multiple_match_policy not in {"error", "first"}
        ):
            raise ConversionError(
                f"Criterion lookup mapping '{criterion}' multiple_match_policy must be "
                "'error' or 'first'."
            )
        mappings[criterion_key] = LookupSpec(
            criterion=criterion,
            endpoint=endpoint,
            catalog=string_fields["catalog"].strip(),
            source_fields=source_fields,
            target_fields=tuple(
                (element, normalized_targets[element]) for element in spec.value_elements
            ),
            query=tuple((name.strip(), value.strip()) for name, value in raw_query.items()),
            required_values=tuple(
                (name.strip(), value) for name, value in raw_required_values.items()
            ),
            multiple_match_policy=multiple_match_policy,
        )
    return mappings


class FusionLookupResolver:
    """Resolve active Fusion lookup meanings through the shared REST client."""

    def __init__(
        self,
        *,
        properties_path: Path = rest_client_common.DEFAULT_PROPERTIES_PATH,
        token_cache: Path = Path("auto"),
        active_date: date | None = None,
        open_browser: bool = True,
        tls_cert_sha256: str | None = None,
        status_callback: Callable[[str], None] | None = None,
    ) -> None:
        self.properties_path = properties_path
        self.token_cache = token_cache
        self.active_date = active_date or date.today()
        try:
            self.tls_cert_sha256 = (
                rest_client_common.normalize_tls_cert_sha256(tls_cert_sha256)
                if tls_cert_sha256 is not None
                else None
            )
        except ValueError as exc:
            raise ConversionError(f"Lookup resolution failed (input validation): {exc}") from exc
        self.status_callback = status_callback
        self._props: dict[str, str] | None = None
        self._session: rest_client_common.FusionRestSession | None = None
        self._cache: dict[
            tuple[str, str, tuple[tuple[str, str], ...]],
            tuple[tuple[str, str], ...],
        ] = {}
        self._items_cache: dict[tuple[str, tuple[tuple[str, str], ...]], tuple[Any, ...]] = {}
        self._auth_args = argparse.Namespace(
            access_token=None,
            redirect_url=None,
            auth_code=None,
            open_browser=open_browser,
            callback_timeout=rest_client_common.DEFAULT_CALLBACK_TIMEOUT_SECONDS,
            token_cache=str(token_cache),
            force_login=False,
            tls_cert_sha256=self.tls_cert_sha256,
        )

    def _status(self, message: str) -> None:
        if self.status_callback is not None:
            self.status_callback(message)

    def _ensure_session(self) -> None:
        if self._session is not None:
            return
        try:
            props = rest_client_common.read_properties(self.properties_path)
            rest_client_common.require_props(props, ["environment", "restBaseUrl"])
            auth_props = rest_client_common.props_with_scope_property(props, "scope")
            self._session = rest_client_common.FusionRestSession(auth_props, self._auth_args)
        except Exception as exc:
            raise ConversionError(
                f"Lookup resolution failed (auth/authz) using {self.properties_path}."
            ) from exc
        self._props = props

    def _request(self, mapping: LookupSpec, query: dict[str, str]) -> dict[str, Any]:
        self._ensure_session()
        assert self._props is not None
        assert self._session is not None
        url = rest_client_common.build_url(self._props, mapping.endpoint, query)
        try:
            response = self._session.request("GET", url, expected={200})
        except rest_client_common.FusionHttpError as exc:
            raise self._request_error(mapping, exc) from exc
        except Exception as exc:
            raise self._request_error(mapping, exc) from exc
        payload = response.body
        if not isinstance(payload, dict):
            raise ConversionError(
                f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                "the REST response was not a JSON object."
            )
        return payload

    @staticmethod
    def _request_error(mapping: LookupSpec, exc: Exception) -> ConversionError:
        if isinstance(exc, rest_client_common.FusionHttpError):
            if exc.status_code in {401, 403}:
                category = "auth/authz"
            elif exc.status_code == 404:
                category = "catalog mismatch"
            else:
                category = "Fusion API"
            detail = f"HTTP {exc.status_code} from {mapping.endpoint}"
        else:
            category = "transport/environment"
            detail = str(exc)
        return ConversionError(
            f"Lookup resolution failed ({category}) for {mapping.catalog}: {detail}"
        )

    @staticmethod
    def _nested_items(
        mapping: LookupSpec,
        page_items: list[Any],
    ) -> list[Any]:
        items = page_items
        for path_element in mapping.items_path:
            nested: list[Any] = []
            for item in items:
                if not isinstance(item, dict):
                    raise ConversionError(
                        f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                        "items must be JSON objects."
                    )
                child_items = item.get(path_element)
                if not isinstance(child_items, list):
                    raise ConversionError(
                        f"Lookup resolution failed (catalog mismatch) for {mapping.catalog}: "
                        f"response has no {'.'.join(mapping.items_path)} array."
                    )
                nested.extend(child_items)
            items = nested
        return items

    @staticmethod
    def _is_active_on(
        mapping: LookupSpec,
        item: dict[str, Any],
        active_date: date,
    ) -> bool:
        if mapping.active_date_fields is None:
            return True
        start_field, end_field = mapping.active_date_fields
        dates: list[date | None] = []
        for field_name in (start_field, end_field):
            value = item.get(field_name)
            if value in {None, ""}:
                dates.append(None)
                continue
            if not isinstance(value, str):
                raise ConversionError(
                    f"Lookup resolution failed (catalog mismatch): {mapping.catalog} "
                    f"row has invalid {field_name}."
                )
            try:
                dates.append(date.fromisoformat(value[:10]))
            except ValueError as exc:
                raise ConversionError(
                    f"Lookup resolution failed (catalog mismatch): {mapping.catalog} "
                    f"row has invalid {field_name}."
                ) from exc
        start_date, end_date = dates
        return (start_date is None or start_date <= active_date) and (
            end_date is None or active_date <= end_date
        )

    @staticmethod
    def _matching_values(
        mapping: LookupSpec,
        meaning: str,
        items: list[Any],
        active_date: date,
    ) -> list[dict[str, str]]:
        expected = _exact_text_key(meaning)
        matches: list[dict[str, str]] = []
        for item in items:
            if not isinstance(item, dict):
                raise ConversionError(
                    f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                    "items must be JSON objects."
                )
            if any(
                item.get(field_name) != required_value
                for field_name, required_value in mapping.required_values
            ):
                continue
            if not FusionLookupResolver._is_active_on(mapping, item, active_date):
                continue
            source_values = [item.get(field_name) for field_name in mapping.source_fields]
            if not any(
                isinstance(source_value, str)
                and _exact_text_key(source_value) == expected
                for source_value in source_values
            ):
                continue
            values: dict[str, str] = {}
            for element, field_name in mapping.target_fields:
                target_value = item.get(field_name)
                if isinstance(target_value, bool) or not isinstance(target_value, (str, int)):
                    raise ConversionError(
                        f"Lookup resolution failed (catalog mismatch): {mapping.catalog} "
                        f"row '{meaning}' has no {field_name}."
                    )
                rendered_value = str(target_value).strip()
                if not rendered_value:
                    raise ConversionError(
                        f"Lookup resolution failed (catalog mismatch): {mapping.catalog} "
                        f"row '{meaning}' has no {field_name}."
                    )
                values[element] = rendered_value
            matches.append(values)
        return matches

    def resolve(self, mapping: LookupSpec, meaning: str) -> dict[str, str]:
        cache_key = (
            mapping.catalog,
            _exact_text_key(meaning),
            mapping.target_fields,
        )
        if cache_key in self._cache:
            self._status(
                f"Reused {mapping.criterion} '{meaning}' from the current-run lookup cache."
            )
            return dict(self._cache[cache_key])

        self._status(
            f"Resolving {mapping.criterion} '{meaning}' using {mapping.catalog}."
        )

        query = {
            name: value.replace("{active_date}", self.active_date.isoformat()).replace(
                "{meaning}", meaning.replace("'", "''")
            )
            for name, value in mapping.query
        }
        items_key = (mapping.catalog, tuple(sorted(query.items())))
        cached_items = self._items_cache.get(items_key)
        items: list[Any] = list(cached_items) if cached_items is not None else []
        item_fields = ",".join(
            dict.fromkeys(
                (
                    *mapping.source_fields,
                    *(field_name for _, field_name in mapping.target_fields),
                    *(field_name for field_name, _ in mapping.required_values),
                    *(mapping.active_date_fields or ()),
                )
            )
        )
        fields = (
            f"{'.'.join(mapping.items_path)}:{item_fields}"
            if mapping.items_path
            else item_fields
        )
        if cached_items is None:
            offset = 0
            for _ in range(MAX_LOOKUP_PAGES):
                page_query = dict(query)
                page_query.update(
                    {
                        "fields": fields,
                        "onlyData": "true",
                        "limit": str(LOOKUP_PAGE_SIZE),
                        "offset": str(offset),
                    }
                )
                payload = self._request(mapping, page_query)
                root_page_items = payload.get("items")
                if not isinstance(root_page_items, list):
                    raise ConversionError(
                        f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                        "response has no items array."
                    )
                page_items = self._nested_items(mapping, root_page_items)
                items.extend(page_items)
                if not payload.get("hasMore", False):
                    break
                count = payload.get("count", len(root_page_items))
                if not isinstance(count, int) or count <= 0:
                    raise ConversionError(
                        f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                        "pagination made no progress."
                    )
                offset += count
            else:
                raise ConversionError(
                    f"Lookup resolution failed (Fusion API) for {mapping.catalog}: "
                    f"pagination exceeded {MAX_LOOKUP_PAGES} pages."
                )
            self._items_cache[items_key] = tuple(items)

        matches = self._matching_values(mapping, meaning, items, self.active_date)
        if not matches:
            raise ConversionError(
                f"No active {mapping.catalog} row has any of "
                f"{', '.join(mapping.source_fields)} "
                f"exactly matching '{meaning}'."
            )
        if len(matches) > 1 and mapping.multiple_match_policy == "first":
            self._status(
                f"WARNING: {mapping.criterion} '{meaning}' matched {len(matches)} active "
                "rows; using the first Fusion response row."
            )
        elif len(matches) != 1:
            raise ConversionError(
                f"Ambiguous {mapping.catalog} meaning '{meaning}': "
                f"expected one active row, found {len(matches)}."
            )
        cached = tuple(matches[0].items())
        self._cache[cache_key] = cached
        self._status(f"Resolved {mapping.criterion} '{meaning}'.")
        return dict(cached)


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _cell(row: tuple[str, ...], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def _find_header(rows: tuple[tuple[str, ...], ...]) -> tuple[int, dict[str, int]]:
    for row_index, row in enumerate(rows):
        normalized = [_normalized(value) for value in row]
        if "eligibility criteria" not in normalized:
            continue
        criterion_index = normalized.index("eligibility criteria")
        before = normalized[:criterion_index]
        after = normalized[criterion_index + 1 :]
        required_profile = {
            "name": "profile_name",
            "description": "description",
            "status": "status",
            "profile type": "profile_type",
            "profile usage": "profile_usage",
            "assignment to use": "assignment_to_use",
        }
        positions: dict[str, int] = {"criterion": criterion_index}
        missing: list[str] = []
        for header, key in required_profile.items():
            if header in before:
                positions[key] = before.index(header)
            else:
                missing.append(header)
        for header, key in (("sequence", "sequence"), ("name", "criterion_name"), ("exclude", "exclude")):
            if header in after:
                positions[key] = criterion_index + 1 + after.index(header)
            else:
                missing.append(header)
        if missing:
            raise ConversionError(
                "Eligibility workbook header is missing: " + ", ".join(sorted(missing))
            )
        return row_index, positions
    raise ConversionError(
        "No eligibility-profile header row was found; expected an 'Eligibility - Criteria' column."
    )


def parse_profiles(rows: tuple[tuple[str, ...], ...]) -> list[Profile]:
    """Parse the human-readable eligibility workbook layout into profile records."""
    header_index, columns = _find_header(rows)
    profiles: list[Profile] = []
    current: Profile | None = None
    seen_names: set[str] = set()

    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        profile_name = _cell(row, columns["profile_name"])
        criterion_kind = _cell(row, columns["criterion"])
        if not profile_name and not criterion_kind and not any(value.strip() for value in row):
            continue
        if profile_name:
            normalized_name = profile_name.casefold()
            if normalized_name in seen_names:
                raise ConversionError(
                    f"Row {row_number} starts a duplicate eligibility profile: {profile_name}"
                )
            seen_names.add(normalized_name)
            current = Profile(
                name=profile_name,
                description=_cell(row, columns["description"]),
                status=_cell(row, columns["status"]),
                profile_type=_cell(row, columns["profile_type"]),
                profile_usage=_cell(row, columns["profile_usage"]),
                assignment_to_use=_cell(row, columns["assignment_to_use"]),
            )
            profiles.append(current)
        elif current is None:
            raise ConversionError(
                f"Row {row_number} contains a criterion before the first eligibility profile."
            )

        if criterion_kind:
            assert current is not None
            sequence = _cell(row, columns["sequence"])
            criterion_name = _cell(row, columns["criterion_name"])
            exclude = _cell(row, columns["exclude"])
            criterion_spec = CRITERION_SPECS.get(_normalized(criterion_kind))
            sequence_required = criterion_spec is None or criterion_spec.sequence_element is not None
            if not criterion_name or (sequence_required and not sequence):
                raise ConversionError(
                    f"Row {row_number} criterion '{criterion_kind}' requires "
                    f"{'Sequence and Name' if sequence_required else 'Name'}."
                )
            if sequence and (not sequence.isdigit() or int(sequence) <= 0):
                raise ConversionError(f"Row {row_number} Sequence must be a positive integer.")
            current.criteria.append(
                Criterion(
                    kind=criterion_kind,
                    sequence=str(int(sequence)) if sequence else "",
                    name=criterion_name,
                    exclude=_yes_no(exclude, f"Row {row_number} Exclude", blank="N"),
                )
            )

    return profiles


def _parse_optional_sheet(sheet, parser):
    """Omitted or wholly blank sections create no objects; validate populated sections."""
    if sheet is None or not any(value.strip() for row in sheet.rows for value in row):
        return []
    return parser(sheet.rows)


def _require_setup_objects(*sections):
    if not any(sections):
        raise ConversionError(
            "The workbook contains no setup rows. Make a copy of the included "
            "Fusion_Elpro_Setup.xlsx sample workbook and enter your data."
        )


def read_workbook_profiles(path: Path) -> list[Profile]:
    if path.suffix.casefold() != ".xlsx":
        raise ConversionError("The input must be an .xlsx workbook; legacy .xls files are not supported.")
    try:
        workbook = workbook_io._read_workbook(path)
    except Exception as exc:
        raise ConversionError(f"Unable to read eligibility workbook {path}: {exc}") from exc
    matches = [
        sheet
        for sheet in workbook.sheets
        if _normalized(sheet.title) == _normalized(ELIGIBILITY_SHEET_NAME)
    ]
    if len(matches) == 1:
        if matches[0].state != "visible":
            raise ConversionError(
                f"The '{ELIGIBILITY_SHEET_NAME}' worksheet must be visible."
            )
        return _parse_optional_sheet(matches[0], parse_profiles)

    # Preserve the legacy one-sheet workbook contract while making the named
    # sheet authoritative for the combined Fusion Benefits workbook.
    visible = [sheet for sheet in workbook.sheets if sheet.state == "visible"]
    if not matches and len(visible) == 1:
        # Only a recognizable legacy profile header may stand in for the named tab.
        if any("eligibility criteria" in [_normalized(value) for value in row]
               for row in visible[0].rows):
            return _parse_optional_sheet(visible[0], parse_profiles)
    if not matches:
        return []
    raise ConversionError(
        f"The workbook must contain exactly one '{ELIGIBILITY_SHEET_NAME}' worksheet."
    )


def _yes_no(value: str, field_name: str, *, blank: str | None = None) -> str:
    normalized = _normalized(value)
    if not normalized and blank is not None:
        return blank
    if normalized in {"y", "yes"}:
        return "Y"
    if normalized in {"n", "no"}:
        return "N"
    raise ConversionError(f"{field_name} must be Y/Yes or N/No.")


def _mapped_profile_value(field_name: str, value: str) -> str:
    normalized = _normalized(value)
    result = PROFILE_VALUE_MAPS[field_name].get(normalized)
    if result is None:
        supported = ", ".join(sorted(PROFILE_VALUE_MAPS[field_name]))
        raise ConversionError(
            f"Unsupported {field_name} value '{value}'. Supported values: {supported}"
        )
    return result


def _validate_archive(archive: zipfile.ZipFile) -> None:
    infos = archive.infolist()
    if len(infos) > MAX_ARCHIVE_ENTRIES:
        raise ConversionError("Sample package contains too many ZIP entries.")
    if sum(info.file_size for info in infos) > MAX_ARCHIVE_EXPANDED_BYTES:
        raise ConversionError("Sample package expands beyond the supported limit.")
    for info in infos:
        if info.flag_bits & 0x1:
            raise ConversionError("Encrypted sample packages are not supported.")
        parts = info.filename.replace("\\", "/").split("/")
        if info.filename.startswith(("/", "\\")) or ".." in parts:
            raise ConversionError("Sample package contains an unsafe ZIP entry path.")


def _template_from_zip(data: bytes, depth: int = 0) -> bytes:
    if depth > MAX_NESTED_ZIP_DEPTH:
        raise ConversionError("Sample package contains too many nested ZIP levels.")
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            _validate_archive(archive)
            names = archive.namelist()
            preferred = [name for name in names if Path(name).name.casefold() == "ben_eligy_prfl.xml"]
            xml_names = preferred or [name for name in names if name.casefold().endswith(".xml")]
            for name in xml_names:
                candidate = archive.read(name)
                if len(candidate) > MAX_TEMPLATE_BYTES:
                    raise ConversionError("Sample XML exceeds the supported size limit.")
                try:
                    root = ET.fromstring(candidate)
                except ET.ParseError:
                    continue
                if _local_name(root.tag) == "EligibilityProfileVO":
                    return candidate
            for name in (name for name in names if name.casefold().endswith(".zip")):
                try:
                    return _template_from_zip(archive.read(name), depth + 1)
                except ConversionError as exc:
                    if "No EligibilityProfileVO XML" not in str(exc):
                        raise
    except zipfile.BadZipFile as exc:
        raise ConversionError("The sample package is not a valid ZIP file.") from exc
    raise ConversionError("No EligibilityProfileVO XML was found in the sample package.")


def read_template_bytes(path: Path) -> bytes:
    """Read a loose override, or a named XML member from sibling templates.zip.

    Archive members are read in memory, never extracted to the filesystem.
    """
    if path.exists() or path.suffix.casefold() != ".xml":
        return path.read_bytes()
    archive_path = path.parent / "templates.zip"
    try:
        with zipfile.ZipFile(archive_path) as archive:
            matches = [info for info in archive.infolist() if info.filename == path.name]
            if len(matches) != 1:
                raise ConversionError(
                    f"Template archive {archive_path} must contain exactly one {path.name}."
                )
            info = matches[0]
            if info.file_size > MAX_ARCHIVE_EXPANDED_BYTES:
                raise ConversionError(f"Template {path.name} exceeds the supported size limit.")
            with archive.open(info) as member:
                data = member.read(MAX_ARCHIVE_EXPANDED_BYTES + 1)
            if len(data) > MAX_ARCHIVE_EXPANDED_BYTES:
                raise ConversionError(f"Template {path.name} exceeds the supported size limit.")
            return data
    except (zipfile.BadZipFile, RuntimeError, NotImplementedError) as exc:
        raise ConversionError(f"Unable to read template archive {archive_path}: {exc}") from exc


def load_template(path: Path) -> ET.Element:
    try:
        data = read_template_bytes(path)
    except OSError as exc:
        raise ConversionError(f"Unable to read sample XML/package {path}: {exc}") from exc
    if len(data) > MAX_ARCHIVE_EXPANDED_BYTES:
        raise ConversionError("Sample XML/package exceeds the supported size limit.")
    if path.suffix.casefold() == ".zip":
        data = _template_from_zip(data)
    elif path.suffix.casefold() != ".xml":
        raise ConversionError("The sample must be an .xml file or a Plan Copy .zip package.")
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ConversionError(f"Sample XML is not well formed: {exc}") from exc
    if _local_name(root.tag) != "EligibilityProfileVO":
        raise ConversionError("Sample XML root must be EligibilityProfileVO.")
    if _direct_child(root, "EligibilityProfileVORow", required=False) is None:
        raise ConversionError(
            "Sample XML must contain an EligibilityProfileVORow; staging-only placeholder XML is insufficient."
        )
    return root


def _direct_child(parent: ET.Element, name: str, *, required: bool = True) -> ET.Element | None:
    for child in parent:
        if _local_name(child.tag) == name:
            return child
    if required:
        raise ConversionError(f"Sample XML is missing required element: {name}")
    return None


def _set_element(parent: ET.Element, name: str, value: str) -> None:
    element = _direct_child(parent, name)
    assert element is not None
    if value == "":
        element.text = None
        element.set("null", "true")
    else:
        element.attrib.pop("null", None)
        element.text = value


def _criterion_xml_values(
    criterion: Criterion,
    *,
    lookup_mappings: dict[str, LookupSpec],
    lookup_resolver: LookupResolver | None,
    package_reference_names: dict[str, frozenset[str]],
) -> dict[str, str]:
    criterion_key = _normalized(criterion.kind)
    spec = CRITERION_SPECS.get(criterion_key)
    local_names = package_reference_names.get(criterion_key)
    if (
        spec is not None
        and local_names is not None
        and _exact_text_key(criterion.name) in local_names
    ):
        return {element: criterion.name for element in spec.value_elements}

    lookup_mapping = lookup_mappings.get(criterion_key)
    if lookup_mapping is not None:
        if lookup_resolver is None:
            raise ConversionError(
                f"Criterion '{criterion.kind}' requires Fusion lookup resolution."
            )
        values = lookup_resolver.resolve(lookup_mapping, criterion.name)
        spec = CRITERION_SPECS[criterion_key]
        missing = [element for element in spec.value_elements if not values.get(element)]
        if missing:
            raise ConversionError(
                f"Lookup resolution failed (catalog mismatch) for {lookup_mapping.catalog}: "
                f"missing XML values {', '.join(missing)}."
            )
        return values
    if criterion_key in PACKAGE_REFERENCE_LABELS and local_names is not None:
        raise ConversionError(
            f"Participant Eligibility {criterion.kind} reference '{criterion.name}' "
            f"was not found in the {PACKAGE_REFERENCE_LABELS[criterion_key]}."
        )
    if spec is not None:
        return {element: criterion.name for element in spec.value_elements}
    raise ConversionError(f"Unsupported eligibility criterion: {criterion.kind}")


def _is_criterion_container(element: ET.Element) -> bool:
    return bool(re.search(r"Criteria(?:V\d+)?VO$", _local_name(element.tag))) and any(
        re.search(r"Criteria(?:V\d+)?VORow$", _local_name(child.tag)) for child in element
    )


def _matching_template_row(
    container: ET.Element,
    row_name: str,
    values: dict[str, str],
) -> ET.Element:
    rows = [child for child in container if _local_name(child.tag) == row_name]
    if not rows:
        raise ConversionError(f"Sample XML is missing required element: {row_name}")
    for row in rows:
        if all(
            (element := _direct_child(row, name, required=False)) is not None
            and (element.text or "").strip() == value
            for name, value in values.items()
        ):
            return row
    return rows[0]


def _build_profile_row(
    template: ET.Element,
    profile: Profile,
    *,
    lookup_mappings: dict[str, LookupSpec],
    lookup_resolver: LookupResolver | None,
    package_reference_names: dict[str, frozenset[str]],
) -> ET.Element:
    row = copy.deepcopy(template)
    _set_element(row, "GroupingKey", profile.name)
    _set_element(row, "ViewInstanceName", "EligibilityProfile")
    _set_element(row, "Name", profile.name)
    _set_element(row, "EligibilityProfileName", profile.name)
    _set_element(row, "Description", profile.description)
    _set_element(row, "StatCd", _mapped_profile_value("status", profile.status))
    _set_element(row, "ProfileType", _mapped_profile_value("profile type", profile.profile_type))
    _set_element(row, "BnftCagrPrtnCd", _mapped_profile_value("profile usage", profile.profile_usage))
    _set_element(
        row,
        "AsmtToUseCd",
        _mapped_profile_value("assignment to use", profile.assignment_to_use),
    )

    containers = {
        _local_name(child.tag): copy.deepcopy(child)
        for child in row
        if _is_criterion_container(child)
    }
    for child in list(row):
        if _is_criterion_container(child):
            row.remove(child)
        elif re.fullmatch(r"Elig.*Flag", _local_name(child.tag)):
            child.attrib.pop("null", None)
            child.text = "N"

    grouped: OrderedDict[str, list[tuple[Criterion, dict[str, str]]]] = OrderedDict()
    for criterion in profile.criteria:
        criterion_key = _normalized(criterion.kind)
        spec = CRITERION_SPECS.get(criterion_key)
        if spec is None:
            supported = ", ".join(sorted(spec_key.title() for spec_key in CRITERION_SPECS))
            raise ConversionError(
                f"Unsupported eligibility criterion '{criterion.kind}'. Supported criteria: {supported}"
            )
        grouped.setdefault(criterion_key, []).append(
            (
                criterion,
                _criterion_xml_values(
                    criterion,
                    lookup_mappings=lookup_mappings,
                    lookup_resolver=lookup_resolver,
                    package_reference_names=package_reference_names,
                ),
            )
        )
        _set_element(row, spec.flag, "Y")

    for criterion_key, criteria in grouped.items():
        spec = CRITERION_SPECS[criterion_key]
        template_container = containers.get(spec.container)
        if template_container is None:
            raise ConversionError(
                f"Sample XML does not contain {spec.container}; use a sample exported with {criteria[0][0].kind}."
            )
        container = copy.deepcopy(template_container)
        for child in list(container):
            if _local_name(child.tag) == spec.row:
                container.remove(child)
        for criterion, xml_values in criteria:
            template_row = _matching_template_row(template_container, spec.row, xml_values)
            criterion_row = copy.deepcopy(template_row)
            for element in spec.value_elements:
                _set_element(criterion_row, element, xml_values[element])
            grouping_values = [profile.name]
            for element_name in spec.grouping_elements:
                element = _direct_child(criterion_row, element_name)
                assert element is not None
                value = (element.text or "").strip()
                if not value:
                    raise ConversionError(
                        f"Sample XML criterion {spec.row} has no grouping value "
                        f"for {element_name}."
                    )
                grouping_values.append(value)
            _set_element(criterion_row, "GroupingKey", ",".join(grouping_values))
            if spec.sequence_element is not None:
                _set_element(criterion_row, spec.sequence_element, criterion.sequence)
            if spec.exclude_element is not None:
                _set_element(criterion_row, spec.exclude_element, criterion.exclude)
            _set_element(criterion_row, "EligibilityProfileName", profile.name)
            container.append(criterion_row)
        row.append(container)
    return row


def convert_profiles(
    template_root: ET.Element,
    profiles: Iterable[Profile],
    *,
    lookup_mappings: dict[str, LookupSpec] | None = None,
    lookup_resolver: LookupResolver | None = None,
    package_reference_names: dict[str, Iterable[str]] | None = None,
) -> ET.Element:
    """Return a new EligibilityProfileVO document populated from profiles."""
    profile_list = list(profiles)
    mappings = lookup_mappings if lookup_mappings is not None else load_lookup_mappings()
    normalized_package_references: dict[str, frozenset[str]] = {}
    for criterion, names in (package_reference_names or {}).items():
        criterion_key = _normalized(criterion)
        if criterion_key not in PACKAGE_REFERENCE_LABELS:
            raise ConversionError(
                f"Unsupported package reference criterion: {criterion}"
            )
        normalized_package_references[criterion_key] = frozenset(
            _exact_text_key(name) for name in names if name.strip()
        )
    needs_lookup = any(
        _normalized(criterion.kind) in mappings
        and _exact_text_key(criterion.name)
        not in normalized_package_references.get(_normalized(criterion.kind), frozenset())
        for profile in profile_list
        for criterion in profile.criteria
    )
    resolver = lookup_resolver
    if needs_lookup and resolver is None:
        resolver = FusionLookupResolver()

    template_row = _direct_child(template_root, "EligibilityProfileVORow")
    assert template_row is not None
    output = copy.deepcopy(template_root)
    for child in list(output):
        if _local_name(child.tag) == "EligibilityProfileVORow":
            output.remove(child)
    for profile in profile_list:
        output.append(
            _build_profile_row(
                template_row,
                profile,
                lookup_mappings=mappings,
                lookup_resolver=resolver,
                package_reference_names=normalized_package_references,
            )
        )
    return output


def _indent(element: ET.Element, level: int = 0) -> None:
    space = "\n" + level * "   "
    if len(element):
        if not element.text or not element.text.strip():
            element.text = space + "   "
        for child in element:
            _indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = space
    if level and (not element.tail or not element.tail.strip()):
        element.tail = space


def render_xml_bytes(root: ET.Element) -> bytes:
    """Render a converted XML tree with the same formatting used for file output."""
    rendered = copy.deepcopy(root)
    _indent(rendered)
    output = io.BytesIO()
    ET.ElementTree(rendered).write(output, encoding="utf-8", xml_declaration=True)
    return output.getvalue()


def write_xml(root: ET.Element, output: Path, *, force: bool = False) -> None:
    if output.exists() and not force:
        raise ConversionError(f"Output already exists: {output}; use --force to replace it.")
    output.parent.mkdir(parents=True, exist_ok=True)
    contents = render_xml_bytes(root)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb", prefix=output.name + ".", suffix=".tmp", dir=output.parent, delete=False
        ) as handle:
            temporary = Path(handle.name)
            handle.write(contents)
        os.replace(temporary, output)
    except OSError as exc:
        if temporary is not None:
            try:
                temporary.unlink()
            except OSError:
                pass
        raise ConversionError(f"Unable to write XML output {output}: {exc}") from exc


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the Participant Eligibility tab in Fusion_Elpro_Setup.xlsx into "
            "BEN_ELIGY_PRFL.xml using an Oracle-exported Plan Copy sample as the structural template."
        )
    )
    parser.add_argument(
        "--input", required=True, type=Path, help="Fusion_Elpro_Setup.xlsx workbook."
    )
    parser.add_argument(
        "--sample",
        required=True,
        type=Path,
        help="Oracle-exported BEN_ELIGY_PRFL.xml or a Plan Copy ZIP containing it.",
    )
    parser.add_argument("--output", required=True, type=Path, help="Destination BEN_ELIGY_PRFL.xml.")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file.")
    parser.add_argument(
        "--properties",
        type=Path,
        default=rest_client_common.DEFAULT_PROPERTIES_PATH,
        help="Fusion OAuth environment properties file.",
    )
    parser.add_argument(
        "--token-cache",
        type=Path,
        default=Path("auto"),
        help="Fusion OAuth token cache file.",
    )
    parser.add_argument(
        "--no-open-browser",
        action="store_false",
        dest="open_browser",
        help="Print the OAuth authorization URL instead of opening a browser.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        input_path = args.input.resolve()
        sample_path = args.sample.resolve()
        output_path = args.output.resolve()
        if output_path in {input_path, sample_path}:
            raise ConversionError("Output must not replace the workbook or sample package.")
        profiles = read_workbook_profiles(input_path)
        template = load_template(sample_path)
        converted = convert_profiles(
            template,
            profiles,
            lookup_resolver=FusionLookupResolver(
                properties_path=args.properties.resolve(),
                token_cache=args.token_cache,
                open_browser=args.open_browser,
            ),
        )
        write_xml(converted, output_path, force=args.force)
        criterion_count = sum(len(profile.criteria) for profile in profiles)
        print(
            f"Generated {output_path} with {len(profiles)} eligibility profile(s) "
            f"and {criterion_count} criterion row(s)."
        )
        print("No ZIP package or checksum was created or modified.")
        return 0
    except ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- excel_to_plan_copy_derived_factor_xml ----
excel_to_plan_copy_derived_factor_xml = _component("excel_to_plan_copy_derived_factor_xml", r'''
#!/usr/bin/env python3
"""Convert Age and Compensation derived-factor worksheets to Plan Copy XML."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


AGE_SHEET_NAMES = ("Derived Factors - Age", "Age")
COMPENSATION_SHEET_NAMES = (
    "Derived Factors - Comp",
    "Comp derived factors",
)

COMMON_LOOKUP_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/commonLookupsLOV"
GENERIC_LOOKUP_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/genericLookups"
CURRENCY_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/currenciesLOV"
FORMULA_ENDPOINT = "/hcmRestApi/resources/11.13.18.05/fastFormulas"
BENEFIT_BALANCE_ENDPOINT = "/hcmRestApi/resources/11.13.18.05/benefitBalancesLOV"

AGE_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "AgeDetCd",
    "AgeToUseCd",
    "AgeUom",
    "MnAgeNum",
    "MxAgeNum",
    "Name",
    "NoMnAgeFlag",
    "NoMxAgeFlag",
    "RndgCd",
    "AgeFactorName",
    "AgeCalcRl",
    "AgeDetRl",
    "AgeFctrId",
    "RndgRl",
}

COMPENSATION_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "CompLvlDetCd",
    "CompLvlUom",
    "CompSrcCd",
    "MnCompVal",
    "MxCompVal",
    "Name",
    "NoMnCompFlag",
    "NoMxCompFlag",
    "RndgCd",
    "CompensationLevelFactorName",
    "BnftsBalId",
    "CompCalcRl",
    "CompLvlDetRl",
    "CompLvlFctrId",
    "DefinedBalanceId",
    "RndgRl",
}


@dataclass(frozen=True)
class AgeFactor:
    name: str
    age_to_use: str
    units: str
    calculation_formula: str
    minimum_age: str
    maximum_age: str
    determination_rule: str
    determination_formula: str
    rounding_rule: str
    rounding_formula: str


@dataclass(frozen=True)
class CompensationFactor:
    name: str
    unit_of_measure: str
    source: str
    source_value: str
    minimum_compensation: str
    maximum_compensation: str
    determination_rule: str
    determination_formula: str
    rounding_rule: str
    rounding_formula: str


def _cell(row: tuple[str, ...], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def _find_header(
    rows: tuple[tuple[str, ...], ...],
    alternatives: dict[str, tuple[str, ...]],
    description: str,
) -> tuple[int, dict[str, int]]:
    for row_index, row in enumerate(rows):
        normalized = [eligibility_xml._normalized(value) for value in row]
        columns: dict[str, int] = {}
        for field, headers in alternatives.items():
            matches = [normalized.index(header) for header in headers if header in normalized]
            if matches:
                columns[field] = matches[0]
        if len(columns) == len(alternatives):
            return row_index, columns
    expected = ", ".join(headers[0] for headers in alternatives.values())
    raise eligibility_xml.ConversionError(
        f"No {description} header row was found; expected {expected}."
    )


def _number(value: str, *, row_number: int, field: str) -> str:
    if not value:
        return ""
    try:
        number = Decimal(value.replace(",", ""))
    except InvalidOperation as exc:
        raise eligibility_xml.ConversionError(
            f"Row {row_number} {field} must be a number."
        ) from exc
    if not number.is_finite() or number < 0:
        raise eligibility_xml.ConversionError(
            f"Row {row_number} {field} must be a nonnegative finite number."
        )
    rendered = format(number, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered or "0"


def _validate_range(
    minimum: str, maximum: str, *, row_number: int, description: str
) -> None:
    if minimum and maximum and Decimal(minimum) >= Decimal(maximum):
        raise eligibility_xml.ConversionError(
            f"Row {row_number} {description} minimum must be less than its maximum."
        )


def _validate_formula_pair(
    rule: str,
    formula: str,
    *,
    row_number: int,
    rule_field: str,
    formula_field: str,
) -> None:
    is_formula = eligibility_xml._normalized(rule) == "formula"
    if is_formula and not formula:
        raise eligibility_xml.ConversionError(
            f"Row {row_number} requires {formula_field} when {rule_field} is Formula."
        )
    if formula and not is_formula:
        raise eligibility_xml.ConversionError(
            f"Row {row_number} must use Formula in {rule_field} when {formula_field} is populated."
        )


def parse_age_factors(rows: tuple[tuple[str, ...], ...]) -> list[AgeFactor]:
    """Parse and validate the Age derived-factor worksheet."""
    headers = {
        "name": ("derived factor name", "name"),
        "age_to_use": ("age to use",),
        "units": ("units", "unit of measure"),
        "calculation_formula": ("calculation formula", "calcualtion formula"),
        "minimum_age": ("greater than or equal to age",),
        "maximum_age": ("less than age",),
        "determination_rule": ("determination rule",),
        "determination_formula": ("determination formula",),
        "rounding_rule": ("rounding rule",),
        "rounding_formula": ("rounding formula",),
    }
    header_index, columns = _find_header(rows, headers, "Age derived-factor")
    factors: list[AgeFactor] = []
    names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = {field: _cell(row, index) for field, index in columns.items()}
        for field, label in (
            ("name", "Derived factor Name"),
            ("age_to_use", "Age to use"),
            ("units", "Units"),
            ("determination_rule", "Determination Rule"),
        ):
            if not values[field]:
                raise eligibility_xml.ConversionError(
                    f"Age worksheet row {row_number} requires {label}."
                )
        name_key = eligibility_xml._exact_text_key(values["name"])
        if name_key in names:
            raise eligibility_xml.ConversionError(
                f"Age worksheet row {row_number} repeats derived factor name '{values['name']}'."
            )
        names.add(name_key)
        minimum = _number(
            values["minimum_age"], row_number=row_number, field="minimum age"
        )
        maximum = _number(
            values["maximum_age"], row_number=row_number, field="maximum age"
        )
        _validate_range(minimum, maximum, row_number=row_number, description="age")
        _validate_formula_pair(
            values["determination_rule"],
            values["determination_formula"],
            row_number=row_number,
            rule_field="Determination Rule",
            formula_field="Determination Formula",
        )
        if values["rounding_formula"] and not values["rounding_rule"]:
            raise eligibility_xml.ConversionError(
                f"Age worksheet row {row_number} requires Rounding Rule when Rounding Formula is populated."
            )
        if values["rounding_rule"]:
            _validate_formula_pair(
                values["rounding_rule"],
                values["rounding_formula"],
                row_number=row_number,
                rule_field="Rounding Rule",
                formula_field="Rounding Formula",
            )
        factors.append(
            AgeFactor(
                values["name"],
                values["age_to_use"],
                values["units"],
                values["calculation_formula"],
                minimum,
                maximum,
                values["determination_rule"],
                values["determination_formula"],
                values["rounding_rule"],
                values["rounding_formula"],
            )
        )
    return factors


def parse_compensation_factors(
    rows: tuple[tuple[str, ...], ...]
) -> list[CompensationFactor]:
    """Parse and validate the Compensation derived-factor worksheet."""
    headers = {
        "name": ("name", "derived factor name"),
        "unit_of_measure": ("unit of measure", "units"),
        "source": ("source",),
        "source_value": ("stated salary calc formula benbaltype",),
        "minimum_compensation": ("greater than or equal to compensation",),
        "maximum_compensation": ("less than compensation",),
        "determination_rule": ("determination rule",),
        "determination_formula": ("determination formula",),
        "rounding_rule": ("rounding rule",),
        "rounding_formula": ("rounding formula",),
    }
    header_index, columns = _find_header(rows, headers, "Compensation derived-factor")
    factors: list[CompensationFactor] = []
    names: set[str] = set()
    supported_sources = {"formula", "benefits balance type"}
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = {field: _cell(row, index) for field, index in columns.items()}
        for field, label in (
            ("name", "Name"),
            ("unit_of_measure", "Unit of Measure"),
            ("source", "Source"),
            ("source_value", "Stated Salary/Calc Formula/BenBalType"),
            ("determination_rule", "Determination Rule"),
        ):
            if not values[field]:
                raise eligibility_xml.ConversionError(
                    f"Compensation worksheet row {row_number} requires {label}."
                )
        source_key = eligibility_xml._normalized(values["source"])
        if source_key not in supported_sources:
            raise eligibility_xml.ConversionError(
                f"Compensation worksheet row {row_number} Source '{values['source']}' is not "
                "supported by the exported sample; use Formula or Benefits balance type."
            )
        name_key = eligibility_xml._exact_text_key(values["name"])
        if name_key in names:
            raise eligibility_xml.ConversionError(
                f"Compensation worksheet row {row_number} repeats derived factor name '{values['name']}'."
            )
        names.add(name_key)
        minimum = _number(
            values["minimum_compensation"],
            row_number=row_number,
            field="minimum compensation",
        )
        maximum = _number(
            values["maximum_compensation"],
            row_number=row_number,
            field="maximum compensation",
        )
        _validate_range(
            minimum, maximum, row_number=row_number, description="compensation"
        )
        _validate_formula_pair(
            values["determination_rule"],
            values["determination_formula"],
            row_number=row_number,
            rule_field="Determination Rule",
            formula_field="Determination Formula",
        )
        if values["rounding_formula"] and not values["rounding_rule"]:
            raise eligibility_xml.ConversionError(
                f"Compensation worksheet row {row_number} requires Rounding Rule when Rounding Formula is populated."
            )
        if values["rounding_rule"]:
            _validate_formula_pair(
                values["rounding_rule"],
                values["rounding_formula"],
                row_number=row_number,
                rule_field="Rounding Rule",
                formula_field="Rounding Formula",
            )
        factors.append(
            CompensationFactor(
                values["name"],
                values["unit_of_measure"],
                values["source"],
                values["source_value"],
                minimum,
                maximum,
                values["determination_rule"],
                values["determination_formula"],
                values["rounding_rule"],
                values["rounding_formula"],
            )
        )
    return factors


def _one_visible_sheet(workbook: object, names: tuple[str, ...], description: str) -> object | None:
    normalized_names = {eligibility_xml._normalized(name) for name in names}
    matches = [
        sheet
        for sheet in workbook.sheets
        if eligibility_xml._normalized(sheet.title) in normalized_names
    ]
    if not matches:
        return None
    if len(matches) != 1:
        expected = " or ".join(repr(name) for name in names)
        raise eligibility_xml.ConversionError(
            f"The workbook must contain exactly one visible {description} worksheet named {expected}."
        )
    if matches[0].state != "visible":
        raise eligibility_xml.ConversionError(
            f"The '{matches[0].title}' worksheet must be visible."
        )
    return matches[0]


def read_workbook_derived_factors(
    path: Path,
) -> tuple[list[AgeFactor], list[CompensationFactor]]:
    if path.suffix.casefold() != ".xlsx":
        raise eligibility_xml.ConversionError(
            "The input must be an .xlsx workbook; legacy .xls files are not supported."
        )
    try:
        workbook = eligibility_xml.workbook_io._read_workbook(path)
    except Exception as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits setup workbook {path}: {exc}"
        ) from exc
    age_sheet = _one_visible_sheet(workbook, AGE_SHEET_NAMES, "Age derived-factor")
    compensation_sheet = _one_visible_sheet(
        workbook, COMPENSATION_SHEET_NAMES, "Compensation derived-factor"
    )
    return (
        eligibility_xml._parse_optional_sheet(age_sheet, parse_age_factors),
        eligibility_xml._parse_optional_sheet(compensation_sheet, parse_compensation_factors),
    )


def _template_rows(path: Path, root_name: str, row_name: str) -> tuple[ET.Element, list[ET.Element]]:
    try:
        root = ET.fromstring(eligibility_xml.read_template_bytes(path))
    except OSError as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read {root_name} sample {path}: {exc}"
        ) from exc
    except ET.ParseError as exc:
        raise eligibility_xml.ConversionError(
            f"{root_name} sample is not well formed: {exc}"
        ) from exc
    if eligibility_xml._local_name(root.tag) != root_name:
        raise eligibility_xml.ConversionError(
            f"Derived-factor sample root must be {root_name}."
        )
    rows = [child for child in root if eligibility_xml._local_name(child.tag) == row_name]
    if not rows:
        raise eligibility_xml.ConversionError(
            f"{root_name} sample has no {row_name}."
        )
    return root, rows


def load_age_template(path: Path) -> ET.Element:
    root, rows = _template_rows(path, "AgeFactorVO", "AgeFactorVORow")
    fields = {eligibility_xml._local_name(child.tag) for child in rows[0]}
    missing = sorted(AGE_REQUIRED_FIELDS - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            "Age factor sample row is missing: " + ", ".join(missing)
        )
    return root


def load_compensation_template(path: Path) -> ET.Element:
    root, rows = _template_rows(
        path, "CompensationLevelFactorVO", "CompensationLevelFactorVORow"
    )
    for row in rows:
        fields = {eligibility_xml._local_name(child.tag) for child in row}
        missing = sorted(COMPENSATION_REQUIRED_FIELDS - fields)
        if missing:
            raise eligibility_xml.ConversionError(
                "Compensation factor sample row is missing: " + ", ".join(missing)
            )
    if not any(eligibility_xml._direct_child(row, "CompensationCalculationFormulaName", required=False) is not None for row in rows):
        raise eligibility_xml.ConversionError(
            "Compensation factor sample has no Formula source row."
        )
    if not any(eligibility_xml._direct_child(row, "BenefitBalanceName", required=False) is not None for row in rows):
        raise eligibility_xml.ConversionError(
            "Compensation factor sample has no Benefits balance type source row."
        )
    return root


def _lookup_spec(
    criterion: str,
    lookup_type: str,
    target_field: str,
) -> eligibility_xml.LookupSpec:
    return eligibility_xml.LookupSpec(
        criterion=criterion,
        endpoint=COMMON_LOOKUP_ENDPOINT,
        catalog=f"{lookup_type} common lookup",
        source_fields=("Meaning", "LookupCode"),
        target_fields=((target_field, "LookupCode"),),
        query=(("finder", f"LookupTypeFinder;LookupType={lookup_type},ActiveDate={{active_date}}"),),
        required_values=(("LookupType", lookup_type),),
    )


def _hcm_standard_lookup_spec(
    criterion: str,
    lookup_type: str,
    target_field: str,
) -> eligibility_xml.LookupSpec:
    return eligibility_xml.LookupSpec(
        criterion=criterion,
        endpoint=GENERIC_LOOKUP_ENDPOINT,
        catalog=f"{lookup_type} HCM_LOOKUPS REST lookup",
        source_fields=("Meaning", "LookupCode"),
        target_fields=((target_field, "LookupCode"),),
        query=(("finder", f"LookupTypeFinder;LookupType={lookup_type},ViewApplicationId=3"),),
        required_values=(("EnabledFlag", "Y"),),
        items_path=("lookupCodes",),
        active_date_fields=("StartDateActive", "EndDateActive"),
    )


AGE_TO_USE_LOOKUP = _lookup_spec("Age to use", "BEN_AGE_TO_USE_CD", "AgeToUseCd")
AGE_UNITS_LOOKUP = _lookup_spec("Age units", "BEN_TM_UOM", "AgeUom")
AGE_DETERMINATION_LOOKUP = _lookup_spec(
    "Age determination rule", "BEN_AGE_DET", "AgeDetCd"
)
AGE_ROUNDING_LOOKUP = _lookup_spec("Age rounding rule", "BEN_RNDG", "RndgCd")
COMPENSATION_SOURCE_LOOKUP = _hcm_standard_lookup_spec(
    "Compensation source", "BEN_COMP_SRC", "CompSrcCd"
)
COMPENSATION_DETERMINATION_LOOKUP = _hcm_standard_lookup_spec(
    "Compensation determination rule", "BEN_COMP_LVL_DET", "CompLvlDetCd"
)
COMPENSATION_ROUNDING_LOOKUP = _lookup_spec(
    "Compensation rounding rule", "BEN_RNDG", "RndgCd"
)
CURRENCY_LOOKUP = eligibility_xml.LookupSpec(
    criterion="Compensation unit of measure",
    endpoint=CURRENCY_ENDPOINT,
    catalog="currenciesLOV",
    source_fields=("Name", "CurrencyCode"),
    target_fields=(("CompLvlUom", "CurrencyCode"),),
    query=(),
    required_values=(),
)
FORMULA_LOOKUP = eligibility_xml.LookupSpec(
    criterion="Fast Formula dependency",
    endpoint=FORMULA_ENDPOINT,
    catalog="fastFormulas",
    source_fields=("FormulaName",),
    target_fields=(("FormulaId", "FormulaId"), ("FormulaName", "FormulaName")),
    query=(("q", "FormulaName='{meaning}'"),),
    required_values=(),
)
BENEFIT_BALANCE_LOOKUP = eligibility_xml.LookupSpec(
    criterion="Benefit Balance dependency",
    endpoint=BENEFIT_BALANCE_ENDPOINT,
    catalog="benefitBalancesLOV",
    source_fields=("BenefitBalanceName",),
    target_fields=(
        ("BenefitBalanceId", "BenefitBalanceId"),
        ("BenefitBalanceName", "BenefitBalanceName"),
    ),
    query=(("q", "BenefitBalanceName='{meaning}'"),),
    required_values=(),
)


def _set_literal_null(row: ET.Element, name: str) -> None:
    element = eligibility_xml._direct_child(row, name)
    assert element is not None
    element.attrib.pop("null", None)
    element.text = "#null"


def _remove_child(row: ET.Element, name: str) -> None:
    child = eligibility_xml._direct_child(row, name, required=False)
    if child is not None:
        row.remove(child)


def _set_or_insert_before(
    row: ET.Element, name: str, value: str, before_name: str
) -> None:
    existing = eligibility_xml._direct_child(row, name, required=False)
    if existing is not None:
        existing.attrib.pop("null", None)
        existing.text = value
        return
    before = eligibility_xml._direct_child(row, before_name)
    assert before is not None
    prefix = before.tag[: -len(eligibility_xml._local_name(before.tag))]
    element = ET.Element(prefix + name)
    element.text = value
    row.insert(list(row).index(before), element)


def _validate_formula_dependency(
    resolver: eligibility_xml.LookupResolver, formula_name: str
) -> None:
    if formula_name:
        resolver.resolve(FORMULA_LOOKUP, formula_name)


def convert_age_factors(
    template_root: ET.Element,
    factors: list[AgeFactor],
    resolver: eligibility_xml.LookupResolver,
) -> ET.Element:
    """Clone the exported Age row and populate target-validated workbook values."""
    template_row = next(
        child
        for child in template_root
        if eligibility_xml._local_name(child.tag) == "AgeFactorVORow"
    )
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == "AgeFactorVORow":
            output.remove(child)
    for factor in factors:
        row = copy.deepcopy(template_row)
        age_to_use = resolver.resolve(AGE_TO_USE_LOOKUP, factor.age_to_use)["AgeToUseCd"]
        units = resolver.resolve(AGE_UNITS_LOOKUP, factor.units)["AgeUom"]
        determination = resolver.resolve(
            AGE_DETERMINATION_LOOKUP, factor.determination_rule
        )["AgeDetCd"]
        rounding = ""
        if factor.rounding_rule:
            rounding = resolver.resolve(AGE_ROUNDING_LOOKUP, factor.rounding_rule)[
                "RndgCd"
            ]
        for formula_name in (
            factor.calculation_formula,
            factor.determination_formula,
            factor.rounding_formula,
        ):
            _validate_formula_dependency(resolver, formula_name)
        values = {
            "ViewInstanceName": "AgeFactor",
            "GroupingKey": factor.name,
            "AgeDetCd": determination,
            "AgeToUseCd": age_to_use,
            "AgeUom": units,
            "MnAgeNum": factor.minimum_age,
            "MxAgeNum": factor.maximum_age,
            "Name": factor.name,
            "NoMnAgeFlag": "Y",
            "NoMxAgeFlag": "Y",
            "RndgCd": rounding,
            "AgeFactorName": factor.name,
            "AgeFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        formula_fields = (
            ("AgeCalculationFormulaName", "AgeCalcRl", factor.calculation_formula),
            ("AgeDeterminationDateFormulaName", "AgeDetRl", factor.determination_formula),
            ("RoundingFormulaName", "RndgRl", factor.rounding_formula),
        )
        for name_field, id_field, formula_name in formula_fields:
            _remove_child(row, name_field)
            if formula_name:
                _set_or_insert_before(row, name_field, formula_name, id_field)
                eligibility_xml._set_element(row, id_field, "")
            else:
                _set_literal_null(row, id_field)
        output.append(row)
    return output


def _compensation_template_row(
    template_root: ET.Element, source_code: str
) -> ET.Element:
    required_reference = (
        "CompensationCalculationFormulaName" if source_code == "RL" else "BenefitBalanceName"
    )
    for row in template_root:
        if (
            eligibility_xml._local_name(row.tag) == "CompensationLevelFactorVORow"
            and eligibility_xml._direct_child(row, required_reference, required=False)
            is not None
        ):
            return row
    raise eligibility_xml.ConversionError(
        f"Compensation factor sample has no row containing {required_reference}."
    )


def convert_compensation_factors(
    template_root: ET.Element,
    factors: list[CompensationFactor],
    resolver: eligibility_xml.LookupResolver,
    *,
    package_benefit_balance_names: set[str] | None = None,
) -> ET.Element:
    """Clone the matching exported Compensation row for each workbook factor."""
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == "CompensationLevelFactorVORow":
            output.remove(child)
    for factor in factors:
        source = resolver.resolve(COMPENSATION_SOURCE_LOOKUP, factor.source)["CompSrcCd"]
        if source not in {"RL", "BNFTBALTYP"}:
            raise eligibility_xml.ConversionError(
                f"Compensation source '{factor.source}' resolved to unsupported code {source}."
            )
        row = copy.deepcopy(_compensation_template_row(template_root, source))
        unit = resolver.resolve(CURRENCY_LOOKUP, factor.unit_of_measure)["CompLvlUom"]
        determination = resolver.resolve(
            COMPENSATION_DETERMINATION_LOOKUP, factor.determination_rule
        )["CompLvlDetCd"]
        rounding = ""
        if factor.rounding_rule:
            rounding = resolver.resolve(
                COMPENSATION_ROUNDING_LOOKUP, factor.rounding_rule
            )["RndgCd"]
        _validate_formula_dependency(resolver, factor.determination_formula)
        _validate_formula_dependency(resolver, factor.rounding_formula)
        values = {
            "ViewInstanceName": "CompensationLevelFactor",
            "GroupingKey": factor.name,
            "CompLvlDetCd": determination,
            "CompLvlUom": unit,
            "CompSrcCd": source,
            "MnCompVal": factor.minimum_compensation,
            "MxCompVal": factor.maximum_compensation,
            "Name": factor.name,
            "NoMnCompFlag": "N",
            "NoMxCompFlag": "N",
            "RndgCd": rounding,
            "CompensationLevelFactorName": factor.name,
            "CompLvlFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        for optional_reference in (
            "CompensationCalculationFormulaName",
            "BenefitBalanceName",
            "CompensationDeterminationDateFormulaName",
            "RoundingFormulaName",
        ):
            _remove_child(row, optional_reference)
        if source == "RL":
            resolver.resolve(FORMULA_LOOKUP, factor.source_value)
            _set_or_insert_before(
                row,
                "CompensationCalculationFormulaName",
                factor.source_value,
                "CompCalcRl",
            )
            eligibility_xml._set_element(row, "CompCalcRl", "")
            _set_literal_null(row, "BnftsBalId")
        else:
            if (
                package_benefit_balance_names is None
                or eligibility_xml._exact_text_key(factor.source_value)
                not in package_benefit_balance_names
            ):
                resolver.resolve(BENEFIT_BALANCE_LOOKUP, factor.source_value)
            _set_or_insert_before(
                row, "BenefitBalanceName", factor.source_value, "BnftsBalId"
            )
            eligibility_xml._set_element(row, "BnftsBalId", "")
            _set_literal_null(row, "CompCalcRl")
        formula_fields = (
            (
                "CompensationDeterminationDateFormulaName",
                "CompLvlDetRl",
                factor.determination_formula,
            ),
            ("RoundingFormulaName", "RndgRl", factor.rounding_formula),
        )
        for name_field, id_field, formula_name in formula_fields:
            if formula_name:
                _set_or_insert_before(row, name_field, formula_name, id_field)
                eligibility_xml._set_element(row, id_field, "")
            else:
                _set_literal_null(row, id_field)
        _set_literal_null(row, "DefinedBalanceId")
        output.append(row)
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the Age and Compensation derived-factor worksheets in "
            "Fusion_Elpro_Setup.xlsx into Plan Copy XML."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--age-sample", required=True, type=Path)
    parser.add_argument("--compensation-level-sample", required=True, type=Path)
    parser.add_argument("--age-output", required=True, type=Path)
    parser.add_argument("--compensation-level-output", required=True, type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument(
        "--properties",
        type=Path,
        default=eligibility_xml.rest_client_common.DEFAULT_PROPERTIES_PATH,
    )
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        input_path = args.input.resolve()
        age_sample = args.age_sample.resolve()
        compensation_sample = args.compensation_level_sample.resolve()
        age_output = args.age_output.resolve()
        compensation_output = args.compensation_level_output.resolve()
        if len({input_path, age_sample, compensation_sample, age_output, compensation_output}) != 5:
            raise eligibility_xml.ConversionError(
                "Workbook, samples, and generated outputs must use distinct paths."
            )
        for output in (age_output, compensation_output):
            if output.exists() and not args.force:
                raise eligibility_xml.ConversionError(
                    f"Output already exists: {output}; use --force to replace it."
                )
        age_factors, compensation_factors = read_workbook_derived_factors(input_path)
        resolver = eligibility_xml.FusionLookupResolver(
            properties_path=args.properties.resolve(),
            token_cache=args.token_cache,
            open_browser=not args.no_open_browser,
        )
        age_root = convert_age_factors(
            load_age_template(age_sample), age_factors, resolver
        )
        compensation_root = convert_compensation_factors(
            load_compensation_template(compensation_sample),
            compensation_factors,
            resolver,
        )
        eligibility_xml.write_xml(age_root, age_output, force=args.force)
        eligibility_xml.write_xml(
            compensation_root, compensation_output, force=args.force
        )
        print(f"Generated {age_output} with {len(age_factors)} Age factor(s).")
        print(
            f"Generated {compensation_output} with "
            f"{len(compensation_factors)} Compensation factor(s)."
        )
        return 0
    except eligibility_xml.ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- excel_to_plan_copy_additional_derived_factor_xml ----
excel_to_plan_copy_additional_derived_factor_xml = _component("excel_to_plan_copy_additional_derived_factor_xml", r'''
#!/usr/bin/env python3
"""Convert LOS, combined Age/LOS, Hours Worked, and FTE worksheets."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_derived_factor_xml as derived_factor_xml  # noqa: E402
import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


LOS_SHEET_NAMES = ("Derived Factors - LOS", "Length of Service")
COMBINED_AGE_LOS_SHEET_NAMES = (
    "Derived Factors - Age and LOS",
    "Age and Service",
)
HOURS_WORKED_SHEET_NAMES = ("Derived Factors - Hours Worked", "Hours Worked")
FTE_SHEET_NAMES = ("Derived Factors - FTE", "Full-Time Equivalent")

LOS_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "LosDetCd",
    "LosDtToUseCd",
    "LosUom",
    "MnLosNum",
    "MxLosNum",
    "Name",
    "NoMnLosNumAplsFlag",
    "NoMxLosNumAplsFlag",
    "RndgCd",
    "UseOveridSvcDtFlag",
    "LosFactorName",
    "ConfigId1",
    "LosCalcRl",
    "LosDetRl",
    "LosDtToUseRl",
    "LosFctrId",
    "RndgRl",
}
COMBINED_AGE_LOS_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "CmbndMaxVal",
    "CmbndMinVal",
    "Name",
    "CombinedAgeLosFactorName",
    "AgeFactorName",
    "LosFactorName",
    "AgeFctrId",
    "CmbnAgeLosFctrId",
    "LosFctrId",
}
HOURS_WORKED_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "HrsSrcCd",
    "HrsWkdDetCd",
    "MnHrsNum",
    "MxHrsNum",
    "Name",
    "NoMnHrsWkdFlag",
    "NoMxHrsWkdFlag",
    "PyrlFreqCd",
    "RndgCd",
    "HoursWorkedFactorName",
    "BenefitBalanceName",
    "BnftsBalId",
    "DefinedBalanceId",
    "HrsWkdCalcRl",
    "HrsWkdDetRl",
    "HrsWkdInPerdFctrId",
    "RndgRl",
}
FTE_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "AssignmentTypeName",
    "MnPctVal",
    "MxPctVal",
    "Name",
    "NoMnPctValFlag",
    "NoMxPctValFlag",
    "RndgCd",
    "UsePrmryAsntOnlyFlag",
    "UseSumOfAllAsntsFlag",
    "FullTimeEquivalentFactorName",
    "PctFlTmFctrId",
    "RndgRl",
}


@dataclass(frozen=True)
class LengthOfServiceFactor:
    name: str
    unit_of_measure: str
    minimum_length: str
    maximum_length: str
    determination_rule: str
    determination_formula: str
    rounding_rule: str
    rounding_formula: str
    period_start_date_rule: str


@dataclass(frozen=True)
class CombinedAgeLosFactor:
    name: str
    age_factor: str
    length_of_service_factor: str
    minimum_value: str
    maximum_value: str


@dataclass(frozen=True)
class HoursWorkedFactor:
    name: str
    source: str
    benefit_balance: str
    payroll_frequency: str
    minimum_hours: str
    maximum_hours: str
    determination_rule: str
    determination_formula: str
    rounding_rule: str
    rounding_formula: str


@dataclass(frozen=True)
class FullTimeEquivalentFactor:
    name: str
    assignment_to_use: str
    minimum_value: str
    maximum_value: str
    rounding_rule: str
    rounding_formula: str


def _values(
    row: tuple[str, ...], columns: dict[str, int]
) -> dict[str, str]:
    return {
        field: derived_factor_xml._cell(row, index)
        for field, index in columns.items()
    }


def _require(
    values: dict[str, str], fields: tuple[tuple[str, str], ...], description: str, row: int
) -> None:
    for field, label in fields:
        if not values[field]:
            raise eligibility_xml.ConversionError(
                f"{description} worksheet row {row} requires {label}."
            )


def _unique_name(name: str, names: set[str], description: str, row: int) -> None:
    key = eligibility_xml._exact_text_key(name)
    if key in names:
        raise eligibility_xml.ConversionError(
            f"{description} worksheet row {row} repeats derived factor name '{name}'."
        )
    names.add(key)


def parse_length_of_service_factors(
    rows: tuple[tuple[str, ...], ...]
) -> list[LengthOfServiceFactor]:
    headers = {
        "name": ("name",),
        "unit_of_measure": ("unit of measure", "units"),
        "minimum_length": ("greater than or equal to length of service",),
        "maximum_length": ("less than length of service",),
        "determination_rule": ("determination rule",),
        "determination_formula": ("determination formula",),
        "rounding_rule": ("rounding rule",),
        "rounding_formula": ("rounding formula",),
        "period_start_date_rule": ("period start date rule",),
    }
    header_index, columns = derived_factor_xml._find_header(
        rows, headers, "Length of Service derived-factor"
    )
    factors: list[LengthOfServiceFactor] = []
    names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = _values(row, columns)
        _require(
            values,
            (
                ("name", "Name"),
                ("unit_of_measure", "Unit of Measure"),
                ("determination_rule", "Determination Rule"),
                ("period_start_date_rule", "Period Start Date Rule"),
            ),
            "Length of Service",
            row_number,
        )
        _unique_name(values["name"], names, "Length of Service", row_number)
        minimum = derived_factor_xml._number(
            values["minimum_length"], row_number=row_number, field="minimum length of service"
        )
        maximum = derived_factor_xml._number(
            values["maximum_length"], row_number=row_number, field="maximum length of service"
        )
        derived_factor_xml._validate_range(
            minimum, maximum, row_number=row_number, description="length of service"
        )
        derived_factor_xml._validate_formula_pair(
            values["determination_rule"],
            values["determination_formula"],
            row_number=row_number,
            rule_field="Determination Rule",
            formula_field="Determination Formula",
        )
        if values["rounding_formula"] and not values["rounding_rule"]:
            raise eligibility_xml.ConversionError(
                f"Length of Service worksheet row {row_number} requires Rounding Rule "
                "when Rounding Formula is populated."
            )
        if values["rounding_rule"]:
            derived_factor_xml._validate_formula_pair(
                values["rounding_rule"],
                values["rounding_formula"],
                row_number=row_number,
                rule_field="Rounding Rule",
                formula_field="Rounding Formula",
            )
        factors.append(
            LengthOfServiceFactor(
                values["name"],
                values["unit_of_measure"],
                minimum,
                maximum,
                values["determination_rule"],
                values["determination_formula"],
                values["rounding_rule"],
                values["rounding_formula"],
                values["period_start_date_rule"],
            )
        )
    return factors


def parse_combined_age_los_factors(
    rows: tuple[tuple[str, ...], ...]
) -> list[CombinedAgeLosFactor]:
    headers = {
        "name": ("name",),
        "age_factor": ("age factor",),
        "length_of_service_factor": ("length of service factor",),
        "minimum_value": ("greater than or equal to age and service",),
        "maximum_value": ("less than age and service",),
    }
    header_index, columns = derived_factor_xml._find_header(
        rows, headers, "Age and Service derived-factor"
    )
    factors: list[CombinedAgeLosFactor] = []
    names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = _values(row, columns)
        _require(
            values,
            (
                ("name", "Name"),
                ("age_factor", "Age Factor"),
                ("length_of_service_factor", "Length of Service Factor"),
                ("minimum_value", "Greater than or Equal to Age and Service"),
                ("maximum_value", "Less Than Age and Service"),
            ),
            "Age and Service",
            row_number,
        )
        _unique_name(values["name"], names, "Age and Service", row_number)
        minimum = derived_factor_xml._number(
            values["minimum_value"], row_number=row_number, field="minimum age and service"
        )
        maximum = derived_factor_xml._number(
            values["maximum_value"], row_number=row_number, field="maximum age and service"
        )
        derived_factor_xml._validate_range(
            minimum, maximum, row_number=row_number, description="age and service"
        )
        factors.append(
            CombinedAgeLosFactor(
                values["name"],
                values["age_factor"],
                values["length_of_service_factor"],
                minimum,
                maximum,
            )
        )
    return factors


def parse_hours_worked_factors(
    rows: tuple[tuple[str, ...], ...]
) -> list[HoursWorkedFactor]:
    headers = {
        "name": ("name",),
        "source": ("source",),
        "benefit_balance": ("benefit balance",),
        "payroll_frequency": ("payroll frequency",),
        "minimum_hours": ("greater than or equal to hours worked",),
        "maximum_hours": ("less than hours worked",),
        "determination_rule": ("determination rule",),
        "determination_formula": ("determination formula",),
        "rounding_rule": ("rounding rule",),
        "rounding_formula": ("rounding formula",),
    }
    header_index, columns = derived_factor_xml._find_header(
        rows, headers, "Hours Worked derived-factor"
    )
    factors: list[HoursWorkedFactor] = []
    names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = _values(row, columns)
        _require(
            values,
            (
                ("name", "Name"),
                ("source", "Source"),
                ("benefit_balance", "Benefit Balance"),
                ("payroll_frequency", "Payroll Frequency"),
                ("determination_rule", "Determination Rule"),
            ),
            "Hours Worked",
            row_number,
        )
        _unique_name(values["name"], names, "Hours Worked", row_number)
        minimum = derived_factor_xml._number(
            values["minimum_hours"], row_number=row_number, field="minimum hours worked"
        )
        maximum = derived_factor_xml._number(
            values["maximum_hours"], row_number=row_number, field="maximum hours worked"
        )
        derived_factor_xml._validate_range(
            minimum, maximum, row_number=row_number, description="hours worked"
        )
        derived_factor_xml._validate_formula_pair(
            values["determination_rule"],
            values["determination_formula"],
            row_number=row_number,
            rule_field="Determination Rule",
            formula_field="Determination Formula",
        )
        if values["rounding_formula"] and not values["rounding_rule"]:
            raise eligibility_xml.ConversionError(
                f"Hours Worked worksheet row {row_number} requires Rounding Rule "
                "when Rounding Formula is populated."
            )
        if values["rounding_rule"]:
            derived_factor_xml._validate_formula_pair(
                values["rounding_rule"],
                values["rounding_formula"],
                row_number=row_number,
                rule_field="Rounding Rule",
                formula_field="Rounding Formula",
            )
        factors.append(
            HoursWorkedFactor(
                values["name"],
                values["source"],
                values["benefit_balance"],
                values["payroll_frequency"],
                minimum,
                maximum,
                values["determination_rule"],
                values["determination_formula"],
                values["rounding_rule"],
                values["rounding_formula"],
            )
        )
    return factors


def parse_fte_factors(
    rows: tuple[tuple[str, ...], ...]
) -> list[FullTimeEquivalentFactor]:
    headers = {
        "name": ("name",),
        "assignment_to_use": ("assignment to use",),
        "minimum_value": ("greater than or equal to full time equivalent",),
        "maximum_value": ("less than full time equivalent",),
        "rounding_rule": ("rounding rule",),
        "rounding_formula": ("rounding formula",),
    }
    header_index, columns = derived_factor_xml._find_header(
        rows, headers, "Full-Time Equivalent derived-factor"
    )
    factors: list[FullTimeEquivalentFactor] = []
    names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = _values(row, columns)
        _require(
            values,
            (("name", "Name"), ("assignment_to_use", "Assignment to Use")),
            "Full-Time Equivalent",
            row_number,
        )
        _unique_name(values["name"], names, "Full-Time Equivalent", row_number)
        if eligibility_xml._normalized(values["assignment_to_use"]) not in {
            "primary assignment",
            "sum of all assignments",
        }:
            raise eligibility_xml.ConversionError(
                f"Full-Time Equivalent worksheet row {row_number} Assignment to Use "
                f"'{values['assignment_to_use']}' is unsupported; use Primary Assignment "
                "or Sum of all assignments."
            )
        minimum = derived_factor_xml._number(
            values["minimum_value"], row_number=row_number, field="minimum full-time equivalent"
        )
        maximum = derived_factor_xml._number(
            values["maximum_value"], row_number=row_number, field="maximum full-time equivalent"
        )
        derived_factor_xml._validate_range(
            minimum, maximum, row_number=row_number, description="full-time equivalent"
        )
        if values["rounding_formula"] and not values["rounding_rule"]:
            raise eligibility_xml.ConversionError(
                f"Full-Time Equivalent worksheet row {row_number} requires Rounding Rule "
                "when Rounding Formula is populated."
            )
        if values["rounding_rule"]:
            derived_factor_xml._validate_formula_pair(
                values["rounding_rule"],
                values["rounding_formula"],
                row_number=row_number,
                rule_field="Rounding Rule",
                formula_field="Rounding Formula",
            )
        factors.append(
            FullTimeEquivalentFactor(
                values["name"],
                values["assignment_to_use"],
                minimum,
                maximum,
                values["rounding_rule"],
                values["rounding_formula"],
            )
        )
    return factors


def read_workbook_additional_factors(
    path: Path,
) -> tuple[
    list[LengthOfServiceFactor],
    list[CombinedAgeLosFactor],
    list[HoursWorkedFactor],
    list[FullTimeEquivalentFactor],
]:
    if path.suffix.casefold() != ".xlsx":
        raise eligibility_xml.ConversionError(
            "The input must be an .xlsx workbook; legacy .xls files are not supported."
        )
    try:
        workbook = eligibility_xml.workbook_io._read_workbook(path)
    except Exception as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits setup workbook {path}: {exc}"
        ) from exc
    los_sheet = derived_factor_xml._one_visible_sheet(
        workbook, LOS_SHEET_NAMES, "Length of Service derived-factor"
    )
    combined_sheet = derived_factor_xml._one_visible_sheet(
        workbook, COMBINED_AGE_LOS_SHEET_NAMES, "Age and Service derived-factor"
    )
    hours_sheet = derived_factor_xml._one_visible_sheet(
        workbook, HOURS_WORKED_SHEET_NAMES, "Hours Worked derived-factor"
    )
    fte_sheet = derived_factor_xml._one_visible_sheet(
        workbook, FTE_SHEET_NAMES, "Full-Time Equivalent derived-factor"
    )
    return (
        eligibility_xml._parse_optional_sheet(los_sheet, parse_length_of_service_factors),
        eligibility_xml._parse_optional_sheet(combined_sheet, parse_combined_age_los_factors),
        eligibility_xml._parse_optional_sheet(hours_sheet, parse_hours_worked_factors),
        eligibility_xml._parse_optional_sheet(fte_sheet, parse_fte_factors),
    )


def _load_template(
    path: Path,
    root_name: str,
    row_name: str,
    required_fields: set[str],
) -> ET.Element:
    root, rows = derived_factor_xml._template_rows(path, root_name, row_name)
    fields = {eligibility_xml._local_name(child.tag) for child in rows[0]}
    missing = sorted(required_fields - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            f"{root_name} sample row is missing: " + ", ".join(missing)
        )
    return root


def load_length_of_service_template(path: Path) -> ET.Element:
    return _load_template(
        path,
        "LengthOfServiceFactorVO",
        "LengthOfServiceFactorVORow",
        LOS_REQUIRED_FIELDS,
    )


def load_combined_age_los_template(path: Path) -> ET.Element:
    return _load_template(
        path,
        "CombinedAgeLosFactorVO",
        "CombinedAgeLosFactorVORow",
        COMBINED_AGE_LOS_REQUIRED_FIELDS,
    )


def load_hours_worked_template(path: Path) -> ET.Element:
    return _load_template(
        path,
        "HoursWorkedFactorVO",
        "HoursWorkedFactorVORow",
        HOURS_WORKED_REQUIRED_FIELDS,
    )


def load_fte_template(path: Path) -> ET.Element:
    return _load_template(
        path,
        "FullTimeEquivalentFactorVO",
        "FullTimeEquivalentFactorVORow",
        FTE_REQUIRED_FIELDS,
    )


LOS_UNITS_LOOKUP = derived_factor_xml._lookup_spec(
    "Length of Service unit", "BEN_TM_UOM", "LosUom"
)
LOS_DETERMINATION_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Length of Service determination rule", "BEN_LOS_DET", "LosDetCd"
)
LOS_PERIOD_START_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Length of Service period start date rule", "BEN_LOS_DT_TO_USE", "LosDtToUseCd"
)
LOS_ROUNDING_LOOKUP = derived_factor_xml._lookup_spec(
    "Length of Service rounding rule", "BEN_RNDG", "RndgCd"
)
HOURS_SOURCE_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Hours Worked source", "BEN_HRS_WKD_SRC", "HrsSrcCd"
)
HOURS_FREQUENCY_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Hours Worked payroll frequency", "BEN_FREQ", "PyrlFreqCd"
)
HOURS_DETERMINATION_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Hours Worked determination rule", "BEN_HRS_WKD_DET", "HrsWkdDetCd"
)
HOURS_ROUNDING_LOOKUP = derived_factor_xml._lookup_spec(
    "Hours Worked rounding rule", "BEN_RNDG", "RndgCd"
)
FTE_ROUNDING_LOOKUP = derived_factor_xml._lookup_spec(
    "Full-Time Equivalent rounding rule", "BEN_RNDG", "RndgCd"
)


def _empty_output(template_root: ET.Element, row_name: str) -> tuple[ET.Element, ET.Element]:
    template_row = next(
        child
        for child in template_root
        if eligibility_xml._local_name(child.tag) == row_name
    )
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == row_name:
            output.remove(child)
    return output, template_row


def _formula_field(
    row: ET.Element, name_field: str, id_field: str, formula_name: str
) -> None:
    derived_factor_xml._remove_child(row, name_field)
    if formula_name:
        derived_factor_xml._set_or_insert_before(
            row, name_field, formula_name, id_field
        )
        eligibility_xml._set_element(row, id_field, "")
    else:
        derived_factor_xml._set_literal_null(row, id_field)


def _validate_formula(
    resolver: eligibility_xml.LookupResolver, formula_name: str
) -> None:
    if formula_name:
        resolver.resolve(derived_factor_xml.FORMULA_LOOKUP, formula_name)


def convert_length_of_service_factors(
    template_root: ET.Element,
    factors: list[LengthOfServiceFactor],
    resolver: eligibility_xml.LookupResolver,
) -> ET.Element:
    output, template_row = _empty_output(
        template_root, "LengthOfServiceFactorVORow"
    )
    for factor in factors:
        row = copy.deepcopy(template_row)
        units = resolver.resolve(LOS_UNITS_LOOKUP, factor.unit_of_measure)["LosUom"]
        determination = resolver.resolve(
            LOS_DETERMINATION_LOOKUP, factor.determination_rule
        )["LosDetCd"]
        period_start = resolver.resolve(
            LOS_PERIOD_START_LOOKUP, factor.period_start_date_rule
        )["LosDtToUseCd"]
        rounding = ""
        if factor.rounding_rule:
            rounding = resolver.resolve(LOS_ROUNDING_LOOKUP, factor.rounding_rule)[
                "RndgCd"
            ]
        _validate_formula(resolver, factor.determination_formula)
        _validate_formula(resolver, factor.rounding_formula)
        values = {
            "ViewInstanceName": "LengthOfServiceFactor",
            "GroupingKey": factor.name,
            "LosDetCd": determination,
            "LosDtToUseCd": period_start,
            "LosUom": units,
            "MnLosNum": factor.minimum_length,
            "MxLosNum": factor.maximum_length,
            "Name": factor.name,
            "NoMnLosNumAplsFlag": "Y",
            "NoMxLosNumAplsFlag": "Y",
            "RndgCd": rounding,
            "UseOveridSvcDtFlag": "Y",
            "LosFactorName": factor.name,
            "LosFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        derived_factor_xml._set_literal_null(row, "ConfigId1")
        derived_factor_xml._set_literal_null(row, "LosCalcRl")
        derived_factor_xml._set_literal_null(row, "LosDtToUseRl")
        _formula_field(
            row,
            "LengthofServiceDeterminationDateFormulaName",
            "LosDetRl",
            factor.determination_formula,
        )
        _formula_field(
            row, "RoundingFormulaName", "RndgRl", factor.rounding_formula
        )
        output.append(row)
    return output


def convert_combined_age_los_factors(
    template_root: ET.Element,
    factors: list[CombinedAgeLosFactor],
    *,
    age_factor_names: set[str],
    los_factor_names: set[str],
) -> ET.Element:
    output, template_row = _empty_output(
        template_root, "CombinedAgeLosFactorVORow"
    )
    for factor in factors:
        if eligibility_xml._exact_text_key(factor.age_factor) not in age_factor_names:
            raise eligibility_xml.ConversionError(
                f"Age and Service factor '{factor.name}' references Age factor "
                f"'{factor.age_factor}', which was not found in the Age worksheet."
            )
        if (
            eligibility_xml._exact_text_key(factor.length_of_service_factor)
            not in los_factor_names
        ):
            raise eligibility_xml.ConversionError(
                f"Age and Service factor '{factor.name}' references Length of Service "
                f"factor '{factor.length_of_service_factor}', which was not found in "
                "the Length of Service worksheet."
            )
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "CombinedAgeLosFactor",
            "GroupingKey": factor.name,
            "CmbndMaxVal": factor.maximum_value,
            "CmbndMinVal": factor.minimum_value,
            "Name": factor.name,
            "CombinedAgeLosFactorName": factor.name,
            "AgeFactorName": factor.age_factor,
            "LosFactorName": factor.length_of_service_factor,
            "AgeFctrId": "",
            "CmbnAgeLosFctrId": "",
            "LosFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        output.append(row)
    return output


def convert_hours_worked_factors(
    template_root: ET.Element,
    factors: list[HoursWorkedFactor],
    resolver: eligibility_xml.LookupResolver,
    *,
    package_benefit_balance_names: set[str] | None = None,
) -> ET.Element:
    output, template_row = _empty_output(template_root, "HoursWorkedFactorVORow")
    for factor in factors:
        source = resolver.resolve(HOURS_SOURCE_LOOKUP, factor.source)["HrsSrcCd"]
        if source != "BNFTBALTYP":
            raise eligibility_xml.ConversionError(
                f"Hours Worked source '{factor.source}' resolved to unsupported code "
                f"{source}; the maintained worksheet and sample require Benefits balance."
            )
        if (
            package_benefit_balance_names is None
            or eligibility_xml._exact_text_key(factor.benefit_balance)
            not in package_benefit_balance_names
        ):
            resolver.resolve(
                derived_factor_xml.BENEFIT_BALANCE_LOOKUP, factor.benefit_balance
            )
        frequency = resolver.resolve(
            HOURS_FREQUENCY_LOOKUP, factor.payroll_frequency
        )["PyrlFreqCd"]
        determination = resolver.resolve(
            HOURS_DETERMINATION_LOOKUP, factor.determination_rule
        )["HrsWkdDetCd"]
        rounding = ""
        if factor.rounding_rule:
            rounding = resolver.resolve(HOURS_ROUNDING_LOOKUP, factor.rounding_rule)[
                "RndgCd"
            ]
        _validate_formula(resolver, factor.determination_formula)
        _validate_formula(resolver, factor.rounding_formula)
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "HoursWorkedFactor",
            "GroupingKey": factor.name,
            "HrsSrcCd": source,
            "HrsWkdDetCd": determination,
            "MnHrsNum": factor.minimum_hours,
            "MxHrsNum": factor.maximum_hours,
            "Name": factor.name,
            "NoMnHrsWkdFlag": "Y",
            "NoMxHrsWkdFlag": "Y",
            "PyrlFreqCd": frequency,
            "RndgCd": rounding,
            "HoursWorkedFactorName": factor.name,
            "BenefitBalanceName": factor.benefit_balance,
            "BnftsBalId": "",
            "HrsWkdInPerdFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        for field in ("HrsAltValToUseCd", "HrsWkdBndryPerdCd", "OnceRCntugCd"):
            element = eligibility_xml._direct_child(row, field, required=False)
            if element is not None:
                eligibility_xml._set_element(row, field, "")
        derived_factor_xml._set_literal_null(row, "DefinedBalanceId")
        derived_factor_xml._set_literal_null(row, "HrsWkdCalcRl")
        _formula_field(
            row,
            "HoursWorkedDeterminationDateFormulaName",
            "HrsWkdDetRl",
            factor.determination_formula,
        )
        _formula_field(
            row, "RoundingFormulaName", "RndgRl", factor.rounding_formula
        )
        output.append(row)
    return output


def convert_fte_factors(
    template_root: ET.Element,
    factors: list[FullTimeEquivalentFactor],
    resolver: eligibility_xml.LookupResolver,
) -> ET.Element:
    output, template_row = _empty_output(
        template_root, "FullTimeEquivalentFactorVORow"
    )
    for factor in factors:
        assignment_key = eligibility_xml._normalized(factor.assignment_to_use)
        primary = assignment_key == "primary assignment"
        assignment_name = (
            "Primary Assignment" if primary else "Sum of all assignments"
        )
        rounding = ""
        if factor.rounding_rule:
            rounding = resolver.resolve(FTE_ROUNDING_LOOKUP, factor.rounding_rule)[
                "RndgCd"
            ]
        _validate_formula(resolver, factor.rounding_formula)
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "FullTimeEquivalentFactor",
            "GroupingKey": factor.name,
            "AssignmentTypeName": assignment_name,
            "MnPctVal": factor.minimum_value,
            "MxPctVal": factor.maximum_value,
            "Name": factor.name,
            "NoMnPctValFlag": "Y",
            "NoMxPctValFlag": "Y",
            "RndgCd": rounding,
            "UsePrmryAsntOnlyFlag": "Y" if primary else "N",
            "UseSumOfAllAsntsFlag": "N" if primary else "Y",
            "FullTimeEquivalentFactorName": factor.name,
            "PctFlTmFctrId": "",
        }
        for field, value in values.items():
            eligibility_xml._set_element(row, field, value)
        _formula_field(
            row, "RoundingFormulaName", "RndgRl", factor.rounding_formula
        )
        output.append(row)
    return output

''')

# ---- excel_to_plan_copy_service_area_xml ----
excel_to_plan_copy_service_area_xml = _component("excel_to_plan_copy_service_area_xml", r'''
#!/usr/bin/env python3
"""Convert Postal Code Ranges and Service Areas worksheets to Plan Copy XML."""

from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_derived_factor_xml as derived_factor_xml  # noqa: E402
import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


POSTAL_CODE_RANGES_SHEET = "Postal Code Ranges"
SERVICE_AREAS_SHEET = "Service Areas"

POSTAL_RANGE_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "StartDate",
    "EndDate",
    "FromValue",
    "ToValue",
    "ZipRange",
    "PostalZipRange",
    "PstlZipRngId",
}
SERVICE_AREA_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "EndDate",
    "Name",
    "OrgUnitPrdct",
    "StartDate",
    "ServiceAreaName",
    "SvcAreaId",
    "PostalZipRangesInServiceAreaVO",
}
SERVICE_AREA_POSTAL_RANGE_REQUIRED_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "StartDate",
    "EndDate",
    "ServiceAreaName",
    "PostalZipRange",
    "SvcAreaPstlZipRngId",
    "SvcAreaId",
    "PstlZipRngId",
}


@dataclass(frozen=True)
class PostalCodeRange:
    from_value: str
    to_value: str
    start_date: str
    end_date: str

    @property
    def name(self) -> str:
        return f"{self.from_value}-{self.to_value}"


@dataclass(frozen=True)
class ServiceAreaPostalRange:
    postal_code_range: str
    start_date: str
    end_date: str


@dataclass(frozen=True)
class ServiceArea:
    name: str
    service_type: str
    start_date: str
    end_date: str
    postal_code_ranges: tuple[ServiceAreaPostalRange, ...]


def _cell(row: tuple[str, ...], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def _required(value: str, *, worksheet: str, row_number: int, field: str) -> str:
    if not value:
        raise eligibility_xml.ConversionError(
            f"{worksheet} worksheet row {row_number} requires {field}."
        )
    return value


def _parse_date(
    value: str, *, worksheet: str, row_number: int, field: str, required: bool
) -> str:
    if not value:
        if required:
            raise eligibility_xml.ConversionError(
                f"{worksheet} worksheet row {row_number} requires {field}."
            )
        return ""
    for pattern in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            pass
    try:
        return date.fromisoformat(value[:10]).isoformat()
    except ValueError as exc:
        raise eligibility_xml.ConversionError(
            f"{worksheet} worksheet row {row_number} has invalid {field} '{value}'; "
            "use YYYY-MM-DD or YYYY/MM/DD."
        ) from exc


def _validate_date_range(
    start_date: str, end_date: str, *, worksheet: str, row_number: int
) -> None:
    if end_date and end_date < start_date:
        raise eligibility_xml.ConversionError(
            f"{worksheet} worksheet row {row_number} has End Date before Start Date."
        )


def _find_postal_header(rows: tuple[tuple[str, ...], ...]) -> int:
    expected = ("from value", "to value", "start date", "end date")
    for row_index, row in enumerate(rows):
        if tuple(eligibility_xml._normalized(value) for value in row[:4]) == expected:
            return row_index
    raise eligibility_xml.ConversionError(
        "No Postal Code Ranges header row was found; expected From Value, To Value, "
        "Start Date, and End Date."
    )


def parse_postal_code_ranges(
    rows: tuple[tuple[str, ...], ...]
) -> list[PostalCodeRange]:
    """Parse and validate unique package-local postal-code ranges."""
    header_index = _find_postal_header(rows)
    ranges: list[PostalCodeRange] = []
    seen: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        from_value = _required(
            _cell(row, 0),
            worksheet=POSTAL_CODE_RANGES_SHEET,
            row_number=row_number,
            field="From Value",
        )
        to_value = _required(
            _cell(row, 1),
            worksheet=POSTAL_CODE_RANGES_SHEET,
            row_number=row_number,
            field="To Value",
        )
        start_date = _parse_date(
            _cell(row, 2),
            worksheet=POSTAL_CODE_RANGES_SHEET,
            row_number=row_number,
            field="Start Date",
            required=True,
        )
        end_date = _parse_date(
            _cell(row, 3),
            worksheet=POSTAL_CODE_RANGES_SHEET,
            row_number=row_number,
            field="End Date",
            required=False,
        )
        _validate_date_range(
            start_date,
            end_date,
            worksheet=POSTAL_CODE_RANGES_SHEET,
            row_number=row_number,
        )
        postal_range = PostalCodeRange(from_value, to_value, start_date, end_date)
        key = eligibility_xml._exact_text_key(postal_range.name)
        if key in seen:
            raise eligibility_xml.ConversionError(
                f"Postal Code Ranges worksheet row {row_number} repeats range "
                f"'{postal_range.name}'."
            )
        seen.add(key)
        ranges.append(postal_range)
    return ranges


def _find_service_area_header(rows: tuple[tuple[str, ...], ...]) -> int:
    expected = (
        "name",
        "service type",
        "start date",
        "end date",
        "from value",
        "to value",
        "start date",
        "end date",
    )
    for row_index, row in enumerate(rows):
        normalized = tuple(eligibility_xml._normalized(value) for value in row[:8])
        if normalized == expected:
            return row_index
    raise eligibility_xml.ConversionError(
        "No Service Areas header row was found; expected Name, Service Type, Start Date, "
        "End Date, From Value, To Value, Start Date, and End Date."
    )


def parse_service_areas(rows: tuple[tuple[str, ...], ...]) -> list[ServiceArea]:
    """Parse service areas and their package-local postal-code-range links."""
    header_index = _find_service_area_header(rows)
    details: dict[str, tuple[str, str, str, str]] = {}
    associations: dict[str, list[ServiceAreaPostalRange]] = {}
    display_names: dict[str, str] = {}
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        name = _required(
            _cell(row, 0),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Name",
        )
        service_type = _required(
            _cell(row, 1),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Service Type",
        )
        start_date = _parse_date(
            _cell(row, 2),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Start Date",
            required=True,
        )
        end_date = _parse_date(
            _cell(row, 3),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="End Date",
            required=False,
        )
        _validate_date_range(
            start_date, end_date, worksheet=SERVICE_AREAS_SHEET, row_number=row_number
        )
        postal_from = _required(
            _cell(row, 4),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Postal Code Ranges From Value",
        )
        postal_to = _required(
            _cell(row, 5),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Postal Code Ranges To Value",
        )
        postal_start_date = _parse_date(
            _cell(row, 6),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Postal Code Ranges Start Date",
            required=True,
        )
        postal_end_date = _parse_date(
            _cell(row, 7),
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
            field="Postal Code Ranges End Date",
            required=False,
        )
        _validate_date_range(
            postal_start_date,
            postal_end_date,
            worksheet=SERVICE_AREAS_SHEET,
            row_number=row_number,
        )
        if postal_start_date < start_date or (end_date and postal_start_date > end_date):
            raise eligibility_xml.ConversionError(
                f"Service Areas worksheet row {row_number} postal-code range start date "
                "must be within the Service Area effective dates."
            )
        if postal_end_date and (postal_end_date < start_date or (end_date and postal_end_date > end_date)):
            raise eligibility_xml.ConversionError(
                f"Service Areas worksheet row {row_number} postal-code range end date "
                "must be within the Service Area effective dates."
            )
        if end_date and not postal_end_date:
            raise eligibility_xml.ConversionError(
                f"Service Areas worksheet row {row_number} requires Postal Code Ranges "
                "End Date when the Service Area has an End Date."
            )
        key = eligibility_xml._exact_text_key(name)
        attributes = (name, service_type, start_date, end_date)
        if key in details and details[key] != attributes:
            raise eligibility_xml.ConversionError(
                f"Service Areas worksheet row {row_number} repeats Service Area '{name}' "
                "with inconsistent Service Type or effective dates."
            )
        details[key] = attributes
        display_names[key] = name
        postal_range = f"{postal_from}-{postal_to}"
        association = ServiceAreaPostalRange(
            postal_range, postal_start_date, postal_end_date
        )
        area_associations = associations.setdefault(key, [])
        if association in area_associations:
            raise eligibility_xml.ConversionError(
                f"Service Areas worksheet row {row_number} repeats postal-code range "
                f"'{postal_range}' for Service Area '{name}'."
            )
        area_associations.append(association)
    return [
        ServiceArea(*details[key], tuple(associations[key]))
        for key in display_names
    ]


def _one_visible_sheet(workbook, sheet_name: str):
    matches = [
        sheet
        for sheet in workbook.sheets
        if eligibility_xml._normalized(sheet.title) == eligibility_xml._normalized(sheet_name)
    ]
    if not matches:
        return None
    if len(matches) != 1:
        raise eligibility_xml.ConversionError(
            f"The workbook must contain exactly one '{sheet_name}' worksheet."
        )
    sheet = matches[0]
    if sheet.state != "visible":
        raise eligibility_xml.ConversionError(f"The '{sheet_name}' worksheet must be visible.")
    return sheet


def read_workbook_service_area_setup(
    path: Path,
) -> tuple[list[PostalCodeRange], list[ServiceArea]]:
    """Read both service-area worksheets from the current Benefits workbook."""
    if path.suffix.casefold() != ".xlsx":
        raise eligibility_xml.ConversionError(
            "The input must be an .xlsx workbook; legacy .xls files are not supported."
        )
    try:
        workbook = eligibility_xml.workbook_io._read_workbook(path)
    except Exception as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits setup workbook {path}: {exc}"
        ) from exc
    postal_ranges = eligibility_xml._parse_optional_sheet(
        _one_visible_sheet(workbook, POSTAL_CODE_RANGES_SHEET), parse_postal_code_ranges
    )
    service_areas = eligibility_xml._parse_optional_sheet(
        _one_visible_sheet(workbook, SERVICE_AREAS_SHEET), parse_service_areas
    )
    validate_service_area_postal_ranges(service_areas, postal_ranges)
    return postal_ranges, service_areas


def validate_service_area_postal_ranges(
    service_areas: list[ServiceArea], postal_ranges: list[PostalCodeRange]
) -> None:
    """Require every service-area link to point at a range in this package."""
    ranges_by_name = {
        eligibility_xml._exact_text_key(postal_range.name): postal_range
        for postal_range in postal_ranges
    }
    for service_area in service_areas:
        for association in service_area.postal_code_ranges:
            range_key = eligibility_xml._exact_text_key(association.postal_code_range)
            postal_range = ranges_by_name.get(range_key)
            if postal_range is None:
                raise eligibility_xml.ConversionError(
                    f"Service Area '{service_area.name}' references postal-code range "
                    f"'{association.postal_code_range}' that is not defined in the "
                    "Postal Code Ranges worksheet."
                )
            if association.start_date < postal_range.start_date or (
                postal_range.end_date and association.start_date > postal_range.end_date
            ):
                raise eligibility_xml.ConversionError(
                    f"Service Area '{service_area.name}' postal-code range "
                    f"'{association.postal_code_range}' starts outside that Postal Code "
                    "Range's effective dates."
                )
            if association.end_date and (
                association.end_date < postal_range.start_date
                or (postal_range.end_date and association.end_date > postal_range.end_date)
            ):
                raise eligibility_xml.ConversionError(
                    f"Service Area '{service_area.name}' postal-code range "
                    f"'{association.postal_code_range}' ends outside that Postal Code "
                    "Range's effective dates."
                )
            if postal_range.end_date and not association.end_date:
                raise eligibility_xml.ConversionError(
                    f"Service Area '{service_area.name}' postal-code range "
                    f"'{association.postal_code_range}' requires an End Date because "
                    "the referenced Postal Code Range has an End Date."
                )


def _load_template(
    path: Path, root_name: str, row_name: str, required_fields: set[str]
) -> tuple[ET.Element, ET.Element]:
    root, rows = derived_factor_xml._template_rows(path, root_name, row_name)
    fields = {eligibility_xml._local_name(child.tag) for child in rows[0]}
    missing = sorted(required_fields - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            f"{root_name} sample row is missing: " + ", ".join(missing)
        )
    return root, rows[0]


def load_postal_code_range_template(path: Path) -> ET.Element:
    root, _ = _load_template(
        path,
        "PostalZipRangeVO",
        "PostalZipRangeVORow",
        POSTAL_RANGE_REQUIRED_FIELDS,
    )
    return root


def load_service_area_template(path: Path) -> ET.Element:
    root, row = _load_template(
        path,
        "ServiceAreaVO",
        "ServiceAreaVORow",
        SERVICE_AREA_REQUIRED_FIELDS,
    )
    child_container = eligibility_xml._direct_child(row, "PostalZipRangesInServiceAreaVO")
    assert child_container is not None
    child_rows = [
        child
        for child in child_container
        if eligibility_xml._local_name(child.tag) == "PostalZipRangesInServiceAreaVORow"
    ]
    if not child_rows:
        raise eligibility_xml.ConversionError(
            "ServiceArea sample has no PostalZipRangesInServiceAreaVORow."
        )
    fields = {eligibility_xml._local_name(child.tag) for child in child_rows[0]}
    missing = sorted(SERVICE_AREA_POSTAL_RANGE_REQUIRED_FIELDS - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            "ServiceArea postal-code range sample row is missing: " + ", ".join(missing)
        )
    return root


SERVICE_TYPE_LOOKUP = derived_factor_xml._hcm_standard_lookup_spec(
    "Service Area service type", "BEN_PRDCT", "OrgUnitPrdct"
)


def _empty_output(template_root: ET.Element, row_name: str) -> tuple[ET.Element, ET.Element]:
    template_row = next(
        child for child in template_root if eligibility_xml._local_name(child.tag) == row_name
    )
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == row_name:
            output.remove(child)
    return output, template_row


def convert_postal_code_ranges(
    template_root: ET.Element, postal_ranges: list[PostalCodeRange]
) -> ET.Element:
    """Clone the exported postal-code range row for every validated range."""
    output, template_row = _empty_output(template_root, "PostalZipRangeVORow")
    for postal_range in postal_ranges:
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "PostalCodeRange",
            "GroupingKey": postal_range.name,
            "StartDate": postal_range.start_date,
            "EndDate": postal_range.end_date,
            "FromValue": postal_range.from_value,
            "ToValue": postal_range.to_value,
            "ZipRange": postal_range.name,
            "PostalZipRange": postal_range.name,
            "PstlZipRngId": "",
        }
        for field_name, value in values.items():
            eligibility_xml._set_element(row, field_name, value)
        output.append(row)
    return output


def convert_service_areas(
    template_root: ET.Element,
    service_areas: list[ServiceArea],
    resolver: eligibility_xml.LookupResolver,
) -> ET.Element:
    """Render service areas and their package-local postal-code-range links."""
    output, template_row = _empty_output(template_root, "ServiceAreaVORow")
    for service_area in service_areas:
        row = copy.deepcopy(template_row)
        service_type = resolver.resolve(SERVICE_TYPE_LOOKUP, service_area.service_type)[
            "OrgUnitPrdct"
        ]
        values = {
            "ViewInstanceName": "ServiceArea",
            "GroupingKey": service_area.name,
            "EndDate": service_area.end_date,
            "Name": service_area.name,
            "OrgUnitPrdct": service_type,
            "StartDate": service_area.start_date,
            "ServiceAreaName": service_area.name,
            "SvcAreaId": "",
        }
        for field_name, value in values.items():
            eligibility_xml._set_element(row, field_name, value)

        container = eligibility_xml._direct_child(row, "PostalZipRangesInServiceAreaVO")
        assert container is not None
        child_template = next(
            child
            for child in container
            if eligibility_xml._local_name(child.tag)
            == "PostalZipRangesInServiceAreaVORow"
        )
        for child in list(container):
            if eligibility_xml._local_name(child.tag) == "PostalZipRangesInServiceAreaVORow":
                container.remove(child)
        for association in service_area.postal_code_ranges:
            child = copy.deepcopy(child_template)
            child_values = {
                "ViewInstanceName": "PostalCodeRangesInServiceArea",
                "GroupingKey": f"{association.postal_code_range},{service_area.name}",
                "StartDate": association.start_date,
                "EndDate": association.end_date,
                "ServiceAreaName": service_area.name,
                "PostalZipRange": association.postal_code_range,
                "SvcAreaPstlZipRngId": "",
                "SvcAreaId": "",
                "PstlZipRngId": "",
            }
            for field_name, value in child_values.items():
                eligibility_xml._set_element(child, field_name, value)
            container.append(child)
        output.append(row)
    return output

''')

# ---- excel_to_plan_copy_map_xml ----
excel_to_plan_copy_map_xml = _component("excel_to_plan_copy_map_xml", r'''
#!/usr/bin/env python3
"""Generate BEN_PL_COPY_MAP.xml from an eligibility-profile workbook."""

from __future__ import annotations

import argparse
from collections import OrderedDict
import copy
import csv
from dataclasses import dataclass
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


SKILL_ROOT = SCRIPT_DIR.parent
RULES_PATH = SKILL_ROOT / "references" / "plan-copy-map-criteria.json"
LOOKUP_MAPPINGS_PATH = SKILL_ROOT / "references" / "criterion-lookup-mappings.json"
MAP_ATTRIBUTES = tuple(f"MapAttribute{number}" for number in range(1, 6))
REQUIRED_TEMPLATE_FIELDS = {
    "ViewInstanceName",
    "ColumnName",
    "CompObjId",
    "CompObjType",
    "SrcId",
    "SrcName",
    "SrcTableName",
    "TableName",
    "TrgId",
    "TrgName",
    "PlanCopyName",
}


@dataclass(frozen=True)
class PlanCopyCriterionSpec:
    criterion: str
    reference_criterion: str
    table_name: str
    column_name: str
    source_table_name: str
    resolver_key: str
    lookup_mapping: eligibility_xml.LookupSpec
    literal_fields: tuple[tuple[str, str], ...]
    input_source: str = "eligibility_criterion"


@dataclass(frozen=True)
class PlanCopyMapContract:
    component_object_id: str
    component_object_type: str
    criteria: tuple[PlanCopyCriterionSpec, ...]


def _read_json(path: Path, description: str) -> dict[str, object]:
    try:
        payload = json.loads(eligibility_xml.read_contract_bytes(path))
    except OSError as exc:
        raise eligibility_xml.ConversionError(f"Unable to read {description} {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise eligibility_xml.ConversionError(f"{description.capitalize()} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise eligibility_xml.ConversionError(f"{description.capitalize()} must be a JSON object.")
    return payload


def _read_csv_index(path: Path, key: str) -> dict[str, dict[str, str]]:
    try:
        if not path.exists():
            catalog_path = path.parent / "mapping-reference.json"
            catalog = _read_json(catalog_path, "Consolidated mapping reference")
            if catalog.get("version") != 1:
                raise eligibility_xml.ConversionError("Mapping reference requires version 1.")
            rows = catalog.get(path.stem.replace("-", "_"))
            if not isinstance(rows, list) or not rows:
                raise eligibility_xml.ConversionError(f"Missing or empty mapping section: {path.stem}")
            if any(not isinstance(row, dict) or key not in row or any(
                not isinstance(name, str) or not isinstance(value, str)
                for name, value in row.items()
            ) for row in rows):
                raise eligibility_xml.ConversionError(f"Invalid mapping section: {path.stem}")
        else:
            with path.open(encoding="utf-8-sig", newline="") as handle:
                reader = csv.DictReader(handle)
                if reader.fieldnames is None or key not in reader.fieldnames:
                    raise eligibility_xml.ConversionError(
                        f"Mapping reference {path.name} has no {key} column."
                    )
                rows = list(reader)
    except OSError as exc:
        raise eligibility_xml.ConversionError(f"Unable to read mapping reference {path}: {exc}") from exc
    indexed: dict[str, dict[str, str]] = {}
    for row_number, row in enumerate(rows, 2):
        value = (row.get(key) or "").strip()
        if not value:
            raise eligibility_xml.ConversionError(
                f"Mapping reference {path.name} row {row_number} has no {key}."
            )
        if value in indexed:
            raise eligibility_xml.ConversionError(
                f"Mapping reference {path.name} contains duplicate {key} '{value}'."
            )
        indexed[value] = {name: (cell or "").strip() for name, cell in row.items() if name}
    return indexed


def _required_text(raw: dict[str, object], name: str, context: str) -> str:
    value = raw.get(name)
    if not isinstance(value, str) or not value.strip():
        raise eligibility_xml.ConversionError(f"{context} requires a non-empty {name}.")
    return value.strip()


def _string_pairs(raw: object, name: str, context: str) -> tuple[tuple[str, str], ...]:
    if raw is None:
        return ()
    if not isinstance(raw, dict) or any(
        not isinstance(key, str)
        or not key.strip()
        or not isinstance(value, str)
        or not value.strip()
        for key, value in raw.items()
    ):
        raise eligibility_xml.ConversionError(f"{context} {name} must contain string pairs.")
    return tuple((key.strip(), value.strip()) for key, value in raw.items())


def load_plan_copy_map_contract(
    mapping_reference_dir: Path,
    *,
    rules_path: Path = RULES_PATH,
    lookup_mappings_path: Path = LOOKUP_MAPPINGS_PATH,
) -> PlanCopyMapContract:
    """Join maintained mapping catalogs to the workbook-to-map declarations."""
    rules = _read_json(rules_path, "Plan Copy map rules")
    if rules.get("version") != 1:
        raise eligibility_xml.ConversionError("Plan Copy map rules must use schema version 1.")
    component_object_id = _required_text(rules, "component_object_id", "Plan Copy map rules")
    component_object_type = _required_text(rules, "component_object_type", "Plan Copy map rules")
    if not component_object_id.isdigit():
        raise eligibility_xml.ConversionError("Plan Copy map component_object_id must be numeric.")
    if component_object_type != "ELIG":
        raise eligibility_xml.ConversionError("Plan Copy map component_object_type must be ELIG.")
    raw_criteria = rules.get("criteria")
    if not isinstance(raw_criteria, dict) or not raw_criteria:
        raise eligibility_xml.ConversionError("Plan Copy map rules require a criteria object.")

    criteria_rows = _read_csv_index(mapping_reference_dir / "criteria-mapping.csv", "criterion")
    link_rows = _read_csv_index(mapping_reference_dir / "criteria-resolver-links.csv", "criterion")
    resolver_rows = _read_csv_index(mapping_reference_dir / "rest-api-resolvers.csv", "resolver_key")
    lookup_mappings = eligibility_xml.load_lookup_mappings(lookup_mappings_path)
    specs: list[PlanCopyCriterionSpec] = []

    for criterion, raw_rule in raw_criteria.items():
        context = f"Plan Copy map criterion '{criterion}'"
        if not isinstance(criterion, str) or not criterion.strip() or not isinstance(raw_rule, dict):
            raise eligibility_xml.ConversionError("Each Plan Copy map criterion must be a named object.")
        criterion = criterion.strip()
        reference_criterion = _required_text(raw_rule, "reference_criterion", context)
        display_field = _required_text(raw_rule, "display_field", context)
        input_source = str(raw_rule.get("input_source") or "eligibility_criterion").strip()
        if input_source not in {
            "eligibility_criterion",
            "benefit_group_legal_employer",
            "benefit_balance_legal_employer",
        }:
            raise eligibility_xml.ConversionError(
                f"{context} has unsupported input_source '{input_source}'."
            )
        expected_classification = str(
            raw_rule.get("classification") or "REQUIRED"
        ).strip()
        if expected_classification not in {"REQUIRED", "CONDITIONAL"}:
            raise eligibility_xml.ConversionError(
                f"{context} classification must be REQUIRED or CONDITIONAL."
            )
        lookup_criterion = str(raw_rule.get("lookup_criterion") or criterion).strip()
        if not lookup_criterion:
            raise eligibility_xml.ConversionError(
                f"{context} requires a non-empty lookup_criterion."
            )
        attribute_fields = _string_pairs(raw_rule.get("attribute_fields"), "attribute_fields", context)
        literal_fields = _string_pairs(raw_rule.get("literal_fields"), "literal_fields", context)
        if any(name not in MAP_ATTRIBUTES for name, _ in (*attribute_fields, *literal_fields)):
            raise eligibility_xml.ConversionError(
                f"{context} may set only MapAttribute1 through MapAttribute5."
            )
        if set(dict(attribute_fields)).intersection(dict(literal_fields)):
            raise eligibility_xml.ConversionError(f"{context} repeats a dynamic and literal field.")

        criterion_row = criteria_rows.get(reference_criterion)
        link_row = link_rows.get(reference_criterion)
        if criterion_row is None or link_row is None:
            raise eligibility_xml.ConversionError(
                f"{context} is absent from the maintained criterion/link catalogs."
            )
        if criterion_row.get("classification") != expected_classification:
            raise eligibility_xml.ConversionError(
                f"{context} must be classified {expected_classification}."
            )
        resolver_key = link_row.get("resolver_key", "")
        resolver_row = resolver_rows.get(resolver_key)
        if resolver_row is None:
            raise eligibility_xml.ConversionError(
                f"{context} references missing resolver_key '{resolver_key}'."
            )
        table_name = criterion_row.get("criterion_table", "")
        source_table_name = criterion_row.get("target_reference", "")
        catalog_column = criterion_row.get("source_column", "")
        column_name = str(raw_rule.get("column_name") or catalog_column).strip()
        allowed_columns = {part.strip() for part in catalog_column.split("/") if part.strip()}
        if not table_name or not source_table_name or column_name not in allowed_columns:
            raise eligibility_xml.ConversionError(
                f"{context} has inconsistent table or column metadata."
            )
        if (
            link_row.get("criterion_table") != table_name
            or link_row.get("source_column") != catalog_column
        ):
            raise eligibility_xml.ConversionError(f"{context} disagrees with criteria-resolver-links.csv.")

        lookup_mapping = lookup_mappings.get(
            eligibility_xml._normalized(lookup_criterion)
        )
        if lookup_mapping is None:
            raise eligibility_xml.ConversionError(f"{context} has no Fusion lookup declaration.")
        resolver_path = resolver_row.get("path", "")
        if resolver_path != lookup_mapping.endpoint:
            raise eligibility_xml.ConversionError(
                f"{context} endpoint differs between lookup and resolver catalogs."
            )
        result_id = resolver_row.get("result_id", "")
        if not result_id:
            raise eligibility_xml.ConversionError(f"{context} resolver has no result_id.")
        target_fields = (
            ("SrcId", result_id),
            ("SrcName", display_field),
            ("TrgId", result_id),
            ("TrgName", display_field),
            *attribute_fields,
        )
        map_lookup = eligibility_xml.LookupSpec(
            criterion=criterion,
            endpoint=lookup_mapping.endpoint,
            catalog=lookup_mapping.catalog,
            source_fields=lookup_mapping.source_fields,
            target_fields=target_fields,
            query=lookup_mapping.query,
            required_values=lookup_mapping.required_values,
            multiple_match_policy=lookup_mapping.multiple_match_policy,
        )
        specs.append(
            PlanCopyCriterionSpec(
                criterion=criterion,
                reference_criterion=reference_criterion,
                table_name=table_name,
                column_name=column_name,
                source_table_name=source_table_name,
                resolver_key=resolver_key,
                lookup_mapping=map_lookup,
                literal_fields=literal_fields,
                input_source=input_source,
            )
        )
    return PlanCopyMapContract(component_object_id, component_object_type, tuple(specs))


def _local_name(element: ET.Element) -> str:
    return eligibility_xml._local_name(element.tag)


def _child_text(parent: ET.Element, name: str) -> str:
    child = eligibility_xml._direct_child(parent, name)
    assert child is not None
    return (child.text or "").strip()


def load_map_template(path: Path) -> ET.Element:
    try:
        root = ET.fromstring(eligibility_xml.read_template_bytes(path))
    except OSError as exc:
        raise eligibility_xml.ConversionError(f"Unable to read Plan Copy map sample {path}: {exc}") from exc
    except ET.ParseError as exc:
        raise eligibility_xml.ConversionError(f"Plan Copy map sample is not well formed: {exc}") from exc
    if _local_name(root) != "PlanCopyMapVO":
        raise eligibility_xml.ConversionError("Plan Copy map sample root must be PlanCopyMapVO.")
    rows = [child for child in root if _local_name(child) == "PlanCopyMapVORow"]
    if not rows:
        raise eligibility_xml.ConversionError("Plan Copy map sample has no PlanCopyMapVORow.")
    for row in rows:
        fields = {_local_name(child) for child in row}
        missing = sorted(REQUIRED_TEMPLATE_FIELDS - fields)
        if missing:
            raise eligibility_xml.ConversionError(
                "Plan Copy map sample row is missing: " + ", ".join(missing)
            )
    return root


def _template_row(root: ET.Element, spec: PlanCopyCriterionSpec, display_name: str) -> ET.Element:
    candidates = [
        row
        for row in root
        if _local_name(row) == "PlanCopyMapVORow"
        and _child_text(row, "ColumnName") == spec.column_name
        and _child_text(row, "SrcTableName") == spec.source_table_name
        and _child_text(row, "TableName") == spec.table_name
    ]
    if not candidates:
        # Plan Copy map rows have a shared schema. Reuse the exported row for
        # the same referenced source and column when a new setup object has no
        # dedicated sample row; fixed fields below set its target table.
        candidates = [
            row
            for row in root
            if _local_name(row) == "PlanCopyMapVORow"
            and _child_text(row, "ColumnName") == spec.column_name
            and _child_text(row, "SrcTableName") == spec.source_table_name
        ]
    if not candidates:
        raise eligibility_xml.ConversionError(
            f"Plan Copy map sample has no row template for {spec.criterion}."
        )
    for row in candidates:
        if eligibility_xml._exact_text_key(_child_text(row, "SrcName")) == eligibility_xml._exact_text_key(display_name):
            return row
    return candidates[0]


def convert_plan_copy_map(
    template_root: ET.Element,
    profiles: list[eligibility_xml.Profile],
    contract: PlanCopyMapContract,
    resolver: eligibility_xml.LookupResolver,
    *,
    benefit_group_legal_employers: tuple[str, ...] = (),
    benefit_balance_legal_employers: tuple[str, ...] = (),
    component_object_id: str | None = None,
) -> ET.Element:
    resolved_component_id = component_object_id or contract.component_object_id
    if not resolved_component_id.isdigit():
        raise eligibility_xml.ConversionError("Component object ID must be numeric.")
    values_by_criterion: OrderedDict[str, list[eligibility_xml.Criterion]] = OrderedDict()
    seen: set[tuple[str, str]] = set()
    for profile in profiles:
        for criterion in profile.criteria:
            criterion_key = eligibility_xml._normalized(criterion.kind)
            value_key = (criterion_key, eligibility_xml._exact_text_key(criterion.name))
            if value_key in seen:
                continue
            seen.add(value_key)
            values_by_criterion.setdefault(criterion_key, []).append(criterion)
    def unique_legal_employers(values: tuple[str, ...]) -> list[str]:
        resolved_values: list[str] = []
        seen_values: set[str] = set()
        for legal_employer in values:
            normalized_name = eligibility_xml._exact_text_key(legal_employer)
            if not legal_employer.strip() or normalized_name in seen_values:
                continue
            seen_values.add(normalized_name)
            resolved_values.append(legal_employer.strip())
        return resolved_values

    benefit_group_values = unique_legal_employers(benefit_group_legal_employers)
    benefit_balance_values = unique_legal_employers(benefit_balance_legal_employers)

    output = copy.deepcopy(template_root)
    for child in list(output):
        if _local_name(child) == "PlanCopyMapVORow":
            output.remove(child)
    emitted_mapping_keys: set[tuple[str, ...]] = set()
    for spec in contract.criteria:
        if spec.input_source == "benefit_group_legal_employer":
            source_values = [
                eligibility_xml.Criterion(spec.criterion, "", value, "N")
                for value in benefit_group_values
            ]
        elif spec.input_source == "benefit_balance_legal_employer":
            source_values = [
                eligibility_xml.Criterion(spec.criterion, "", value, "N")
                for value in benefit_balance_values
            ]
        else:
            source_values = values_by_criterion.get(
                eligibility_xml._normalized(spec.criterion), []
            )
        for criterion in source_values:
            values = resolver.resolve(spec.lookup_mapping, criterion.name)
            template_row = _template_row(template_root, spec, values["SrcName"])
            row = copy.deepcopy(template_row)
            for attribute in MAP_ATTRIBUTES:
                eligibility_xml._set_element(row, attribute, "")
            fixed_fields = {
                "ViewInstanceName": "PlanCopyMap",
                "ColumnName": spec.column_name,
                "CompObjId": resolved_component_id,
                "CompObjType": contract.component_object_type,
                "SrcId": values["SrcId"],
                "SrcName": values["SrcName"],
                "SrcTableName": spec.source_table_name,
                "TableName": spec.table_name,
                "TrgId": values["TrgId"],
                "TrgName": values["TrgName"],
            }
            for field_name, value in (*fixed_fields.items(), *spec.literal_fields):
                eligibility_xml._set_element(row, field_name, value)
            for attribute in MAP_ATTRIBUTES:
                if attribute in values:
                    eligibility_xml._set_element(row, attribute, values[attribute])
            logical_mapping_key = tuple(
                _child_text(row, field)
                for field in ("SrcTableName", "SrcId", "SrcName", *MAP_ATTRIBUTES)
            )
            if logical_mapping_key in emitted_mapping_keys:
                continue
            emitted_mapping_keys.add(logical_mapping_key)
            output.append(row)
    # Criteria and supporting setup without target IDs need no mapping rows.
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate BEN_PL_COPY_MAP.xml from Fusion_Elpro_Setup.xlsx, a Plan Copy "
            "map sample, maintained mapping catalogs, and read-only Fusion lookups."
        )
    )
    parser.add_argument(
        "--input", type=Path, required=True, help="Fusion_Elpro_Setup.xlsx workbook."
    )
    parser.add_argument("--sample", type=Path, required=True, help="Oracle-exported BEN_PL_COPY_MAP.xml sample.")
    parser.add_argument(
        "--mapping-reference-dir",
        type=Path,
        required=True,
        help="Directory containing mapping-reference.json (or custom legacy CSV catalogs).",
    )
    parser.add_argument("--output", type=Path, required=True, help="Destination BEN_PL_COPY_MAP.xml.")
    parser.add_argument("--force", action="store_true", help="Replace an existing output file.")
    parser.add_argument(
        "--component-object-id",
        help="Override the static component object ID declared by the maintained map rules.",
    )
    parser.add_argument(
        "--properties",
        type=Path,
        default=eligibility_xml.rest_client_common.DEFAULT_PROPERTIES_PATH,
        help="Fusion OAuth environment properties file.",
    )
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        input_path = args.input.resolve()
        sample_path = args.sample.resolve()
        output_path = args.output.resolve()
        if output_path in {input_path, sample_path}:
            raise eligibility_xml.ConversionError("Output must not replace the workbook or sample XML.")
        profiles = eligibility_xml.read_workbook_profiles(input_path)
        template = load_map_template(sample_path)
        contract = load_plan_copy_map_contract(args.mapping_reference_dir.resolve())
        resolver = eligibility_xml.FusionLookupResolver(
            properties_path=args.properties.resolve(),
            token_cache=args.token_cache,
            open_browser=not args.no_open_browser,
        )
        converted = convert_plan_copy_map(
            template,
            profiles,
            contract,
            resolver,
            benefit_group_legal_employers=(),
            benefit_balance_legal_employers=(),
            component_object_id=args.component_object_id,
        )
        eligibility_xml.write_xml(converted, output_path, force=args.force)
        row_count = sum(1 for child in converted if _local_name(child) == "PlanCopyMapVORow")
        print(f"Generated {output_path} with {row_count} Plan Copy mapping row(s).")
        print("No ZIP package or checksum was created or modified.")
        return 0
    except eligibility_xml.ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- excel_to_plan_copy_benefits_group_xml ----
excel_to_plan_copy_benefits_group_xml = _component("excel_to_plan_copy_benefits_group_xml", r'''
#!/usr/bin/env python3
"""Convert the Benefit Groups worksheet into Oracle Plan Copy XML."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


SHEET_NAME = "Benefit Groups"
REQUIRED_TEMPLATE_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "BngDesc",
    "Name",
    "BenefitsGroupName",
    "LegalEntityName",
    "BenftsGrpId",
    "LegalEntityId",
}


@dataclass(frozen=True)
class BenefitGroup:
    name: str
    description: str
    legal_employer: str


def _cell(row: tuple[str, ...], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def _find_header(rows: tuple[tuple[str, ...], ...]) -> tuple[int, dict[str, int]]:
    expected = {
        "benefits group name": "name",
        "benefits group description": "description",
        "legal employer": "legal_employer",
    }
    for row_index, row in enumerate(rows):
        normalized = [eligibility_xml._normalized(value) for value in row]
        if all(header in normalized for header in expected):
            return row_index, {
                field: normalized.index(header) for header, field in expected.items()
            }
    raise eligibility_xml.ConversionError(
        "No Benefit Groups header row was found; expected Benefits Group Name, "
        "Benefits Group Description, and Legal Employer columns."
    )


def parse_benefit_groups(rows: tuple[tuple[str, ...], ...]) -> list[BenefitGroup]:
    """Parse Benefit Groups rows and reject incomplete or duplicate records."""
    header_index, columns = _find_header(rows)
    groups: list[BenefitGroup] = []
    seen_names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        name = _cell(row, columns["name"])
        description = _cell(row, columns["description"])
        legal_employer = _cell(row, columns["legal_employer"])
        if not name:
            raise eligibility_xml.ConversionError(
                f"Benefit Groups row {row_number} requires Benefits Group Name."
            )
        name_key = eligibility_xml._exact_text_key(name)
        if name_key in seen_names:
            raise eligibility_xml.ConversionError(
                f"Benefit Groups row {row_number} repeats Benefits Group Name '{name}'."
            )
        seen_names.add(name_key)
        groups.append(BenefitGroup(name, description, legal_employer))
    if not groups:
        raise eligibility_xml.ConversionError(
            "The Benefit Groups worksheet contains no benefit group rows."
        )
    return groups


def read_workbook_benefit_groups(path: Path) -> list[BenefitGroup]:
    if path.suffix.casefold() != ".xlsx":
        raise eligibility_xml.ConversionError(
            "The input must be an .xlsx workbook; legacy .xls files are not supported."
        )
    try:
        workbook = eligibility_xml.workbook_io._read_workbook(path)
    except Exception as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits setup workbook {path}: {exc}"
        ) from exc
    matches = [
        sheet
        for sheet in workbook.sheets
        if eligibility_xml._normalized(sheet.title)
        == eligibility_xml._normalized(SHEET_NAME)
    ]
    if len(matches) != 1:
        raise eligibility_xml.ConversionError(
            f"The workbook must contain exactly one '{SHEET_NAME}' worksheet."
        )
    sheet = matches[0]
    if sheet.state != "visible":
        raise eligibility_xml.ConversionError(
            f"The '{SHEET_NAME}' worksheet must be visible."
        )
    return parse_benefit_groups(sheet.rows)


def load_template(path: Path) -> ET.Element:
    try:
        root = ET.fromstring(eligibility_xml.read_template_bytes(path))
    except OSError as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits Group sample {path}: {exc}"
        ) from exc
    except ET.ParseError as exc:
        raise eligibility_xml.ConversionError(
            f"Benefits Group sample is not well formed: {exc}"
        ) from exc
    if eligibility_xml._local_name(root.tag) != "BenefitsGroupVO":
        raise eligibility_xml.ConversionError(
            "Benefits Group sample root must be BenefitsGroupVO."
        )
    rows = [
        child
        for child in root
        if eligibility_xml._local_name(child.tag) == "BenefitsGroupVORow"
    ]
    if not rows:
        raise eligibility_xml.ConversionError(
            "Benefits Group sample has no BenefitsGroupVORow."
        )
    fields = {eligibility_xml._local_name(child.tag) for child in rows[0]}
    missing = sorted(REQUIRED_TEMPLATE_FIELDS - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            "Benefits Group sample row is missing: " + ", ".join(missing)
        )
    return root


def convert_benefit_groups(
    template_root: ET.Element, groups: list[BenefitGroup]
) -> ET.Element:
    """Clone the exported row shape for every validated workbook group."""
    template_row = next(
        child
        for child in template_root
        if eligibility_xml._local_name(child.tag) == "BenefitsGroupVORow"
    )
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == "BenefitsGroupVORow":
            output.remove(child)
    for group in groups:
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "BenefitsGroup",
            "GroupingKey": group.name,
            "BngDesc": group.description,
            "Name": group.name,
            "BenefitsGroupName": group.name,
            "LegalEntityName": group.legal_employer,
            "BenftsGrpId": "",
            "LegalEntityId": "",
        }
        for field_name, value in values.items():
            eligibility_xml._set_element(row, field_name, value)
        output.append(row)
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the Benefit Groups worksheet in Fusion_Benefits_Setup.xlsx "
            "into BEN_BENFTS_GRP.xml."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--sample", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--force", action="store_true", help="Replace an existing output file."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        input_path = args.input.resolve()
        sample_path = args.sample.resolve()
        output_path = args.output.resolve()
        if output_path in {input_path, sample_path}:
            raise eligibility_xml.ConversionError(
                "Output must not replace the workbook or Benefits Group sample."
            )
        groups = read_workbook_benefit_groups(input_path)
        converted = convert_benefit_groups(load_template(sample_path), groups)
        eligibility_xml.write_xml(converted, output_path, force=args.force)
        print(f"Generated {output_path} with {len(groups)} benefit group(s).")
        print("No ZIP package or checksum was created or modified.")
        return 0
    except eligibility_xml.ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- excel_to_plan_copy_benefit_balance_xml ----
excel_to_plan_copy_benefit_balance_xml = _component("excel_to_plan_copy_benefit_balance_xml", r'''
#!/usr/bin/env python3
"""Convert the Benefit Balances worksheet into Oracle Plan Copy XML."""

from __future__ import annotations

import argparse
import copy
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402


SHEET_NAME = "Benefit Balances"
GENERIC_LOOKUP_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/genericLookups"
CURRENCY_ENDPOINT = "/fscmRestApi/resources/11.13.18.05/currenciesLOV"
REQUIRED_TEMPLATE_FIELDS = {
    "ViewInstanceName",
    "GroupingKey",
    "LogicalStartDate",
    "LogicalEndDate",
    "EffectiveStartDate",
    "EffectiveEndDate",
    "BnftsBalDesc",
    "BnftsBalUsgCd",
    "Name",
    "NnmntryUom",
    "Uom",
    "SrcName",
    "BenefitBalanceName",
    "LegalEntityName",
    "BnftsBalId",
    "LegalEntityId",
}


@dataclass(frozen=True)
class BenefitBalance:
    session_effective_date: str
    effective_start_date: str
    effective_end_date: str
    name: str
    description: str
    legal_employer: str
    currency: str
    nonmonetary_units: str
    balance_usage: str


def _cell(row: tuple[str, ...], index: int) -> str:
    return row[index].strip() if index < len(row) else ""


def _parse_date(value: str, *, row_number: int, field: str) -> str:
    if not value:
        raise eligibility_xml.ConversionError(
            f"Benefit Balances worksheet row {row_number} requires {field}."
        )
    for pattern in ("%Y-%m-%d", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, pattern).date().isoformat()
        except ValueError:
            pass
    try:
        return date.fromisoformat(value[:10]).isoformat()
    except ValueError as exc:
        raise eligibility_xml.ConversionError(
            f"Benefit Balances worksheet row {row_number} has invalid {field} "
            f"'{value}'; use YYYY-MM-DD or YYYY/MM/DD."
        ) from exc


def _find_header(rows: tuple[tuple[str, ...], ...]) -> tuple[int, dict[str, int]]:
    expected = {
        "session effective date": "session_effective_date",
        "effective start date": "effective_start_date",
        "effective end date": "effective_end_date",
        "benefit balance": "name",
        "description": "description",
        "legal employer": "legal_employer",
        "currency": "currency",
        "nonmonetary units": "nonmonetary_units",
        "balance usage": "balance_usage",
    }
    for row_index, row in enumerate(rows):
        normalized = [eligibility_xml._normalized(value) for value in row]
        if all(header in normalized for header in expected):
            return row_index, {
                field: normalized.index(header) for header, field in expected.items()
            }
    raise eligibility_xml.ConversionError(
        "No Benefit Balances header row was found; expected Session Effective Date, "
        "Effective Start Date, Effective End Date, Benefit Balance, Description, "
        "Legal Employer, Currency, Nonmonetary Units, and Balance Usage columns."
    )


def parse_benefit_balances(rows: tuple[tuple[str, ...], ...]) -> list[BenefitBalance]:
    """Parse Benefit Balances and reject ambiguous or invalid effective-dated rows."""
    header_index, columns = _find_header(rows)
    balances: list[BenefitBalance] = []
    seen_names: set[str] = set()
    for row_number, row in enumerate(rows[header_index + 1 :], header_index + 2):
        if not any(value.strip() for value in row):
            continue
        values = {field: _cell(row, index) for field, index in columns.items()}
        for field, label in (("name", "Benefit Balance"), ("balance_usage", "Balance Usage")):
            if not values[field]:
                raise eligibility_xml.ConversionError(
                    f"Benefit Balances worksheet row {row_number} requires {label}."
                )
        if values["currency"] and values["nonmonetary_units"]:
            raise eligibility_xml.ConversionError(
                f"Benefit Balances worksheet row {row_number} must provide Currency "
                "or Nonmonetary Units, not both."
            )
        session_date = _parse_date(
            values["session_effective_date"],
            row_number=row_number,
            field="Session Effective Date",
        )
        start_date = _parse_date(
            values["effective_start_date"],
            row_number=row_number,
            field="Effective Start Date",
        )
        end_date = _parse_date(
            values["effective_end_date"],
            row_number=row_number,
            field="Effective End Date",
        )
        if end_date < start_date:
            raise eligibility_xml.ConversionError(
                f"Benefit Balances worksheet row {row_number} has Effective End Date "
                "before Effective Start Date."
            )
        if not start_date <= session_date <= end_date:
            raise eligibility_xml.ConversionError(
                f"Benefit Balances worksheet row {row_number} has Session Effective Date "
                "outside the effective-date range."
            )
        name_key = eligibility_xml._exact_text_key(values["name"])
        if name_key in seen_names:
            raise eligibility_xml.ConversionError(
                f"Benefit Balances worksheet row {row_number} repeats Benefit Balance "
                f"'{values['name']}'."
            )
        seen_names.add(name_key)
        balances.append(
            BenefitBalance(
                session_date,
                start_date,
                end_date,
                values["name"],
                values["description"],
                values["legal_employer"],
                values["currency"],
                values["nonmonetary_units"],
                values["balance_usage"],
            )
        )
    if not balances:
        raise eligibility_xml.ConversionError(
            "The Benefit Balances worksheet contains no Benefit Balance rows."
        )
    return balances


def common_session_effective_date(balances: list[BenefitBalance]) -> str:
    """Return the one Plan Copy effective date shared by all balance rows."""
    session_dates = sorted({balance.session_effective_date for balance in balances})
    if len(session_dates) != 1:
        raise eligibility_xml.ConversionError(
            "All Benefit Balances worksheet rows must use the same Session Effective Date "
            "for the Plan Copy import."
        )
    return session_dates[0]


def read_workbook_benefit_balances(path: Path) -> list[BenefitBalance]:
    if path.suffix.casefold() != ".xlsx":
        raise eligibility_xml.ConversionError(
            "The input must be an .xlsx workbook; legacy .xls files are not supported."
        )
    try:
        workbook = eligibility_xml.workbook_io._read_workbook(path)
    except Exception as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefits setup workbook {path}: {exc}"
        ) from exc
    matches = [
        sheet
        for sheet in workbook.sheets
        if eligibility_xml._normalized(sheet.title)
        == eligibility_xml._normalized(SHEET_NAME)
    ]
    if len(matches) != 1:
        raise eligibility_xml.ConversionError(
            f"The workbook must contain exactly one '{SHEET_NAME}' worksheet."
        )
    sheet = matches[0]
    if sheet.state != "visible":
        raise eligibility_xml.ConversionError(
            f"The '{SHEET_NAME}' worksheet must be visible."
        )
    return parse_benefit_balances(sheet.rows)


def load_template(path: Path) -> ET.Element:
    try:
        root = ET.fromstring(eligibility_xml.read_template_bytes(path))
    except OSError as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to read Benefit Balance sample {path}: {exc}"
        ) from exc
    except ET.ParseError as exc:
        raise eligibility_xml.ConversionError(
            f"Benefit Balance sample is not well formed: {exc}"
        ) from exc
    if eligibility_xml._local_name(root.tag) != "BenefitBalanceVO":
        raise eligibility_xml.ConversionError(
            "Benefit Balance sample root must be BenefitBalanceVO."
        )
    rows = [
        child
        for child in root
        if eligibility_xml._local_name(child.tag) == "BenefitBalanceVORow"
    ]
    if not rows:
        raise eligibility_xml.ConversionError(
            "Benefit Balance sample has no BenefitBalanceVORow."
        )
    fields = {eligibility_xml._local_name(child.tag) for child in rows[0]}
    missing = sorted(REQUIRED_TEMPLATE_FIELDS - fields)
    if missing:
        raise eligibility_xml.ConversionError(
            "Benefit Balance sample row is missing: " + ", ".join(missing)
        )
    return root


def _hcm_lookup_spec(
    criterion: str, lookup_type: str, target_field: str
) -> eligibility_xml.LookupSpec:
    return eligibility_xml.LookupSpec(
        criterion=criterion,
        endpoint=GENERIC_LOOKUP_ENDPOINT,
        catalog=f"{lookup_type} HCM_LOOKUPS REST lookup",
        source_fields=("Meaning", "LookupCode"),
        target_fields=((target_field, "LookupCode"),),
        query=(
            ("finder", f"LookupTypeFinder;LookupType={lookup_type},ViewApplicationId=3"),
        ),
        required_values=(("EnabledFlag", "Y"),),
        items_path=("lookupCodes",),
        active_date_fields=("StartDateActive", "EndDateActive"),
    )


BALANCE_USAGE_LOOKUP = _hcm_lookup_spec(
    "Benefit Balance usage", "BEN_BNFTS_BAL_USG", "BnftsBalUsgCd"
)
NONMONETARY_UNITS_LOOKUP = _hcm_lookup_spec(
    "Benefit Balance nonmonetary units", "BEN_NNMNTRY_UOM", "NnmntryUom"
)
CURRENCY_LOOKUP = eligibility_xml.LookupSpec(
    criterion="Benefit Balance currency",
    endpoint=CURRENCY_ENDPOINT,
    catalog="currenciesLOV",
    source_fields=("Name", "CurrencyCode"),
    target_fields=(("Uom", "CurrencyCode"),),
    query=(),
    required_values=(),
)


def convert_benefit_balances(
    template_root: ET.Element,
    balances: list[BenefitBalance],
    resolver: eligibility_xml.LookupResolver,
) -> ET.Element:
    """Clone the exported row shape for each validated Benefit Balance."""
    template_row = next(
        child
        for child in template_root
        if eligibility_xml._local_name(child.tag) == "BenefitBalanceVORow"
    )
    output = copy.deepcopy(template_root)
    for child in list(output):
        if eligibility_xml._local_name(child.tag) == "BenefitBalanceVORow":
            output.remove(child)
    for balance in balances:
        usage = resolver.resolve(BALANCE_USAGE_LOOKUP, balance.balance_usage)[
            "BnftsBalUsgCd"
        ]
        currency = ""
        nonmonetary_units = ""
        if balance.currency:
            currency = resolver.resolve(CURRENCY_LOOKUP, balance.currency)["Uom"]
            nonmonetary_units = "MONEY"
        elif balance.nonmonetary_units:
            nonmonetary_units = resolver.resolve(
                NONMONETARY_UNITS_LOOKUP, balance.nonmonetary_units
            )["NnmntryUom"]
        row = copy.deepcopy(template_row)
        values = {
            "ViewInstanceName": "BenefitBalance",
            "GroupingKey": balance.name,
            "LogicalStartDate": balance.effective_start_date,
            "LogicalEndDate": balance.effective_end_date,
            "EffectiveStartDate": balance.effective_start_date,
            "EffectiveEndDate": balance.effective_end_date,
            "BnftsBalDesc": balance.description,
            "BnftsBalUsgCd": usage,
            "Name": balance.name,
            "NnmntryUom": nonmonetary_units,
            "Uom": currency,
            "SrcName": "",
            "BenefitBalanceName": balance.name,
            "LegalEntityName": balance.legal_employer,
            "BnftsBalId": "",
            "LegalEntityId": "",
        }
        for field_name, value in values.items():
            eligibility_xml._set_element(row, field_name, value)
        output.append(row)
    return output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Convert the Benefit Balances worksheet in Fusion_Benefits_Setup.xlsx "
            "into BEN_BNFTS_BAL_F.xml."
        )
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--sample", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--force", action="store_true", help="Replace an existing output file.")
    parser.add_argument(
        "--properties",
        type=Path,
        default=eligibility_xml.rest_client_common.DEFAULT_PROPERTIES_PATH,
    )
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    parser.add_argument("--no-open-browser", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        input_path = args.input.resolve()
        sample_path = args.sample.resolve()
        output_path = args.output.resolve()
        if output_path in {input_path, sample_path}:
            raise eligibility_xml.ConversionError(
                "Output must not replace the workbook or Benefit Balance sample."
            )
        balances = read_workbook_benefit_balances(input_path)
        resolver = eligibility_xml.FusionLookupResolver(
            properties_path=args.properties.resolve(),
            token_cache=args.token_cache,
            open_browser=not args.no_open_browser,
        )
        converted = convert_benefit_balances(
            load_template(sample_path), balances, resolver
        )
        eligibility_xml.write_xml(converted, output_path, force=args.force)
        print(f"Generated {output_path} with {len(balances)} Benefit Balance(s).")
        print("No ZIP package or checksum was created or modified.")
        return 0
    except eligibility_xml.ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- excel_to_plan_copy_package ----
excel_to_plan_copy_package = _component("excel_to_plan_copy_package", r'''
#!/usr/bin/env python3
"""Generate eligibility Plan Copy XML artifacts and their import package."""

from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import xml.etree.ElementTree as ET
import zipfile


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_map_xml as plan_copy_map_xml  # noqa: E402
import excel_to_plan_copy_xml as eligibility_xml  # noqa: E402
import excel_to_plan_copy_benefits_group_xml as benefits_group_xml  # noqa: E402
import excel_to_plan_copy_benefit_balance_xml as benefit_balance_xml  # noqa: E402
import excel_to_plan_copy_derived_factor_xml as derived_factor_xml  # noqa: E402
import excel_to_plan_copy_additional_derived_factor_xml as additional_factor_xml  # noqa: E402
import excel_to_plan_copy_service_area_xml as service_area_xml  # noqa: E402


SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_SAMPLES_DIR = SKILL_ROOT / "assets" / "plan-copy"
DEFAULT_MAPPING_REFERENCE_DIR = (
    SKILL_ROOT / "references" / "eligibility-profile-mapping-reference"
)
SAMPLE_BASENAMES = {
    "eligibility": "BEN_ELIGY_PRFL.xml",
    "postal_code_range": "BEN_PSTL_ZIP_RNG.xml",
    "service_area": "BEN_SVC_AREA.xml",
    "age": "BEN_AGE_FCTR.xml",
    "compensation_level": "BEN_COMP_LVL_FCTR.xml",
    "length_of_service": "BEN_LOS_FCTR.xml",
    "combined_age_los": "BEN_CMBN_AGE_LOS_FCTR.xml",
    "hours_worked": "BEN_HRS_WKD_IN_PERD_FCTR.xml",
    "full_time_equivalent": "BEN_PCT_FL_TM_FCTR.xml",
    "map": "BEN_PL_COPY_MAP.xml",
}

ELIGIBILITY_OUTPUT_NAME = "BEN_ELIGY_PRFL-converted.xml"
BENEFITS_GROUP_OUTPUT_NAME = "BEN_BENFTS_GRP-converted.xml"
BENEFIT_BALANCE_OUTPUT_NAME = "BEN_BNFTS_BAL_F-converted.xml"
POSTAL_CODE_RANGE_OUTPUT_NAME = "BEN_PSTL_ZIP_RNG-converted.xml"
SERVICE_AREA_OUTPUT_NAME = "BEN_SVC_AREA-converted.xml"
AGE_OUTPUT_NAME = "BEN_AGE_FCTR-converted.xml"
COMPENSATION_LEVEL_OUTPUT_NAME = "BEN_COMP_LVL_FCTR-converted.xml"
LENGTH_OF_SERVICE_OUTPUT_NAME = "BEN_LOS_FCTR-converted.xml"
COMBINED_AGE_LOS_OUTPUT_NAME = "BEN_CMBN_AGE_LOS_FCTR-converted.xml"
HOURS_WORKED_OUTPUT_NAME = "BEN_HRS_WKD_IN_PERD_FCTR-converted.xml"
FULL_TIME_EQUIVALENT_OUTPUT_NAME = "BEN_PCT_FL_TM_FCTR-converted.xml"
MAP_OUTPUT_NAME = "BEN_PL_COPY_MAP-converted.xml"
DEFAULT_PACKAGE_NAME = "benefits_eligibility.zip"
ELIGIBILITY_BATCH = "EligibilityProfile/1_BATCH.zip"
BENEFITS_GROUP_BATCH = "BenefitsGroup/1_BATCH.zip"
BENEFIT_BALANCE_BATCH = "BenefitBalance/1_BATCH.zip"
POSTAL_CODE_RANGE_BATCH = "PostalCodeRange/1_BATCH.zip"
SERVICE_AREA_BATCH = "ServiceArea/1_BATCH.zip"
AGE_BATCH = "AgeFactor/1_BATCH.zip"
COMPENSATION_LEVEL_BATCH = "CompensationLevelFactor/1_BATCH.zip"
LENGTH_OF_SERVICE_BATCH = "LengthOfServiceFactor/1_BATCH.zip"
COMBINED_AGE_LOS_BATCH = "CombinedAgeLosFactor/1_BATCH.zip"
HOURS_WORKED_BATCH = "HoursWorkedFactor/1_BATCH.zip"
FULL_TIME_EQUIVALENT_BATCH = "FullTimeEquivalentFactor/1_BATCH.zip"
MAP_BATCH = "PlanCopyMap/1_BATCH.zip"
MIGRATOR_PROPERTIES_NAME = "MIGRATOR_PROPERTIES.xml"
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
MIGRATOR_PROPERTIES = b"""<?xml version="1.0" encoding="UTF-8"?>
<java version="17.0.19" class="java.beans.XMLDecoder">
 <object
  class="oracle.apps.setupHub.remoteApp.publicModel.migrator.MigratorZipProperties"
  id="MigratorZipProperties0">
  <void property="batchImportSequence">
   <void method="add">
    <string>PlanCopyMap</string>
   </void>
   <void method="add">
   <string>BenefitsGroup</string>
   </void>
   <void method="add">
    <string>BenefitBalance</string>
   </void>
   <void method="add">
    <string>PostalCodeRange</string>
   </void>
   <void method="add">
    <string>ServiceArea</string>
   </void>
   <void method="add">
   <string>AgeFactor</string>
   </void>
   <void method="add">
    <string>LengthOfServiceFactor</string>
   </void>
   <void method="add">
    <string>CombinedAgeLosFactor</string>
   </void>
   <void method="add">
    <string>CompensationLevelFactor</string>
   </void>
   <void method="add">
    <string>HoursWorkedFactor</string>
   </void>
   <void method="add">
    <string>FullTimeEquivalentFactor</string>
   </void>
   <void method="add">
    <string>EligibilityProfile</string>
   </void>
  </void>
  <void property="batchMode">
   <boolean>true</boolean>
  </void>
  <void property="batchSizeMap">
   <void method="put">
    <string>PlanCopyMap</string>
    <int>500</int>
   </void>
  </void>
 </object>
</java>
"""

BATCH_SPECS = {
    "map": (MAP_BATCH, "PlanCopyMap", "BEN_PL_COPY_MAP.xml", "PlanCopyMapVO", "Plan Copy map"),
    "benefits_group": (
        BENEFITS_GROUP_BATCH,
        "BenefitsGroup",
        "BEN_BENFTS_GRP.xml",
        "BenefitsGroupVO",
        "Benefits Group",
    ),
    "benefit_balance": (
        BENEFIT_BALANCE_BATCH,
        "BenefitBalance",
        "BEN_BNFTS_BAL_F.xml",
        "BenefitBalanceVO",
        "Benefit Balance",
    ),
    "postal_code_range": (
        POSTAL_CODE_RANGE_BATCH,
        "PostalCodeRange",
        "BEN_PSTL_ZIP_RNG.xml",
        "PostalZipRangeVO",
        "Postal Code Range",
    ),
    "service_area": (
        SERVICE_AREA_BATCH,
        "ServiceArea",
        "BEN_SVC_AREA.xml",
        "ServiceAreaVO",
        "Service Area",
    ),
    "age": (AGE_BATCH, "AgeFactor", "BEN_AGE_FCTR.xml", "AgeFactorVO", "Age factor"),
    "length_of_service": (
        LENGTH_OF_SERVICE_BATCH,
        "LengthOfServiceFactor",
        "BEN_LOS_FCTR.xml",
        "LengthOfServiceFactorVO",
        "Length of Service factor",
    ),
    "combined_age_los": (
        COMBINED_AGE_LOS_BATCH,
        "CombinedAgeLosFactor",
        "BEN_CMBN_AGE_LOS_FCTR.xml",
        "CombinedAgeLosFactorVO",
        "Age and Service factor",
    ),
    "compensation_level": (
        COMPENSATION_LEVEL_BATCH,
        "CompensationLevelFactor",
        "BEN_COMP_LVL_FCTR.xml",
        "CompensationLevelFactorVO",
        "Compensation factor",
    ),
    "hours_worked": (
        HOURS_WORKED_BATCH,
        "HoursWorkedFactor",
        "BEN_HRS_WKD_IN_PERD_FCTR.xml",
        "HoursWorkedFactorVO",
        "Hours Worked factor",
    ),
    "full_time_equivalent": (
        FULL_TIME_EQUIVALENT_BATCH,
        "FullTimeEquivalentFactor",
        "BEN_PCT_FL_TM_FCTR.xml",
        "FullTimeEquivalentFactorVO",
        "Full-Time Equivalent factor",
    ),
    "eligibility": (
        ELIGIBILITY_BATCH,
        "EligibilityProfile",
        "BEN_ELIGY_PRFL.xml",
        "EligibilityProfileVO",
        "eligibility profile",
    ),
}

GENERAL_BENEFITS_CONFIG_BATCH_KEYS = (
    "map",
    "benefits_group",
    "benefit_balance",
    "eligibility",
)
ELIGIBILITY_BATCH_KEYS = (
    "map",
    "postal_code_range",
    "service_area",
    "age",
    "length_of_service",
    "combined_age_los",
    "compensation_level",
    "hours_worked",
    "full_time_equivalent",
    "eligibility",
)
COMBINED_BATCH_KEYS = (
    "map",
    "benefits_group",
    "benefit_balance",
    "postal_code_range",
    "service_area",
    "age",
    "length_of_service",
    "combined_age_los",
    "compensation_level",
    "hours_worked",
    "full_time_equivalent",
    "eligibility",
)

# The Plan Copy REST package validator requires an EligibilityProfile batch for
# every package whose ComponentObjType is ELIG. Retain this marker for the
# compatibility package builder used by older callers.
EMPTY_ELIGIBILITY_COMPONENT_XML = (
    b'<?xml version="1.0" encoding="UTF-8"?>\n'
    b'<EligibilityProfileVO />\n'
)


def _zip_info(name: str) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o600 << 16
    return info


def _single_file_zip(name: str, contents: bytes) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w") as archive:
        archive.writestr(_zip_info(name), contents)
    return output.getvalue()


def _xml_root(contents: bytes, description: str) -> ET.Element:
    try:
        return ET.fromstring(contents)
    except ET.ParseError as exc:
        raise eligibility_xml.ConversionError(
            f"Generated {description} is not well-formed XML: {exc}"
        ) from exc


def _validate_xml_root(contents: bytes, expected_root: str, description: str) -> None:
    root = _xml_root(contents, description)
    if eligibility_xml._local_name(root.tag) != expected_root:
        raise eligibility_xml.ConversionError(
            f"Generated {description} root must be {expected_root}."
        )


def _migrator_properties(batch_keys: tuple[str, ...]) -> bytes:
    sequence = "\n".join(
        "   <void method=\"add\">\n"
        f"    <string>{BATCH_SPECS[key][1]}</string>\n"
        "   </void>"
        for key in batch_keys
    )
    return (
        "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
        "<java version=\"17.0.19\" class=\"java.beans.XMLDecoder\">\n"
        " <object\n"
        "  class=\"oracle.apps.setupHub.remoteApp.publicModel.migrator.MigratorZipProperties\"\n"
        "  id=\"MigratorZipProperties0\">\n"
        "  <void property=\"batchImportSequence\">\n"
        f"{sequence}\n"
        "  </void>\n"
        "  <void property=\"batchMode\">\n"
        "   <boolean>true</boolean>\n"
        "  </void>\n"
        "  <void property=\"batchSizeMap\">\n"
        "   <void method=\"put\">\n"
        "    <string>PlanCopyMap</string>\n"
        "    <int>500</int>\n"
        "   </void>\n"
        "  </void>\n"
        " </object>\n"
        "</java>\n"
    ).encode("utf-8")


def _build_scoped_import_package(
    batch_keys: tuple[str, ...], batch_contents: dict[str, bytes]
) -> bytes:
    if set(batch_contents) != set(batch_keys):
        raise eligibility_xml.ConversionError(
            "Generated package contents do not match the selected Plan Copy scope."
        )
    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w") as archive:
        for key in batch_keys:
            batch_name, _sequence_name, member_name, root_name, description = BATCH_SPECS[key]
            contents = batch_contents[key]
            _validate_xml_root(contents, root_name, description)
            archive.writestr(
                _zip_info(batch_name),
                _single_file_zip(member_name, contents),
            )
        archive.writestr(
            _zip_info(MIGRATOR_PROPERTIES_NAME), _migrator_properties(batch_keys)
        )
    package = output.getvalue()
    validate_import_package(package)
    return package


def build_general_benefits_config_package(
    *, map_contents: bytes, benefits_group_contents: bytes, benefit_balance_contents: bytes
) -> bytes:
    """Build Benefit Groups/Balances plus the required empty ELIG marker."""
    return _build_scoped_import_package(
        GENERAL_BENEFITS_CONFIG_BATCH_KEYS,
        {
            "map": map_contents,
            "benefits_group": benefits_group_contents,
            "benefit_balance": benefit_balance_contents,
            "eligibility": EMPTY_ELIGIBILITY_COMPONENT_XML,
        },
    )


def build_eligibility_import_package(
    *,
    eligibility_contents: bytes,
    map_contents: bytes,
    postal_code_range_contents: bytes,
    service_area_contents: bytes,
    age_contents: bytes,
    compensation_level_contents: bytes,
    length_of_service_contents: bytes,
    combined_age_los_contents: bytes,
    hours_worked_contents: bytes,
    full_time_equivalent_contents: bytes,
) -> bytes:
    """Build the eligibility, service-area, and derived-factor Plan Copy package."""
    return _build_scoped_import_package(
        ELIGIBILITY_BATCH_KEYS,
        {
            "map": map_contents,
            "postal_code_range": postal_code_range_contents,
            "service_area": service_area_contents,
            "age": age_contents,
            "length_of_service": length_of_service_contents,
            "combined_age_los": combined_age_los_contents,
            "compensation_level": compensation_level_contents,
            "hours_worked": hours_worked_contents,
            "full_time_equivalent": full_time_equivalent_contents,
            "eligibility": eligibility_contents,
        },
    )


def build_import_package(
    eligibility_contents: bytes,
    map_contents: bytes,
    benefits_group_contents: bytes,
    benefit_balance_contents: bytes,
    postal_code_range_contents: bytes,
    service_area_contents: bytes,
    age_contents: bytes,
    compensation_level_contents: bytes,
    length_of_service_contents: bytes,
    combined_age_los_contents: bytes,
    hours_worked_contents: bytes,
    full_time_equivalent_contents: bytes,
) -> bytes:
    """Build and validate the nested Benefits setup Plan Copy import archive."""
    _validate_xml_root(eligibility_contents, "EligibilityProfileVO", "eligibility profile")
    _validate_xml_root(map_contents, "PlanCopyMapVO", "Plan Copy map")
    _validate_xml_root(benefits_group_contents, "BenefitsGroupVO", "Benefits Group")
    _validate_xml_root(benefit_balance_contents, "BenefitBalanceVO", "Benefit Balance")
    _validate_xml_root(
        postal_code_range_contents, "PostalZipRangeVO", "Postal Code Range"
    )
    _validate_xml_root(service_area_contents, "ServiceAreaVO", "Service Area")
    _validate_xml_root(age_contents, "AgeFactorVO", "Age factor")
    _validate_xml_root(
        compensation_level_contents,
        "CompensationLevelFactorVO",
        "Compensation factor",
    )
    _validate_xml_root(
        length_of_service_contents,
        "LengthOfServiceFactorVO",
        "Length of Service factor",
    )
    _validate_xml_root(
        combined_age_los_contents,
        "CombinedAgeLosFactorVO",
        "Age and Service factor",
    )
    _validate_xml_root(
        hours_worked_contents,
        "HoursWorkedFactorVO",
        "Hours Worked factor",
    )
    _validate_xml_root(
        full_time_equivalent_contents,
        "FullTimeEquivalentFactorVO",
        "Full-Time Equivalent factor",
    )

    output = io.BytesIO()
    with zipfile.ZipFile(output, mode="w") as archive:
        archive.writestr(
            _zip_info(MAP_BATCH),
            _single_file_zip("BEN_PL_COPY_MAP.xml", map_contents),
        )
        archive.writestr(
            _zip_info(BENEFITS_GROUP_BATCH),
            _single_file_zip("BEN_BENFTS_GRP.xml", benefits_group_contents),
        )
        archive.writestr(
            _zip_info(BENEFIT_BALANCE_BATCH),
            _single_file_zip("BEN_BNFTS_BAL_F.xml", benefit_balance_contents),
        )
        archive.writestr(
            _zip_info(POSTAL_CODE_RANGE_BATCH),
            _single_file_zip("BEN_PSTL_ZIP_RNG.xml", postal_code_range_contents),
        )
        archive.writestr(
            _zip_info(SERVICE_AREA_BATCH),
            _single_file_zip("BEN_SVC_AREA.xml", service_area_contents),
        )
        archive.writestr(
            _zip_info(AGE_BATCH),
            _single_file_zip("BEN_AGE_FCTR.xml", age_contents),
        )
        archive.writestr(
            _zip_info(LENGTH_OF_SERVICE_BATCH),
            _single_file_zip("BEN_LOS_FCTR.xml", length_of_service_contents),
        )
        archive.writestr(
            _zip_info(COMBINED_AGE_LOS_BATCH),
            _single_file_zip("BEN_CMBN_AGE_LOS_FCTR.xml", combined_age_los_contents),
        )
        archive.writestr(
            _zip_info(COMPENSATION_LEVEL_BATCH),
            _single_file_zip("BEN_COMP_LVL_FCTR.xml", compensation_level_contents),
        )
        archive.writestr(
            _zip_info(HOURS_WORKED_BATCH),
            _single_file_zip("BEN_HRS_WKD_IN_PERD_FCTR.xml", hours_worked_contents),
        )
        archive.writestr(
            _zip_info(FULL_TIME_EQUIVALENT_BATCH),
            _single_file_zip("BEN_PCT_FL_TM_FCTR.xml", full_time_equivalent_contents),
        )
        archive.writestr(
            _zip_info(ELIGIBILITY_BATCH),
            _single_file_zip("BEN_ELIGY_PRFL.xml", eligibility_contents),
        )
        archive.writestr(_zip_info(MIGRATOR_PROPERTIES_NAME), MIGRATOR_PROPERTIES)
    package = output.getvalue()
    validate_import_package(package)
    return package


def validate_import_package(contents: bytes) -> None:
    """Fail closed unless the archive matches one supported exact batch scope."""
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as outer:
            names = outer.namelist()
            if len(names) != len(set(names)):
                raise eligibility_xml.ConversionError(
                    "Generated package does not contain the exact Plan Copy batch members."
                )
            outer_names = set(names)
            matching_scopes = [
                batch_keys
                for batch_keys in (
                    GENERAL_BENEFITS_CONFIG_BATCH_KEYS,
                    ELIGIBILITY_BATCH_KEYS,
                    COMBINED_BATCH_KEYS,
                )
                if outer_names
                == {BATCH_SPECS[key][0] for key in batch_keys}
                | {MIGRATOR_PROPERTIES_NAME}
            ]
            if len(matching_scopes) != 1:
                raise eligibility_xml.ConversionError(
                    "Generated package does not contain one supported exact Plan Copy scope."
                )
            batch_keys = matching_scopes[0]
            if outer.testzip() is not None:
                raise eligibility_xml.ConversionError("Generated package failed its ZIP CRC check.")
            _validate_xml_root(
                outer.read(MIGRATOR_PROPERTIES_NAME), "java", "migrator properties"
            )
            for key in batch_keys:
                batch_name, _sequence_name, member_name, root_name, description = BATCH_SPECS[key]
                with zipfile.ZipFile(io.BytesIO(outer.read(batch_name))) as batch:
                    if batch.namelist() != [member_name]:
                        raise eligibility_xml.ConversionError(
                            f"Generated {batch_name} must contain only {member_name}."
                        )
                    if batch.testzip() is not None:
                        raise eligibility_xml.ConversionError(
                            f"Generated {batch_name} failed its ZIP CRC check."
                        )
                    _validate_xml_root(batch.read(member_name), root_name, description)
            if any("checksum" in name.casefold() for name in names):
                raise eligibility_xml.ConversionError(
                    "Generated package unexpectedly contains a checksum member."
                )
    except zipfile.BadZipFile as exc:
        raise eligibility_xml.ConversionError(
            f"Generated package is not a valid ZIP archive: {exc}"
        ) from exc


def _preflight_outputs(paths: tuple[Path, ...], *, force: bool) -> None:
    if len(paths) != len(set(paths)):
        raise eligibility_xml.ConversionError("Generated output paths must be distinct.")
    existing = [path for path in paths if path.exists()]
    if existing and not force:
        rendered = ", ".join(str(path) for path in existing)
        raise eligibility_xml.ConversionError(
            f"Output already exists: {rendered}; use --force to replace generated artifacts."
        )


def write_artifacts(artifacts: tuple[tuple[Path, bytes], ...], *, force: bool) -> None:
    """Write all validated artifacts through temporary files before replacement."""
    paths = tuple(path for path, _ in artifacts)
    _preflight_outputs(paths, force=force)
    temporary_files: list[tuple[Path, Path]] = []
    try:
        for output, contents in artifacts:
            output.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="wb",
                prefix=output.name + ".",
                suffix=".tmp",
                dir=output.parent,
                delete=False,
            ) as handle:
                temporary = Path(handle.name)
                handle.write(contents)
                handle.flush()
                os.fsync(handle.fileno())
            temporary_files.append((temporary, output))
        _preflight_outputs(paths, force=force)
        for temporary, output in temporary_files:
            os.replace(temporary, output)
    except OSError as exc:
        raise eligibility_xml.ConversionError(
            f"Unable to write generated artifacts: {exc}"
        ) from exc
    finally:
        for temporary, _ in temporary_files:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass
            except OSError:
                pass


def _resolver(args: argparse.Namespace) -> eligibility_xml.FusionLookupResolver:
    return eligibility_xml.FusionLookupResolver(
        properties_path=args.properties.resolve(),
        token_cache=args.token_cache,
        open_browser=not args.no_open_browser,
        tls_cert_sha256=args.tls_cert_sha256,
        status_callback=_status,
    )


def _status(message: str) -> None:
    print(f"STATUS: {message}", flush=True)


def resolve_sample_paths(args: argparse.Namespace) -> dict[str, Path]:
    """Resolve convention-named samples, retaining hidden per-file overrides."""
    samples_dir = args.samples_dir.resolve()
    paths: dict[str, Path] = {}
    for key, basename in SAMPLE_BASENAMES.items():
        override = getattr(args, f"{key}_sample", None)
        paths[key] = override.resolve() if override is not None else samples_dir / basename
    return paths


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate BEN_ELIGY_PRFL.xml, BEN_BENFTS_GRP.xml, BEN_BNFTS_BAL_F.xml, "
            "BEN_PL_COPY_MAP.xml, "
            "Postal Code Range and Service Area XML files, all six maintained "
            "derived-factor XML files, and the nested "
            "benefits_eligibility.zip Plan Copy import package in one command."
        )
    )
    parser.add_argument(
        "--input", required=True, type=Path, help="Fusion_Benefits_Setup.xlsx workbook."
    )
    parser.add_argument(
        "--samples-dir",
        type=Path,
        default=DEFAULT_SAMPLES_DIR,
        help=(
            "Directory containing convention-named Plan Copy XML samples; defaults "
            "to this skill's assets/plan-copy directory."
        ),
    )
    # Retain the original per-file flags for existing automation, but keep the
    # scalable directory interface as the documented contract.
    parser.add_argument(
        "--eligibility-sample", type=Path, help=argparse.SUPPRESS
    )
    parser.add_argument(
        "--benefits-group-sample",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--benefit-balance-sample",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--age-sample",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--compensation-level-sample",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--map-sample",
        type=Path,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--mapping-reference-dir",
        type=Path,
        default=DEFAULT_MAPPING_REFERENCE_DIR,
        help="Directory containing the maintained eligibility mapping CSV files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help=(
            "Directory for BEN_ELIGY_PRFL-converted.xml, "
            "BEN_AGE_FCTR-converted.xml, "
            "BEN_PSTL_ZIP_RNG-converted.xml, BEN_SVC_AREA-converted.xml, "
            "BEN_COMP_LVL_FCTR-converted.xml, BEN_LOS_FCTR-converted.xml, "
            "BEN_CMBN_AGE_LOS_FCTR-converted.xml, "
            "BEN_HRS_WKD_IN_PERD_FCTR-converted.xml, "
            "BEN_PCT_FL_TM_FCTR-converted.xml, BEN_PL_COPY_MAP-converted.xml, "
            "and the default ZIP."
        ),
    )
    parser.add_argument(
        "--zip-output",
        type=Path,
        help=f"ZIP destination; defaults to <output-dir>/{DEFAULT_PACKAGE_NAME}.",
    )
    parser.add_argument(
        "--force", action="store_true", help="Replace existing generated artifacts."
    )
    parser.add_argument(
        "--component-object-id",
        help="Override the static component object ID declared by the maintained map rules.",
    )
    parser.add_argument(
        "--properties",
        type=Path,
        default=eligibility_xml.rest_client_common.DEFAULT_PROPERTIES_PATH,
        help="Fusion OAuth environment properties file.",
    )
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    parser.add_argument("--no-open-browser", action="store_true")
    parser.add_argument(
        "--tls-cert-sha256",
        help="Exact development/test pod leaf-certificate SHA-256 fingerprint.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return _run(args)


def _run(args: argparse.Namespace) -> int:
    try:
        _status("Preflighting input and output paths.")
        input_path = args.input.resolve()
        sample_paths = resolve_sample_paths(args)
        eligibility_sample = sample_paths["eligibility"]
        postal_code_range_sample = sample_paths["postal_code_range"]
        service_area_sample = sample_paths["service_area"]
        age_sample = sample_paths["age"]
        compensation_level_sample = sample_paths["compensation_level"]
        length_of_service_sample = sample_paths["length_of_service"]
        combined_age_los_sample = sample_paths["combined_age_los"]
        hours_worked_sample = sample_paths["hours_worked"]
        full_time_equivalent_sample = sample_paths["full_time_equivalent"]
        map_sample = sample_paths["map"]
        mapping_reference_dir = args.mapping_reference_dir.resolve()
        output_dir = args.output_dir.resolve()
        eligibility_output = output_dir / ELIGIBILITY_OUTPUT_NAME
        postal_code_range_output = output_dir / POSTAL_CODE_RANGE_OUTPUT_NAME
        service_area_output = output_dir / SERVICE_AREA_OUTPUT_NAME
        age_output = output_dir / AGE_OUTPUT_NAME
        compensation_level_output = output_dir / COMPENSATION_LEVEL_OUTPUT_NAME
        length_of_service_output = output_dir / LENGTH_OF_SERVICE_OUTPUT_NAME
        combined_age_los_output = output_dir / COMBINED_AGE_LOS_OUTPUT_NAME
        hours_worked_output = output_dir / HOURS_WORKED_OUTPUT_NAME
        full_time_equivalent_output = output_dir / FULL_TIME_EQUIVALENT_OUTPUT_NAME
        map_output = output_dir / MAP_OUTPUT_NAME
        zip_output = (
            args.zip_output.resolve()
            if args.zip_output is not None
            else output_dir / DEFAULT_PACKAGE_NAME
        )
        outputs = (
            eligibility_output,
            postal_code_range_output,
            service_area_output,
            age_output,
            compensation_level_output,
            length_of_service_output,
            combined_age_los_output,
            hours_worked_output,
            full_time_equivalent_output,
            map_output,
            zip_output,
        )
        protected_inputs = {
            input_path,
            eligibility_sample,
            postal_code_range_sample,
            service_area_sample,
            age_sample,
            compensation_level_sample,
            length_of_service_sample,
            combined_age_los_sample,
            hours_worked_sample,
            full_time_equivalent_sample,
            map_sample,
        }
        if protected_inputs.intersection(outputs):
            raise eligibility_xml.ConversionError(
                "Generated outputs must not replace the workbook or XML samples."
            )
        if zip_output.suffix.casefold() != ".zip":
            raise eligibility_xml.ConversionError("--zip-output must end in .zip.")
        _preflight_outputs(outputs, force=args.force)

        _status("Reading the workbook and Oracle-exported XML samples.")
        profiles = eligibility_xml.read_workbook_profiles(input_path)
        postal_code_ranges, service_areas = (
            service_area_xml.read_workbook_service_area_setup(input_path)
        )
        age_factors, compensation_factors = (
            derived_factor_xml.read_workbook_derived_factors(input_path)
        )
        (
            length_of_service_factors,
            combined_age_los_factors,
            hours_worked_factors,
            full_time_equivalent_factors,
        ) = additional_factor_xml.read_workbook_additional_factors(input_path)
        eligibility_xml._require_setup_objects(
            profiles, postal_code_ranges, service_areas, age_factors,
            compensation_factors, length_of_service_factors, combined_age_los_factors,
            hours_worked_factors, full_time_equivalent_factors,
        )
        eligibility_template = eligibility_xml.load_template(eligibility_sample)
        postal_code_range_template = service_area_xml.load_postal_code_range_template(
            postal_code_range_sample
        )
        service_area_template = service_area_xml.load_service_area_template(
            service_area_sample
        )
        age_template = derived_factor_xml.load_age_template(age_sample)
        compensation_level_template = derived_factor_xml.load_compensation_template(
            compensation_level_sample
        )
        length_of_service_template = (
            additional_factor_xml.load_length_of_service_template(
                length_of_service_sample
            )
        )
        combined_age_los_template = additional_factor_xml.load_combined_age_los_template(
            combined_age_los_sample
        )
        hours_worked_template = additional_factor_xml.load_hours_worked_template(
            hours_worked_sample
        )
        full_time_equivalent_template = additional_factor_xml.load_fte_template(
            full_time_equivalent_sample
        )
        criterion_count = sum(len(profile.criteria) for profile in profiles)
        _status(
            f"Loaded {len(profiles)} eligibility profile(s) with "
            f"{criterion_count} criterion row(s), "
            f"{len(postal_code_ranges)} Postal Code Range(s), "
            f"{len(service_areas)} Service Area(s), "
            f"{len(age_factors)} Age factor(s), and "
            f"{len(compensation_factors)} Compensation factor(s), "
            f"{len(length_of_service_factors)} Length of Service factor(s), "
            f"{len(combined_age_los_factors)} Age and Service factor(s), "
            f"{len(hours_worked_factors)} Hours Worked factor(s), and "
            f"{len(full_time_equivalent_factors)} Full-Time Equivalent factor(s)."
        )
        _status("Loading and validating the Plan Copy mapping contract.")
        map_template = plan_copy_map_xml.load_map_template(map_sample)
        map_contract = plan_copy_map_xml.load_plan_copy_map_contract(mapping_reference_dir)
        _status(f"Loaded {len(map_contract.criteria)} mapping contract(s).")
        resolver = _resolver(args)
        _status("Resolving Plan Copy mapping IDs and display names.")
        map_converted = plan_copy_map_xml.convert_plan_copy_map(
            map_template,
            profiles,
            map_contract,
            resolver,
            benefit_group_legal_employers=(),
            benefit_balance_legal_employers=(),
            component_object_id=args.component_object_id,
        )
        map_row_count = sum(
            1
            for child in map_converted
            if eligibility_xml._local_name(child.tag) == "PlanCopyMapVORow"
        )
        _status(f"Resolved {map_row_count} Plan Copy mapping row(s).")

        _status("Resolving eligibility XML lookup values.")
        eligibility_converted = eligibility_xml.convert_profiles(
            eligibility_template,
            profiles,
            lookup_resolver=resolver,
            package_reference_names={
                "Age": (factor.name for factor in age_factors),
                "Compensation": (factor.name for factor in compensation_factors),
                "Length of Service": (
                    factor.name for factor in length_of_service_factors
                ),
                "Age and Service": (
                    factor.name for factor in combined_age_los_factors
                ),
                "Combined Age and Length of Service": (
                    factor.name for factor in combined_age_los_factors
                ),
                "Hours Worked": (factor.name for factor in hours_worked_factors),
                "Full-Time Equivalent": (
                    factor.name for factor in full_time_equivalent_factors
                ),
                "Postal Code Range": (
                    postal_code_range.name for postal_code_range in postal_code_ranges
                ),
                "Postal Code Ranges": (
                    postal_code_range.name for postal_code_range in postal_code_ranges
                ),
                "Service Area": (service_area.name for service_area in service_areas),
                "Service Areas": (service_area.name for service_area in service_areas),
            },
        )
        _status("Eligibility XML lookup resolution completed.")

        _status("Rendering Postal Code Ranges XML.")
        postal_code_range_converted = service_area_xml.convert_postal_code_ranges(
            postal_code_range_template, postal_code_ranges
        )
        _status("Resolving and rendering Service Areas XML.")
        service_area_converted = service_area_xml.convert_service_areas(
            service_area_template, service_areas, resolver
        )

        _status("Resolving and rendering Age derived factors.")
        age_converted = derived_factor_xml.convert_age_factors(
            age_template, age_factors, resolver
        )
        _status("Resolving and rendering Compensation derived factors.")
        package_benefit_balance_names: set[str] = set()
        compensation_level_converted = derived_factor_xml.convert_compensation_factors(
            compensation_level_template,
            compensation_factors,
            resolver,
            package_benefit_balance_names=package_benefit_balance_names,
        )
        _status("Resolving and rendering Length of Service derived factors.")
        length_of_service_converted = (
            additional_factor_xml.convert_length_of_service_factors(
                length_of_service_template, length_of_service_factors, resolver
            )
        )
        _status("Cross-validating and rendering Age and Service derived factors.")
        combined_age_los_converted = (
            additional_factor_xml.convert_combined_age_los_factors(
                combined_age_los_template,
                combined_age_los_factors,
                age_factor_names={
                    eligibility_xml._exact_text_key(factor.name)
                    for factor in age_factors
                },
                los_factor_names={
                    eligibility_xml._exact_text_key(factor.name)
                    for factor in length_of_service_factors
                },
            )
        )
        _status("Resolving and rendering Hours Worked derived factors.")
        hours_worked_converted = additional_factor_xml.convert_hours_worked_factors(
            hours_worked_template,
            hours_worked_factors,
            resolver,
            package_benefit_balance_names=package_benefit_balance_names,
        )
        _status("Resolving and rendering Full-Time Equivalent derived factors.")
        full_time_equivalent_converted = additional_factor_xml.convert_fte_factors(
            full_time_equivalent_template, full_time_equivalent_factors, resolver
        )

        _status("Rendering all XML files and validating the nested ZIP package.")
        eligibility_contents = eligibility_xml.render_xml_bytes(eligibility_converted)
        postal_code_range_contents = eligibility_xml.render_xml_bytes(
            postal_code_range_converted
        )
        service_area_contents = eligibility_xml.render_xml_bytes(service_area_converted)
        age_contents = eligibility_xml.render_xml_bytes(age_converted)
        compensation_level_contents = eligibility_xml.render_xml_bytes(
            compensation_level_converted
        )
        length_of_service_contents = eligibility_xml.render_xml_bytes(
            length_of_service_converted
        )
        combined_age_los_contents = eligibility_xml.render_xml_bytes(
            combined_age_los_converted
        )
        hours_worked_contents = eligibility_xml.render_xml_bytes(
            hours_worked_converted
        )
        full_time_equivalent_contents = eligibility_xml.render_xml_bytes(
            full_time_equivalent_converted
        )
        map_contents = eligibility_xml.render_xml_bytes(map_converted)
        package_contents = build_eligibility_import_package(
            eligibility_contents=eligibility_contents,
            map_contents=map_contents,
            postal_code_range_contents=postal_code_range_contents,
            service_area_contents=service_area_contents,
            age_contents=age_contents,
            compensation_level_contents=compensation_level_contents,
            length_of_service_contents=length_of_service_contents,
            combined_age_los_contents=combined_age_los_contents,
            hours_worked_contents=hours_worked_contents,
            full_time_equivalent_contents=full_time_equivalent_contents,
        )
        _status("Package validation completed; writing all generated artifacts.")
        write_artifacts(
            (
                (eligibility_output, eligibility_contents),
                (postal_code_range_output, postal_code_range_contents),
                (service_area_output, service_area_contents),
                (age_output, age_contents),
                (compensation_level_output, compensation_level_contents),
                (length_of_service_output, length_of_service_contents),
                (combined_age_los_output, combined_age_los_contents),
                (hours_worked_output, hours_worked_contents),
                (full_time_equivalent_output, full_time_equivalent_contents),
                (map_output, map_contents),
                (zip_output, package_contents),
            ),
            force=args.force,
        )
        _status("All generated artifacts were written successfully.")

        print(
            f"Generated {eligibility_output} with {len(profiles)} eligibility profile(s) "
            f"and {criterion_count} criterion row(s)."
        )
        print(
            f"Generated {postal_code_range_output} with "
            f"{len(postal_code_ranges)} Postal Code Range(s)."
        )
        print(f"Generated {service_area_output} with {len(service_areas)} Service Area(s).")
        print(f"Generated {age_output} with {len(age_factors)} Age factor(s).")
        print(
            f"Generated {compensation_level_output} with "
            f"{len(compensation_factors)} Compensation factor(s)."
        )
        print(
            f"Generated {length_of_service_output} with "
            f"{len(length_of_service_factors)} Length of Service factor(s)."
        )
        print(
            f"Generated {combined_age_los_output} with "
            f"{len(combined_age_los_factors)} Age and Service factor(s)."
        )
        print(
            f"Generated {hours_worked_output} with "
            f"{len(hours_worked_factors)} Hours Worked factor(s)."
        )
        print(
            f"Generated {full_time_equivalent_output} with "
            f"{len(full_time_equivalent_factors)} Full-Time Equivalent factor(s)."
        )
        print(f"Generated {map_output} with {map_row_count} Plan Copy mapping row(s).")
        print(f"Generated {zip_output} with the ten nested Plan Copy XML batches.")
        print("No checksum was created or modified.")
        return 0
    except eligibility_xml.ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- generate_eligibility_package ----
generate_eligibility_package = _component("generate_eligibility_package", r'''
#!/usr/bin/env python3
"""Generate the eligibility-only Benefits Plan Copy package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import excel_to_plan_copy_package as common  # noqa: E402


eligibility_xml = common.eligibility_xml
plan_copy_map_xml = common.plan_copy_map_xml
derived_factor_xml = common.derived_factor_xml
additional_factor_xml = common.additional_factor_xml
service_area_xml = common.service_area_xml

DEFAULT_PACKAGE_NAME = "benefits_eligibility.zip"
OUTPUT_NAMES = {
    "eligibility": common.ELIGIBILITY_OUTPUT_NAME,
    "postal_code_range": common.POSTAL_CODE_RANGE_OUTPUT_NAME,
    "service_area": common.SERVICE_AREA_OUTPUT_NAME,
    "age": common.AGE_OUTPUT_NAME,
    "compensation_level": common.COMPENSATION_LEVEL_OUTPUT_NAME,
    "length_of_service": common.LENGTH_OF_SERVICE_OUTPUT_NAME,
    "combined_age_los": common.COMBINED_AGE_LOS_OUTPUT_NAME,
    "hours_worked": common.HOURS_WORKED_OUTPUT_NAME,
    "full_time_equivalent": common.FULL_TIME_EQUIVALENT_OUTPUT_NAME,
    "map": common.MAP_OUTPUT_NAME,
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the eligibility-profile, service-area, derived-factor, and "
            "Plan Copy map batches from Fusion_Elpro_Setup.xlsx."
        ),
        allow_abbrev=False,
    )
    parser.add_argument(
        "--input", required=True, type=Path, help="Fusion_Elpro_Setup.xlsx workbook."
    )
    parser.add_argument(
        "--samples-dir",
        type=Path,
        default=common.DEFAULT_SAMPLES_DIR,
        help="Directory containing convention-named Plan Copy XML samples.",
    )
    parser.add_argument(
        "--mapping-reference-dir",
        type=Path,
        default=common.DEFAULT_MAPPING_REFERENCE_DIR,
        help="Directory containing the maintained eligibility mapping CSV files.",
    )
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--zip-output", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--component-object-id")
    parser.add_argument(
        "--properties",
        type=Path,
        default=eligibility_xml.rest_client_common.DEFAULT_PROPERTIES_PATH,
    )
    parser.add_argument("--token-cache", type=Path, default=Path("auto"))
    parser.add_argument("--no-open-browser", action="store_true")
    parser.add_argument("--tls-cert-sha256")
    return parser.parse_args(argv)


def _sample_paths(samples_dir: Path) -> dict[str, Path]:
    return {
        key: samples_dir / common.SAMPLE_BASENAMES[key]
        for key in OUTPUT_NAMES
    }


def _run(args: argparse.Namespace) -> dict[str, object]:
    input_path = args.input.resolve(strict=True)
    output_dir = args.output_dir.resolve()
    samples = _sample_paths(args.samples_dir.resolve(strict=True))
    mapping_reference_dir = args.mapping_reference_dir.resolve()
    outputs = {key: output_dir / name for key, name in OUTPUT_NAMES.items()}
    zip_output = (
        args.zip_output.resolve()
        if args.zip_output is not None
        else output_dir / DEFAULT_PACKAGE_NAME
    )
    if zip_output.suffix.casefold() != ".zip":
        raise eligibility_xml.ConversionError("--zip-output must end in .zip.")
    all_outputs = tuple(outputs.values()) + (zip_output,)
    protected_inputs = {input_path, *samples.values()}
    if protected_inputs.intersection(all_outputs):
        raise eligibility_xml.ConversionError(
            "Generated outputs must not replace the workbook or XML samples."
        )
    common._preflight_outputs(all_outputs, force=args.force)

    common._status("Reading Fusion_Elpro_Setup.xlsx and eligibility XML samples.")
    profiles = eligibility_xml.read_workbook_profiles(input_path)
    postal_code_ranges, service_areas = service_area_xml.read_workbook_service_area_setup(
        input_path
    )
    age_factors, compensation_factors = derived_factor_xml.read_workbook_derived_factors(
        input_path
    )
    (
        length_of_service_factors,
        combined_age_los_factors,
        hours_worked_factors,
        full_time_equivalent_factors,
    ) = additional_factor_xml.read_workbook_additional_factors(input_path)
    eligibility_xml._require_setup_objects(
        profiles, postal_code_ranges, service_areas, age_factors,
        compensation_factors, length_of_service_factors, combined_age_los_factors,
        hours_worked_factors, full_time_equivalent_factors,
    )
    criterion_count = sum(len(profile.criteria) for profile in profiles)

    resolver = common._resolver(args)
    map_template = plan_copy_map_xml.load_map_template(samples["map"])
    map_contract = plan_copy_map_xml.load_plan_copy_map_contract(mapping_reference_dir)
    map_converted = plan_copy_map_xml.convert_plan_copy_map(
        map_template,
        profiles,
        map_contract,
        resolver,
        benefit_group_legal_employers=(),
        benefit_balance_legal_employers=(),
        component_object_id=args.component_object_id,
    )

    package_references = {
        "Age": (factor.name for factor in age_factors),
        "Compensation": (factor.name for factor in compensation_factors),
        "Length of Service": (factor.name for factor in length_of_service_factors),
        "Age and Service": (factor.name for factor in combined_age_los_factors),
        "Combined Age and Length of Service": (
            factor.name for factor in combined_age_los_factors
        ),
        "Hours Worked": (factor.name for factor in hours_worked_factors),
        "Full-Time Equivalent": (factor.name for factor in full_time_equivalent_factors),
        "Postal Code Range": (item.name for item in postal_code_ranges),
        "Postal Code Ranges": (item.name for item in postal_code_ranges),
        "Service Area": (item.name for item in service_areas),
        "Service Areas": (item.name for item in service_areas),
    }
    eligibility_converted = eligibility_xml.convert_profiles(
        eligibility_xml.load_template(samples["eligibility"]),
        profiles,
        lookup_resolver=resolver,
        package_reference_names=package_references,
    )
    postal_code_range_converted = service_area_xml.convert_postal_code_ranges(
        service_area_xml.load_postal_code_range_template(samples["postal_code_range"]),
        postal_code_ranges,
    )
    service_area_converted = service_area_xml.convert_service_areas(
        service_area_xml.load_service_area_template(samples["service_area"]),
        service_areas,
        resolver,
    )
    age_converted = derived_factor_xml.convert_age_factors(
        derived_factor_xml.load_age_template(samples["age"]), age_factors, resolver
    )
    compensation_converted = derived_factor_xml.convert_compensation_factors(
        derived_factor_xml.load_compensation_template(samples["compensation_level"]),
        compensation_factors,
        resolver,
        package_benefit_balance_names=set(),
    )
    length_of_service_converted = additional_factor_xml.convert_length_of_service_factors(
        additional_factor_xml.load_length_of_service_template(samples["length_of_service"]),
        length_of_service_factors,
        resolver,
    )
    combined_age_los_converted = additional_factor_xml.convert_combined_age_los_factors(
        additional_factor_xml.load_combined_age_los_template(samples["combined_age_los"]),
        combined_age_los_factors,
        age_factor_names={eligibility_xml._exact_text_key(item.name) for item in age_factors},
        los_factor_names={
            eligibility_xml._exact_text_key(item.name) for item in length_of_service_factors
        },
    )
    hours_worked_converted = additional_factor_xml.convert_hours_worked_factors(
        additional_factor_xml.load_hours_worked_template(samples["hours_worked"]),
        hours_worked_factors,
        resolver,
        package_benefit_balance_names=set(),
    )
    fte_converted = additional_factor_xml.convert_fte_factors(
        additional_factor_xml.load_fte_template(samples["full_time_equivalent"]),
        full_time_equivalent_factors,
        resolver,
    )

    rendered = {
        "eligibility": eligibility_xml.render_xml_bytes(eligibility_converted),
        "map": eligibility_xml.render_xml_bytes(map_converted),
        "postal_code_range": eligibility_xml.render_xml_bytes(postal_code_range_converted),
        "service_area": eligibility_xml.render_xml_bytes(service_area_converted),
        "age": eligibility_xml.render_xml_bytes(age_converted),
        "compensation_level": eligibility_xml.render_xml_bytes(compensation_converted),
        "length_of_service": eligibility_xml.render_xml_bytes(length_of_service_converted),
        "combined_age_los": eligibility_xml.render_xml_bytes(combined_age_los_converted),
        "hours_worked": eligibility_xml.render_xml_bytes(hours_worked_converted),
        "full_time_equivalent": eligibility_xml.render_xml_bytes(fte_converted),
    }
    package_contents = common.build_eligibility_import_package(
        eligibility_contents=rendered["eligibility"],
        map_contents=rendered["map"],
        postal_code_range_contents=rendered["postal_code_range"],
        service_area_contents=rendered["service_area"],
        age_contents=rendered["age"],
        compensation_level_contents=rendered["compensation_level"],
        length_of_service_contents=rendered["length_of_service"],
        combined_age_los_contents=rendered["combined_age_los"],
        hours_worked_contents=rendered["hours_worked"],
        full_time_equivalent_contents=rendered["full_time_equivalent"],
    )
    common.write_artifacts(
        tuple((outputs[key], contents) for key, contents in rendered.items())
        + ((zip_output, package_contents),),
        force=args.force,
    )
    return {
        "event": "package_ready",
        "workbook": input_path.name,
        "archive": str(zip_output),
        "batchCount": len(common.ELIGIBILITY_BATCH_KEYS),
        "eligibilityProfileCount": len(profiles),
        "eligibilityCriterionRowCount": criterion_count,
        "postalCodeRangeCount": len(postal_code_ranges),
        "serviceAreaCount": len(service_areas),
        "ageFactorCount": len(age_factors),
        "compensationFactorCount": len(compensation_factors),
        "lengthOfServiceFactorCount": len(length_of_service_factors),
        "combinedAgeLosFactorCount": len(combined_age_los_factors),
        "hoursWorkedFactorCount": len(hours_worked_factors),
        "fullTimeEquivalentFactorCount": len(full_time_equivalent_factors),
    }


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        event = _run(args)
        print(f"Created {event['archive']}")
        return 0
    except (OSError, eligibility_xml.ConversionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')

# ---- plan_copy_import ----
plan_copy_import = _component("plan_copy_import", r'''
#!/usr/bin/env python3
"""Preview or execute an approval-gated Eligibility Plan Copy import."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from datetime import date, datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import time
from typing import Any, Callable
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
REST_CLIENT_SCRIPTS = REPOSITORY_ROOT / "core/fusion-api/rest-api-client/scripts"
ESS_SCRIPTS = REPOSITORY_ROOT / "core/fusion-api/ess-job-submitter/scripts"
TASK_HOOK_SCRIPTS = REPOSITORY_ROOT / "core/data-loader/task-hook/scripts"
for module_path in (SCRIPT_DIR, REST_CLIENT_SCRIPTS, ESS_SCRIPTS, TASK_HOOK_SCRIPTS):
    if str(module_path) not in sys.path:
        sys.path.insert(0, str(module_path))

import ess_job_submitter  # noqa: E402
import excel_to_plan_copy_package  # noqa: E402
import rest_client_compat as rest_client_common  # noqa: E402
import task_hook  # noqa: E402


FRAMEWORK_VERSION = "9"
TASK_CODE = "BEN_MANAGE_ELIGIBILITY_PROFILES"
TASK_NAME = "Eligibility Profiles"
COMPONENT_OBJECT_TYPE = "ELIG"
REQUEST_SOURCE = "FDOS"
ADF_ITEM_MEDIA_TYPE = "application/vnd.oracle.adf.resourceitem+json"
ADF_ACTION_MEDIA_TYPE = "application/vnd.oracle.adf.action+json"
PACKAGE_MEDIA_TYPE = "application/zip"
DEFAULT_POLL_INTERVAL_SECONDS = 10
DEFAULT_WAIT_SECONDS = 1800
MAX_POLL_INTERVAL_SECONDS = 60
MAX_REQUEST_LOG_BYTES = 5 * 1024 * 1024
PROCESS_ERROR = 10
PROCESS_SUCCESS = 12
REQUIRED_OPERATIONS = {
    "create": (
        "POST",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters",
    ),
    "upload": (
        "PUT",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/enclosure/PackageContent",
    ),
    "generate": (
        "POST",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/action/generateMappings",
    ),
    "ess_mapping": (
        "GET",
        "/ess/rest/scheduler/v1/requests/{mappingRequestId}",
    ),
    "parent": (
        "GET",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}",
    ),
    "unresolved": (
        "GET",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/child/mappings",
    ),
    "all_mappings": (
        "GET",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/child/mappings",
    ),
    "logs": (
        "GET",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/child/logs",
    ),
    "request_log": (
        "GET",
        "/hcmRestApi/resources/latest/benefitPlanCopyParameters/{plCopyId}/enclosure/RequestLogs",
    ),
}
OPENAPI_OPERATION_IDS = {
    "createPlanCopy": ("POST", REQUIRED_OPERATIONS["create"][1], 201, ADF_ITEM_MEDIA_TYPE),
    "uploadPlanCopyPackage": ("PUT", REQUIRED_OPERATIONS["upload"][1], 204, PACKAGE_MEDIA_TYPE),
    "generatePlanCopyMappings": (
        "POST",
        REQUIRED_OPERATIONS["generate"][1],
        200,
        ADF_ACTION_MEDIA_TYPE,
    ),
    "getEssRequest": ("GET", "/ess/rest/scheduler/v1/requests/{requestId}", 200, None),
    "getPlanCopy": ("GET", REQUIRED_OPERATIONS["parent"][1], 200, None),
    "listPlanCopyMappings": ("GET", REQUIRED_OPERATIONS["unresolved"][1], 200, None),
    "listPlanCopyLogs": ("GET", REQUIRED_OPERATIONS["logs"][1], 200, None),
    "getPlanCopyRequestLog": (
        "GET",
        REQUIRED_OPERATIONS["request_log"][1],
        200,
        None,
    ),
}
FAILURE_CLASS_ALIASES = {
    "input validation": "input_validation",
    "catalog mismatch": "catalog_or_metadata_mismatch",
    "auth/authz": "auth_expired_or_invalid",
    "Fusion API": "fusion_api_error",
    "transport/environment": "transport_or_environment",
    "process failed": "process_failed",
    "process timeout": "process_timeout",
    "artifact persistence": "artifact_persistence",
    "approval blocker": "approval_blocker",
}
RECOMMENDED_ACTIONS = {
    "input_validation": "Correct the reported input and build a new preview.",
    "catalog_or_metadata_mismatch": "Correct the mapping or reviewed OpenAPI document and build a new preview.",
    "auth_expired_or_invalid": "Configure or renew OAuth for the exact target pod.",
    "authorization_or_privilege": "Verify the target pod roles and REST privileges before retrying.",
    "transport_or_environment": "Verify DNS, proxy, certificate, and pod availability before retrying.",
    "fusion_api_error": "Review the sanitized Fusion response and do not replay a live write automatically.",
    "process_timeout": "Check the same request ID; do not submit a replacement without new approval.",
    "process_failed": (
        "Review the consolidated RequestLogs result and ESS status; do not replay "
        "the import automatically."
    ),
    "artifact_persistence": "Correct the output path or permissions and rebuild the preview.",
    "approval_blocker": (
        "Review the displayed artifact summary or immutable preview and provide the exact "
        "required approval before retrying."
    ),
}


class PlanCopyImportError(RuntimeError):
    """A fail-closed Plan Copy workflow error."""

    def __init__(
        self,
        failure_class: str,
        stage: str,
        message: str,
        *,
        identifiers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.failure_class = FAILURE_CLASS_ALIASES.get(failure_class, failure_class)
        self.stage = stage
        self.message = message
        self.identifiers = identifiers or {}


@dataclass(frozen=True)
class OpenApiContract:
    path: Path
    sha256: str
    base_url: str
    effective_date: str
    operations: dict[str, str]


HttpResult = rest_client_common.RestResponse


def _status(message: str) -> None:
    print(f"STATUS: {message}", flush=True)


def _sha256(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def _normalized_origin(value: str, description: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname:
        raise PlanCopyImportError(
            "input validation", "environment-preflight", f"{description} must be an HTTPS origin."
        )
    if parsed.username or parsed.password:
        raise PlanCopyImportError(
            "input validation", "environment-preflight", f"{description} must not contain credentials."
        )
    if parsed.path not in {"", "/"} or parsed.params or parsed.query or parsed.fragment:
        raise PlanCopyImportError(
            "input validation",
            "environment-preflight",
            f"{description} must contain only scheme, host, and optional port.",
        )
    port = f":{parsed.port}" if parsed.port is not None else ""
    return f"https://{parsed.hostname}{port}"


def contract_for_target(
    contract: OpenApiContract, target_origin: str | None
) -> OpenApiContract:
    """Apply an explicit origin override without changing the OpenAPI document."""
    if target_origin is None:
        return contract
    normalized = _normalized_origin(target_origin, "Target origin override")
    return replace(contract, base_url=normalized)


def _openapi_request_media_type(
    document: dict[str, Any], operation: dict[str, Any]
) -> str | None:
    request_body = operation.get("requestBody")
    if request_body is None:
        return None
    if request_body == {"$ref": "#/components/requestBodies/AdfAction"}:
        request_body = (
            document.get("components", {}).get("requestBodies", {}).get("AdfAction")
        )
    if not isinstance(request_body, dict):
        return None
    content = request_body.get("content")
    if not isinstance(content, dict) or len(content) != 1:
        return None
    return next(iter(content))


def load_openapi_contract(path: Path) -> OpenApiContract:
    try:
        contents = excel_to_plan_copy_package.eligibility_xml.read_contract_bytes(path)
        payload = json.loads(contents.decode("utf-8"))
    except OSError as exc:
        raise PlanCopyImportError(
            "input validation",
            "rest-contract-validation",
            f"Plan Copy OpenAPI document is unreadable: {path}",
        ) from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PlanCopyImportError(
            "input validation",
            "rest-contract-validation",
            "Plan Copy OpenAPI document is not valid UTF-8 JSON.",
        ) from exc
    if not isinstance(payload, dict):
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI document root must be an object.",
        )
    if payload.get("openapi") != "3.1.2":
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy API must use OpenAPI 3.1.2.",
        )
    info = payload.get("info")
    if not isinstance(info, dict) or info.get("title") != "Oracle Fusion Benefits Plan Copy Import API":
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI identity does not match the reviewed API.",
        )
    if payload.get("servers") != [
        {
            "url": "/",
            "description": "Fusion origin supplied by the selected OAuth environment",
        }
    ]:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI servers must remain host-neutral.",
        )
    paths = payload.get("paths")
    if not isinstance(paths, dict):
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI paths must be an object.",
        )
    discovered: dict[str, tuple[str, str, dict[str, Any]]] = {}
    for path_template, path_item in paths.items():
        if not isinstance(path_template, str) or not isinstance(path_item, dict):
            continue
        for method in ("get", "post", "put", "patch", "delete"):
            operation = path_item.get(method)
            if not isinstance(operation, dict):
                continue
            operation_id = operation.get("operationId")
            if not isinstance(operation_id, str) or operation_id in discovered:
                raise PlanCopyImportError(
                    "catalog mismatch",
                    "rest-contract-validation",
                    "Every Plan Copy OpenAPI operation must have a unique operationId.",
                )
            discovered[operation_id] = (method.upper(), path_template, operation)
    if set(discovered) != set(OPENAPI_OPERATION_IDS):
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI must define every supported operation exactly once.",
        )
    for operation_id, (method, path_template, status, media_type) in OPENAPI_OPERATION_IDS.items():
        actual_method, actual_path, operation = discovered[operation_id]
        if actual_method != method or actual_path != path_template:
            raise PlanCopyImportError(
                "catalog mismatch",
                "rest-contract-validation",
                f"OpenAPI operation {operation_id!r} method or path changed.",
            )
        responses = operation.get("responses")
        if not isinstance(responses, dict) or str(status) not in responses:
            raise PlanCopyImportError(
                "catalog mismatch",
                "rest-contract-validation",
                f"OpenAPI operation {operation_id!r} is missing response {status}.",
            )
        if _openapi_request_media_type(payload, operation) != media_type:
            raise PlanCopyImportError(
                "catalog mismatch",
                "rest-contract-validation",
                f"OpenAPI operation {operation_id!r} request media type changed.",
            )
    request_log_response = discovered["getPlanCopyRequestLog"][2]["responses"]["200"]
    request_log_content = (
        request_log_response.get("content")
        if isinstance(request_log_response, dict)
        else None
    )
    if not isinstance(request_log_content, dict) or set(request_log_content) != {
        "application/octet-stream"
    }:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy RequestLogs response must be application/octet-stream.",
        )

    components = payload.get("components")
    security_schemes = (
        components.get("securitySchemes") if isinstance(components, dict) else None
    )
    expected_security = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "OAuth 2.0 access token",
        "description": "Access token supplied by the shared Fusion OAuth client",
    }
    if (
        payload.get("security") != [{"FusionOAuth": []}]
        or not isinstance(security_schemes, dict)
        or security_schemes.get("FusionOAuth") != expected_security
    ):
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI must use the shared Fusion OAuth bearer-token contract.",
        )
    schemas = components.get("schemas") if isinstance(components, dict) else None
    create_schema = schemas.get("PlanCopyCreate") if isinstance(schemas, dict) else None
    expected_required = {
        "Name",
        "EffectiveDate",
        "FileName",
        "ComponentObjType",
        "Description",
        "ReuseCode",
        "SendNotifications",
        "RequestSource",
    }
    if not isinstance(create_schema, dict) or set(create_schema.get("required", [])) != expected_required:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI create schema is incomplete.",
        )
    properties = create_schema.get("properties")
    expected_constants = {
        "ComponentObjType": COMPONENT_OBJECT_TYPE,
        "Description": "Benefits Plan Copy REST import",
        "ReuseCode": "N",
        "SendNotifications": "N",
        "RequestSource": REQUEST_SOURCE,
    }
    if not isinstance(properties, dict) or any(
        not isinstance(properties.get(name), dict)
        or properties[name].get("const") != value
        for name, value in expected_constants.items()
    ):
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI create constants changed.",
        )
    parameters = components.get("parameters") if isinstance(components, dict) else None
    framework = parameters.get("RestFrameworkVersion") if isinstance(parameters, dict) else None
    if not isinstance(framework, dict) or framework.get("schema", {}).get("const") != FRAMEWORK_VERSION:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI REST framework version changed.",
        )
    mappings_parameters = discovered["listPlanCopyMappings"][2].get("parameters")
    mapping_query_names = {
        parameter.get("name")
        for parameter in mappings_parameters or []
        if isinstance(parameter, dict) and parameter.get("in") == "query"
    }
    if mapping_query_names != {"q", "fields", "limit", "totalResults"}:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "Plan Copy OpenAPI mapping query parameters changed.",
        )

    ess_path = discovered["getEssRequest"][1]
    matched = {
        "create": discovered["createPlanCopy"][1],
        "upload": discovered["uploadPlanCopyPackage"][1],
        "generate": discovered["generatePlanCopyMappings"][1],
        "ess_mapping": ess_path.replace("{requestId}", "{mappingRequestId}"),
        "parent": discovered["getPlanCopy"][1],
        "unresolved": discovered["listPlanCopyMappings"][1],
        "all_mappings": discovered["listPlanCopyMappings"][1],
        "logs": discovered["listPlanCopyLogs"][1],
        "request_log": discovered["getPlanCopyRequestLog"][1],
    }
    return OpenApiContract(
        path=path.resolve(),
        sha256=_sha256(contents),
        base_url="",
        effective_date="",
        operations=matched,
    )


def _validated_effective_date(value: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError, ValueError) as exc:
        raise PlanCopyImportError(
            "input validation", "metadata-validation", "Effective date must use YYYY-MM-DD."
        ) from exc


def _effective_date_for_import(
    *,
    workbook: Path | None,
    explicit_effective_date: str | None,
    contract_effective_date: str,
) -> str:
    """Resolve EffectiveDate from the Benefits workbook when one is supplied."""
    workbook_effective_date: str | None = None
    if workbook is not None:
        try:
            balances = (
                excel_to_plan_copy_package.benefit_balance_xml.read_workbook_benefit_balances(
                    workbook
                )
            )
            workbook_effective_date = (
                excel_to_plan_copy_package.benefit_balance_xml.common_session_effective_date(
                    balances
                )
            )
        except excel_to_plan_copy_package.eligibility_xml.ConversionError as exc:
            raise PlanCopyImportError(
                "input validation", "effective-date", str(exc)
            ) from exc

    if explicit_effective_date is not None:
        explicit = _validated_effective_date(explicit_effective_date)
        if workbook_effective_date is not None and explicit != workbook_effective_date:
            raise PlanCopyImportError(
                "input validation",
                "effective-date",
                "--effective-date must match the Benefit Balances worksheet Session "
                "Effective Date in the supplied date-source workbook.",
            )
        return explicit
    if workbook_effective_date is not None:
        return _validated_effective_date(workbook_effective_date)
    if contract_effective_date:
        return _validated_effective_date(contract_effective_date)
    raise PlanCopyImportError(
        "input validation",
        "effective-date",
        "Supply --workbook or --effective-date; the OpenAPI document does not contain runtime data.",
    )


def _xml_local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _xml_child_text(element: ET.Element, child_name: str) -> str:
    for child in element:
        if _xml_local_name(child.tag) == child_name:
            return (child.text or "").strip()
    return ""


def summarize_import_objects(contents: bytes) -> dict[str, Any]:
    """Inventory the setup objects inside an already validated Plan Copy package."""
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as outer:
            outer_names = set(outer.namelist())

            def read_batch(batch_name: str, member_name: str, root_name: str) -> ET.Element:
                if batch_name not in outer_names:
                    return ET.Element(root_name)
                with zipfile.ZipFile(io.BytesIO(outer.read(batch_name))) as batch:
                    return ET.fromstring(batch.read(member_name))

            eligibility_root = read_batch(
                excel_to_plan_copy_package.ELIGIBILITY_BATCH,
                "BEN_ELIGY_PRFL.xml",
                "EligibilityProfileVO",
            )
            map_root = read_batch(
                excel_to_plan_copy_package.MAP_BATCH,
                "BEN_PL_COPY_MAP.xml",
                "PlanCopyMapVO",
            )
            benefits_group_root = read_batch(
                excel_to_plan_copy_package.BENEFITS_GROUP_BATCH,
                "BEN_BENFTS_GRP.xml",
                "BenefitsGroupVO",
            )
            benefit_balance_root = read_batch(
                excel_to_plan_copy_package.BENEFIT_BALANCE_BATCH,
                "BEN_BNFTS_BAL_F.xml",
                "BenefitBalanceVO",
            )
            postal_code_range_root = read_batch(
                excel_to_plan_copy_package.POSTAL_CODE_RANGE_BATCH,
                "BEN_PSTL_ZIP_RNG.xml",
                "PostalZipRangeVO",
            )
            service_area_root = read_batch(
                excel_to_plan_copy_package.SERVICE_AREA_BATCH,
                "BEN_SVC_AREA.xml",
                "ServiceAreaVO",
            )
            age_root = read_batch(
                excel_to_plan_copy_package.AGE_BATCH,
                "BEN_AGE_FCTR.xml",
                "AgeFactorVO",
            )
            compensation_root = read_batch(
                excel_to_plan_copy_package.COMPENSATION_LEVEL_BATCH,
                "BEN_COMP_LVL_FCTR.xml",
                "CompensationLevelFactorVO",
            )
            length_of_service_root = read_batch(
                excel_to_plan_copy_package.LENGTH_OF_SERVICE_BATCH,
                "BEN_LOS_FCTR.xml",
                "LengthOfServiceFactorVO",
            )
            combined_age_los_root = read_batch(
                excel_to_plan_copy_package.COMBINED_AGE_LOS_BATCH,
                "BEN_CMBN_AGE_LOS_FCTR.xml",
                "CombinedAgeLosFactorVO",
            )
            hours_worked_root = read_batch(
                excel_to_plan_copy_package.HOURS_WORKED_BATCH,
                "BEN_HRS_WKD_IN_PERD_FCTR.xml",
                "HoursWorkedFactorVO",
            )
            full_time_equivalent_root = read_batch(
                excel_to_plan_copy_package.FULL_TIME_EQUIVALENT_BATCH,
                "BEN_PCT_FL_TM_FCTR.xml",
                "FullTimeEquivalentFactorVO",
            )
    except (KeyError, ET.ParseError, zipfile.BadZipFile) as exc:
        raise PlanCopyImportError(
            "input validation",
            "archive-object-summary",
            "Unable to inventory the validated Plan Copy package.",
        ) from exc

    profiles: list[dict[str, Any]] = []
    criterion_type_counts: dict[str, int] = {}
    for profile_row in eligibility_root:
        if _xml_local_name(profile_row.tag) != "EligibilityProfileVORow":
            continue
        profile_name = (
            _xml_child_text(profile_row, "EligibilityProfileName")
            or _xml_child_text(profile_row, "Name")
            or _xml_child_text(profile_row, "GroupingKey")
        )
        if not profile_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "EligibilityProfileVORow has no profile name.",
            )
        profile_criterion_count = 0
        for container in profile_row:
            for criterion_row in container:
                if not _xml_local_name(criterion_row.tag).endswith("VORow"):
                    continue
                object_type = _xml_child_text(criterion_row, "ViewInstanceName")
                if not object_type:
                    object_type = _xml_local_name(criterion_row.tag).removesuffix("VORow")
                criterion_type_counts[object_type] = (
                    criterion_type_counts.get(object_type, 0) + 1
                )
                profile_criterion_count += 1
        profiles.append({"name": profile_name, "criterionCount": profile_criterion_count})

    benefit_groups: list[dict[str, str]] = []
    for group_row in benefits_group_root:
        if _xml_local_name(group_row.tag) != "BenefitsGroupVORow":
            continue
        group_name = (
            _xml_child_text(group_row, "BenefitsGroupName")
            or _xml_child_text(group_row, "Name")
            or _xml_child_text(group_row, "GroupingKey")
        )
        if not group_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "BenefitsGroupVORow has no Benefits Group name.",
            )
        benefit_groups.append(
            {
                "name": group_name,
                "legalEmployer": _xml_child_text(group_row, "LegalEntityName"),
            }
        )
    if (
        excel_to_plan_copy_package.BENEFITS_GROUP_BATCH in outer_names
        and not benefit_groups
    ):
        raise PlanCopyImportError(
            "input validation",
            "archive-object-summary",
            "Plan Copy package contains no Benefit Groups to import.",
        )

    benefit_balances: list[dict[str, str]] = []
    for balance_row in benefit_balance_root:
        if _xml_local_name(balance_row.tag) != "BenefitBalanceVORow":
            continue
        balance_name = (
            _xml_child_text(balance_row, "BenefitBalanceName")
            or _xml_child_text(balance_row, "Name")
            or _xml_child_text(balance_row, "GroupingKey")
        )
        if not balance_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "BenefitBalanceVORow has no Benefit Balance name.",
            )
        benefit_balances.append(
            {
                "name": balance_name,
                "legalEmployer": _xml_child_text(balance_row, "LegalEntityName"),
            }
        )
    if (
        excel_to_plan_copy_package.BENEFIT_BALANCE_BATCH in outer_names
        and not benefit_balances
    ):
        raise PlanCopyImportError(
            "input validation",
            "archive-object-summary",
            "Plan Copy package contains no Benefit Balances to import.",
        )

    postal_code_ranges: list[str] = []
    for postal_range_row in postal_code_range_root:
        if _xml_local_name(postal_range_row.tag) != "PostalZipRangeVORow":
            continue
        postal_range = (
            _xml_child_text(postal_range_row, "PostalZipRange")
            or _xml_child_text(postal_range_row, "ZipRange")
            or _xml_child_text(postal_range_row, "GroupingKey")
        )
        if not postal_range:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "PostalZipRangeVORow has no Postal Code Range name.",
            )
        postal_code_ranges.append(postal_range)
    service_areas: list[dict[str, Any]] = []
    service_area_postal_code_range_count = 0
    for service_area_row in service_area_root:
        if _xml_local_name(service_area_row.tag) != "ServiceAreaVORow":
            continue
        service_area_name = (
            _xml_child_text(service_area_row, "ServiceAreaName")
            or _xml_child_text(service_area_row, "Name")
            or _xml_child_text(service_area_row, "GroupingKey")
        )
        if not service_area_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "ServiceAreaVORow has no Service Area name.",
            )
        postal_ranges_container = next(
            (
                child
                for child in service_area_row
                if _xml_local_name(child.tag) == "PostalZipRangesInServiceAreaVO"
            ),
            None,
        )
        if postal_ranges_container is None:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                f"Service Area '{service_area_name}' has no postal-code range collection.",
            )
        service_area_ranges: list[str] = []
        for link_row in postal_ranges_container:
            if _xml_local_name(link_row.tag) != "PostalZipRangesInServiceAreaVORow":
                continue
            postal_range = _xml_child_text(link_row, "PostalZipRange")
            if not postal_range:
                raise PlanCopyImportError(
                    "input validation",
                    "archive-object-summary",
                    f"Service Area '{service_area_name}' has a postal-code range link "
                    "without a Postal Code Range name.",
                )
            service_area_ranges.append(postal_range)
        if not service_area_ranges:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                f"Service Area '{service_area_name}' has no postal-code range links.",
            )
        service_area_postal_code_range_count += len(service_area_ranges)
        service_areas.append(
            {"name": service_area_name, "postalCodeRanges": service_area_ranges}
        )
    age_factors: list[str] = []
    for factor_row in age_root:
        if _xml_local_name(factor_row.tag) != "AgeFactorVORow":
            continue
        factor_name = (
            _xml_child_text(factor_row, "AgeFactorName")
            or _xml_child_text(factor_row, "Name")
            or _xml_child_text(factor_row, "GroupingKey")
        )
        if not factor_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "AgeFactorVORow has no Age factor name.",
            )
        age_factors.append(factor_name)
    compensation_factors: list[str] = []
    for factor_row in compensation_root:
        if _xml_local_name(factor_row.tag) != "CompensationLevelFactorVORow":
            continue
        factor_name = (
            _xml_child_text(factor_row, "CompensationLevelFactorName")
            or _xml_child_text(factor_row, "Name")
            or _xml_child_text(factor_row, "GroupingKey")
        )
        if not factor_name:
            raise PlanCopyImportError(
                "input validation",
                "archive-object-summary",
                "CompensationLevelFactorVORow has no Compensation factor name.",
            )
        compensation_factors.append(factor_name)
    def factor_names(
        root: ET.Element,
        row_name: str,
        name_field: str,
        description: str,
    ) -> list[str]:
        names: list[str] = []
        for factor_row in root:
            if _xml_local_name(factor_row.tag) != row_name:
                continue
            factor_name = (
                _xml_child_text(factor_row, name_field)
                or _xml_child_text(factor_row, "Name")
                or _xml_child_text(factor_row, "GroupingKey")
            )
            if not factor_name:
                raise PlanCopyImportError(
                    "input validation",
                    "archive-object-summary",
                    f"{row_name} has no {description} name.",
                )
            names.append(factor_name)
        return names

    length_of_service_factors = factor_names(
        length_of_service_root,
        "LengthOfServiceFactorVORow",
        "LosFactorName",
        "Length of Service",
    )
    combined_age_los_factors = factor_names(
        combined_age_los_root,
        "CombinedAgeLosFactorVORow",
        "CombinedAgeLosFactorName",
        "Age and Service",
    )
    hours_worked_factors = factor_names(
        hours_worked_root,
        "HoursWorkedFactorVORow",
        "HoursWorkedFactorName",
        "Hours Worked",
    )
    full_time_equivalent_factors = factor_names(
        full_time_equivalent_root,
        "FullTimeEquivalentFactorVORow",
        "FullTimeEquivalentFactorName",
        "Full-Time Equivalent",
    )

    if not any((profiles, benefit_groups, benefit_balances, postal_code_ranges,
                service_areas, age_factors, compensation_factors,
                length_of_service_factors, combined_age_los_factors,
                hours_worked_factors, full_time_equivalent_factors)):
        raise PlanCopyImportError(
            "input validation", "archive-object-summary",
            "Plan Copy package contains no setup objects to import.",
        )

    mapping_rows = [
        row for row in map_root if _xml_local_name(row.tag) == "PlanCopyMapVORow"
    ]
    criterion_row_count = sum(criterion_type_counts.values())
    return {
        "setupObjectCount": (
            len(profiles)
            + criterion_row_count
            + len(benefit_groups)
            + len(benefit_balances)
            + len(postal_code_ranges)
            + len(service_areas)
            + service_area_postal_code_range_count
            + len(age_factors)
            + len(compensation_factors)
            + len(length_of_service_factors)
            + len(combined_age_los_factors)
            + len(hours_worked_factors)
            + len(full_time_equivalent_factors)
        ),
        "eligibilityProfileCount": len(profiles),
        "eligibilityProfiles": profiles,
        "benefitGroupCount": len(benefit_groups),
        "benefitGroups": benefit_groups,
        "benefitBalanceCount": len(benefit_balances),
        "benefitBalances": benefit_balances,
        "postalCodeRangeCount": len(postal_code_ranges),
        "postalCodeRanges": postal_code_ranges,
        "serviceAreaCount": len(service_areas),
        "serviceAreas": service_areas,
        "serviceAreaPostalCodeRangeCount": service_area_postal_code_range_count,
        "ageFactorCount": len(age_factors),
        "ageFactors": age_factors,
        "compensationFactorCount": len(compensation_factors),
        "compensationFactors": compensation_factors,
        "lengthOfServiceFactorCount": len(length_of_service_factors),
        "lengthOfServiceFactors": length_of_service_factors,
        "combinedAgeLosFactorCount": len(combined_age_los_factors),
        "combinedAgeLosFactors": combined_age_los_factors,
        "hoursWorkedFactorCount": len(hours_worked_factors),
        "hoursWorkedFactors": hours_worked_factors,
        "fullTimeEquivalentFactorCount": len(full_time_equivalent_factors),
        "fullTimeEquivalentFactors": full_time_equivalent_factors,
        "criterionRowCount": criterion_row_count,
        "criterionTypeCounts": [
            {"type": object_type, "count": count}
            for object_type, count in sorted(criterion_type_counts.items())
        ],
        "planCopyMappingCount": len(mapping_rows),
    }


def _read_package(path: Path) -> tuple[Path, bytes, dict[str, Any]]:
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_file() or resolved.suffix.casefold() != ".zip":
            raise OSError
        contents = resolved.read_bytes()
    except OSError as exc:
        raise PlanCopyImportError(
            "input validation", "archive-validation", f"Plan Copy ZIP is unreadable: {path}"
        ) from exc
    if not contents:
        raise PlanCopyImportError(
            "input validation", "archive-validation", "Plan Copy ZIP must not be empty."
        )
    try:
        excel_to_plan_copy_package.validate_import_package(contents)
    except Exception as exc:
        raise PlanCopyImportError(
            "input validation", "archive-validation", f"Plan Copy ZIP failed validation: {exc}"
        ) from exc
    return resolved, contents, summarize_import_objects(contents)


def _oauth_properties(
    path: Path, expected_origin: str | None = None
) -> dict[str, str]:
    try:
        props = rest_client_common.read_properties(path.resolve(strict=True))
    except (OSError, ValueError) as exc:
        raise PlanCopyImportError(
            "auth/authz",
            "environment-preflight",
            "OAuth properties are unreadable or malformed.",
        ) from exc

    issues: list[str] = []
    pkce = str(props.get("pkce", "true")).strip().casefold()
    if pkce not in {"true", "false"}:
        issues.append("pkce must be true or false")
    required = [
        "environment",
        "restBaseUrl",
        "clientId",
        "scope",
        "redirectUrl",
    ]
    # Shared authentication retrieves confidential-client secrets from Keychain.
    missing = [name for name in required if not str(props.get(name) or "").strip()]
    if missing:
        issues.append("missing " + ", ".join(missing))

    configured_origin: str | None = None
    environment_origin: str | None = None
    if props.get("restBaseUrl"):
        try:
            configured_origin = _normalized_origin(props["restBaseUrl"], "OAuth restBaseUrl")
        except PlanCopyImportError:
            issues.append("restBaseUrl is not an HTTPS origin")
    if props.get("environment"):
        try:
            environment_origin = _normalized_origin(props["environment"], "OAuth environment")
        except PlanCopyImportError:
            issues.append("environment is not an HTTPS origin")
    if configured_origin and environment_origin and environment_origin != configured_origin:
        issues.append("environment does not match restBaseUrl")
    normalized_expected: str | None = None
    if expected_origin:
        try:
            normalized_expected = _normalized_origin(
                expected_origin, "Selected target origin"
            )
        except PlanCopyImportError:
            issues.append("selected target origin is not an HTTPS origin")
    if configured_origin and normalized_expected and configured_origin != normalized_expected:
        issues.append("restBaseUrl does not match the selected target origin")
    if issues:
        raise PlanCopyImportError(
            "auth/authz",
            "environment-preflight",
            "OAuth properties preflight failed: " + "; ".join(issues) + ".",
        )
    assert configured_origin is not None
    props["restBaseUrl"] = configured_origin
    return props


def _import_name(value: str | None, prefix: str = "BENEFITS_ELIG_") -> str:
    if value is None:
        value = prefix + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    normalized = value.strip()
    if not normalized or len(normalized) > 120 or not re.fullmatch(r"[A-Za-z0-9_.-]+", normalized):
        raise PlanCopyImportError(
            "input validation",
            "metadata-validation",
            "Import name must be 1-120 characters using letters, numbers, underscore, dot, or hyphen.",
        )
    return normalized


def build_metadata(
    *,
    package_name: str,
    effective_date: str,
    import_name: str | None,
    import_prefix: str = "BENEFITS_ELIG_",
) -> dict[str, str]:
    return {
        "Name": _import_name(import_name, import_prefix),
        "ComponentObjType": COMPONENT_OBJECT_TYPE,
        "EffectiveDate": _validated_effective_date(effective_date),
        "FileName": package_name,
        "Description": "Benefits Plan Copy REST import",
        "ReuseCode": "N",
        "SendNotifications": "N",
        "RequestSource": REQUEST_SOURCE,
    }


def _read_json_object(path: Path, description: str) -> dict[str, Any]:
    try:
        value = json.loads(path.resolve(strict=True).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PlanCopyImportError(
            "input validation", "approval", f"{description} is unreadable or invalid JSON: {path}"
        ) from exc
    if not isinstance(value, dict):
        raise PlanCopyImportError(
            "input validation", "approval", f"{description} must be a JSON object."
        )
    return value


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=path.name + ".",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, stat.S_IRUSR | stat.S_IWUSR)
        os.replace(temporary, path)
    except OSError as exc:
        raise PlanCopyImportError(
            "artifact persistence", "approval-preview", f"Unable to write preview: {path}"
        ) from exc
    finally:
        if temporary is not None:
            try:
                temporary.unlink()
            except FileNotFoundError:
                pass


def _rule_results(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    value = _read_json_object(path, "Rule-results file")
    results = value.get("ruleResults")
    if not isinstance(results, list):
        raise PlanCopyImportError(
            "input validation", "task-validation", "Rule-results file requires a ruleResults array."
        )
    return results


_BUILT_IN_PREVIEW_RULE_STATUSES = {
    "ora_input_validation.md": "passed",
    "ora_dependency_readiness.md": "passed",
    "ora_reference_lookups.md": "passed",
    "ora_design_enforcement.md": "passed",
    # The live execution gate is intentionally not applicable while building
    # the no-write preview. The separate approval path enforces it later.
    "ora_error_handling.md": "not_applicable",
}


def _preview_rule_results(
    *,
    task_context: Path,
    sequence: int,
    supplied: list[dict[str, Any]],
    task_name: str = TASK_NAME,
) -> list[dict[str, Any]]:
    """Return explicit results or the importer's built-in preflight evidence."""
    if supplied:
        return supplied
    try:
        plan = task_hook.resolve_task_rules_from_context(
            repository_root=REPOSITORY_ROOT,
            task_context_path=task_context.resolve(strict=True),
            task_name=task_name,
            sequence=sequence,
        )
    except (OSError, ValueError) as exc:
        raise PlanCopyImportError(
            "approval blocker",
            "task-validation",
            f"Unable to resolve task rule resources: {exc}",
        ) from exc

    resources = plan.get("ruleResources")
    if not isinstance(resources, list):
        raise PlanCopyImportError(
            "approval blocker",
            "task-validation",
            "Task rule plan has no ruleResources array.",
        )

    results: list[dict[str, Any]] = []
    for resource in resources:
        source = resource.get("file") if isinstance(resource, dict) else None
        status = _BUILT_IN_PREVIEW_RULE_STATUSES.get(source)
        if status is None:
            raise PlanCopyImportError(
                "approval blocker",
                "task-validation",
                f"No built-in evaluator is registered for task rule resource {source!r}; "
                "supply reviewed --rule-results.",
            )
        results.append(
            {
                "source": source,
                "status": status,
                "issues": [],
                "changes": [],
            }
        )
    return results


def build_approval_preview(
    *,
    archive_path: Path,
    archive_contents: bytes,
    contract: OpenApiContract,
    metadata: dict[str, str],
    import_objects: dict[str, Any],
    task_context: Path,
    sequence: int,
    rule_results: list[dict[str, Any]],
    task_name: str = TASK_NAME,
    operation_label: str = "Eligibility Plan Copy import",
) -> dict[str, Any]:
    final_data = {
        "archiveName": archive_path.name,
        "archivePath": str(archive_path),
        "archiveSha256": _sha256(archive_contents),
        "archiveSizeBytes": len(archive_contents),
        "openApiPath": str(contract.path),
        "openApiSha256": contract.sha256,
        "targetEnvironment": contract.base_url,
        "operation": operation_label,
        "metadata": metadata,
        "importObjects": import_objects,
        "workflow": [
            "create metadata",
            "upload enclosure",
            "generate mappings",
            "monitor the combined mapping and import ESS request",
            "verify zero unresolved mappings",
            "verify final Plan Copy status",
            "verify the consolidated RequestLogs import result",
        ],
    }
    try:
        evaluated_rule_results = _preview_rule_results(
            task_context=task_context,
            sequence=sequence,
            supplied=rule_results,
            task_name=task_name,
        )
        return task_hook.build_data_load_preview(
            {
                "taskContextPath": str(task_context.resolve(strict=True)),
                "taskName": task_name,
                "sequence": sequence,
                "finalData": final_data,
                "ruleResults": evaluated_rule_results,
            }
        )
    except (OSError, ValueError) as exc:
        raise PlanCopyImportError(
            "approval blocker", "task-validation", f"Task Hook preview failed: {exc}"
        ) from exc


def _preview_from_artifact(payload: dict[str, Any]) -> dict[str, Any]:
    preview = payload.get("preview")
    if not isinstance(preview, dict):
        raise PlanCopyImportError(
            "approval blocker", "approval", "Preview artifact has no Task Hook preview object."
        )
    return preview


def verify_and_approve_preview(
    *,
    preview_artifact: dict[str, Any],
    archive_path: Path,
    archive_contents: bytes,
    contract: OpenApiContract,
    import_objects: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, str]]:
    preview = _preview_from_artifact(preview_artifact)
    final_data = preview.get("finalData")
    if not isinstance(final_data, dict):
        raise PlanCopyImportError(
            "approval blocker", "approval", "Preview finalData is missing."
        )
    expected = {
        "archiveName": archive_path.name,
        "archivePath": str(archive_path),
        "archiveSha256": _sha256(archive_contents),
        "archiveSizeBytes": len(archive_contents),
        "openApiPath": str(contract.path),
        "openApiSha256": contract.sha256,
        "targetEnvironment": contract.base_url,
        "importObjects": import_objects,
    }
    changed = [key for key, value in expected.items() if final_data.get(key) != value]
    if changed:
        raise PlanCopyImportError(
            "approval blocker",
            "approval",
            "Approval preview is stale; changed fields: " + ", ".join(changed) + ".",
        )
    metadata = final_data.get("metadata")
    if (
        not isinstance(metadata, dict)
        or metadata.get("ComponentObjType") != COMPONENT_OBJECT_TYPE
        or metadata.get("RequestSource") != REQUEST_SOURCE
    ):
        raise PlanCopyImportError(
            "approval blocker", "approval", "Approval preview metadata is invalid."
        )
    if metadata.get("FileName") != archive_path.name:
        raise PlanCopyImportError(
            "approval blocker", "approval", "Approved metadata does not match the ZIP filename."
        )
    try:
        approved = task_hook.approve_data_load_preview({"preview": preview})
        task_hook.verify_approved_data_load_archive(approved, archive_path)
    except (OSError, ValueError) as exc:
        raise PlanCopyImportError(
            "approval blocker", "approval", f"Task Hook approval verification failed: {exc}"
        ) from exc
    return approved, {str(key): str(value) for key, value in metadata.items()}


def _safe_error_body(contents: bytes) -> str:
    text = contents.decode("utf-8", errors="replace")[:1500]
    text = re.sub(
        r"(?i)(authorization|access[_-]?token|password|client[_-]?secret)(\s*[:=]\s*)[^,}\s]+",
        r"\1\2<redacted>",
        text,
    )
    return " ".join(text.split())


class FusionSession:
    """Plan Copy error adapter over the shared OAuth REST transport."""

    def __init__(
        self,
        props: dict[str, str],
        args: argparse.Namespace,
    ) -> None:
        self.props = props
        self._client = rest_client_common.FusionRestSession(
            props,
            args,
            default_headers={"REST-Framework-Version": FRAMEWORK_VERSION},
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        raw_body: bytes | None = None,
        content_type: str | None = None,
        expected: set[int],
        stage: str,
        retry_auth: bool = True,
        parse_json: bool = True,
        accept: str = "application/json",
    ) -> HttpResult:
        try:
            return self._client.request(
                method,
                path,
                json_body=json_body,
                raw_body=raw_body,
                content_type=content_type,
                expected=expected,
                retry_auth=retry_auth,
                parse_json=parse_json,
                accept=accept,
            )
        except rest_client_common.FusionHttpError as exc:
            raise PlanCopyImportError(
                (
                    "auth_expired_or_invalid"
                    if exc.status_code == 401
                    else "authorization_or_privilege"
                    if exc.status_code == 403
                    else "Fusion API"
                ),
                stage,
                f"Fusion returned HTTP {exc.status_code}: "
                f"{_safe_error_body(exc.body.encode('utf-8'))}",
            ) from exc
        except RuntimeError as exc:
            raise PlanCopyImportError(
                "transport/environment", stage, f"Fusion request failed: {exc}"
            ) from exc


def _positive_identifier(payload: Any, keys: tuple[str, ...], description: str) -> int:
    if not isinstance(payload, dict):
        raise PlanCopyImportError(
            "Fusion API", description, "Fusion action response must be a JSON object."
        )
    for key in keys:
        value = payload.get(key)
        if isinstance(value, dict):
            value = value.get("RequestId") or value.get("requestId") or value.get("result")
        try:
            identifier = int(str(value))
        except (TypeError, ValueError):
            continue
        if identifier > 0:
            return identifier
    raise PlanCopyImportError(
        "Fusion API", description, f"Fusion response did not contain a positive {description} ID."
    )


def _render_path(template: str, **values: int) -> str:
    result = template
    for key, value in values.items():
        result = result.replace("{" + key + "}", str(value))
    if "{" in result or "}" in result:
        raise PlanCopyImportError(
            "catalog mismatch",
            "rest-contract-validation",
            "REST resource path has unresolved variables.",
        )
    return result


def _ess_label(status: dict[str, Any]) -> str:
    for key in ("stateDescription", "state", "processPhaseDescription", "processPhase", "cause"):
        value = status.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return "UNKNOWN"


def _is_successful_ess_status(status: dict[str, Any]) -> bool:
    """Accept the status codes and display values returned by Fusion ESS."""
    if ess_job_submitter.is_success_status(status):
        return True
    state = str(status.get("state") or "").strip().upper()
    error_fields = (
        status.get("errorType"),
        status.get("errorWarningMessage"),
        status.get("errorWarningDetail"),
    )
    return state in {"SUCCESS", "SUCCEEDED", "COMPLETED"} and not any(error_fields)


def poll_ess_request(
    session: FusionSession,
    path: str,
    *,
    request_id: int,
    purpose: str,
    wait_seconds: int,
    poll_interval: int,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    report_status: bool = True,
) -> dict[str, Any]:
    def fetch() -> dict[str, Any]:
        response = session.request(
            "GET", path, expected={200}, stage=f"monitor-{purpose}"
        )
        if not isinstance(response.body, dict):
            raise PlanCopyImportError(
                "Fusion API", f"monitor-{purpose}", "ESS status response must be a JSON object."
            )
        return response.body

    def report(status: dict[str, Any], elapsed: int) -> None:
        if report_status:
            status_label = _ess_label(status)
            _status(f"{purpose} ESS request {request_id}: {status_label} ({elapsed}s elapsed).")

    outcome = rest_client_common.poll_until(
        fetch,
        lambda status: (
            "success"
            if _is_successful_ess_status(status)
            else "failure"
            if ess_job_submitter.is_terminal_status(status)
            else "continue"
        ),
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
        clock=clock,
        sleep=sleep,
        on_observation=report,
    )
    last = outcome.value
    identifiers = {
        "environment": getattr(session, "props", {}).get("restBaseUrl"),
        "taskCode": TASK_CODE,
        "requestId": request_id,
        "lastStatus": _ess_label(last),
        "elapsedSeconds": outcome.elapsed_seconds,
        **({"ecid": last.get("ecid")} if last.get("ecid") else {}),
    }
    if outcome.state == "failure":
        raise PlanCopyImportError(
            "process failed",
            f"monitor-{purpose}",
            f"{purpose} ESS request reached unsuccessful terminal status {_ess_label(last)!r}.",
            identifiers=identifiers,
        )
    if outcome.state == "timeout":
        raise PlanCopyImportError(
            "process timeout",
            f"monitor-{purpose}",
            f"Timed out after {outcome.elapsed_seconds}s waiting for {purpose} ESS request.",
            identifiers=identifiers,
        )
    return last


def _page_items(body: Any, stage: str) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(body, dict) or not isinstance(body.get("items"), list):
        raise PlanCopyImportError(
            "Fusion API", stage, "Fusion collection response must contain an items array."
        )
    items = [item for item in body["items"] if isinstance(item, dict)]
    if len(items) != len(body["items"]):
        raise PlanCopyImportError("Fusion API", stage, "Fusion collection contains a non-object row.")
    has_more_value = body.get("hasMore", False)
    has_more = has_more_value is True or str(has_more_value).strip().casefold() == "true"
    return items, has_more


def get_mappings(
    session: FusionSession,
    base_path: str,
    *,
    unresolved_only: bool,
    limit: int = 500,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        query = {
            "fields": (
                "PlCopyMapId,SrcId,SrcName,TrgId,TrgName,ComponentObjType,"
                "ComponentObjName,ObjectVersionNumber"
            ),
            "limit": str(limit),
            "offset": str(offset),
            "totalResults": "true",
        }
        if unresolved_only:
            query["q"] = "TrgId is null"
        path = base_path + "?" + urllib.parse.urlencode(query)
        response = session.request("GET", path, expected={200}, stage="mapping-verification")
        page, has_more = _page_items(response.body, "mapping-verification")
        rows.extend(page)
        if not has_more:
            return rows
        if not page:
            raise PlanCopyImportError(
                "Fusion API", "mapping-verification", "Mapping pagination reported hasMore without rows."
            )
        offset += len(page)


def _parent_status_failure(parent: Any, field: str, stage: str) -> None:
    if not isinstance(parent, dict):
        raise PlanCopyImportError("Fusion API", stage, "Plan Copy parent response must be an object.")
    value = str(parent.get(field) or "").strip()
    if value == str(PROCESS_ERROR):
        raise PlanCopyImportError(
            "process failed", stage, f"Plan Copy parent reports {field}=ERROR ({PROCESS_ERROR})."
        )
    if value and ess_job_submitter.terminal_by_text(value):
        normalized = value.upper()
        failure_tokens = ("ERROR", "FAIL", "CANCEL", "EXPIRE", "TIMEOUT", "TIMED OUT")
        if any(token in normalized for token in failure_tokens):
            raise PlanCopyImportError(
                "process failed", stage, f"Plan Copy parent reports {field}={value!r}."
            )


def _mapping_status_label(value: Any) -> str:
    """Return the user-facing outcome derived from MappingRequestStatus."""
    normalized = str(value or "").strip().upper()
    if normalized == str(PROCESS_SUCCESS) or normalized in {
        "SUCCESS",
        "SUCCEEDED",
        "COMPLETED",
    }:
        return "SUCCESS"
    if normalized == str(PROCESS_ERROR) or any(
        token in normalized
        for token in ("ERROR", "FAIL", "CANCEL", "EXPIRE", "TIMEOUT", "TIMED OUT")
    ):
        return "ERROR"
    return "IN_PROGRESS" if normalized else "UNKNOWN"


def _processing_log_rows(session: FusionSession, logs_path: str) -> list[dict[str, Any]]:
    response = session.request(
        "GET",
        logs_path + "?limit=500&totalResults=true",
        expected={200},
        stage="import-logs",
    )
    rows, _ = _page_items(response.body, "import-logs")
    return rows


def _processing_log_messages(rows: list[dict[str, Any]], limit: int = 5) -> list[str]:
    messages: list[str] = []
    for row in rows:
        value = next(
            (
                row.get(key)
                for key in ("Message", "message", "LogMessage", "ProcessLog")
                if row.get(key) not in {None, ""}
            ),
            None,
        )
        if value is None:
            continue
        message = _safe_error_body(str(value).encode("utf-8", errors="replace"))
        if message and message not in messages:
            messages.append(message)
        if len(messages) >= limit:
            break
    return messages


_REQUEST_LOG_ERROR_PATTERN = re.compile(
    r"(?i)(?:\b(?:cannot|exception|failed|failure|severe)\b|"
    r"\b(?:ORA|JBO)-\d+\b|"
    r"\bJBO-[A-Z][A-Z0-9_]*:::[A-Z][A-Z0-9_]*\b|\berrors?\b)"
)
_REQUEST_LOG_NO_ERROR_PATTERN = re.compile(
    r"(?i)(?:\bno\s+errors?\b|\berrors?\s*[:=]\s*0\b|\b0\s+errors?\b)"
)


def _request_log_error_messages(text: str, limit: int = 5) -> list[str]:
    """Return unique, redacted error lines from PARAM_ATTRIBUTE_BLOB2."""
    messages: list[str] = []
    for line in text.splitlines():
        normalized = " ".join(line.split())
        if (
            not normalized
            or _REQUEST_LOG_NO_ERROR_PATTERN.search(normalized)
            or not _REQUEST_LOG_ERROR_PATTERN.search(normalized)
        ):
            continue
        message = _safe_error_body(normalized.encode("utf-8", errors="replace"))
        if message and message not in messages:
            messages.append(message)
        if len(messages) >= limit:
            break
    return messages


def _request_log_evidence(session: FusionSession, request_log_path: str) -> dict[str, Any]:
    """Read the REST enclosure backed by BEN_PL_COPY_PARAMS.PARAM_ATTRIBUTE_BLOB2."""
    response = session.request(
        "GET",
        request_log_path,
        expected={200},
        stage="import-request-log",
        parse_json=False,
        accept="application/octet-stream",
    )
    contents = response.body
    if isinstance(contents, str):
        contents = contents.encode("utf-8")
    if not isinstance(contents, bytes):
        raise PlanCopyImportError(
            "Fusion API",
            "import-request-log",
            "Plan Copy RequestLogs enclosure did not return binary or text content.",
        )
    if len(contents) > MAX_REQUEST_LOG_BYTES:
        raise PlanCopyImportError(
            "Fusion API",
            "import-request-log",
            f"Plan Copy RequestLogs enclosure exceeds {MAX_REQUEST_LOG_BYTES} bytes.",
        )
    text = contents.decode("utf-8", errors="replace")
    return {
        "sizeBytes": len(contents),
        "text": text,
        "errorMessages": _request_log_error_messages(text),
    }


def _raise_with_request_log(
    error: PlanCopyImportError,
    evidence: dict[str, Any],
    identifiers: dict[str, Any],
) -> None:
    messages = evidence["errorMessages"]
    detail = (
        " Consolidated import log: " + " | ".join(messages)
        if messages
        else " The consolidated import log contained no recognized error message."
    )
    raise PlanCopyImportError(
        error.failure_class,
        error.stage,
        error.message + detail,
        identifiers={
            **identifiers,
            "mappingStatus": "ERROR",
            "requestLogSizeBytes": evidence["sizeBytes"],
            "requestLogErrorCount": len(messages),
            "errorDetails": messages or [error.message],
        },
    ) from error


def _recover_failed_import_log(
    error: PlanCopyImportError,
    session: FusionSession,
    contract: OpenApiContract,
) -> None:
    """Read a known import's consolidated log without replacing its failure."""
    pl_copy_id = error.identifiers.get("plCopyId")
    if not pl_copy_id or "requestLogSizeBytes" in error.identifiers:
        return
    if error.stage == "import-request-log":
        return
    request_log_path = _render_path(
        contract.operations["request_log"], plCopyId=pl_copy_id
    )
    try:
        evidence = _request_log_evidence(session, request_log_path)
    except PlanCopyImportError as log_error:
        error.identifiers["requestLogRecoveryError"] = log_error.message
        details = list(error.identifiers.get("errorDetails") or [error.message])
        details.append("Unable to retrieve consolidated RequestLogs: " + log_error.message)
        error.identifiers["errorDetails"] = details
        return
    messages = evidence["errorMessages"]
    error.identifiers["requestLogSizeBytes"] = evidence["sizeBytes"]
    error.identifiers["requestLogErrorCount"] = len(messages)
    if messages:
        error.message += " Consolidated import log: " + " | ".join(messages)
        error.args = (error.message,)
        error.identifiers["errorDetails"] = messages
    else:
        details = list(error.identifiers.get("errorDetails") or [error.message])
        details.append(
            "The consolidated RequestLogs log is empty."
            if not evidence["text"].strip()
            else "No recognized error message in consolidated RequestLogs."
        )
        error.identifiers["errorDetails"] = details


def poll_plan_copy_import_status(
    session: FusionSession,
    parent_path: str,
    logs_path: str,
    request_log_path: str,
    *,
    identifiers: dict[str, Any],
    wait_seconds: int,
    poll_interval: int,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[dict[str, Any], list[dict[str, Any]], dict[str, Any]]:
    """Require the Plan Copy application result after ESS itself succeeds."""
    def fetch() -> dict[str, Any]:
        response = session.request(
            "GET", parent_path, expected={200}, stage="import-parent-status"
        )
        if not isinstance(response.body, dict):
            raise PlanCopyImportError(
                "Fusion API",
                "import-parent-status",
                "Plan Copy parent response must be an object.",
                identifiers=identifiers,
            )
        return response.body

    def classify(parent: dict[str, Any]) -> str:
        import_value = str(parent.get("ImportPlDesign") or "").strip()
        request_failed = False
        try:
            _parent_status_failure(parent, "RequestStatus", "import-parent-status")
        except PlanCopyImportError:
            request_failed = True
        if import_value == str(PROCESS_SUCCESS) and not request_failed:
            return "success"
        if import_value == str(PROCESS_ERROR) or request_failed:
            return "failure"
        return "continue"

    def report(parent: dict[str, Any], elapsed: int) -> None:
        if classify(parent) != "continue":
            return
        _status(f"Plan Copy import is still processing ({elapsed}s elapsed).")

    outcome = rest_client_common.poll_until(
        fetch,
        classify,
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
        clock=clock,
        sleep=sleep,
        on_observation=report,
    )
    last_parent = outcome.value
    import_value = str(last_parent.get("ImportPlDesign") or "").strip()
    request_value = str(last_parent.get("RequestStatus") or "").strip()
    request_log = _request_log_evidence(session, request_log_path)
    request_log_errors = request_log["errorMessages"]
    if request_log_errors:
        raise PlanCopyImportError(
            "process failed",
            "import-request-log",
            "The consolidated Plan Copy import log reports errors: "
            + " | ".join(request_log_errors),
            identifiers={
                **identifiers,
                "mappingStatus": "ERROR",
                "importPlDesign": import_value or "UNKNOWN",
                "requestStatus": request_value or "UNKNOWN",
                "requestLogSizeBytes": request_log["sizeBytes"],
                "requestLogErrorCount": len(request_log_errors),
                "errorDetails": request_log_errors,
            },
        )
    if outcome.state == "success":
        if not request_log["text"].strip():
            raise PlanCopyImportError(
                "process failed",
                "import-request-log",
                "Plan Copy parent reached success, but the consolidated import log is empty.",
                identifiers={
                    **identifiers,
                    "mappingStatus": "ERROR",
                    "importPlDesign": import_value,
                    "requestStatus": request_value or "UNKNOWN",
                    "requestLogSizeBytes": 0,
                    "requestLogErrorCount": 0,
                    "errorDetails": [
                        "The consolidated Plan Copy import log is empty."
                    ],
                },
            )
        return last_parent, _processing_log_rows(session, logs_path), request_log
    if outcome.state == "failure":
        logs = _processing_log_rows(session, logs_path)
        messages = _processing_log_messages(logs)
        detail = (
            " Processing log: " + " | ".join(messages)
            if messages
            else " The consolidated RequestLogs log contained no recognized error message. "
            "No processing-log rows were returned by REST."
        )
        raise PlanCopyImportError(
            "process failed",
            "import-parent-status",
            "The ESS request succeeded, but the Plan Copy application result is "
            f"ImportPlDesign={import_value or 'UNKNOWN'}, "
            f"RequestStatus={request_value or 'UNKNOWN'}.{detail}",
            identifiers={
                **identifiers,
                "mappingStatus": "ERROR",
                "importPlDesign": import_value or "UNKNOWN",
                "requestStatus": request_value or "UNKNOWN",
                "processingLogCount": len(logs),
                "requestLogSizeBytes": request_log["sizeBytes"],
                "requestLogErrorCount": len(request_log_errors),
                "errorDetails": messages or [
                    "No recognized error message in RequestLogs; no child processing-log "
                    "error details were returned."
                ],
            },
        )
    raise PlanCopyImportError(
        "process timeout",
        "import-parent-status",
        "ESS succeeded, but the Plan Copy parent did not reach application status "
        f"{PROCESS_SUCCESS} or {PROCESS_ERROR} within {outcome.elapsed_seconds}s.",
        identifiers={
            **identifiers,
            "importPlDesign": import_value or "UNKNOWN",
            "requestStatus": request_value or "UNKNOWN",
            "elapsedSeconds": outcome.elapsed_seconds,
            "requestLogSizeBytes": request_log["sizeBytes"],
            "requestLogErrorCount": len(request_log_errors),
        },
    )


def print_import_object_summary(
    import_objects: dict[str, Any], *, indent: str = "  "
) -> None:
    """Print a concise, reviewable inventory of setup objects in the package."""
    print(f"{indent}Setup objects: {import_objects['setupObjectCount']}")
    print(f"{indent}  Eligibility profiles: {import_objects['eligibilityProfileCount']}")
    for profile in import_objects["eligibilityProfiles"]:
        print(
            f"{indent}    - {profile['name']}: {profile['criterionCount']} criterion row(s)"
        )
    print(f"{indent}  Benefit Groups: {import_objects['benefitGroupCount']}")
    for group in import_objects["benefitGroups"]:
        legal_employer = group["legalEmployer"] or "none"
        print(
            f"{indent}    - {group['name']}: Legal Employer {legal_employer}"
        )
    print(f"{indent}  Benefit Balances: {import_objects['benefitBalanceCount']}")
    for balance in import_objects["benefitBalances"]:
        legal_employer = balance["legalEmployer"] or "none"
        print(
            f"{indent}    - {balance['name']}: Legal Employer {legal_employer}"
        )
    print(f"{indent}  Postal Code Ranges: {import_objects['postalCodeRangeCount']}")
    for postal_range in import_objects["postalCodeRanges"]:
        print(f"{indent}    - {postal_range}")
    print(f"{indent}  Service Areas: {import_objects['serviceAreaCount']}")
    for service_area in import_objects["serviceAreas"]:
        print(
            f"{indent}    - {service_area['name']}: "
            f"{len(service_area['postalCodeRanges'])} Postal Code Range(s)"
        )
    print(f"{indent}  Age factors: {import_objects['ageFactorCount']}")
    for factor_name in import_objects["ageFactors"]:
        print(f"{indent}    - {factor_name}")
    print(
        f"{indent}  Compensation factors: "
        f"{import_objects['compensationFactorCount']}"
    )
    for factor_name in import_objects["compensationFactors"]:
        print(f"{indent}    - {factor_name}")
    print(
        f"{indent}  Length of Service factors: "
        f"{import_objects['lengthOfServiceFactorCount']}"
    )
    for factor_name in import_objects["lengthOfServiceFactors"]:
        print(f"{indent}    - {factor_name}")
    print(
        f"{indent}  Age and Service factors: "
        f"{import_objects['combinedAgeLosFactorCount']}"
    )
    for factor_name in import_objects["combinedAgeLosFactors"]:
        print(f"{indent}    - {factor_name}")
    print(
        f"{indent}  Hours Worked factors: "
        f"{import_objects['hoursWorkedFactorCount']}"
    )
    for factor_name in import_objects["hoursWorkedFactors"]:
        print(f"{indent}    - {factor_name}")
    print(
        f"{indent}  Full-Time Equivalent factors: "
        f"{import_objects['fullTimeEquivalentFactorCount']}"
    )
    for factor_name in import_objects["fullTimeEquivalentFactors"]:
        print(f"{indent}    - {factor_name}")
    print(f"{indent}  Eligibility criterion rows: {import_objects['criterionRowCount']}")
    for criterion in import_objects["criterionTypeCounts"]:
        print(f"{indent}    - {criterion['type']}: {criterion['count']}")
    print(
        f"{indent}Supporting Plan Copy mappings: "
        f"{import_objects['planCopyMappingCount']} row(s)"
    )


def prompt_upload_approval(summary: dict[str, Any]) -> None:
    """Display the immutable upload summary and require exact interactive approval."""
    print("\nPlan Copy upload summary")
    print(f"  Target: {summary['targetEnvironment']}")
    print(f"  ZIP: {summary['archiveName']} ({summary['archiveSizeBytes']} bytes)")
    print(f"  ZIP SHA-256: {summary['archiveSha256']}")
    print(f"  Import name: {summary['importName']}")
    print(f"  Effective date: {summary['effectiveDate']}")
    print("  Objects to import:")
    print_import_object_summary(summary["importObjects"], indent="    ")
    print(
        "  Next action: create the Benefits Plan Copy import, upload "
        "this ZIP, then submit and monitor the combined mapping and import request"
    )
    try:
        response = input("Type exactly 'approve' to create and upload this Plan Copy import: ")
    except EOFError as exc:
        raise PlanCopyImportError(
            "approval blocker",
            "upload-approval",
            "Interactive approval input was unavailable; no Plan Copy POST or PUT was called.",
        ) from exc
    if response.strip() != "approve":
        raise PlanCopyImportError(
            "approval blocker",
            "upload-approval",
            "Approval was not the exact word 'approve'; no Plan Copy POST or PUT was called.",
        )
    _status("Plan Copy upload approved; starting the import workflow.")


def _verify_mappings_and_finalize(
    *,
    session: FusionSession,
    contract: OpenApiContract,
    pl_copy_id: int,
    mapping_status: dict[str, Any],
    identifiers: dict[str, Any],
    wait_seconds: int,
    poll_interval: int,
    clock: Callable[[], float],
    sleep: Callable[[float], None],
    expected_mapping_count: int | None = None,
) -> dict[str, Any]:
    parent_path = _render_path(contract.operations["parent"], plCopyId=pl_copy_id)
    parent = session.request(
        "GET", parent_path, expected={200}, stage="mapping-parent-status"
    ).body
    if isinstance(parent, dict):
        parent_name = str(parent.get("Name") or "").strip()
        if parent_name:
            identifiers["planCopyName"] = parent_name
        identifiers["mappingStatus"] = _mapping_status_label(
            parent.get("MappingRequestStatus")
        )
    try:
        _parent_status_failure(parent, "MappingRequestStatus", "mapping-parent-status")
    except PlanCopyImportError as exc:
        request_log_path = _render_path(
            contract.operations["request_log"], plCopyId=pl_copy_id
        )
        _raise_with_request_log(
            exc,
            _request_log_evidence(session, request_log_path),
            identifiers,
        )

    mappings_path = _render_path(contract.operations["unresolved"], plCopyId=pl_copy_id)
    unresolved_candidates = get_mappings(session, mappings_path, unresolved_only=True)
    unresolved = [
        row
        for row in unresolved_candidates
        if str(row.get("SrcName") or "").strip() and row.get("TrgId") in {None, ""}
    ]
    if unresolved:
        names = [str(row.get("SrcName")) for row in unresolved[:10]]
        suffix = "" if len(unresolved) <= 10 else f" and {len(unresolved) - 10} more"
        raise PlanCopyImportError(
            "catalog mismatch",
            "mapping-verification",
            f"{len(unresolved)} mandatory mapping(s) remain unresolved: {', '.join(names)}{suffix}.",
            identifiers=identifiers,
        )
    all_mappings = get_mappings(session, mappings_path, unresolved_only=False)
    unresolved_all = [
        row
        for row in all_mappings
        if str(row.get("SrcName") or "").strip() and row.get("TrgId") in {None, ""}
    ]
    if unresolved_all:
        raise PlanCopyImportError(
            "catalog mismatch",
            "mapping-verification",
            "The complete mapping list still contains unresolved source mappings.",
            identifiers=identifiers,
        )
    resolved_count = sum(
        1
        for row in all_mappings
        if str(row.get("SrcName") or "").strip() and row.get("TrgId") not in {None, ""}
    )
    if resolved_count == 0 and expected_mapping_count != 0:
        raise PlanCopyImportError(
            "catalog mismatch",
            "mapping-verification",
            "Fusion returned no resolved source mappings for the uploaded eligibility package.",
            identifiers=identifiers,
        )
    _status(f"Mapping verification passed: 0 unresolved; {resolved_count} resolved mapping(s).")
    logs_path = _render_path(contract.operations["logs"], plCopyId=pl_copy_id)
    request_log_path = _render_path(
        contract.operations["request_log"], plCopyId=pl_copy_id
    )
    parent, log_rows, request_log = poll_plan_copy_import_status(
        session,
        parent_path,
        logs_path,
        request_log_path,
        identifiers=identifiers,
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
        clock=clock,
        sleep=sleep,
    )
    _status(f"Plan Copy import completed successfully; retrieved {len(log_rows)} processing log row(s).")
    return {
        **identifiers,
        "targetEnvironment": contract.base_url,
        "mappingResolvedCount": resolved_count,
        "mappingUnresolvedCount": 0,
        "mappingStatus": identifiers.get("mappingStatus", "SUCCESS"),
        "importStatus": _ess_label(mapping_status),
        "planCopyImportStatusCode": PROCESS_SUCCESS,
        "planCopyRequestStatus": parent.get("RequestStatus"),
        "finalStatus": "SUCCESS",
        "processingLogCount": len(log_rows),
        "requestLogStatus": "SUCCESS",
        "requestLogSizeBytes": request_log["sizeBytes"],
        "requestLogErrorCount": 0,
    }


def _execute_import(
    *,
    session: FusionSession,
    contract: OpenApiContract,
    archive_contents: bytes,
    metadata: dict[str, str],
    import_objects: dict[str, Any],
    wait_seconds: int,
    poll_interval: int,
    identifiers: dict[str, Any],
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    approve_upload: Callable[[dict[str, Any]], None] = prompt_upload_approval,
) -> dict[str, Any]:
    if metadata.get("RequestSource") != REQUEST_SOURCE:
        raise PlanCopyImportError(
            "input validation",
            "metadata-validation",
            f"Plan Copy metadata requires RequestSource={REQUEST_SOURCE}.",
        )
    session_props = getattr(session, "props", {})
    session_base_url = (
        session_props.get("restBaseUrl") if isinstance(session_props, dict) else None
    )
    approve_upload(
        {
            "targetEnvironment": session_base_url or contract.base_url,
            "archiveName": metadata["FileName"],
            "archiveSizeBytes": len(archive_contents),
            "archiveSha256": _sha256(archive_contents),
            "importName": metadata["Name"],
            "effectiveDate": metadata["EffectiveDate"],
            "importObjects": import_objects,
        }
    )

    _status("Creating the Plan Copy import metadata row.")
    created = session.request(
        "POST",
        contract.operations["create"],
        json_body=metadata,
        content_type=ADF_ITEM_MEDIA_TYPE,
        expected={201},
        stage="create-import",
        retry_auth=False,
    )
    pl_copy_id = _positive_identifier(created.body, ("PlCopyId", "plCopyId"), "PlCopyId")
    identifiers["plCopyId"] = pl_copy_id
    _status(
        f"Created Plan Copy import '{metadata['Name']}'; uploading "
        f"{metadata['FileName']}."
    )

    session.request(
        "PUT",
        _render_path(contract.operations["upload"], plCopyId=pl_copy_id),
        raw_body=archive_contents,
        content_type=PACKAGE_MEDIA_TYPE,
        expected={204},
        stage="upload-enclosure",
        retry_auth=False,
    )
    _status("ZIP upload completed; submitting the combined mapping and import request.")
    generated = session.request(
        "POST",
        _render_path(contract.operations["generate"], plCopyId=pl_copy_id),
        json_body={},
        content_type=ADF_ACTION_MEDIA_TYPE,
        expected={200},
        stage="generate-mappings",
        retry_auth=False,
    )
    mapping_request_id = _positive_identifier(
        generated.body, ("result", "RequestId", "requestId"), "mapping request"
    )
    identifiers["mappingRequestId"] = mapping_request_id
    mapping_status = poll_ess_request(
        session,
        _render_path(
            contract.operations["ess_mapping"], mappingRequestId=mapping_request_id
        ),
        request_id=mapping_request_id,
        purpose="Plan Copy mapping and import",
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
        clock=clock,
        sleep=sleep,
        report_status=False,
    )
    return _verify_mappings_and_finalize(
        session=session,
        contract=contract,
        pl_copy_id=pl_copy_id,
        mapping_status=mapping_status,
        expected_mapping_count=import_objects.get("planCopyMappingCount"),
        identifiers=identifiers,
        wait_seconds=wait_seconds,
        poll_interval=poll_interval,
        clock=clock,
        sleep=sleep,
    )


def execute_import(
    *,
    session: FusionSession,
    contract: OpenApiContract,
    archive_contents: bytes,
    metadata: dict[str, str],
    import_objects: dict[str, Any],
    wait_seconds: int,
    poll_interval: int,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
    approve_upload: Callable[[dict[str, Any]], None] = prompt_upload_approval,
) -> dict[str, Any]:
    """Execute once and retain every server-issued identifier on failure."""
    identifiers: dict[str, Any] = {"planCopyName": metadata["Name"]}
    try:
        result = _execute_import(
            session=session,
            contract=contract,
            archive_contents=archive_contents,
            metadata=metadata,
            import_objects=import_objects,
            wait_seconds=wait_seconds,
            poll_interval=poll_interval,
            identifiers=identifiers,
            clock=clock,
            sleep=sleep,
            approve_upload=approve_upload,
        )
        result["planCopyName"] = metadata["Name"]
        return result
    except PlanCopyImportError as exc:
        exc.identifiers = {**identifiers, **exc.identifiers}
        _recover_failed_import_log(exc, session, contract)
        raise


def resume_import_after_mapping(
    *,
    session: FusionSession,
    contract: OpenApiContract,
    pl_copy_id: int,
    mapping_request_id: int,
    wait_seconds: int,
    poll_interval: int,
    clock: Callable[[], float] = time.monotonic,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Continue an existing import without recreating metadata or re-uploading its ZIP."""
    identifiers: dict[str, Any] = {
        "plCopyId": pl_copy_id,
        "mappingRequestId": mapping_request_id,
    }
    try:
        _status(
            "Resuming the existing Plan Copy import; no metadata row or ZIP is created."
        )
        mapping_status = poll_ess_request(
            session,
            _render_path(
                contract.operations["ess_mapping"],
                mappingRequestId=mapping_request_id,
            ),
            request_id=mapping_request_id,
            purpose="Plan Copy mapping and import",
            wait_seconds=wait_seconds,
            poll_interval=poll_interval,
            clock=clock,
            sleep=sleep,
            report_status=False,
        )
        return _verify_mappings_and_finalize(
            session=session,
            contract=contract,
            pl_copy_id=pl_copy_id,
            mapping_status=mapping_status,
            identifiers=identifiers,
            wait_seconds=wait_seconds,
            poll_interval=poll_interval,
            clock=clock,
            sleep=sleep,
        )
    except PlanCopyImportError as exc:
        exc.identifiers = {**identifiers, **exc.identifiers}
        _recover_failed_import_log(exc, session, contract)
        raise


def _preview_output(args: argparse.Namespace, archive_path: Path) -> Path:
    return (
        args.preview_output.resolve()
        if args.preview_output is not None
        else archive_path.with_name(archive_path.name + ".plan-copy-import-preview.json")
    )


def _print_preview_result(
    *,
    output: Path,
    archive_path: Path,
    archive_contents: bytes,
    contract: OpenApiContract,
    metadata: dict[str, str],
    import_objects: dict[str, Any],
) -> None:
    """Render the approval preview and object inventory."""
    print(f"Approval preview: {output}")
    print(f"Target environment: {contract.base_url}")
    print(f"ZIP: {archive_path} ({len(archive_contents)} bytes)")
    print(f"SHA-256: {_sha256(archive_contents)}")
    print(f"Import name: {metadata['Name']}")
    print("Objects to import:")
    print_import_object_summary(import_objects)
    print("No Fusion POST or PUT request was sent.")
    print("Reply exactly `approve` to authorize this immutable preview.")


def _user_facing_import_result(result: dict[str, Any]) -> dict[str, Any]:
    """Expose only the Plan Copy name and mapping-derived outcome."""
    displayed = {
        "planCopyName": result.get("planCopyName"),
        "status": result.get("mappingStatus") or "UNKNOWN",
    }
    if result.get("errorDetails"):
        displayed["errorDetails"] = result["errorDetails"]
    return displayed


def _user_facing_import_error(error: PlanCopyImportError) -> dict[str, Any]:
    """Render a failed import without exposing internal recovery identifiers."""
    identifiers = error.identifiers
    details = identifiers.get("errorDetails")
    if not isinstance(details, list) or not details:
        details = [error.message]
    displayed: dict[str, Any] = {
        "status": "ERROR",
        "errorDetails": details,
    }
    plan_copy_name = identifiers.get("planCopyName")
    if plan_copy_name:
        displayed = {"planCopyName": plan_copy_name, **displayed}
    return displayed


def _print_import_result(result: dict[str, Any]) -> None:
    """Render the completed import result without internal IDs or ESS state."""
    print(json.dumps(_user_facing_import_result(result), indent=2, sort_keys=True))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate an Eligibility Plan Copy ZIP and OpenAPI contract, create a Task Hook "
            "approval preview, or execute the approved import and monitor its combined ESS request."
        ),
        allow_abbrev=False,
    )
    parser.add_argument("--zip", required=True, type=Path, help="Generated benefits_eligibility.zip.")
    parser.add_argument(
        "--openapi",
        required=True,
        type=Path,
        help="OpenAPI 3.1.2 document for the Plan Copy REST API.",
    )
    parser.add_argument(
        "--target-origin",
        help=(
            "Explicit HTTPS origin override; endpoint paths and payloads remain fixed by "
            "the reviewed OpenAPI document and the selected origin is approval-bound."
        ),
    )
    parser.add_argument(
        "--properties",
        type=Path,
        default=rest_client_common.DEFAULT_PROPERTIES_PATH,
        help="OAuth properties configured for the effective target origin.",
    )
    parser.add_argument(
        "--effective-date",
        help="Import effective date; defaults to the workbook Session Effective Date.",
    )
    parser.add_argument(
        "--workbook",
        type=Path,
        help=(
            "Workbook containing Benefit Balances; used only to derive the common "
            "Session Effective Date for Plan Copy metadata."
        ),
    )
    parser.add_argument("--import-name", help="Immutable import name to include in the approval preview.")
    parser.add_argument(
        "--import-prefix",
        default="BENEFITS_ELIG_",
        help="Prefix used when --import-name is omitted.",
    )
    parser.add_argument(
        "--task-name",
        default=TASK_NAME,
        help="Task name in the supplied task-context JSON.",
    )
    parser.add_argument(
        "--operation-label",
        default="Eligibility Plan Copy import",
        help="Customer-facing operation bound into the approval preview.",
    )
    parser.add_argument("--task-context", type=Path, help="Existing Run Book task-context JSON.")
    parser.add_argument("--sequence", type=int, default=1, help="Task sequence in task context.")
    parser.add_argument(
        "--rule-results",
        type=Path,
        help=(
            "Optional reviewed Task Hook ruleResults JSON. When omitted, the importer "
            "reports the built-in package, target, REST lookup, and design preflight results."
        ),
    )
    parser.add_argument("--preview-output", type=Path, help="Approval preview JSON destination.")
    parser.add_argument(
        "--approve-upload",
        action="store_true",
        help="Execute only after a later standalone user message exactly `approve`.",
    )
    parser.add_argument(
        "--approval-preview",
        type=Path,
        help="Exact preview JSON produced before approval; required with --approve-upload.",
    )
    parser.add_argument(
        "--tls-cert-sha256",
        help="Exact development/test pod leaf-certificate SHA-256 fingerprint.",
    )
    parser.add_argument(
        "--resume-pl-copy-id",
        type=int,
        help="Existing PlCopyId to resume after mapping generation; never creates or uploads.",
    )
    parser.add_argument(
        "--mapping-request-id",
        type=int,
        help="Existing mapping ESS request paired with --resume-pl-copy-id.",
    )
    parser.add_argument("--wait-seconds", type=int, default=DEFAULT_WAIT_SECONDS)
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL_SECONDS)
    parser.add_argument("--timeout", type=int, default=60, help="Per-request timeout in seconds.")
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=300)
    parser.add_argument("--token-cache", default="auto")
    parser.add_argument("--force-login", action="store_true")
    parser.set_defaults(access_token=None)
    parser.add_argument("--open-browser", action="store_true", default=True)
    parser.add_argument("--no-open-browser", action="store_false", dest="open_browser")
    args = parser.parse_args(argv)
    if args.sequence < 1:
        parser.error("--sequence must be positive.")
    if args.wait_seconds < 0:
        parser.error("--wait-seconds must not be negative.")
    if args.poll_interval < 1 or args.poll_interval > MAX_POLL_INTERVAL_SECONDS:
        parser.error(f"--poll-interval must be between 1 and {MAX_POLL_INTERVAL_SECONDS}.")
    if args.timeout < 1:
        parser.error("--timeout must be positive.")
    if bool(args.resume_pl_copy_id) != bool(args.mapping_request_id):
        parser.error("--resume-pl-copy-id and --mapping-request-id are required together.")
    if args.resume_pl_copy_id is not None and args.resume_pl_copy_id < 1:
        parser.error("--resume-pl-copy-id must be positive.")
    if args.mapping_request_id is not None and args.mapping_request_id < 1:
        parser.error("--mapping-request-id must be positive.")
    if args.resume_pl_copy_id is not None and args.target_origin is not None:
        parser.error("Resume mode cannot be combined with --target-origin.")
    if args.tls_cert_sha256 is not None:
        try:
            args.tls_cert_sha256 = rest_client_common.normalize_tls_cert_sha256(
                args.tls_cert_sha256
            )
        except ValueError as exc:
            parser.error(str(exc))
    if args.approve_upload and args.approval_preview is None:
        parser.error("--approval-preview is required with --approve-upload.")
    if (
        args.resume_pl_copy_id is None
        and not args.approve_upload
        and args.task_context is None
    ):
        parser.error("--task-context is required to build the Task Hook approval preview.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return _run(args)


def _run(args: argparse.Namespace) -> int:
    try:
        _status("Validating the Plan Copy OpenAPI document.")
        contract = load_openapi_contract(args.openapi)
        _status("Validating the exact nested Plan Copy ZIP.")
        archive_path, archive_contents, import_objects = _read_package(args.zip)
        effective_date = _effective_date_for_import(
            workbook=args.workbook,
            explicit_effective_date=args.effective_date,
            contract_effective_date=contract.effective_date,
        )

        props = _oauth_properties(args.properties, args.target_origin)
        contract = replace(contract, base_url=props["restBaseUrl"])

        if args.resume_pl_copy_id is not None:
            _status("Acquiring OAuth authorization to resume the existing Plan Copy import.")
            try:
                session = FusionSession(props, args)
            except Exception as exc:
                raise PlanCopyImportError(
                    "auth/authz", "oauth-login", "Unable to obtain OAuth authorization."
                ) from exc
            result = resume_import_after_mapping(
                session=session,
                contract=contract,
                pl_copy_id=args.resume_pl_copy_id,
                mapping_request_id=args.mapping_request_id,
                wait_seconds=args.wait_seconds,
                poll_interval=args.poll_interval,
            )
            _print_import_result(result)
            return 0

        if not args.approve_upload:
            metadata = build_metadata(
                package_name=archive_path.name,
                effective_date=effective_date,
                import_name=args.import_name,
                import_prefix=args.import_prefix,
            )
            _status("Building the immutable Task Hook approval preview; no Fusion request is sent.")
            preview = build_approval_preview(
                archive_path=archive_path,
                archive_contents=archive_contents,
                contract=contract,
                metadata=metadata,
                import_objects=import_objects,
                task_context=args.task_context,
                sequence=args.sequence,
                rule_results=_rule_results(args.rule_results),
                task_name=args.task_name,
                operation_label=args.operation_label,
            )
            output = _preview_output(args, archive_path)
            _atomic_json(output, preview)
            _print_preview_result(
                output=output,
                archive_path=archive_path,
                archive_contents=archive_contents,
                contract=contract,
                metadata=metadata,
                import_objects=import_objects,
            )
            return 0

        preview_artifact = _read_json_object(args.approval_preview, "Approval preview")
        _approved, metadata = verify_and_approve_preview(
            preview_artifact=preview_artifact,
            archive_path=archive_path,
            archive_contents=archive_contents,
            contract=contract,
            import_objects=import_objects,
        )
        if metadata.get("EffectiveDate") != effective_date:
            raise PlanCopyImportError(
                "approval blocker",
                "approval-preview",
                "The effective-date source workbook no longer matches "
                "the approved preview.",
            )
        _status("Approval and archive SHA-256 match; acquiring OAuth authorization.")
        try:
            session = FusionSession(props, args)
        except Exception as exc:
            raise PlanCopyImportError(
                "auth/authz", "oauth-login", "Unable to obtain OAuth authorization."
            ) from exc
        result = execute_import(
            session=session,
            contract=contract,
            archive_contents=archive_contents,
            metadata=metadata,
            import_objects=import_objects,
            wait_seconds=args.wait_seconds,
            poll_interval=args.poll_interval,
        )
        result["setupObjectCount"] = import_objects["setupObjectCount"]
        result["objectBreakdown"] = import_objects
        # Native plan inventories contain counts, not evaluable profile records.
        profiles = import_objects.get("eligibilityProfiles", [])
        result["evaluationAvailable"] = bool(profiles)
        result["eligibilityProfiles"] = [
            profile["name"] for profile in profiles
        ]
        result["evaluationEffectiveDate"] = effective_date
        _print_import_result(result)
        return 0
    except PlanCopyImportError as exc:
        print(
            json.dumps(_user_facing_import_error(exc), indent=2, sort_keys=True),
            file=sys.stderr,
        )
        if exc.failure_class == "process_timeout":
            return 3
        if exc.failure_class == "process_failed":
            return 4
        if exc.failure_class == "catalog_or_metadata_mismatch":
            return 2
        return 1
    except Exception as exc:
        print(f"ERROR [input validation] stage=preflight: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')


# ---- eligibility_evaluator ----
eligibility_evaluator = _component("eligibility_evaluator", r'''
#!/usr/bin/env python3
"""Resolve imported profiles and a primary person assignment, then evaluate eligibility."""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path
import sys
import urllib.parse
from typing import Any

import excel_to_plan_copy_package
import plan_copy_import
import rest_client_compat as rest_client_common


HCM_ROOT = "/hcmRestApi/resources/11.13.18.05"
PROFILE_PATH = HCM_ROOT + "/eligibilityProfilesLOV"
PERSON_PATH = HCM_ROOT + "/personHeaders"
EVALUATION_PATH = HCM_ROOT + "/formulaEvaluations"
EVALUATION_ACTION_PATH = EVALUATION_PATH + "/action/evaluateEligibility"
RESULT_TYPES = ("L", "OPE", "ED", "FC", "IP")
ADF_ITEM_MEDIA_TYPE = "application/vnd.oracle.adf.resourceitem+json"
ADF_ACTION_MEDIA_TYPE = "application/vnd.oracle.adf.action+json"


class EligibilityEvaluationError(RuntimeError):
    """A fail-closed post-import eligibility evaluation error."""


def _positive_id(value: Any, label: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise EligibilityEvaluationError(f"Fusion did not return a valid {label}.") from exc
    if number < 1:
        raise EligibilityEvaluationError(f"Fusion did not return a valid {label}.")
    return number


def _collection_path(path: str, **parameters: Any) -> str:
    query = urllib.parse.urlencode(
        [(key, str(value)) for key, value in parameters.items() if value is not None]
    )
    return path + ("?" + query if query else "")


def _items(response: plan_copy_import.HttpResult, label: str) -> list[dict[str, Any]]:
    body = response.body
    rows = body.get("items") if isinstance(body, dict) else None
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise EligibilityEvaluationError(f"Fusion returned an invalid {label} response.")
    return rows


def resolve_profiles(
    session: plan_copy_import.FusionSession,
    profile_names: list[str],
    effective_date: str,
) -> list[dict[str, Any]]:
    resolved = []
    for requested_name in profile_names:
        name = requested_name.strip()
        if not name:
            raise EligibilityEvaluationError("Eligibility profile names must not be empty.")
        response = session.request(
            "GET",
            _collection_path(
                PROFILE_PATH,
                finder=f"findByName;Name={name}",
                effectiveDate=effective_date,
                fields="EligyPrflId,Name,ProfileType,StatCd,AsmtToUseCd",
                onlyData="true",
                limit=2,
            ),
            expected={200},
            stage="resolve-eligibility-profile",
        )
        matches = [
            row for row in _items(response, "eligibility profile")
            if row.get("Name") == name
            and row.get("ProfileType") == "PRTP"
            and row.get("StatCd") == "A"
        ]
        if len(matches) != 1:
            raise EligibilityEvaluationError(
                f"Expected one active participant eligibility profile named {name!r}; "
                f"Fusion returned {len(matches)}."
            )
        row = matches[0]
        resolved.append(
            {
                "profileId": _positive_id(row.get("EligyPrflId"), "eligibility profile ID"),
                "profileName": name,
            }
        )
    return resolved


def _adf_literal(value: str) -> str:
    return value.replace("'", "''")


def resolve_person(
    session: plan_copy_import.FusionSession,
    person_name: str,
    effective_date: str,
    person_number: str | None = None,
) -> dict[str, Any]:
    name = person_name.strip()
    if not name:
        raise EligibilityEvaluationError("Person name must not be empty.")
    response = session.request(
        "GET",
        _collection_path(
            PERSON_PATH,
            q=f"DisplayName='{_adf_literal(name)}' and PrimaryFlag='Y'",
            effectiveDate=effective_date,
            fields=(
                "PersonId,PersonNumber,DisplayName,AssignmentId,AssignmentNumber,"
                "AssignmentName,PrimaryFlag"
            ),
            onlyData="true",
            limit=20,
        ),
        expected={200},
        stage="resolve-person",
    )
    matches = [row for row in _items(response, "person") if row.get("DisplayName") == name]
    if person_number:
        matches = [row for row in matches if str(row.get("PersonNumber")) == person_number]
    if len(matches) != 1:
        suffix = " Supply --person-number to disambiguate." if len(matches) > 1 else ""
        raise EligibilityEvaluationError(
            f"Expected one primary assignment for person {name!r}; Fusion returned "
            f"{len(matches)}.{suffix}"
        )
    row = matches[0]
    return {
        "personId": _positive_id(row.get("PersonId"), "person ID"),
        "personName": name,
        "personNumber": str(row.get("PersonNumber") or ""),
        "assignmentId": _positive_id(row.get("AssignmentId"), "assignment ID"),
        "assignmentNumber": str(row.get("AssignmentNumber") or ""),
        "assignmentName": str(row.get("AssignmentName") or ""),
    }


def _detail_bytes(
    session: plan_copy_import.FusionSession,
    request_id: int,
    data_id: int,
) -> bytes:
    path = (
        f"{EVALUATION_PATH}/{request_id}/child/formulaEvaluationResults/{data_id}"
        "/enclosure/MessageDetails"
    )
    return session.request(
        "GET",
        path,
        expected={200},
        stage="read-evaluation-detail",
        parse_json=False,
        accept="application/octet-stream",
    ).body


def _decoded_detail(contents: bytes) -> Any:
    text = contents.decode("utf-8", errors="replace").strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def read_results(
    session: plan_copy_import.FusionSession, request_id: int
) -> dict[str, list[Any]]:
    results: dict[str, list[Any]] = {}
    for result_type in RESULT_TYPES:
        path = _collection_path(
            f"{EVALUATION_PATH}/{request_id}/child/formulaEvaluationResults",
            q=f"DataTypeCd='{result_type}'",
            fields="DataId,DataTypeCd,MessageText,Name,Value",
            onlyData="true",
            limit=200,
        )
        rows = _items(
            session.request(
                "GET", path, expected={200}, stage=f"read-evaluation-{result_type.lower()}"
            ),
            f"evaluation {result_type}",
        )
        details = []
        for row in rows:
            try:
                details.append(
                    _decoded_detail(
                        _detail_bytes(
                            session,
                            request_id,
                            _positive_id(row.get("DataId"), "evaluation result ID"),
                        )
                    )
                )
            except plan_copy_import.PlanCopyImportError as exc:
                if "HTTP 404" not in str(exc):
                    raise
                scalar = row.get("Value")
                if scalar in {None, ""}:
                    scalar = row.get("MessageText")
                if scalar not in {None, ""}:
                    details.append({"Name": row.get("Name"), "Value": scalar})
        results[result_type] = details
    return results


def _flatten(values: list[Any]) -> list[Any]:
    flattened = []
    for value in values:
        if isinstance(value, list):
            flattened.extend(value)
        elif isinstance(value, dict) and isinstance(value.get("items"), list):
            flattened.extend(value["items"])
        elif value is not None:
            flattened.append(value)
    return flattened


def _result_text(value: Any) -> str:
    return "" if value is None else str(value)


def summarize_profile(profile_name: str, results: dict[str, list[Any]]) -> dict[str, Any]:
    overall = _flatten(results.get("OPE", []))
    failed = _flatten(results.get("FC", []))
    inputs = _flatten(results.get("IP", []))
    outcome = next((item for item in overall if isinstance(item, dict)), {})
    eligible_flag = str(outcome.get("EligibleFlag") or "").upper()
    status = "Eligible" if eligible_flag in {"Y", "YES", "TRUE"} else (
        "Ineligible" if eligible_flag in {"N", "NO", "FALSE"} else
        str(outcome.get("EligibleMeaning") or "Unknown")
    )
    criteria_results = []
    for item in failed:
        if isinstance(item, dict):
            label = (
                item.get("IneligibleCriteria")
                or item.get("CriteriaName")
                or item.get("Name")
                or item.get("CriterionName")
            )
            criteria_results.append(
                {
                    "criterion": _result_text(label),
                    "expectedValue": _result_text(item.get("CriteriaValue")),
                    "actualValue": _result_text(item.get("PersonOrAssignmentValue")),
                }
            )
    return {
        "profileName": profile_name,
        "outcome": status,
        "reason": str(outcome.get("IneligReason") or ""),
        "criteriaResults": criteria_results,
        "inputParameterCount": len(inputs),
        "logAvailable": any(
            value is not None and value != "" for value in results.get("L", [])
        ),
    }


def evaluate_profiles(
    session: plan_copy_import.FusionSession,
    profiles: list[dict[str, Any]],
    person: dict[str, Any],
    effective_date: str,
) -> list[dict[str, Any]]:
    summaries = []
    for profile in profiles:
        created = session.request(
            "POST",
            EVALUATION_PATH,
            json_body={
                "AssignmentId": person["assignmentId"],
                "EligibilityProfileId": profile["profileId"],
                "RunTime": effective_date,
                "EvaluationType": "ORA_ELPRO",
            },
            content_type=ADF_ITEM_MEDIA_TYPE,
            expected={201},
            stage="create-evaluation-request",
            retry_auth=False,
        )
        request_id = _positive_id(
            created.body.get("EvaluationRequestId") if isinstance(created.body, dict) else None,
            "evaluation request ID",
        )
        session.request(
            "POST",
            EVALUATION_ACTION_PATH,
            json_body={
                "evaluationRequestId": request_id,
                "personId": person["personId"],
                "effectiveDate": effective_date,
                "evalType": "C",
            },
            content_type=ADF_ACTION_MEDIA_TYPE,
            expected={200, 204},
            stage="evaluate-eligibility",
            retry_auth=False,
        )
        summaries.append(summarize_profile(profile["profileName"], read_results(session, request_id)))
    return summaries


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview or run post-import eligibility evaluation in the selected environment.",
        allow_abbrev=False,
    )
    parser.add_argument("--zip", required=True, type=Path)
    parser.add_argument("--person-name", required=True)
    parser.add_argument("--person-number")
    parser.add_argument("--effective-date", default=date.today().isoformat())
    parser.add_argument("--properties", type=Path, required=True)
    parser.add_argument("--token-cache", type=Path, required=True)
    parser.add_argument("--approve-evaluation", action="store_true")
    parser.add_argument(
        "--completed-profile",
        action="append",
        default=[],
        help=(
            "Imported profile already verified as successfully evaluated during recovery; "
            "may be repeated."
        ),
    )
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--auth-code")
    parser.add_argument("--redirect-url")
    parser.add_argument("--callback-timeout", type=int, default=300)
    parser.add_argument("--force-login", action="store_true")
    parser.set_defaults(access_token=None, open_browser=True, tls_cert_sha256=None)
    args = parser.parse_args(argv)
    try:
        date.fromisoformat(args.effective_date)
    except ValueError as exc:
        parser.error("--effective-date must use YYYY-MM-DD.")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        props = plan_copy_import._oauth_properties(args.properties)
        target_origin = props["restBaseUrl"]
        session = plan_copy_import.FusionSession(props, args)
        _archive, _contents, import_objects = plan_copy_import._read_package(args.zip)
        profile_names = [item["name"] for item in import_objects["eligibilityProfiles"]]
        unknown_completed = sorted(set(args.completed_profile) - set(profile_names))
        if unknown_completed:
            raise EligibilityEvaluationError(
                "Completed profile is not present in the imported package: "
                + ", ".join(unknown_completed)
            )
        profile_names = [
            name for name in profile_names if name not in set(args.completed_profile)
        ]
        if not profile_names:
            raise EligibilityEvaluationError("No profiles remain to evaluate.")
        profiles = resolve_profiles(session, profile_names, args.effective_date)
        person = resolve_person(
            session, args.person_name, args.effective_date, args.person_number
        )
        common = {
            "targetEnvironment": target_origin,
            "personName": person["personName"],
            "personNumber": person["personNumber"],
            "assignmentNumber": person["assignmentNumber"],
            "effectiveDate": args.effective_date,
            "eligibilityProfiles": [item["profileName"] for item in profiles],
            "completedProfiles": list(dict.fromkeys(args.completed_profile)),
        }
        if not args.approve_evaluation:
            payload = {"event": "evaluation_preview_ready", **common, "requiresApproval": True}
        else:
            summaries = evaluate_profiles(session, profiles, person, args.effective_date)
            payload = {
                "event": "evaluation_completed",
                **common,
                "profileCount": len(summaries),
                "eligibleCount": sum(item["outcome"] == "Eligible" for item in summaries),
                "ineligibleCount": sum(item["outcome"] == "Ineligible" for item in summaries),
                "results": summaries,
            }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0
    except (OSError, ValueError, EligibilityEvaluationError, plan_copy_import.PlanCopyImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

''')


def run_workflow(argv=None):
    """Generate the package, then preview or execute its approved import."""
    import argparse
    from datetime import date
    import os
    import urllib.parse

    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    default_properties = REPOSITORY_ROOT / 'core/auth/fusionEnv.properties'
    default_token_cache = Path("auto")
    options = (
        ('work-dir', 'BENEFITS_WORK_DIR', None),
        ('input', 'BENEFITS_INPUT_XLSX', None),
        ('properties', 'FUSION_OAUTH_PROPERTIES', default_properties),
        ('token-cache', 'FUSION_TOKEN_CACHE', default_token_cache),
        ('task-context', 'BENEFITS_TASK_CONTEXT', None),
        ('samples-dir', 'BENEFITS_SAMPLES_DIR', SKILL_ROOT / 'assets/plan-copy'),
        ('mapping-reference-dir', 'BENEFITS_MAPPING_REFERENCE_DIR', SKILL_ROOT / 'references/eligibility-profile-mapping-reference'),
        ('openapi', 'BENEFITS_PLAN_COPY_OPENAPI', SKILL_ROOT / 'references/plan-copy.openapi.json'),
    )
    for name, env, fallback in options:
        parser.add_argument('--' + name, type=Path, default=os.environ.get(env) or fallback)
    parser.add_argument(
        '--effective-date',
        default=os.environ.get('BENEFITS_EFFECTIVE_DATE') or date.today().isoformat(),
        help='Eligibility import effective date in YYYY-MM-DD format; defaults to today.',
    )
    parser.add_argument('--sequence', type=int, default=os.environ.get('BENEFITS_TASK_SEQUENCE', '1'))
    parser.add_argument('--wait-seconds', type=int, default=os.environ.get('BENEFITS_WAIT_SECONDS', '1800'))
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--approve-upload', action='store_true')
    args = parser.parse_args(argv)
    try:
        if args.wait_seconds < 0 or args.sequence < 1:
            raise ValueError('Wait seconds must be non-negative and sequence must be positive.')
        if args.work_dir is None:
            raise ValueError('--work-dir or BENEFITS_WORK_DIR is required.')
        workbook = args.input or args.work_dir / 'Fusion_Elpro_Setup.xlsx'
        context = args.task_context or args.work_dir / 'task-context.json'
        archive = args.work_dir / 'benefits_eligibility.zip'
        preview = Path(str(archive) + '.plan-copy-import-preview.json')
        required = [workbook, args.samples_dir, args.mapping_reference_dir,
                    args.openapi, args.properties]
        required.append(preview if args.approve_upload else context)
        for path in required:
            if not excel_to_plan_copy_xml.contract_path_exists(path):
                raise ValueError(f'Required path does not exist: {path}')
        props = rest_client_compat.read_properties(args.properties)
        parsed = urllib.parse.urlparse(str(props.get('restBaseUrl', '')).strip())
        if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or
            parsed.password or parsed.path not in ('', '/') or parsed.params or
            parsed.query or parsed.fragment):
            raise ValueError('OAuth restBaseUrl must be an HTTPS origin.')
        generated = generate_eligibility_package.main([
            '--input', str(workbook), '--samples-dir', str(args.samples_dir),
            '--mapping-reference-dir', str(args.mapping_reference_dir),
            '--output-dir', str(args.work_dir), '--properties', str(args.properties),
            '--token-cache', str(args.token_cache),
            *(['--force'] if args.force else []),
        ])
        if generated:
            return generated
        arguments = ['--zip', str(archive), '--openapi', str(args.openapi),
                     '--effective-date', args.effective_date,
                     '--properties', str(args.properties), '--token-cache', str(args.token_cache),
                     '--wait-seconds', str(args.wait_seconds)]
        if args.approve_upload:
            arguments += ['--approve-upload', '--approval-preview', str(preview)]
        else:
            arguments += ['--task-context', str(context), '--sequence', str(args.sequence)]
        return plan_copy_import.main(arguments)
    except (OSError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1


COMMANDS = {
    'generate': generate_eligibility_package.main,
    'import': plan_copy_import.main,
    'evaluate': eligibility_evaluator.main,
    'convert-profiles': excel_to_plan_copy_xml.main,
    'convert-map': excel_to_plan_copy_map_xml.main,
    'convert-factors': excel_to_plan_copy_derived_factor_xml.main,
    'legacy-package': excel_to_plan_copy_package.main,
}


def main(argv=None):
    arguments = list(sys.argv[1:] if argv is None else argv)
    if arguments and arguments[0] in COMMANDS:
        return COMMANDS[arguments.pop(0)](arguments)
    if arguments and arguments[0] == 'workflow':
        arguments.pop(0)
    return run_workflow(arguments)


if __name__ == '__main__':
    raise SystemExit(main())
