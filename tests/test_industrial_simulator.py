import unittest

from src.industrial_simulator import (
    PROVENANCE_SIMULATED,
    SCENARIOS,
    SimulatorConfig,
    generate_case,
)


class IndustrialSimulatorTests(unittest.TestCase):
    def test_all_scenarios_generate(self):
        self.assertEqual(len(SCENARIOS), 13)

        for scenario in SCENARIOS:
            metadata, observations = generate_case(
                SimulatorConfig(scenario_id=scenario, seed=5101)
            )

            self.assertEqual(metadata.provenance, PROVENANCE_SIMULATED)
            self.assertTrue(observations)
            self.assertTrue(
                all(
                    observation.provenance == PROVENANCE_SIMULATED
                    for observation in observations
                )
            )

    def test_repeatability(self):
        for scenario in SCENARIOS:
            config = SimulatorConfig(
                scenario_id=scenario,
                seed=5101,
            )

            first = generate_case(config)
            second = generate_case(config)

            self.assertEqual(first, second)

    def test_missing_data_is_none_not_zero(self):
        for scenario in (
            "I_MISSING_DATA",
            "J_INSUFFICIENT_SAMPLING",
            "K_INTERMITTENT_PACKET_LOSS",
        ):
            metadata, observations = generate_case(
                SimulatorConfig(scenario_id=scenario, seed=5101)
            )

            missing = [
                observation
                for observation in observations
                if observation.raw_value is None
            ]

            self.assertEqual(len(missing), metadata.dropped_samples)
            self.assertEqual(
                metadata.observed_sample_count + metadata.dropped_samples,
                metadata.expected_sample_count,
            )

            for observation in missing:
                self.assertIsNone(observation.raw_value)

    def test_packet_loss_is_not_machine_anomaly(self):
        metadata, _ = generate_case(
            SimulatorConfig(
                scenario_id="K_INTERMITTENT_PACKET_LOSS",
                seed=5101,
            )
        )

        self.assertEqual(metadata.machine_ground_truth, "HEALTHY")
        self.assertEqual(
            metadata.expected_screening_state,
            "SENSOR_QUALITY_PROBLEM",
        )

    def test_latency_is_not_machine_anomaly(self):
        metadata, _ = generate_case(
            SimulatorConfig(
                scenario_id="L_LATENCY_DEGRADATION",
                seed=5101,
            )
        )

        self.assertEqual(metadata.machine_ground_truth, "HEALTHY")
        self.assertEqual(
            metadata.expected_screening_state,
            "SENSOR_QUALITY_PROBLEM",
        )
        self.assertEqual(metadata.latency_ms, 250.0)

    def test_invalid_config_rejected(self):
        with self.assertRaises(ValueError):
            SimulatorConfig(
                scenario_id="UNKNOWN",
                seed=1,
            )

        with self.assertRaises(ValueError):
            SimulatorConfig(
                scenario_id="A_HEALTHY_STABLE",
                seed=1,
                sample_count=0,
            )

        with self.assertRaises(ValueError):
            SimulatorConfig(
                scenario_id="A_HEALTHY_STABLE",
                seed=1,
                sampling_rate_hz=0,
            )


if __name__ == "__main__":
    unittest.main()

class IndustrialSimulatorExtendedTests(unittest.TestCase):
    def test_exact_expected_states(self):
        expected = {
            "A_HEALTHY_STABLE": "NORMAL",
            "B_REFERENCE_RANGE_DEVIATION": "OUT_OF_RANGE",
            "C_MULTISENSOR_ANOMALOUS_PATTERN": "ANOMALOUS_PATTERN",
            "D_TRANSIENT_NONFAULT_EVENT": "NORMAL",
            "E_LOAD_CONTEXT_SHIFT": "NORMAL",
            "F_SENSOR_TIMEOUT": "SENSOR_QUALITY_PROBLEM",
            "G_SENSOR_NO_RESPONSE": "SENSOR_QUALITY_PROBLEM",
            "H_INVALID_RESPONSE": "SENSOR_QUALITY_PROBLEM",
            "I_MISSING_DATA": "SENSOR_QUALITY_PROBLEM",
            "J_INSUFFICIENT_SAMPLING": "INSUFFICIENT_DATA",
            "K_INTERMITTENT_PACKET_LOSS": "SENSOR_QUALITY_PROBLEM",
            "L_LATENCY_DEGRADATION": "SENSOR_QUALITY_PROBLEM",
            "M_SENSOR_ERROR": "SENSOR_QUALITY_PROBLEM",
        }

        for scenario, expected_state in expected.items():
            metadata, _ = generate_case(
                SimulatorConfig(scenario_id=scenario, seed=5101)
            )
            self.assertEqual(
                metadata.expected_screening_state,
                expected_state,
            )

    def test_invalid_operating_context_rejected(self):
        with self.assertRaises(ValueError):
            SimulatorConfig(
                scenario_id="A_HEALTHY_STABLE",
                seed=1,
                operating_context="INVALID_CONTEXT",
            )

    def test_provenance_cannot_drift(self):
        for scenario in SCENARIOS:
            metadata, observations = generate_case(
                SimulatorConfig(scenario_id=scenario, seed=5101)
            )

            self.assertEqual(metadata.provenance, "SIMULATED")
            self.assertTrue(
                all(
                    observation.provenance == "SIMULATED"
                    for observation in observations
                )
            )

    def test_affected_sensor_metadata(self):
        metadata, _ = generate_case(
            SimulatorConfig(
                scenario_id="C_MULTISENSOR_ANOMALOUS_PATTERN",
                seed=5101,
            )
        )

        self.assertEqual(
            metadata.affected_sensors,
            ("vibration", "temperature", "motor_current"),
        )
