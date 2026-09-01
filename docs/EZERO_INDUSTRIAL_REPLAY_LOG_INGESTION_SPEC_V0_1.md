# E-ZERO Industrial Intelligence
## Industrial Replay / Log Ingestion Specification V0.1

Status: PRE-REGISTERED / READ-ONLY LOG INGESTION / NO DIAGNOSTIC CLAIM

## 1. Purpose

This specification defines deterministic ingestion of historical industrial
sensor logs for E-ZERO Industrial Intelligence.

The ingestion layer converts supported log formats into normalized,
evidence-preserving observations without changing the source data.

## 2. Provenance

All observations ingested through this layer MUST use:

`LOG_REPLAY`

LOG_REPLAY data MUST NOT be promoted to:
- REAL_SENSOR
- maintenance-confirmed evidence
- independently validated evidence

## 3. Read-Only Boundary

The ingestion layer MUST NOT:
- connect to live machinery
- connect to PLCs or VFDs
- issue control commands
- modify source log files
- overwrite raw source evidence
- change machine state
- claim physical diagnosis

## 4. Initial Supported Formats

V0.1 MAY support:
- CSV
- JSON

Additional formats require separate reviewed extension.

## 5. Required Observation Fields

Where available, normalized observations SHOULD preserve:
- timestamp or sample index
- sensor name
- raw value
- unit
- operating context
- source row/index
- source file identity
- provenance
- parsing/quality status

## 6. Raw Evidence Preservation

The original source representation MUST remain preserved.

Normalization MUST NOT silently:
- replace missing values with zero
- alter numeric values
- discard malformed rows without recording them
- invent timestamps
- invent units
- invent operating context

## 7. Missing Data

Missing fields MUST remain missing.

Missing values MUST NOT be:
- zero-filled
- forward-filled
- replaced with healthy defaults
- silently dropped from evidence accounting

## 8. Invalid Data

The ingestion layer MUST distinguish:
- malformed row
- missing required field
- invalid numeric value
- non-finite numeric value
- unsupported structure
- unknown sensor
- invalid timestamp where timestamp is required

Invalid input MUST fail closed or be explicitly preserved as invalid evidence.

## 9. Determinism

For identical:
- source bytes
- parser configuration
- schema mapping
- ingestion version

the normalized output MUST be identical.

## 10. Schema Mapping

Column/key mapping MUST be explicit.

No fuzzy, guessed, or automatic semantic mapping is permitted in V0.1.

Example mappings may include:
- timestamp
- sensor_name
- value
- unit
- operating_context

Machine- or customer-specific mappings require explicit configuration.

## 11. Source Identity

Where technically available, ingestion SHOULD preserve:
- filename
- byte length
- SHA-256 hash
- ingestion timestamp
- parser version

Hashing establishes source identity, not physical truth.

## 12. Ordering

Source order MUST be preserved unless an explicit transformation is requested.

If timestamp sorting is performed in a future layer, it MUST be recorded as a
transformation and must not silently replace original ordering evidence.

## 13. Duplicate Rows

Duplicate rows MUST NOT be silently removed.

They may be:
- preserved
- flagged
- counted

Deduplication requires explicit transformation metadata.

## 14. Integration with Sensor Quality Layer

Replay observations may be passed into the frozen Sensor Quality Layer.

Quality assessment MUST remain separate from ingestion.

Ingestion failure MUST NOT automatically become a machine anomaly.

## 15. Integration with Simulator

SIMULATED data and LOG_REPLAY data MUST remain distinguishable.

A replay file created from simulator output still uses explicit provenance
according to the source/evidence chain and MUST NOT become REAL_SENSOR.

## 16. Security and Privacy

Raw customer or proprietary industrial logs are private by default.

The ingestion layer MUST NOT publish:
- customer-identifying information
- confidential machine identifiers
- internal network details
- credentials
- proprietary plant data

without separate review and authorization.

## 17. Initial Output

An ingestion result SHOULD include:
- source_identity
- source_format
- provenance
- total_rows
- accepted_rows
- invalid_rows
- missing_rows
- duplicate_rows
- observations
- limitations
- source_hash

## 18. Acceptance Gates

Replay / Log Ingestion V0.1 PASS requires:

1. CSV ingestion is deterministic
2. JSON ingestion is deterministic
3. provenance is always LOG_REPLAY
4. raw source evidence is preserved
5. missing data is never fabricated as zero
6. malformed rows remain distinguishable
7. invalid numeric values remain distinguishable
8. non-finite values remain distinguishable
9. explicit schema mapping is required
10. source ordering is preserved
11. duplicate rows are not silently removed
12. source SHA-256 identity is preserved
13. no live-device or network access occurs
14. no control path exists
15. integration with Sensor Quality Layer preserves boundaries
16. invalid configuration fails closed
17. dedicated tests pass
18. full project regression passes
19. `git diff --check` passes

## 19. Claims Boundary

A PASS means only:

`INDUSTRIAL_REPLAY_LOG_INGESTION_V0_1 = SOFTWARE_VALIDATED`

It does NOT establish:
- real machinery validation
- diagnosis
- root cause
- causality
- failure prediction
- RUL validation
- industrial safety certification
- universal log-format compatibility

## 20. Next Gate

Only after this specification is frozen may implementation begin.

After implementation and audit, the next intended milestone is:

`INDUSTRIAL_FIRST_PROFILE_V0_1`

END OF SPECIFICATION
