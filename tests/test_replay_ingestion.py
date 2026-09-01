import unittest

from src.replay_ingestion import (
    PROVENANCE_LOG_REPLAY,
    ReplaySchemaMapping,
    ingest_csv_bytes,
    ingest_json_bytes,
)


class ReplayIngestionTests(unittest.TestCase):
    def setUp(self):
        self.mapping = ReplaySchemaMapping(
            timestamp_field="timestamp",
            sensor_name_field="sensor",
            value_field="value",
            unit_field="unit",
            operating_context_field="context",
        )

    def test_valid_csv_ingestion(self):
        source = (
            b"timestamp,sensor,value,unit,context\n"
            b"1,vibration,1.2,mm/s,NORMAL_LOAD\n"
            b"2,temperature,61.5,C,NORMAL_LOAD\n"
        )

        result = ingest_csv_bytes(
            source_bytes=source,
            source_identity="valid.csv",
            mapping=self.mapping,
        )

        self.assertEqual(result.provenance, PROVENANCE_LOG_REPLAY)
        self.assertEqual(result.total_rows, 2)
        self.assertEqual(result.accepted_rows, 2)
        self.assertEqual(result.invalid_rows, 0)

    def test_missing_value_not_zero(self):
        source = (
            b"timestamp,sensor,value,unit,context\n"
            b"1,vibration,,mm/s,NORMAL_LOAD\n"
        )

        result = ingest_csv_bytes(
            source_bytes=source,
            source_identity="missing.csv",
            mapping=self.mapping,
        )

        observation = result.observations[0]
        self.assertIsNone(observation.raw_value)
        self.assertEqual(
            observation.parse_status,
            "MISSING_REQUIRED_FIELD",
        )

    def test_invalid_numeric_value(self):
        source = (
            b"timestamp,sensor,value,unit,context\n"
            b"1,vibration,abc,mm/s,NORMAL_LOAD\n"
        )

        result = ingest_csv_bytes(
            source_bytes=source,
            source_identity="invalid.csv",
            mapping=self.mapping,
        )

        self.assertEqual(
            result.observations[0].parse_status,
            "INVALID_NUMERIC_VALUE",
        )

    def test_non_finite_values(self):
        for value in (b"nan", b"inf", b"-inf"):
            source = (
                b"timestamp,sensor,value,unit,context\n"
                b"1,vibration,"
                + value
                + b",mm/s,NORMAL_LOAD\n"
            )

            result = ingest_csv_bytes(
                source_bytes=source,
                source_identity="nonfinite.csv",
                mapping=self.mapping,
            )

            self.assertEqual(
                result.observations[0].parse_status,
                "NON_FINITE_VALUE",
            )

    def test_duplicate_rows_preserved_and_counted(self):
        source = (
            b"timestamp,sensor,value,unit,context\n"
            b"1,vibration,1.2,mm/s,NORMAL_LOAD\n"
            b"1,vibration,1.2,mm/s,NORMAL_LOAD\n"
        )

        result = ingest_csv_bytes(
            source_bytes=source,
            source_identity="duplicates.csv",
            mapping=self.mapping,
        )

        self.assertEqual(result.total_rows, 2)
        self.assertEqual(len(result.observations), 2)
        self.assertEqual(result.duplicate_rows, 1)

    def test_hash_and_output_are_deterministic(self):
        source = (
            b"timestamp,sensor,value,unit,context\n"
            b"1,vibration,1.2,mm/s,NORMAL_LOAD\n"
        )

        first = ingest_csv_bytes(
            source_bytes=source,
            source_identity="same.csv",
            mapping=self.mapping,
        )

        second = ingest_csv_bytes(
            source_bytes=source,
            source_identity="same.csv",
            mapping=self.mapping,
        )

        self.assertEqual(first, second)
        self.assertEqual(first.source_hash, second.source_hash)

    def test_missing_required_column_fails_closed(self):
        source = (
            b"timestamp,value,unit,context\n"
            b"1,1.2,mm/s,NORMAL_LOAD\n"
        )

        with self.assertRaises(ValueError):
            ingest_csv_bytes(
                source_bytes=source,
                source_identity="bad-schema.csv",
                mapping=self.mapping,
            )

    def test_invalid_mapping_rejected(self):
        with self.assertRaises(ValueError):
            ReplaySchemaMapping(
                timestamp_field="timestamp",
                sensor_name_field="",
                value_field="value",
            )

        with self.assertRaises(ValueError):
            ReplaySchemaMapping(
                timestamp_field="timestamp",
                sensor_name_field="sensor",
                value_field="",
            )


