from dataclasses import dataclass
from typing import Optional, Tuple

PROVENANCE_LOG_REPLAY = "LOG_REPLAY"

PARSE_STATUSES = (
    "ACCEPTED",
    "MALFORMED_ROW",
    "MISSING_REQUIRED_FIELD",
    "INVALID_NUMERIC_VALUE",
    "NON_FINITE_VALUE",
    "UNSUPPORTED_STRUCTURE",
    "UNKNOWN_SENSOR",
    "INVALID_TIMESTAMP",
)


@dataclass(frozen=True)
class ReplaySchemaMapping:
    timestamp_field: Optional[str]
    sensor_name_field: str
    value_field: str
    unit_field: Optional[str] = None
    operating_context_field: Optional[str] = None

    def __post_init__(self):
        if not self.sensor_name_field.strip():
            raise ValueError("sensor_name_field must not be blank")
        if not self.value_field.strip():
            raise ValueError("value_field must not be blank")


@dataclass(frozen=True)
class ReplayObservation:
    source_index: int
    timestamp: Optional[str]
    sensor_name: Optional[str]
    raw_value: Optional[float]
    unit: Optional[str]
    operating_context: Optional[str]
    parse_status: str
    provenance: str = PROVENANCE_LOG_REPLAY


@dataclass(frozen=True)
class ReplayIngestionResult:
    source_identity: str
    source_format: str
    provenance: str
    total_rows: int
    accepted_rows: int
    invalid_rows: int
    missing_rows: int
    duplicate_rows: int
    source_hash: str
    observations: Tuple[ReplayObservation, ...]
    limitations: Tuple[str, ...]

import csv
import hashlib
import io
import math


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _parse_numeric(value):
    if value is None or str(value).strip() == "":
        return None, "MISSING_REQUIRED_FIELD"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None, "INVALID_NUMERIC_VALUE"

    if not math.isfinite(number):
        return None, "NON_FINITE_VALUE"

    return number, "ACCEPTED"


def ingest_csv_bytes(
    *,
    source_bytes,
    source_identity,
    mapping,
):
    if not isinstance(source_bytes, (bytes, bytearray)):
        raise TypeError("source_bytes must be bytes")

    if not isinstance(mapping, ReplaySchemaMapping):
        raise TypeError("mapping must be ReplaySchemaMapping")

    source_hash = _sha256_bytes(bytes(source_bytes))

    try:
        text = bytes(source_bytes).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV source must be valid UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV header is required")

    required_fields = {
        mapping.sensor_name_field,
        mapping.value_field,
    }

    if mapping.timestamp_field:
        required_fields.add(mapping.timestamp_field)

    missing_columns = required_fields.difference(reader.fieldnames)
    if missing_columns:
        raise ValueError(
            "Missing required CSV columns: "
            + ", ".join(sorted(missing_columns))
        )

    observations = []
    seen_rows = set()
    duplicate_rows = 0
    accepted_rows = 0
    invalid_rows = 0
    missing_rows = 0

    for source_index, row in enumerate(reader, start=1):
        row_key = tuple((name, row.get(name)) for name in reader.fieldnames)

        if row_key in seen_rows:
            duplicate_rows += 1
        else:
            seen_rows.add(row_key)

        sensor_name = row.get(mapping.sensor_name_field)
        sensor_name = (
            sensor_name.strip()
            if isinstance(sensor_name, str)
            else None
        )

        raw_value, parse_status = _parse_numeric(
            row.get(mapping.value_field)
        )

        if not sensor_name:
            parse_status = "MISSING_REQUIRED_FIELD"

        timestamp = (
            row.get(mapping.timestamp_field)
            if mapping.timestamp_field
            else None
        )

        unit = (
            row.get(mapping.unit_field)
            if mapping.unit_field
            else None
        )

        operating_context = (
            row.get(mapping.operating_context_field)
            if mapping.operating_context_field
            else None
        )

        if parse_status == "ACCEPTED":
            accepted_rows += 1
        else:
            invalid_rows += 1
            if parse_status == "MISSING_REQUIRED_FIELD":
                missing_rows += 1

        observations.append(
            ReplayObservation(
                source_index=source_index,
                timestamp=timestamp,
                sensor_name=sensor_name,
                raw_value=raw_value,
                unit=unit,
                operating_context=operating_context,
                parse_status=parse_status,
            )
        )

    return ReplayIngestionResult(
        source_identity=source_identity,
        source_format="CSV",
        provenance=PROVENANCE_LOG_REPLAY,
        total_rows=len(observations),
        accepted_rows=accepted_rows,
        invalid_rows=invalid_rows,
        missing_rows=missing_rows,
        duplicate_rows=duplicate_rows,
        source_hash=source_hash,
        observations=tuple(observations),
        limitations=(),
    )

import csv
import hashlib
import io
import math


def _sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def _parse_numeric(value):
    if value is None or str(value).strip() == "":
        return None, "MISSING_REQUIRED_FIELD"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None, "INVALID_NUMERIC_VALUE"

    if not math.isfinite(number):
        return None, "NON_FINITE_VALUE"

    return number, "ACCEPTED"


