import unittest

from src.end_to_end_demo_flow import (
    DemoFlowInput,
    run_demo_flow,
)


class EndToEndDemoFlowTests(unittest.TestCase):
    def test_scenario_a_healthy_simulated(self):
        demo_input = DemoFlowInput(
            provenance="SIMULATED",
            machine_family="SEWING_GARMENT_SYSTEM",
            configured_sensors=(
                "motor_current",
                "rpm",
                "vibration",
                "temperature",
                "power",
            ),
            operating_context="NORMAL_PRODUCTION",
        )

        result = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="VALID",
            condition_screening="NORMAL",
            evidence_level="L2_REFERENCE_SCREENED",
        )

        self.assertEqual(result.provenance, "SIMULATED")
        self.assertEqual(result.sensor_quality, "VALID")
        self.assertEqual(result.condition_screening, "NORMAL")
        self.assertTrue(result.read_only)
        self.assertFalse(result.diagnostic_claim)

    def test_scenario_b_simulated_anomalous_pattern(self):
        demo_input = DemoFlowInput(
            provenance="SIMULATED",
            machine_family="ROTATING_DRIVE_SYSTEM",
            configured_sensors=(
                "vibration",
                "temperature",
                "rpm",
                "motor_current",
                "power",
                "load",
            ),
            operating_context="HIGH_LOAD",
        )

        result = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="VALID",
            condition_screening="ANOMALOUS_PATTERN",
            evidence_level="L3_PATTERN_SUPPORTED",
        )

        self.assertEqual(
            result.condition_screening,
            "ANOMALOUS_PATTERN",
        )
        self.assertFalse(result.diagnostic_claim)

    def test_scenario_c_replay_missing_data(self):
        demo_input = DemoFlowInput(
            provenance="LOG_REPLAY",
            machine_family="WEAVING_LOOM_SYSTEM",
            configured_sensors=("vibration", "rpm"),
            operating_context="NORMAL_PRODUCTION",
            source_identity="loom_replay.csv",
        )

        result = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="MISSING_DATA",
            condition_screening="INSUFFICIENT_DATA",
            evidence_level="L1_MEASURED",
        )

        self.assertEqual(result.provenance, "LOG_REPLAY")
        self.assertEqual(result.sensor_quality, "MISSING_DATA")
        self.assertEqual(
            result.condition_screening,
            "INSUFFICIENT_DATA",
        )

    def test_scenario_d_quality_problem_does_not_create_fault(self):
        demo_input = DemoFlowInput(
            provenance="LOG_REPLAY",
            machine_family="KNITTING_SYSTEM",
            configured_sensors=("rpm", "vibration"),
            operating_context="NORMAL_PRODUCTION",
            source_identity="quality_issue.json",
        )

        result = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="SUSPECT_SIGNAL_QUALITY",
            condition_screening="NORMAL",
            evidence_level="L1_MEASURED",
        )

        self.assertEqual(
            result.sensor_quality,
            "SUSPECT_SIGNAL_QUALITY",
        )
        self.assertEqual(result.condition_screening, "NORMAL")

    def test_scenario_e_missing_recommended_sensors_reported(self):
        demo_input = DemoFlowInput(
            provenance="SIMULATED",
            machine_family="EMBROIDERY_MACHINE_SYSTEM",
            configured_sensors=("rpm", "vibration"),
            operating_context="NORMAL_PRODUCTION",
        )

        result = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="VALID",
            condition_screening="NORMAL",
            evidence_level="L1_MEASURED",
        )

        self.assertTrue(result.missing_recommended_sensors)
        self.assertIn(
            "MISSING_RECOMMENDED_SENSORS",
            result.limitations,
        )

    def test_real_sensor_is_rejected(self):
        with self.assertRaises(ValueError):
            DemoFlowInput(
                provenance="REAL_SENSOR",
                machine_family="ROTATING_DRIVE_SYSTEM",
                configured_sensors=("vibration",),
                operating_context="NORMAL_PRODUCTION",
            )

    def test_invalid_screening_rejected(self):
        demo_input = DemoFlowInput(
            provenance="SIMULATED",
            machine_family="ROTATING_DRIVE_SYSTEM",
            configured_sensors=("vibration",),
            operating_context="NORMAL_PRODUCTION",
        )

        with self.assertRaises(ValueError):
            run_demo_flow(
                demo_input=demo_input,
                sensor_quality="VALID",
                condition_screening="DIAGNOSED_FAILURE",
                evidence_level="L1_MEASURED",
            )

    def test_identical_input_is_deterministic(self):
        demo_input = DemoFlowInput(
            provenance="SIMULATED",
            machine_family="SPINNING_WINDING_SYSTEM",
            configured_sensors=("vibration", "rpm"),
            operating_context="NORMAL_PRODUCTION",
        )

        first = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="VALID",
            condition_screening="NORMAL",
            evidence_level="L1_MEASURED",
        )

        second = run_demo_flow(
            demo_input=demo_input,
            sensor_quality="VALID",
            condition_screening="NORMAL",
            evidence_level="L1_MEASURED",
        )

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