if __name__ == "__main__":
    unittest.main()

class ReplayJsonIngestionTests(unittest.TestCase):
    def setUp(self):
        self.mapping = ReplaySchemaMapping(
            timestamp_field="timestamp",
            sensor_name_field="sensor",
            value_field="value",
            unit_field="unit",
            operating_context_field="context",
        )

    def test_valid_json_ingestion(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":1.2,"unit":"mm/s","context":"NORMAL_LOAD"},
            {"timestamp":"2","sensor":"temperature","value":61.5,"unit":"C","context":"NORMAL_LOAD"}
        ]'''

        result = ingest_json_bytes(
            source_bytes=source,
            source_identity="valid.json",
            mapping=self.mapping,
        )

        self.assertEqual(result.provenance, PROVENANCE_LOG_REPLAY)
        self.assertEqual(result.source_format, "JSON")
        self.assertEqual(result.total_rows, 2)
        self.assertEqual(result.accepted_rows, 2)

    def test_json_output_is_deterministic(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":1.2,"unit":"mm/s","context":"NORMAL_LOAD"}
        ]'''

        first = ingest_json_bytes(
            source_bytes=source,
            source_identity="same.json",
            mapping=self.mapping,
        )
        second = ingest_json_bytes(
            source_bytes=source,
            source_identity="same.json",
            mapping=self.mapping,
        )

        self.assertEqual(first, second)
        self.assertEqual(first.source_hash, second.source_hash)

    def test_json_missing_value_not_zero(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":null,"unit":"mm/s","context":"NORMAL_LOAD"}
        ]'''

        result = ingest_json_bytes(
            source_bytes=source,
            source_identity="missing.json",
            mapping=self.mapping,
        )

        observation = result.observations[0]
        self.assertIsNone(observation.raw_value)
        self.assertEqual(
            observation.parse_status,
            "MISSING_REQUIRED_FIELD",
        )

    def test_json_invalid_numeric_value(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":"abc","unit":"mm/s","context":"NORMAL_LOAD"}
        ]'''

        result = ingest_json_bytes(
            source_bytes=source,
            source_identity="invalid.json",
            mapping=self.mapping,
        )

        self.assertEqual(
            result.observations[0].parse_status,
            "INVALID_NUMERIC_VALUE",
        )

    def test_json_duplicate_rows_preserved(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":1.2,"unit":"mm/s","context":"NORMAL_LOAD"},
            {"timestamp":"1","sensor":"vibration","value":1.2,"unit":"mm/s","context":"NORMAL_LOAD"}
        ]'''

        result = ingest_json_bytes(
            source_bytes=source,
            source_identity="duplicates.json",
            mapping=self.mapping,
        )

        self.assertEqual(result.total_rows, 2)
        self.assertEqual(len(result.observations), 2)
        self.assertEqual(result.duplicate_rows, 1)

    def test_json_unsupported_structure_preserved(self):
        source = b'''[
            {"timestamp":"1","sensor":"vibration","value":1.2},
            "not-an-object"
        ]'''

        result = ingest_json_bytes(
            source_bytes=source,
            source_identity="structure.json",
            mapping=self.mapping,
        )

        self.assertEqual(result.total_rows, 2)
        self.assertEqual(
            result.observations[1].parse_status,
            "UNSUPPORTED_STRUCTURE",
        )
