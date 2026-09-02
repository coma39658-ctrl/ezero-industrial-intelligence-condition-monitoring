import unittest

from src.real_sensor_acquisition import (
    AcquisitionAuthorization,
    AcquisitionSession,
    RealSensorSourceConfig,
    build_acquisition_evidence,
)


class RealSensorAcquisitionTests(unittest.TestCase):

    def _session(self, **source_overrides):
        auth = AcquisitionAuthorization(
            site_authorized=True,
            consent_accepted=True,
        )

        source_args = {
            "source_type": "EXTERNAL_SENSOR",
            "source_identity": "sensor-gateway-01",
            "sensor_identity": "vibration-01",
            "machine_family": "ROTATING_DRIVE_SYSTEM",
            "operating_context": "NORMAL_PRODUCTION",
            "expected_unit": "mm/s",
        }
        source_args.update(source_overrides)

        source = RealSensorSourceConfig(**source_args)

        return AcquisitionSession(
            session_id="EZRA-TEST-001",
            authorization=auth,
            source=source,
        )

    def test_authorization_required(self):
        with self.assertRaises(ValueError):
            AcquisitionAuthorization(
                site_authorized=False,
                consent_accepted=True,
            )

    def test_consent_required(self):
        with self.assertRaises(ValueError):
            AcquisitionAuthorization(
                site_authorized=True,
                consent_accepted=False,
            )

    def test_auto_discovery_rejected(self):
        with self.assertRaises(ValueError):
            self._session(auto_discovery=True)

    def test_control_rejected(self):
        with self.assertRaises(ValueError):
            self._session(control_allowed=True)

    def test_write_credentials_rejected(self):
        with self.assertRaises(ValueError):
            self._session(write_credentials_required=True)

    def test_live_io_rejected_in_software_validation(self):
        auth = AcquisitionAuthorization(
            site_authorized=True,
            consent_accepted=True,
        )

        source = RealSensorSourceConfig(
            source_type="EXTERNAL_SENSOR",
            source_identity="sensor-gateway-01",
            sensor_identity="vibration-01",
            machine_family="ROTATING_DRIVE_SYSTEM",
            operating_context="NORMAL_PRODUCTION",
        )

        with self.assertRaises(ValueError):
            AcquisitionSession(
                session_id="EZRA-LIVE",
                authorization=auth,
                source=source,
                live_io_authorized=True,
            )

    def test_valid_numeric_payload(self):
        session = self._session()

        evidence = build_acquisition_evidence(
            session=session,
            raw_payload=b"12.50",
            sensor_quality="VALID",
        )

        self.assertEqual(evidence.provenance, "REAL_SENSOR")
        self.assertEqual(evidence.parsed_value, 12.5)
        self.assertEqual(evidence.source_identity, "sensor-gateway-01")
        self.assertEqual(evidence.sensor_identity, "vibration-01")
        self.assertFalse(evidence.control_allowed)
        self.assertFalse(evidence.diagnostic_claim)

    def test_source_and_evidence_hashes_are_distinct(self):
        session = self._session()

        evidence = build_acquisition_evidence(
            session=session,
            raw_payload=b"12.50",
            sensor_quality="VALID",
        )

        self.assertNotEqual(
            evidence.source_hash,
            evidence.evidence_hash,
        )

    def test_deterministic_evidence(self):
        session = self._session()

        first = build_acquisition_evidence(
            session=session,
            raw_payload=b"12.50",
            sensor_quality="VALID",
            limitations=("SOFTWARE_ONLY",),
        )

        second = build_acquisition_evidence(
            session=session,
            raw_payload=b"12.50",
            sensor_quality="VALID",
            limitations=("SOFTWARE_ONLY",),
        )

        self.assertEqual(first, second)

    def test_invalid_numeric_payload_rejected(self):
        session = self._session()

        with self.assertRaises(ValueError):
            build_acquisition_evidence(
                session=session,
                raw_payload=b"not-a-number",
                sensor_quality="VALID",
            )

    def test_non_finite_payload_rejected(self):
        session = self._session()

        with self.assertRaises(ValueError):
            build_acquisition_evidence(
                session=session,
                raw_payload=b"nan",
                sensor_quality="VALID",
            )

    def test_missing_data_is_not_fabricated(self):
        session = self._session()

        evidence = build_acquisition_evidence(
            session=session,
            raw_payload=b"",
            sensor_quality="MISSING_DATA",
        )

        self.assertIsNone(evidence.parsed_value)
        self.assertEqual(evidence.raw_payload, b"")

    def test_quality_problem_does_not_create_value(self):
        session = self._session()

        evidence = build_acquisition_evidence(
            session=session,
            raw_payload=b"999",
            sensor_quality="SENSOR_ERROR",
        )

        self.assertIsNone(evidence.parsed_value)
        self.assertEqual(evidence.sensor_quality, "SENSOR_ERROR")


if __name__ == "__main__":
    unittest.main()
