"""Resolve pillar skill metadata for shared setup workflows."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fusion_skill_paths import FUSION_SKILLS_ROOT


FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---", re.DOTALL)
SCALAR_PATTERN = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


@dataclass(frozen=True)
class PillarSkillMetadata:
    path: Path
    skill_id: str = ""
    offering: str = ""
    functional_area: str = ""
    functional_area_code: str = ""
    task_code: str = ""
    task_name: str = ""

    @property
    def is_offering_skill(self) -> bool:
        return bool(self.offering and not self.functional_area and not self.task_code)

    @property
    def is_functional_area_skill(self) -> bool:
        return bool(self.offering and self.functional_area and not self.task_code)

    @property
    def is_task_skill(self) -> bool:
        return bool(self.task_code or self.task_name)


def kebab_case(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower())
    return normalized.strip("-")


def unquote(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in {"'", '"'} and value[-1:] == value[0]:
        return value[1:-1]
    return value


def read_frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER_PATTERN.match(path.read_text(encoding="utf-8"))
    if not match:
        return {}

    metadata: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if raw_line.startswith((" ", "-")):
            continue
        scalar_match = SCALAR_PATTERN.match(raw_line)
        if scalar_match:
            metadata[scalar_match.group(1)] = unquote(scalar_match.group(2))
    return metadata


def load_pillar_skill_metadata() -> list[PillarSkillMetadata]:
    pillars_root = FUSION_SKILLS_ROOT / "pillars"
    if not pillars_root.exists():
        return []

    results: list[PillarSkillMetadata] = []
    metadata_paths = sorted({*pillars_root.rglob("SKILL.md"), *pillars_root.rglob("*.md")})
    for path in metadata_paths:
        frontmatter = read_frontmatter(path)
        if not frontmatter:
            continue
        task_code = frontmatter.get("task_code", "")
        task_name = frontmatter.get("task_name", "")
        if path.name != "SKILL.md" and not (task_code or task_name):
            continue
        results.append(
            PillarSkillMetadata(
                path=path,
                skill_id=frontmatter.get("skill_id", ""),
                offering=frontmatter.get("offering", ""),
                functional_area=frontmatter.get("functional_area", ""),
                functional_area_code=frontmatter.get("functional_area_code", ""),
                task_code=task_code,
                task_name=task_name,
            )
        )
    return results


def matches_optional(actual: str, expected: str | None) -> bool:
    return not expected or actual.casefold() == expected.casefold()


def resolve_task_skill_metadata(
    *,
    task_code: str | None = None,
    task_name: str | None = None,
    offering: str | None = None,
    functional_area: str | None = None,
    functional_area_code: str | None = None,
) -> PillarSkillMetadata | None:
    candidates = [item for item in load_pillar_skill_metadata() if item.is_task_skill]

    def score(item: PillarSkillMetadata) -> int:
        value = 0
        if task_code and item.task_code.casefold() == task_code.casefold():
            value += 100
        if task_name and item.task_name.casefold() == task_name.casefold():
            value += 50
        if offering and item.offering.casefold() == offering.casefold():
            value += 10
        if functional_area and item.functional_area.casefold() == functional_area.casefold():
            value += 10
        if functional_area_code and item.functional_area_code.casefold() == functional_area_code.casefold():
            value += 10
        return value

    filtered: list[PillarSkillMetadata] = []
    for item in candidates:
        if task_code and item.task_code.casefold() != task_code.casefold():
            continue
        if task_name and item.task_name.casefold() != task_name.casefold():
            continue
        if not matches_optional(item.offering, offering):
            continue
        if not matches_optional(item.functional_area, functional_area):
            continue
        if not matches_optional(item.functional_area_code, functional_area_code):
            continue
        filtered.append(item)

    if not filtered:
        return None
    return sorted(filtered, key=score, reverse=True)[0]


def parent_skill_chain(task_metadata: PillarSkillMetadata) -> dict[str, PillarSkillMetadata | None]:
    all_metadata = load_pillar_skill_metadata()
    offering_matches = [
        item
        for item in all_metadata
        if item.is_offering_skill and item.offering.casefold() == task_metadata.offering.casefold()
    ]
    functional_area_matches = [
        item
        for item in all_metadata
        if item.is_functional_area_skill
        and item.offering.casefold() == task_metadata.offering.casefold()
        and item.functional_area.casefold() == task_metadata.functional_area.casefold()
    ]
    offering_skill = min(offering_matches, key=lambda item: len(item.path.parts), default=None)
    functional_area_skill = min(functional_area_matches, key=lambda item: len(item.path.parts), default=None)
    return {
        "offering": offering_skill,
        "functional_area": functional_area_skill,
        "task": task_metadata,
    }


def repo_relative(path: Path) -> str:
    try:
        return str(path.relative_to(FUSION_SKILLS_ROOT))
    except ValueError:
        return str(path)