def ingest_csv_bytes(
    *,
    source_bytes,
    source_identity,
    mapping,
):
    if not isinstance(source_bytes, (bytes, bytearray)):
        raise TypeError("source_bytes must be bytes")

    if not isinstance(mapping, ReplaySchemaMapping):
        raise TypeError("mapping must be ReplaySchemaMapping")

    source_hash = _sha256_bytes(bytes(source_bytes))

    try:
        text = bytes(source_bytes).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("CSV source must be valid UTF-8") from exc

    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None:
        raise ValueError("CSV header is required")

    required_fields = {
        mapping.sensor_name_field,
        mapping.value_field,
    }

    if mapping.timestamp_field:
        required_fields.add(mapping.timestamp_field)

    missing_columns = required_fields.difference(reader.fieldnames)
    if missing_columns:
        raise ValueError(
            "Missing required CSV columns: "
            + ", ".join(sorted(missing_columns))
        )

    observations = []
    seen_rows = set()
    duplicate_rows = 0
    accepted_rows = 0
    invalid_rows = 0
    missing_rows = 0

    for source_index, row in enumerate(reader, start=1):
        row_key = tuple((name, row.get(name)) for name in reader.fieldnames)

        if row_key in seen_rows:
            duplicate_rows += 1
        else:
            seen_rows.add(row_key)

        sensor_name = row.get(mapping.sensor_name_field)
        sensor_name = (
            sensor_name.strip()
            if isinstance(sensor_name, str)
            else None
        )

        raw_value, parse_status = _parse_numeric(
            row.get(mapping.value_field)
        )

        if not sensor_name:
            parse_status = "MISSING_REQUIRED_FIELD"

        timestamp = (
            row.get(mapping.timestamp_field)
            if mapping.timestamp_field
            else None
        )

        unit = (
            row.get(mapping.unit_field)
            if mapping.unit_field
            else None
        )

        operating_context = (
            row.get(mapping.operating_context_field)
            if mapping.operating_context_field
            else None
        )

        if parse_status == "ACCEPTED":
            accepted_rows += 1
        else:
            invalid_rows += 1
            if parse_status == "MISSING_REQUIRED_FIELD":
                missing_rows += 1

        observations.append(
            ReplayObservation(
                source_index=source_index,
                timestamp=timestamp,
                sensor_name=sensor_name,
                raw_value=raw_value,
                unit=unit,
                operating_context=operating_context,
                parse_status=parse_status,
            )
        )

    return ReplayIngestionResult(
        source_identity=source_identity,
        source_format="CSV",
        provenance=PROVENANCE_LOG_REPLAY,
        total_rows=len(observations),
        accepted_rows=accepted_rows,
        invalid_rows=invalid_rows,
        missing_rows=missing_rows,
        duplicate_rows=duplicate_rows,
        source_hash=source_hash,
        observations=tuple(observations),
        limitations=(),
    )

import json


def ingest_json_bytes(
    *,
    source_bytes,
    source_identity,
    mapping,
):
    if not isinstance(source_bytes, (bytes, bytearray)):
        raise TypeError("source_bytes must be bytes")

    if not isinstance(mapping, ReplaySchemaMapping):
        raise TypeError("mapping must be ReplaySchemaMapping")

    source_hash = _sha256_bytes(bytes(source_bytes))

    try:
        text = bytes(source_bytes).decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON source must be valid UTF-8") from exc

    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid JSON source") from exc

    if not isinstance(payload, list):
        raise ValueError("JSON source must be a list of observation objects")

    observations = []
    seen_rows = set()
    duplicate_rows = 0
    accepted_rows = 0
    invalid_rows = 0
    missing_rows = 0

    for source_index, row in enumerate(payload, start=1):
        if not isinstance(row, dict):
            observations.append(
                ReplayObservation(
                    source_index=source_index,
                    timestamp=None,
                    sensor_name=None,
                    raw_value=None,
                    unit=None,
                    operating_context=None,
                    parse_status="UNSUPPORTED_STRUCTURE",
                )
            )
            invalid_rows += 1
            continue

        row_key = json.dumps(
            row,
            sort_keys=True,
            separators=(",", ":"),
        )

        if row_key in seen_rows:
            duplicate_rows += 1
        else:
            seen_rows.add(row_key)

        sensor_name = row.get(mapping.sensor_name_field)
        sensor_name = (
            sensor_name.strip()
            if isinstance(sensor_name, str)
            else None
        )

        raw_value, parse_status = _parse_numeric(
            row.get(mapping.value_field)
        )

        if not sensor_name:
            parse_status = "MISSING_REQUIRED_FIELD"

        timestamp = (
            row.get(mapping.timestamp_field)
            if mapping.timestamp_field
            else None
        )

        unit = (
            row.get(mapping.unit_field)
            if mapping.unit_field
            else None
        )

        operating_context = (
            row.get(mapping.operating_context_field)
            if mapping.operating_context_field
            else None
        )

        if parse_status == "ACCEPTED":
            accepted_rows += 1
        else:
            invalid_rows += 1
            if parse_status == "MISSING_REQUIRED_FIELD":
                missing_rows += 1

        observations.append(
            ReplayObservation(
                source_index=source_index,
                timestamp=timestamp,
                sensor_name=sensor_name,
                raw_value=raw_value,
                unit=unit,
                operating_context=operating_context,
                parse_status=parse_status,
            )
        )

    return ReplayIngestionResult(
        source_identity=source_identity,
        source_format="JSON",
        provenance=PROVENANCE_LOG_REPLAY,
        total_rows=len(observations),
        accepted_rows=accepted_rows,
        invalid_rows=invalid_rows,
        missing_rows=missing_rows,
        duplicate_rows=duplicate_rows,
        source_hash=source_hash,
        observations=tuple(observations),
        limitations=(),
    )
