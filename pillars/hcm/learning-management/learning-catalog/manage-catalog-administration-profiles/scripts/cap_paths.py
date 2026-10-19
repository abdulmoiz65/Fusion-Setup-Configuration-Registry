"""Locate FSCR for the nested CAP package; no cwd or environment override."""
from pathlib import Path


def repository_root(skill):
    skill = Path(skill).resolve(strict=True)
    suffix = Path('pillars/hcm/learning-management/learning-catalog/manage-catalog-administration-profiles')
    for root in skill.parents:
        if (root / suffix).resolve() != skill:
            continue
        if all((root / marker).is_file() for marker in (
                'schemas/skill-manifest.schema.json',
                'core/runbook/scripts/runbook_guard.py',
                'core/fusion-api/rest-api-client/scripts/fusion_rest_client.py')):
            return root
    raise ValueError('CAP must reside in the supported FSCR nested pillar location')
