# E-ZERO Industrial Intelligence
## Industrial Sensor Quality Layer Specification V0.1

Status: PRE-REGISTERED / READ-ONLY DATA QUALITY LAYER / NO DIAGNOSTIC CLAIM

## 1. Purpose

This specification defines the Industrial Sensor Quality Layer V0.1 for the
E-ZERO Industrial Machinery Condition Monitoring Core.

Its purpose is to classify sensor and transport quality separately from
physical machinery condition.

A data-quality problem MUST NOT automatically become a machinery fault.

## 2. Scope

The layer evaluates quality characteristics such as:
- missing samples
- dropped samples
- packet loss
- sensor timeout
- sensor no response
- explicit sensor error
- malformed or invalid response
- insufficient sampling
- excessive latency
- unstable sampling interval
- suspicious discontinuity
- stale/repeated samples
- non-finite numeric values
- physically impossible values where profile limits exist

This layer does not perform root-cause diagnosis.

## 3. Read-Only Boundary

The layer:
- reads observations and metadata
- produces quality classifications
- preserves evidence
- performs no actuator control
- performs no PLC/VFD writes
- performs no machine-state changes
- performs no alarm reset
- performs no safety override

## 4. Provenance

The layer MUST preserve incoming provenance.

It MUST NOT convert:
- SIMULATED to REAL_SENSOR
- LOG_REPLAY to REAL_SENSOR
- MANUAL_ENTRY to REAL_SENSOR
- VIDEO_ESTIMATE to REAL_SENSOR

Quality assessment does not upgrade evidence provenance.

## 5. Canonical Quality States

V0.1 canonical quality states:

- VALID
- OUT_OF_RANGE
- SENSOR_TIMEOUT
- SENSOR_NO_RESPONSE
- SENSOR_ERROR
- INVALID_RESPONSE
- MISSING_DATA
- NOT_QUERIED
- INSUFFICIENT_SAMPLING
- SUSPECT_SIGNAL_QUALITY

No parallel synonym vocabulary should be created without a new specification.

## 6. Required Quality Metrics

Where technically available, the layer SHOULD compute:

- expected_sample_count
- observed_sample_count
- missing_sample_count
- drop_rate
- non_null_sample_count
- non_finite_sample_count
- invalid_response_count
- timeout_count
- no_response_count
- sensor_error_count
- mean_sampling_interval
- max_sampling_interval
- sampling_interval_jitter
- mean_latency_ms
- max_latency_ms
- stale_sample_count
- repeated_sample_count

Metrics MUST remain separate from machinery health interpretation.

## 7. Coverage

Coverage SHOULD be represented as:

`observed_valid_samples / expected_samples`

Coverage MUST NOT be silently treated as 100% when expected sample count is
unknown.

Unknown expected count MUST remain explicitly unknown.

## 8. Missing Data

Missing observations MUST remain missing.

They MUST NOT be:
- replaced with zero
- replaced with a healthy baseline
- forward-filled without explicit transformation provenance
- silently dropped from quality statistics

Any imputation requires a separate transformation layer and explicit metadata.

## 9. Packet Loss

Packet/sample loss MUST be recorded separately from machine condition.

Packet loss may result in:
`SUSPECT_SIGNAL_QUALITY`
or
`INSUFFICIENT_SAMPLING`

depending on frozen thresholds.

Packet loss alone MUST NOT produce:
`ANOMALOUS_PATTERN`

without separate valid machine-condition evidence.

## 10. Latency

Latency degradation MUST be represented as data/transport quality.

High latency alone MUST NOT establish:
- physical degradation
- bearing fault
- motor fault
- pressure fault
- process fault
- root cause

Latency thresholds MUST be configuration/profile data, not universal claims.

## 11. Sampling Adequacy

Sampling adequacy MUST consider:
- expected sampling rate
- observed sampling rate
- duration
- missing fraction
- jitter
- continuity

A high-frequency phenomenon MUST NOT be declared normal when sampling is too
slow to observe it reliably.

When sampling is insufficient, the preferred outcome is:
`INSUFFICIENT_SAMPLING`
with core screening:
`INSUFFICIENT_DATA`

## 12. Invalid Responses

Examples include:
- malformed payload
- impossible type
- non-numeric content where numeric data is required
- NaN
- positive/negative infinity
- structurally incomplete observation

Invalid responses MUST remain distinct from:
- timeout
- no response
- unsupported/not queried
- physical machine anomaly

## 13. Stale / Repeated Samples

Repeated identical values MAY be valid for some sensors.

The layer MUST NOT classify repetition as an error without profile/context
evidence.

Where repetition is suspicious, the state should be:
`SUSPECT_SIGNAL_QUALITY`

not a machine diagnosis.

## 14. Out-of-Range Boundary

`OUT_OF_RANGE` means a valid observation exceeded a configured reference range.

It does NOT itself prove:
- component failure
- causality
- root cause
- maintenance requirement

Reference ranges MUST be profile/configuration data.

## 15. Machine Condition Separation

The quality layer MUST expose quality results separately from machine screening.

Example:

machine_screening = `ANOMALOUS_PATTERN`
sensor_quality = `SUSPECT_SIGNAL_QUALITY`

or:

machine_screening = `NORMAL`
sensor_quality = `SENSOR_QUALITY_PROBLEM`

The two dimensions MUST NOT overwrite each other.

## 16. Mixed Evidence

If valid observations support a machinery anomaly while some samples are poor,
the system MUST preserve both:
- anomaly evidence
- quality limitation

A quality problem MUST NOT erase valid anomaly evidence.
An anomaly MUST NOT hide poor data quality.

## 17. Determinism

Given identical:
- observations
- timestamps
- expected sampling configuration
- thresholds
- provenance
- profile metadata

the quality layer MUST return identical results.

## 18. Configuration Boundary

Thresholds for:
- drop rate
- latency
- coverage
- jitter
- stale samples
- acceptable gaps
- reference ranges

MUST be explicit configuration.

They MUST NOT be presented as universal across all machines and industries.

## 19. Initial Output

A quality result SHOULD include:
- quality_state
- expected_sample_count
- observed_sample_count
- valid_sample_count
- missing_sample_count
- coverage
- drop_rate
- latency summary
- sampling summary
- affected sensors
- provenance
- limitations

## 20. Acceptance Gates

Sensor Quality Layer V0.1 PASS requires:

1. canonical quality states are implemented
2. missing data is never fabricated as zero
3. timeout and no-response remain distinct
4. invalid response remains distinct
5. packet loss remains distinct from machine anomaly
6. latency remains distinct from machine anomaly
7. insufficient sampling produces insufficient-data behavior
8. provenance is preserved
9. mixed anomaly/quality evidence preserves both dimensions
10. identical input produces identical output
11. invalid configuration fails closed
12. tests cover all canonical quality states
13. tests cover missing/packet-loss/latency boundaries
14. tests cover non-finite values
15. full project regression passes
16. `git diff --check` passes

## 21. Claims Boundary

A PASS means only:

`INDUSTRIAL_SENSOR_QUALITY_LAYER_V0_1 = SOFTWARE_VALIDATED`

It does NOT establish:
- real industrial machinery validation
- diagnosis
- root cause
- causality
- failure prediction
- RUL validation
- safety certification
- universal sensor compatibility

## 22. Next Gate

Only after this specification is frozen may implementation begin.

After implementation and audit, the next intended milestone is:

`INDUSTRIAL_REPLAY_LOG_INGESTION_V0_1`

END OF SPECIFICATION
