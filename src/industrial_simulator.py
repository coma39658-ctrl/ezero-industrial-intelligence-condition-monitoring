from dataclasses import dataclass
from typing import Optional, Tuple

PROVENANCE_SIMULATED = "SIMULATED"

OPERATING_CONTEXTS = (
    "OFF",
    "STARTUP",
    "IDLE",
    "LOW_LOAD",
    "NORMAL_LOAD",
    "HIGH_LOAD",
    "TRANSIENT",
    "SHUTDOWN",
    "UNKNOWN_CONTEXT",
)

SENSOR_QUALITY_STATES = (
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
)

SCREENING_STATES = (
    "NORMAL",
    "OUT_OF_RANGE",
    "ANOMALOUS_PATTERN",
    "SENSOR_QUALITY_PROBLEM",
    "INSUFFICIENT_DATA",
)

SCENARIOS = (
    "A_HEALTHY_STABLE",
    "B_REFERENCE_RANGE_DEVIATION",
    "C_MULTISENSOR_ANOMALOUS_PATTERN",
    "D_TRANSIENT_NONFAULT_EVENT",
    "E_LOAD_CONTEXT_SHIFT",
    "F_SENSOR_TIMEOUT",
    "G_SENSOR_NO_RESPONSE",
    "H_INVALID_RESPONSE",
    "I_MISSING_DATA",
    "J_INSUFFICIENT_SAMPLING",
    "K_INTERMITTENT_PACKET_LOSS",
    "L_LATENCY_DEGRADATION",
    "M_SENSOR_ERROR",
)


@dataclass(frozen=True)
class SimulatorConfig:
    scenario_id: str
    seed: int
    sample_count: int = 240
    sampling_rate_hz: float = 10.0
    operating_context: str = "NORMAL_LOAD"

    def __post_init__(self):
        if self.scenario_id not in SCENARIOS:
            raise ValueError(f"Unsupported scenario_id: {self.scenario_id}")
        if not isinstance(self.seed, int):
            raise TypeError("seed must be an integer")
        if not isinstance(self.sample_count, int) or self.sample_count <= 0:
            raise ValueError("sample_count must be a positive integer")
        if not isinstance(self.sampling_rate_hz, (int, float)):
            raise TypeError("sampling_rate_hz must be numeric")
        if self.sampling_rate_hz <= 0:
            raise ValueError("sampling_rate_hz must be greater than zero")
        if self.operating_context not in OPERATING_CONTEXTS:
            raise ValueError(
                f"Unsupported operating_context: {self.operating_context}"
            )

@dataclass(frozen=True)
class SimulatedObservation:
    case_id: str
    scenario_id: str
    seed: int
    sample_index: int
    sensor_name: str
    raw_value: Optional[float]
    unit: str
    operating_context: str
    sensor_quality_state: str
    machine_ground_truth: str
    expected_screening_state: str
    provenance: str = PROVENANCE_SIMULATED


@dataclass(frozen=True)
class SimulatedCaseMetadata:
    case_id: str
    scenario_id: str
    seed: int
    sample_count: int
    sampling_rate_hz: float
    operating_context: str
    change_point: Optional[int]
    affected_sensors: Tuple[str, ...]
    expected_sample_count: int
    observed_sample_count: int
    dropped_samples: int
    latency_ms: Optional[float]
    machine_ground_truth: str
    sensor_quality_state: str
    expected_screening_state: str
    provenance: str = PROVENANCE_SIMULATED

