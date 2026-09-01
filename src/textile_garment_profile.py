from dataclasses import dataclass
from typing import Tuple

PROFILE_NAME = "TEXTILE_GARMENT_PROFILE_V0_1"

MACHINE_FAMILIES = (
    "ROTATING_DRIVE_SYSTEM",
    "SPINNING_WINDING_SYSTEM",
    "WEAVING_LOOM_SYSTEM",
    "KNITTING_SYSTEM",
    "SEWING_GARMENT_SYSTEM",
    "EMBROIDERY_MACHINE_SYSTEM",
)

ALLOWED_SENSORS = (
    "vibration",
    "temperature",
    "rpm",
    "motor_current",
    "voltage",
    "power",
    "load",
    "pressure",
    "flow",
    "acoustic_level",
    "bearing_temperature",
    "spindle_temperature",
    "ambient_temperature",
    "humidity",
)

OPERATING_CONTEXTS = (
    "OFF",
    "STARTUP",
    "IDLE",
    "THREADING_SETUP",
    "LOW_SPEED",
    "NORMAL_PRODUCTION",
    "HIGH_SPEED",
    "HIGH_LOAD",
    "TRANSIENT",
    "CHANGEOVER",
    "SHUTDOWN",
    "MAINTENANCE_TEST",
    "UNKNOWN_CONTEXT",
)


@dataclass(frozen=True)
class TextileGarmentProfileConfig:
    machine_family: str
    sensors: Tuple[str, ...]
    operating_context: str = "UNKNOWN_CONTEXT"

    def __post_init__(self):
        if self.machine_family not in MACHINE_FAMILIES:
            raise ValueError(
                f"Unsupported machine_family: {self.machine_family}"
            )

        if not self.sensors:
            raise ValueError("At least one sensor is required")

        unknown = tuple(
            sensor for sensor in self.sensors
            if sensor not in ALLOWED_SENSORS
        )

        if unknown:
            raise ValueError(
                "Unsupported sensors: " + ", ".join(sorted(unknown))
            )

        if self.operating_context not in OPERATING_CONTEXTS:
            raise ValueError(
                f"Unsupported operating_context: {self.operating_context}"
            )

MACHINE_FAMILY_SENSOR_MAP = {
    "ROTATING_DRIVE_SYSTEM": (
        "vibration",
        "temperature",
        "rpm",
        "motor_current",
        "power",
        "load",
    ),
    "SPINNING_WINDING_SYSTEM": (
        "vibration",
        "spindle_temperature",
        "rpm",
        "motor_current",
        "load",
    ),
    "WEAVING_LOOM_SYSTEM": (
        "vibration",
        "temperature",
        "rpm",
        "motor_current",
        "power",
    ),
    "KNITTING_SYSTEM": (
        "rpm",
        "vibration",
        "temperature",
        "motor_current",
        "load",
    ),
    "SEWING_GARMENT_SYSTEM": (
        "motor_current",
        "rpm",
        "vibration",
        "temperature",
        "power",
    ),
    "EMBROIDERY_MACHINE_SYSTEM": (
        "rpm",
        "vibration",
        "motor_current",
        "spindle_temperature",
        "load",
    ),
}


@dataclass(frozen=True)
class TextileGarmentProfileValidation:
    profile_name: str
    machine_family: str
    configured_sensors: Tuple[str, ...]
    recommended_sensors: Tuple[str, ...]
    missing_recommended_sensors: Tuple[str, ...]
    operating_context: str
    read_only: bool = True
    diagnostic_claim: bool = False
    real_sensor_authorized: bool = False


def validate_profile_config(config):
    recommended = MACHINE_FAMILY_SENSOR_MAP[config.machine_family]

    missing = tuple(
        sensor
        for sensor in recommended
        if sensor not in config.sensors
    )

    return TextileGarmentProfileValidation(
        profile_name=PROFILE_NAME,
        machine_family=config.machine_family,
        configured_sensors=tuple(config.sensors),
        recommended_sensors=tuple(recommended),
        missing_recommended_sensors=missing,
        operating_context=config.operating_context,
    )
