from dataclasses import dataclass
from typing import Optional, Tuple

ALLOWED_DEMO_PROVENANCE = (
    "SIMULATED",
    "LOG_REPLAY",
)

SCREENING_STATES = (
    "NORMAL",
    "OUT_OF_RANGE",
    "ANOMALOUS_PATTERN",
    "SENSOR_QUALITY_PROBLEM",
    "INSUFFICIENT_DATA",
)


@dataclass(frozen=True)
class DemoFlowInput:
    provenance: str
    machine_family: str
    configured_sensors: Tuple[str, ...]
    operating_context: str
    source_identity: Optional[str] = None

    def __post_init__(self):
        if self.provenance not in ALLOWED_DEMO_PROVENANCE:
            raise ValueError(
                f"Unsupported demo provenance: {self.provenance}"
            )

        if not self.machine_family:
            raise ValueError("machine_family must not be blank")

        if not self.configured_sensors:
            raise ValueError("configured_sensors must not be empty")

        if not self.operating_context:
            raise ValueError("operating_context must not be blank")


@dataclass(frozen=True)
class DemoFlowResult:
    provenance: str
    machine_family: str
    configured_sensors: Tuple[str, ...]
    missing_recommended_sensors: Tuple[str, ...]
    operating_context: str
    source_identity: Optional[str]
    sensor_quality: str
    condition_screening: str
    evidence_level: str
    limitations: Tuple[str, ...]
    read_only: bool = True
    diagnostic_claim: bool = False
    real_sensor_authorized: bool = False

from src.textile_garment_profile import (
    TextileGarmentProfileConfig,
    validate_profile_config,
)


def run_demo_flow(
    *,
    demo_input,
    sensor_quality,
    condition_screening,
    evidence_level,
    limitations=(),
):
    if not isinstance(demo_input, DemoFlowInput):
        raise TypeError("demo_input must be DemoFlowInput")

    if sensor_quality not in (
        "VALID",
        "OUT_OF_RANGE",
        "SENSOR_TIMEOUT",
        "SENSOR_NO_RESPONSE",
        "SENSOR_ERROR",
        "INVALID_RESPONSE",
        "MISSING_DATA",
        "NOT_QUERIED",
        "INSUFFICIENT_SAMPLING",
        "SUSPECT_SIGNAL_QUALITY",
    ):
        raise ValueError(
            f"Unsupported sensor_quality: {sensor_quality}"
        )

    if condition_screening not in SCREENING_STATES:
        raise ValueError(
            f"Unsupported condition_screening: {condition_screening}"
        )

    if not isinstance(evidence_level, str) or not evidence_level.strip():
        raise ValueError("evidence_level must not be blank")

    profile_config = TextileGarmentProfileConfig(
        machine_family=demo_input.machine_family,
        sensors=tuple(demo_input.configured_sensors),
        operating_context=demo_input.operating_context,
    )

    profile_result = validate_profile_config(profile_config)

    combined_limitations = tuple(limitations)

    if profile_result.missing_recommended_sensors:
        combined_limitations += (
            "MISSING_RECOMMENDED_SENSORS",
        )

    if sensor_quality != "VALID":
        combined_limitations += (
            "SENSOR_QUALITY_LIMITATION_PRESENT",
        )

    return DemoFlowResult(
        provenance=demo_input.provenance,
        machine_family=profile_result.machine_family,
        configured_sensors=profile_result.configured_sensors,
        missing_recommended_sensors=(
            profile_result.missing_recommended_sensors
        ),
        operating_context=profile_result.operating_context,
        source_identity=demo_input.source_identity,
        sensor_quality=sensor_quality,
        condition_screening=condition_screening,
        evidence_level=evidence_level,
        limitations=combined_limitations,
    )
