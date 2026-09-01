import unittest

from src.textile_garment_profile import (
    MACHINE_FAMILIES,
    MACHINE_FAMILY_SENSOR_MAP,
    TextileGarmentProfileConfig,
    validate_profile_config,
)


class TextileGarmentProfileTests(unittest.TestCase):
    def test_all_machine_families_have_mapping(self):
        self.assertEqual(len(MACHINE_FAMILIES), 6)

        for family in MACHINE_FAMILIES:
            self.assertIn(family, MACHINE_FAMILY_SENSOR_MAP)
            self.assertTrue(MACHINE_FAMILY_SENSOR_MAP[family])

    def test_valid_profile_is_deterministic(self):
        config = TextileGarmentProfileConfig(
            machine_family="EMBROIDERY_MACHINE_SYSTEM",
            sensors=(
                "rpm",
                "vibration",
                "motor_current",
                "spindle_temperature",
                "load",
            ),
            operating_context="NORMAL_PRODUCTION",
        )

        first = validate_profile_config(config)
        second = validate_profile_config(config)

        self.assertEqual(first, second)

    def test_missing_recommended_sensors_are_reported_not_fabricated(self):
        config = TextileGarmentProfileConfig(
            machine_family="ROTATING_DRIVE_SYSTEM",
            sensors=("vibration", "rpm"),
            operating_context="NORMAL_PRODUCTION",
        )

        result = validate_profile_config(config)

        self.assertEqual(
            result.configured_sensors,
            ("vibration", "rpm"),
        )

        self.assertIn(
            "temperature",
            result.missing_recommended_sensors,
        )

        self.assertNotIn(
            "temperature",
            result.configured_sensors,
        )

    def test_read_only_and_claim_boundaries(self):
        config = TextileGarmentProfileConfig(
            machine_family="SEWING_GARMENT_SYSTEM",
            sensors=("motor_current", "rpm"),
        )

        result = validate_profile_config(config)

        self.assertTrue(result.read_only)
        self.assertFalse(result.diagnostic_claim)
        self.assertFalse(result.real_sensor_authorized)

    def test_invalid_machine_family_rejected(self):
        with self.assertRaises(ValueError):
            TextileGarmentProfileConfig(
                machine_family="UNKNOWN_MACHINE",
                sensors=("vibration",),
            )

    def test_invalid_sensor_rejected(self):
        with self.assertRaises(ValueError):
            TextileGarmentProfileConfig(
                machine_family="ROTATING_DRIVE_SYSTEM",
                sensors=("vibration", "imaginary_sensor"),
            )

    def test_empty_sensor_list_rejected(self):
        with self.assertRaises(ValueError):
            TextileGarmentProfileConfig(
                machine_family="ROTATING_DRIVE_SYSTEM",
                sensors=(),
            )

    def test_invalid_context_rejected(self):
        with self.assertRaises(ValueError):
            TextileGarmentProfileConfig(
                machine_family="ROTATING_DRIVE_SYSTEM",
                sensors=("vibration",),
                operating_context="INVALID_CONTEXT",
            )


if __name__ == "__main__":
    unittest.main()
