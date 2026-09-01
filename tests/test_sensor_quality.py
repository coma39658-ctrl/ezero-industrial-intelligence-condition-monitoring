import math
import unittest

from src.sensor_quality import (
    QUALITY_STATES,
    SensorQualityConfig,
    assess_sensor_quality,
)


class SensorQualityTests(unittest.TestCase):
    def test_canonical_states_count(self):
        self.assertEqual(len(QUALITY_STATES), 10)

    def test_valid_data(self):
        result = assess_sensor_quality(
            values=[1.0, 1.1, 0.9, 1.0],
            provenance="SIMULATED",
            config=SensorQualityConfig(expected_sample_count=4),
        )
        self.assertEqual(result.quality_state, "VALID")
        self.assertEqual(result.coverage, 1.0)
        self.assertEqual(result.drop_rate, 0.0)
        self.assertEqual(result.provenance, "SIMULATED")

    def test_timeout_distinct(self):
        result = assess_sensor_quality(
            values=[1.0, None],
            provenance="SIMULATED",
            config=SensorQualityConfig(expected_sample_count=2),
            timeout_count=1,
        )
        self.assertEqual(result.quality_state, "SENSOR_TIMEOUT")

    def test_no_response_distinct(self):
        result = assess_sensor_quality(
            values=[1.0, None],
            provenance="SIMULATED",
            config=SensorQualityConfig(expected_sample_count=2),
            no_response_count=1,
        )
        self.assertEqual(result.quality_state, "SENSOR_NO_RESPONSE")

    def test_sensor_error_distinct(self):
        result = assess_sensor_quality(
            values=[1.0, None],
            provenance="SIMULATED",
            config=SensorQualityConfig(expected_sample_count=2),
            sensor_error_count=1,
        )
        self.assertEqual(result.quality_state, "SENSOR_ERROR")

    def test_invalid_response_distinct(self):
        result = assess_sensor_quality(
            values=[1.0, None],
            provenance="SIMULATED",
            config=SensorQualityConfig(expected_sample_count=2),
            invalid_response_count=1,
        )
        self.assertEqual(result.quality_state, "INVALID_RESPONSE")

    def test_non_finite_is_invalid(self):
        for bad in (math.nan, math.inf, -math.inf):
            result = assess_sensor_quality(
                values=[1.0, bad],
                provenance="SIMULATED",
                config=SensorQualityConfig(expected_sample_count=2),
            )
            self.assertEqual(result.quality_state, "INVALID_RESPONSE")
            self.assertEqual(result.non_finite_sample_count, 1)

    def test_missing_data_not_zero(self):
        values = [1.0, None, 2.0]
        result = assess_sensor_quality(
            values=values,
            provenance="SIMULATED",
            config=SensorQualityConfig(
                expected_sample_count=3,
                min_coverage=0.60,
                max_drop_rate=0.50,
            ),
        )
        self.assertEqual(result.quality_state, "MISSING_DATA")
        self.assertEqual(result.missing_sample_count, 1)
        self.assertNotIn(0, [v for v in values if v is None])

    def test_low_coverage_is_insufficient_sampling(self):
        result = assess_sensor_quality(
            values=[1.0, None, None, None],
            provenance="SIMULATED",
            config=SensorQualityConfig(
                expected_sample_count=4,
                min_coverage=0.80,
            ),
        )
        self.assertEqual(result.quality_state, "INSUFFICIENT_SAMPLING")

    def test_excessive_drop_rate_is_suspect_quality(self):
        result = assess_sensor_quality(
            values=[1.0] * 9,
            provenance="SIMULATED",
            config=SensorQualityConfig(
                expected_sample_count=10,
                max_drop_rate=0.05,
                min_coverage=0.80,
            ),
        )
        self.assertEqual(result.quality_state, "SUSPECT_SIGNAL_QUALITY")
        self.assertAlmostEqual(result.drop_rate, 0.1)

    def test_latency_is_quality_problem_not_machine_state(self):
        result = assess_sensor_quality(
            values=[1.0, 1.1, 1.2],
            provenance="SIMULATED",
            config=SensorQualityConfig(
                expected_sample_count=3,
                max_latency_ms=200.0,
            ),
            latencies_ms=[50.0, 250.0, 75.0],
        )
        self.assertEqual(result.quality_state, "SUSPECT_SIGNAL_QUALITY")
        self.assertEqual(result.max_latency_ms, 250.0)

    def test_unknown_expected_count_remains_unknown(self):
        result = assess_sensor_quality(
            values=[1.0, 2.0],
            provenance="LOG_REPLAY",
            config=SensorQualityConfig(expected_sample_count=None),
        )
        self.assertIsNone(result.coverage)
        self.assertIsNone(result.drop_rate)
        self.assertIn(
            "EXPECTED_SAMPLE_COUNT_UNKNOWN",
            result.limitations,
        )
        self.assertEqual(result.provenance, "LOG_REPLAY")

    def test_provenance_preserved(self):
        for provenance in (
            "SIMULATED",
            "LOG_REPLAY",
            "MANUAL_ENTRY",
            "VIDEO_ESTIMATE",
            "REAL_SENSOR",
        ):
            result = assess_sensor_quality(
                values=[1.0],
                provenance=provenance,
                config=SensorQualityConfig(expected_sample_count=1),
            )
            self.assertEqual(result.provenance, provenance)

    def test_invalid_config_rejected(self):
        with self.assertRaises(ValueError):
            SensorQualityConfig(expected_sample_count=0)

        with self.assertRaises(ValueError):
            SensorQualityConfig(
                expected_sample_count=10,
                max_drop_rate=1.1,
            )

        with self.assertRaises(ValueError):
            SensorQualityConfig(
                expected_sample_count=10,
                min_coverage=-0.1,
            )

        with self.assertRaises(ValueError):
            SensorQualityConfig(
                expected_sample_count=10,
                max_latency_ms=-1,
            )


if __name__ == "__main__":
    unittest.main()
