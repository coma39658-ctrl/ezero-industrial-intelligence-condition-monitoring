from dataclasses import dataclass
from typing import Optional, Tuple

QUALITY_STATES = (
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


@dataclass(frozen=True)
class SensorQualityConfig:
    expected_sample_count: Optional[int]
    max_drop_rate: float = 0.10
    max_latency_ms: float = 200.0
    min_coverage: float = 0.80

    def __post_init__(self):
        if self.expected_sample_count is not None:
            if (
                not isinstance(self.expected_sample_count, int)
                or self.expected_sample_count <= 0
            ):
                raise ValueError(
                    "expected_sample_count must be a positive integer or None"
                )

        for name, value in (
            ("max_drop_rate", self.max_drop_rate),
            ("min_coverage", self.min_coverage),
        ):
            if not isinstance(value, (int, float)):
                raise TypeError(f"{name} must be numeric")
            if not 0 <= float(value) <= 1:
                raise ValueError(f"{name} must be between 0 and 1")

        if not isinstance(self.max_latency_ms, (int, float)):
            raise TypeError("max_latency_ms must be numeric")
        if self.max_latency_ms < 0:
            raise ValueError("max_latency_ms cannot be negative")


@dataclass(frozen=True)
class SensorQualityResult:
    quality_state: str
    expected_sample_count: Optional[int]
    observed_sample_count: int
    valid_sample_count: int
    missing_sample_count: int
    coverage: Optional[float]
    drop_rate: Optional[float]
    non_finite_sample_count: int
    timeout_count: int
    no_response_count: int
    sensor_error_count: int
    invalid_response_count: int
    stale_sample_count: int
    repeated_sample_count: int
    mean_latency_ms: Optional[float]
    max_latency_ms: Optional[float]
    affected_sensors: Tuple[str, ...]
    provenance: str
    limitations: Tuple[str, ...]

import math


def assess_sensor_quality(
    *,
    values,
    provenance,
    config,
    timeout_count=0,
    no_response_count=0,
    sensor_error_count=0,
    invalid_response_count=0,
    latencies_ms=(),
    affected_sensors=(),
):
    values = tuple(values)
    latencies_ms = tuple(latencies_ms)
    affected_sensors = tuple(sorted(set(affected_sensors)))

    observed_sample_count = len(values)
    missing_sample_count = sum(value is None for value in values)

    non_finite_sample_count = sum(
        1
        for value in values
        if isinstance(value, (int, float))
        and not isinstance(value, bool)
        and not math.isfinite(float(value))
    )

    valid_numeric_values = tuple(
        float(value)
        for value in values
        if isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
    )

    valid_sample_count = len(valid_numeric_values)

    if config.expected_sample_count is None:
        coverage = None
        drop_rate = None
    else:
        missing_from_expected = max(
            config.expected_sample_count - observed_sample_count,
            0,
        )

        total_missing = missing_sample_count + missing_from_expected

        coverage = valid_sample_count / config.expected_sample_count
        drop_rate = total_missing / config.expected_sample_count

    mean_latency_ms = (
        sum(float(value) for value in latencies_ms) / len(latencies_ms)
        if latencies_ms
        else None
    )

    max_latency_ms = (
        max(float(value) for value in latencies_ms)
        if latencies_ms
        else None
    )

    repeated_sample_count = 0
    stale_sample_count = 0

    limitations = []

    if config.expected_sample_count is None:
        limitations.append("EXPECTED_SAMPLE_COUNT_UNKNOWN")

    if timeout_count > 0:
        quality_state = "SENSOR_TIMEOUT"

    elif no_response_count > 0:
        quality_state = "SENSOR_NO_RESPONSE"

    elif sensor_error_count > 0:
        quality_state = "SENSOR_ERROR"

    elif invalid_response_count > 0 or non_finite_sample_count > 0:
        quality_state = "INVALID_RESPONSE"

    elif observed_sample_count == 0:
        quality_state = "MISSING_DATA"

    elif (
        coverage is not None
        and coverage < config.min_coverage
    ):
        quality_state = "INSUFFICIENT_SAMPLING"

    elif (
        drop_rate is not None
        and drop_rate > config.max_drop_rate
    ):
        quality_state = "SUSPECT_SIGNAL_QUALITY"

    elif (
        max_latency_ms is not None
        and max_latency_ms > config.max_latency_ms
    ):
        quality_state = "SUSPECT_SIGNAL_QUALITY"

    elif missing_sample_count > 0:
        quality_state = "MISSING_DATA"

    else:
        quality_state = "VALID"

    return SensorQualityResult(
        quality_state=quality_state,
        expected_sample_count=config.expected_sample_count,
        observed_sample_count=observed_sample_count,
        valid_sample_count=valid_sample_count,
        missing_sample_count=missing_sample_count,
        coverage=coverage,
        drop_rate=drop_rate,
        non_finite_sample_count=non_finite_sample_count,
        timeout_count=int(timeout_count),
        no_response_count=int(no_response_count),
        sensor_error_count=int(sensor_error_count),
        invalid_response_count=int(invalid_response_count),
        stale_sample_count=stale_sample_count,
        repeated_sample_count=repeated_sample_count,
        mean_latency_ms=mean_latency_ms,
        max_latency_ms=max_latency_ms,
        affected_sensors=affected_sensors,
        provenance=provenance,
        limitations=tuple(limitations),
    )
