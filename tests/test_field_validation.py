import unittest

from src.field_validation import (
    FIELD_VALIDATION_PROVENANCE,
    FieldValidationAuthorization,
    FieldValidationSession,
    build_field_validation_evidence,
    canonical_evidence_hash,
    generate_session_id,
    validate_session_safety,
)


class FieldValidationTests(unittest.TestCase):
    def _authorized_session(self, session_id="EZFV-TEST"):
        authorization = FieldValidationAuthorization(
            site_authorized=True,
            consent_accepted=True,
            operator_reference="operator-approved",
        )

        return FieldValidationSession(
            session_id=session_id,
            machine_family="ROTATING_DRIVE_SYSTEM",
            sensor_names=("vibration", "temperature"),
            operating_context="NORMAL_PRODUCTION",
            authorization=authorization,
        )

    def test_authorization_required(self):
        with self.assertRaises(ValueError):
            FieldValidationAuthorization(
                site_authorized=False,
                consent_accepted=True,
            )

    def test_consent_required(self):
        with self.assertRaises(ValueError):
            FieldValidationAuthorization(
                site_authorized=True,
                consent_accepted=False,
            )

    def test_session_ids_are_unique(self):
        first = generate_session_id()
        second = generate_session_id()

        self.assertNotEqual(first, second)
        self.assertTrue(first.startswith("EZFV-"))
        self.assertTrue(second.startswith("EZFV-"))

    def test_session_safety_defaults(self):
        session = self._authorized_session()

        self.assertTrue(validate_session_safety(session))
        self.assertTrue(session.read_only)
        self.assertFalse(session.control_allowed)
        self.assertFalse(session.diagnostic_claim)
        self.assertFalse(session.autonomous_action)
        self.assertTrue(session.real_sensor_mode)

    def test_control_enabled_is_rejected(self):
        authorization = FieldValidationAuthorization(
            site_authorized=True,
            consent_accepted=True,
        )

        session = FieldValidationSession(
            session_id="EZFV-CONTROL",
            machine_family="ROTATING_DRIVE_SYSTEM",
            sensor_names=("vibration",),
            operating_context="NORMAL_PRODUCTION",
            authorization=authorization,
            control_allowed=True,
        )

        with self.assertRaises(ValueError):
            validate_session_safety(session)

    def test_diagnostic_claim_enabled_is_rejected(self):
        authorization = FieldValidationAuthorization(
            site_authorized=True,
            consent_accepted=True,
        )

        session = FieldValidationSession(
            session_id="EZFV-DIAG",
            machine_family="ROTATING_DRIVE_SYSTEM",
            sensor_names=("vibration",),
            operating_context="NORMAL_PRODUCTION",
            authorization=authorization,
            diagnostic_claim=True,
        )

        with self.assertRaises(ValueError):
            validate_session_safety(session)

    def test_real_sensor_provenance_is_explicit(self):
        session = self._authorized_session()

        evidence = build_field_validation_evidence(
            session=session,
            raw_source_bytes=b"sensor-payload",
            sensor_quality="VALID",
            condition_screening="NORMAL",
        )

        self.assertEqual(
            evidence.provenance,
            FIELD_VALIDATION_PROVENANCE,
        )
        self.assertEqual(evidence.provenance, "REAL_SENSOR")
        self.assertTrue(evidence.read_only)
        self.assertFalse(evidence.control_allowed)
        self.assertFalse(evidence.diagnostic_claim)

    def test_evidence_hash_is_deterministic(self):
        session = self._authorized_session()

        first = build_field_validation_evidence(
            session=session,
            raw_source_bytes=b"same-payload",
            sensor_quality="VALID",
            condition_screening="NORMAL",
            limitations=("FIELD_VALIDATION_ONLY",),
        )

        second = build_field_validation_evidence(
            session=session,
            raw_source_bytes=b"same-payload",
            sensor_quality="VALID",
            condition_screening="NORMAL",
            limitations=("FIELD_VALIDATION_ONLY",),
        )

        self.assertEqual(first, second)

    def test_canonical_hash_key_order_is_deterministic(self):
        first = canonical_evidence_hash(
            {"b": 2, "a": 1}
        )
        second = canonical_evidence_hash(
            {"a": 1, "b": 2}
        )

        self.assertEqual(first, second)

    def test_source_hash_and_evidence_hash_are_distinct_and_deterministic(self):
        session = self._authorized_session()

        first = build_field_validation_evidence(
            session=session,
            raw_source_bytes=b"same-payload",
            sensor_quality="VALID",
            condition_screening="NORMAL",
        )

        second = build_field_validation_evidence(
            session=session,
            raw_source_bytes=b"same-payload",
            sensor_quality="VALID",
            condition_screening="NORMAL",
        )

        self.assertEqual(first.source_hash, second.source_hash)
        self.assertEqual(first.evidence_hash, second.evidence_hash)
        self.assertNotEqual(first.source_hash, first.evidence_hash)



if __name__ == "__main__":
    unittest.main()
