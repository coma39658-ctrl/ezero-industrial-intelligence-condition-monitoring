from dataclasses import dataclass
from typing import Optional, Tuple

FIELD_VALIDATION_PROVENANCE = "REAL_SENSOR"


@dataclass(frozen=True)
class FieldValidationAuthorization:
    site_authorized: bool
    consent_accepted: bool
    operator_reference: Optional[str] = None

    def __post_init__(self):
        if self.site_authorized is not True:
            raise ValueError("site authorization is required")

        if self.consent_accepted is not True:
            raise ValueError("consent acceptance is required")


@dataclass(frozen=True)
class FieldValidationSession:
    session_id: str
    machine_family: str
    sensor_names: Tuple[str, ...]
    operating_context: str
    authorization: FieldValidationAuthorization

    read_only: bool = True
    control_allowed: bool = False
    diagnostic_claim: bool = False
    autonomous_action: bool = False
    real_sensor_mode: bool = True

    def __post_init__(self):
        if not self.session_id.strip():
            raise ValueError("session_id must not be blank")

        if not self.machine_family.strip():
            raise ValueError("machine_family must not be blank")

        if not self.sensor_names:
            raise ValueError("sensor_names must not be empty")

        if not self.operating_context.strip():
            raise ValueError("operating_context must not be blank")


@dataclass(frozen=True)
class FieldValidationEvidence:
    session_id: str
    provenance: str
    source_hash: str
    evidence_hash: str
    sensor_quality: str
    condition_screening: str
    limitations: Tuple[str, ...]
    read_only: bool = True
    control_allowed: bool = False
    diagnostic_claim: bool = False

import hashlib
import json
import uuid


def generate_session_id():
    return f"EZFV-{uuid.uuid4().hex}"


def sha256_bytes(data):
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")

    return hashlib.sha256(bytes(data)).hexdigest()


def canonical_evidence_hash(payload):
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dict")

    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")

    return hashlib.sha256(encoded).hexdigest()


def validate_session_safety(session):
    if not isinstance(session, FieldValidationSession):
        raise TypeError("session must be FieldValidationSession")

    if session.read_only is not True:
        raise ValueError("field validation must remain read-only")

    if session.control_allowed is not False:
        raise ValueError("control must remain disabled")

    if session.diagnostic_claim is not False:
        raise ValueError("diagnostic claims must remain disabled")

    if session.autonomous_action is not False:
        raise ValueError("autonomous action must remain disabled")

    if session.real_sensor_mode is not True:
        raise ValueError("field-validation mode must remain explicit")

    return True


def build_field_validation_evidence(
    *,
    session,
    raw_source_bytes,
    sensor_quality,
    condition_screening,
    limitations=(),
):
    validate_session_safety(session)

    source_hash = sha256_bytes(raw_source_bytes)

    payload = {
        "session_id": session.session_id,
        "provenance": FIELD_VALIDATION_PROVENANCE,
        "source_hash": source_hash,
        "sensor_quality": sensor_quality,
        "condition_screening": condition_screening,
        "limitations": list(limitations),
        "read_only": True,
        "control_allowed": False,
        "diagnostic_claim": False,
    }

    evidence_hash = canonical_evidence_hash(payload)

    return FieldValidationEvidence(
        session_id=session.session_id,
        provenance=FIELD_VALIDATION_PROVENANCE,
        source_hash=source_hash,
        evidence_hash=evidence_hash,
        sensor_quality=sensor_quality,
        condition_screening=condition_screening,
        limitations=tuple(limitations),
    )