SCENARIO_BEHAVIOR = {
    "A_HEALTHY_STABLE": {
        "machine_ground_truth": "HEALTHY",
        "sensor_quality_state": "VALID",
        "expected_screening_state": "NORMAL",
        "affected_sensors": (),
        "change_point": None,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "B_REFERENCE_RANGE_DEVIATION": {
        "machine_ground_truth": "REFERENCE_RANGE_DEVIATION",
        "sensor_quality_state": "OUT_OF_RANGE",
        "expected_screening_state": "OUT_OF_RANGE",
        "affected_sensors": ("temperature",),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "C_MULTISENSOR_ANOMALOUS_PATTERN": {
        "machine_ground_truth": "MULTISENSOR_ANOMALOUS_PATTERN",
        "sensor_quality_state": "VALID",
        "expected_screening_state": "ANOMALOUS_PATTERN",
        "affected_sensors": ("vibration", "temperature", "motor_current"),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "D_TRANSIENT_NONFAULT_EVENT": {
        "machine_ground_truth": "TRANSIENT_NONFAULT",
        "sensor_quality_state": "VALID",
        "expected_screening_state": "NORMAL",
        "affected_sensors": ("rpm", "load"),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "E_LOAD_CONTEXT_SHIFT": {
        "machine_ground_truth": "LOAD_CONTEXT_SHIFT",
        "sensor_quality_state": "VALID",
        "expected_screening_state": "NORMAL",
        "affected_sensors": ("rpm", "motor_current", "power", "load"),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "F_SENSOR_TIMEOUT": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_SENSOR_QUALITY",
        "sensor_quality_state": "SENSOR_TIMEOUT",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": ("pressure",),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "G_SENSOR_NO_RESPONSE": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_SENSOR_QUALITY",
        "sensor_quality_state": "SENSOR_NO_RESPONSE",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": ("flow",),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "H_INVALID_RESPONSE": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_SENSOR_QUALITY",
        "sensor_quality_state": "INVALID_RESPONSE",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": ("temperature",),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
    "I_MISSING_DATA": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_MISSING_DATA",
        "sensor_quality_state": "MISSING_DATA",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": ("vibration",),
        "change_point": 120,
        "drop_rate": 0.25,
        "latency_ms": None,
    },
    "J_INSUFFICIENT_SAMPLING": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_INSUFFICIENT_DATA",
        "sensor_quality_state": "INSUFFICIENT_SAMPLING",
        "expected_screening_state": "INSUFFICIENT_DATA",
        "affected_sensors": ("vibration",),
        "change_point": None,
        "drop_rate": 0.75,
        "latency_ms": None,
    },
    "K_INTERMITTENT_PACKET_LOSS": {
        "machine_ground_truth": "HEALTHY",
        "sensor_quality_state": "SUSPECT_SIGNAL_QUALITY",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": (),
        "change_point": None,
        "drop_rate": 0.20,
        "latency_ms": None,
    },
    "L_LATENCY_DEGRADATION": {
        "machine_ground_truth": "HEALTHY",
        "sensor_quality_state": "SUSPECT_SIGNAL_QUALITY",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": (),
        "change_point": None,
        "drop_rate": 0.0,
        "latency_ms": 250.0,
    },
    "M_SENSOR_ERROR": {
        "machine_ground_truth": "UNKNOWN_DUE_TO_SENSOR_QUALITY",
        "sensor_quality_state": "SENSOR_ERROR",
        "expected_screening_state": "SENSOR_QUALITY_PROBLEM",
        "affected_sensors": ("voltage",),
        "change_point": 120,
        "drop_rate": 0.0,
        "latency_ms": None,
    },
}

import random

SENSOR_BASELINES = {
    "vibration": (1.0, "mm/s"),
    "temperature": (60.0, "C"),
    "rpm": (1500.0, "rpm"),
    "motor_current": (20.0, "A"),
    "voltage": (400.0, "V"),
    "power": (12.0, "kW"),
    "pressure": (5.0, "bar"),
    "flow": (100.0, "L/min"),
    "load": (0.60, "ratio"),
}


def _deterministic_noise(rng, scale):
    return rng.uniform(-scale, scale)


def _base_sensor_value(sensor_name, rng):
    baseline, _unit = SENSOR_BASELINES[sensor_name]
    scale = max(abs(baseline) * 0.01, 0.001)
    return baseline + _deterministic_noise(rng, scale)

def generate_case(config):
    behavior = SCENARIO_BEHAVIOR[config.scenario_id]
    rng = random.Random(config.seed)

    case_id = f"{config.scenario_id}_{config.seed}_{config.sample_count}"

    expected_sample_count = config.sample_count * len(SENSOR_BASELINES)
    observations = []
    dropped_samples = 0

    for sample_index in range(config.sample_count):
        for sensor_name, (_baseline, unit) in SENSOR_BASELINES.items():
            raw_value = _base_sensor_value(sensor_name, rng)
            sensor_quality_state = "VALID"

            is_affected = sensor_name in behavior["affected_sensors"]
            after_change = (
                behavior["change_point"] is not None
                and sample_index >= behavior["change_point"]
            )

            if config.scenario_id == "B_REFERENCE_RANGE_DEVIATION":
                if is_affected and after_change:
                    raw_value += 20.0
                    sensor_quality_state = "OUT_OF_RANGE"

            elif config.scenario_id == "C_MULTISENSOR_ANOMALOUS_PATTERN":
                if is_affected and after_change:
                    if sensor_name == "vibration":
                        raw_value *= 2.5
                    elif sensor_name == "temperature":
                        raw_value += 15.0
                    elif sensor_name == "motor_current":
                        raw_value *= 1.35

            elif config.scenario_id == "D_TRANSIENT_NONFAULT_EVENT":
                if is_affected and after_change and sample_index < behavior["change_point"] + 10:
                    raw_value *= 1.15

            elif config.scenario_id == "E_LOAD_CONTEXT_SHIFT":
                if is_affected and after_change:
                    raw_value *= 1.20

            elif config.scenario_id == "F_SENSOR_TIMEOUT":
                if is_affected and after_change:
                    raw_value = None
                    sensor_quality_state = "SENSOR_TIMEOUT"

            elif config.scenario_id == "G_SENSOR_NO_RESPONSE":
                if is_affected and after_change:
                    raw_value = None
                    sensor_quality_state = "SENSOR_NO_RESPONSE"

            elif config.scenario_id == "H_INVALID_RESPONSE":
                if is_affected and after_change:
                    raw_value = None
                    sensor_quality_state = "INVALID_RESPONSE"

            elif config.scenario_id == "I_MISSING_DATA":
                if is_affected and rng.random() < behavior["drop_rate"]:
                    raw_value = None
                    sensor_quality_state = "MISSING_DATA"
                    dropped_samples += 1

            elif config.scenario_id == "J_INSUFFICIENT_SAMPLING":
                if is_affected and rng.random() < behavior["drop_rate"]:
                    raw_value = None
                    sensor_quality_state = "INSUFFICIENT_SAMPLING"
                    dropped_samples += 1

            elif config.scenario_id == "K_INTERMITTENT_PACKET_LOSS":
                if rng.random() < behavior["drop_rate"]:
                    raw_value = None
                    sensor_quality_state = "SUSPECT_SIGNAL_QUALITY"
                    dropped_samples += 1

            elif config.scenario_id == "L_LATENCY_DEGRADATION":
                sensor_quality_state = "SUSPECT_SIGNAL_QUALITY"

            elif config.scenario_id == "M_SENSOR_ERROR":
                if is_affected and after_change:
                    raw_value = None
                    sensor_quality_state = "SENSOR_ERROR"

            observations.append(
                SimulatedObservation(
                    case_id=case_id,
                    scenario_id=config.scenario_id,
                    seed=config.seed,
                    sample_index=sample_index,
                    sensor_name=sensor_name,
                    raw_value=raw_value,
                    unit=unit,
                    operating_context=config.operating_context,
                    sensor_quality_state=sensor_quality_state,
                    machine_ground_truth=behavior["machine_ground_truth"],
                    expected_screening_state=behavior["expected_screening_state"],
                )
            )

    observed_sample_count = sum(
        1 for observation in observations if observation.raw_value is not None
    )

    metadata = SimulatedCaseMetadata(
        case_id=case_id,
        scenario_id=config.scenario_id,
        seed=config.seed,
        sample_count=config.sample_count,
        sampling_rate_hz=float(config.sampling_rate_hz),
        operating_context=config.operating_context,
        change_point=behavior["change_point"],
        affected_sensors=tuple(behavior["affected_sensors"]),
        expected_sample_count=expected_sample_count,
        observed_sample_count=observed_sample_count,
        dropped_samples=dropped_samples,
        latency_ms=behavior["latency_ms"],
        machine_ground_truth=behavior["machine_ground_truth"],
        sensor_quality_state=behavior["sensor_quality_state"],
        expected_screening_state=behavior["expected_screening_state"],
    )

    return metadata, tuple(observations)
