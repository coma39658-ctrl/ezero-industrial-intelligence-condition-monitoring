from dataclasses import dataclass
from typing import Optional, Tuple

REAL_SENSOR_PROVENANCE = "REAL_SENSOR"

ALLOWED_SOURCE_TYPES = (
    "EXTERNAL_SENSOR",
    "DATA_LOGGER",
    "READ_ONLY_TELEMETRY_API",
    "OPC_UA_READ_ONLY",
    "MQTT_READ_ONLY",
    "SERIAL_USB_READ_ONLY",
    "NETWORK_TELEMETRY_READ_ONLY",
)


@dataclass(frozen=True)
class AcquisitionAuthorization:
    site_authorized: bool
    consent_accepted: bool

    def __post_init__(self):
        if self.site_authorized is not True:
            raise ValueError("site authorization is required")

        if self.consent_accepted is not True:
            raise ValueError("consent acceptance is required")


@dataclass(frozen=True)
class RealSensorSourceConfig:
    source_type: str
    source_identity: str
    sensor_identity: str
    machine_family: str
    operating_context: str
    expected_unit: Optional[str] = None

    auto_discovery: bool = False
    control_allowed: bool = False
    write_credentials_required: bool = False

    def __post_init__(self):
        if self.source_type not in ALLOWED_SOURCE_TYPES:
            raise ValueError(f"unsupported source_type: {self.source_type}")

        if not self.source_identity.strip():
            raise ValueError("source_identity must not be blank")

        if not self.sensor_identity.strip():
            raise ValueError("sensor_identity must not be blank")

        if not self.machine_family.strip():
            raise ValueError("machine_family must not be blank")

        if not self.operating_context.strip():
            raise ValueError("operating_context must not be blank")

        if self.auto_discovery is not False:
            raise ValueError("automatic discovery is forbidden")

        if self.control_allowed is not False:
            raise ValueError("control must remain disabled")

        if self.write_credentials_required is not False:
            raise ValueError("write/control credentials are forbidden")


@dataclass(frozen=True)
class AcquisitionSession:
    session_id: str
    authorization: AcquisitionAuthorization
    source: RealSensorSourceConfig

    read_only: bool = True
    diagnostic_claim: bool = False
    autonomous_action: bool = False
    live_io_authorized: bool = False

    def __post_init__(self):
        if not self.session_id.strip():
            raise ValueError("session_id must not be blank")

        if self.read_only is not True:
            raise ValueError("acquisition must remain read-only")

        if self.diagnostic_claim is not False:
            raise ValueError("diagnostic claims must remain disabled")

        if self.autonomous_action is not False:
            raise ValueError("autonomous action must remain disabled")

        if self.live_io_authorized is not False:
            raise ValueError(
                "live I/O is not authorized in software-only validation"
            )


@dataclass(frozen=True)
class AcquisitionEvidence:
    session_id: str
    provenance: str
    source_identity: str
    sensor_identity: str
    raw_payload: bytes
    parsed_value: Optional[float]
    sensor_quality: str
    source_hash: str
    evidence_hash: str
    limitations: Tuple[str, ...]
    diagnostic_claim: bool = False
    control_allowed: bool = False

import hashlib
import json
import math


ALLOWED_SENSOR_QUALITY = (
    "VALID",
    "MISSING_DATA",
    "INVALID_RESPONSE",
    "SENSOR_TIMEOUT",
    "SENSOR_NO_RESPONSE",
    "SENSOR_ERROR",
    "INSUFFICIENT_SAMPLING",
    "SUSPECT_SIGNAL_QUALITY",
)


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


def parse_numeric_payload(raw_payload):
    if not isinstance(raw_payload, (bytes, bytearray)):
        raise TypeError("raw_payload must be bytes")

    text = bytes(raw_payload).decode("utf-8").strip()

    if not text:
        return None

    try:
        value = float(text)
    except ValueError as exc:
        raise ValueError("unsupported numeric payload") from exc

    if not math.isfinite(value):
        raise ValueError("non-finite numeric payload")

    return value


def build_acquisition_evidence(
    *,
    session,
    raw_payload,
    sensor_quality,
    limitations=(),
):
    if not isinstance(session, AcquisitionSession):
        raise TypeError("session must be AcquisitionSession")

    if session.live_io_authorized is not False:
        raise ValueError("live I/O must remain unauthorized")

    if sensor_quality not in ALLOWED_SENSOR_QUALITY:
        raise ValueError(
            f"unsupported sensor_quality: {sensor_quality}"
        )

    raw_bytes = bytes(raw_payload)
    source_hash = sha256_bytes(raw_bytes)

    if sensor_quality == "VALID":
        parsed_value = parse_numeric_payload(raw_bytes)
    else:
        parsed_value = None

    payload = {
        "session_id": session.session_id,
        "provenance": REAL_SENSOR_PROVENANCE,
        "source_identity": session.source.source_identity,
        "sensor_identity": session.source.sensor_identity,
        "sensor_quality": sensor_quality,
        "source_hash": source_hash,
        "parsed_value": parsed_value,
        "limitations": list(limitations),
        "read_only": True,
        "control_allowed": False,
        "diagnostic_claim": False,
    }

    evidence_hash = canonical_evidence_hash(payload)

    return AcquisitionEvidence(
        session_id=session.session_id,
        provenance=REAL_SENSOR_PROVENANCE,
        source_identity=session.source.source_identity,
        sensor_identity=session.source.sensor_identity,
        raw_payload=raw_bytes,
        parsed_value=parsed_value,
        sensor_quality=sensor_quality,
        source_hash=source_hash,
        evidence_hash=evidence_hash,
        limitations=tuple(limitations),
    )
