"""Durable, sanitized state transitions for one Alert batch attempt."""
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class ReceiptError(ValueError):
    """Receipt is unsafe, mismatched, non-monotonic, or already reserved."""


_ALLOWED = {"attempt_id", "work_unit_sha256", "execution_mode", "classification", "stages", "request_attempts", "automatic_write_retry"}
_STAGES = ("approval_validated", "authentication_ready", "request_started", "response_received")


def build(*, attempt_id: str, work_unit_sha256: str, execution_mode: str, stages: dict[str, bool]) -> dict[str, Any]:
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ReceiptError("receipt requires attempt_id")
    if not isinstance(work_unit_sha256, str) or len(work_unit_sha256) != 64:
        raise ReceiptError("receipt requires work_unit_sha256")
    if execution_mode != "batch-create":
        raise ReceiptError("receipt supports batch-create only")
    if set(stages) != set(_STAGES) or any(type(stages[key]) is not bool for key in _STAGES):
        raise ReceiptError("receipt stages must contain only boolean lifecycle stages")
    if stages["response_received"] and not stages["request_started"]:
        raise ReceiptError("response_received requires request_started")
    if stages["request_started"] and not stages["authentication_ready"]:
        raise ReceiptError("request_started requires authentication_ready")
    if stages["authentication_ready"] and not stages["approval_validated"]:
        raise ReceiptError("authentication_ready requires approval_validated")
    classification = "response_received" if stages["response_received"] else ("outcome_unknown" if stages["request_started"] else "not_submitted")
    return {"attempt_id": attempt_id, "work_unit_sha256": work_unit_sha256, "execution_mode": execution_mode,
            "classification": classification, "stages": dict(stages), "request_attempts": int(stages["request_started"]),
            "automatic_write_retry": False}


def _canonical(receipt: dict[str, Any]) -> bytes:
    if set(receipt) != _ALLOWED:
        raise ReceiptError("receipt contains unsupported fields")
    expected = build(attempt_id=receipt.get("attempt_id"), work_unit_sha256=receipt.get("work_unit_sha256"),
                     execution_mode=receipt.get("execution_mode"), stages=receipt.get("stages"))
    if receipt != expected:
        raise ReceiptError("receipt is not canonical")
    return (json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _write_temp(destination: Path, payload: bytes) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".alert-receipt-", dir=str(destination.parent))
    with os.fdopen(fd, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return Path(temporary)


def _read(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    try:
        record = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ReceiptError("existing receipt is not valid JSON") from exc
    if not isinstance(record, dict) or _canonical(record) != raw:
        raise ReceiptError("existing receipt is not canonical")
    return record, raw


class Receipt:
    """Owns one reserved receipt and allows only durable monotonic transitions."""

    def __init__(self, path: str | Path, attempt_id: str, work_unit_sha256: str):
        self.path = Path(path)
        self.attempt_id = attempt_id
        self.work_unit_sha256 = work_unit_sha256
        self._raw: bytes | None = None

    def reserve(self) -> dict[str, Any]:
        record = build(attempt_id=self.attempt_id, work_unit_sha256=self.work_unit_sha256,
                       execution_mode="batch-create", stages={key: False for key in _STAGES})
        payload = _canonical(record)
        temporary = _write_temp(self.path, payload)
        try:
            try:
                os.link(temporary, self.path)
            except FileExistsError:
                raise FileExistsError("execution receipt is already reserved; refusing batch replay") from None
        finally:
            temporary.unlink(missing_ok=True)
        self._raw = payload
        return record

    def transition(self, stage: str) -> dict[str, Any]:
        if stage not in _STAGES:
            raise ReceiptError("unsupported receipt transition")
        if self._raw is None:
            raise ReceiptError("receipt must be reserved before transition")
        existing, raw = _read(self.path)
        if raw != self._raw:
            raise ReceiptError("receipt changed outside this execution")
        if existing["attempt_id"] != self.attempt_id or existing["work_unit_sha256"] != self.work_unit_sha256:
            raise ReceiptError("receipt attempt or work-unit binding differs")
        stages = dict(existing["stages"])
        position = _STAGES.index(stage)
        if stages[stage] or any(not stages[prior] for prior in _STAGES[:position]):
            raise ReceiptError("receipt transition is non-monotonic or already completed")
        stages[stage] = True
        updated = build(attempt_id=self.attempt_id, work_unit_sha256=self.work_unit_sha256,
                        execution_mode="batch-create", stages=stages)
        payload = _canonical(updated)
        temporary = _write_temp(self.path, payload)
        try:
            if self.path.read_bytes() != self._raw:
                raise ReceiptError("receipt changed outside this execution")
            os.replace(temporary, self.path)
        finally:
            temporary.unlink(missing_ok=True)
        self._raw = payload
        return updated


def write_atomic(path: str | Path, receipt: dict[str, Any]) -> None:
    """Compatibility helper: reserve exactly one canonical record."""
    payload = _canonical(receipt)
    destination = Path(path)
    temporary = _write_temp(destination, payload)
    try:
        try:
            os.link(temporary, destination)
        except FileExistsError:
            raise FileExistsError("execution receipt already exists") from None
    finally:
        temporary.unlink(missing_ok=True)
