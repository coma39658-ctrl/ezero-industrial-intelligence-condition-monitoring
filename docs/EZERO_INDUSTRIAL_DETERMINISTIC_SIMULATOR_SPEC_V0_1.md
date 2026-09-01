# E-ZERO Industrial Intelligence
## Deterministic Industrial Simulator Specification V0.1

Status: PRE-REGISTERED / SIMULATED DATA ONLY / NO DIAGNOSTIC CLAIM

## 1. Purpose

This specification defines a deterministic simulator for the
E-ZERO Industrial Machinery Condition Monitoring Core V0.1.

The simulator exists to validate software behavior before using real
industrial machinery data.

A simulator PASS does NOT establish real industrial validation.

## 2. Provenance

All simulator outputs MUST use:

`SIMULATED`

Simulator data MUST NOT be promoted to:
- REAL_SENSOR
- maintenance-confirmed evidence
- independently validated evidence

## 3. Safety Boundary

The simulator is read-only software.

It MUST NOT:
- connect to real machinery
- connect to PLCs
- connect to VFDs
- control actuators
- change machine state
- issue industrial control commands
- claim physical diagnosis

## 4. Determinism

For a fixed:
- scenario
- seed
- sample count
- sampling rate
- machine profile
- sensor configuration

the simulator MUST produce identical output.

Each generated case MUST preserve:
- scenario_id
- seed
- timestamp or deterministic sample index
- provenance
- operating context
- sensor-quality state
- screening ground truth
- raw simulated values

## 5. Initial Sensor Set

The simulator MUST initially support:
- vibration
- temperature
- rpm
- motor_current
- voltage
- power
- pressure
- flow
- load

A scenario MAY use only a relevant subset.

Unused sensors MUST NOT be fabricated as meaningful machine evidence.

## 6. Operating Contexts

Initial contexts:
- OFF
- STARTUP
- IDLE
- LOW_LOAD
- NORMAL_LOAD
- HIGH_LOAD
- TRANSIENT
- SHUTDOWN
- UNKNOWN_CONTEXT

## 7. Core Machine-Condition Scenarios

The initial deterministic scenario suite MUST include:

### A — HEALTHY_STABLE
Stable sensor behavior within configured reference expectations.

Expected screening:
`NORMAL`

### B — REFERENCE_RANGE_DEVIATION
One or more valid sensor values move outside configured reference range.

Expected screening:
`OUT_OF_RANGE`

### C — MULTISENSOR_ANOMALOUS_PATTERN
A coordinated change occurs across multiple valid sensors.

Example:
- vibration increase
- bearing/process temperature increase
- current or load pattern change

Expected screening:
`ANOMALOUS_PATTERN`

This does NOT establish root cause.

### D — TRANSIENT_NONFAULT_EVENT
A short operating transient occurs without persistent abnormal condition.

The simulator MUST allow testing whether transient behavior is incorrectly
classified as persistent machinery degradation.

### E — LOAD_CONTEXT_SHIFT
Sensor values change because operating load changes.

The simulator MUST preserve the changed operating context so that valid
load-related changes are not automatically treated as faults.

## 8. Sensor / Communication Quality Scenarios

These scenarios MUST remain separate from machine-condition scenarios.

### F — SENSOR_TIMEOUT
Expected quality state:
`SENSOR_TIMEOUT`

Expected core screening:
`SENSOR_QUALITY_PROBLEM`

### G — SENSOR_NO_RESPONSE
Expected quality state:
`SENSOR_NO_RESPONSE`

Expected core screening:
`SENSOR_QUALITY_PROBLEM`

### H — INVALID_RESPONSE
Malformed or physically invalid sensor response.

Expected quality state:
`INVALID_RESPONSE`

Expected core screening:
`SENSOR_QUALITY_PROBLEM`

### I — MISSING_DATA
Samples are absent.

Expected quality state:
`MISSING_DATA`

Expected core screening:
`SENSOR_QUALITY_PROBLEM` or `INSUFFICIENT_DATA`, according to frozen
coverage criteria.

### J — INSUFFICIENT_SAMPLING
Sampling density is below the minimum required for reliable screening.

Expected quality state:
`INSUFFICIENT_SAMPLING`

Expected core screening:
`INSUFFICIENT_DATA`

### K — INTERMITTENT_PACKET_LOSS
Deterministic sample drops are introduced.

The simulator MUST preserve:
- expected sample count
- observed sample count
- dropped sample count
- drop rate

Packet loss MUST NOT itself become:
`ANOMALOUS_PATTERN`

unless separate valid machine evidence also supports that state.

### L — LATENCY_DEGRADATION
Deterministic timing delays are introduced.

Latency degradation MUST be reported as data/transport quality evidence,
not as physical machinery degradation.

### M — SENSOR_ERROR
Explicit sensor-error state.

Expected quality state:
`SENSOR_ERROR`

Expected core screening:
`SENSOR_QUALITY_PROBLEM`

## 9. Mixed Scenarios

The simulator MUST also support mixed cases where both:
- a real simulated machine-condition change
and
- a sensor-quality problem

occur together.

The result MUST preserve both dimensions separately.

Example:
machine screening = `ANOMALOUS_PATTERN`
sensor quality = `SUSPECT_SIGNAL_QUALITY`

The quality issue MUST NOT erase valid evidence, and valid anomaly evidence
MUST NOT hide the quality issue.

## 10. Ground Truth

Every simulated case MUST preserve explicit ground truth for:
- machine condition class
- sensor-quality class
- operating context
- injected change point where applicable
- affected sensors
- provenance

Ground truth is simulator truth only.
It is not physical-world proof.

## 11. Reference Ranges

Reference ranges MUST be profile/configuration data.

They MUST NOT be presented as universal limits for all machines.

Machine-specific or industry-specific limits require separate profiles and
supporting evidence.

## 12. Initial Output Schema

Each simulated observation SHOULD include:
- case_id
- scenario_id
- seed
- sample_index
- sensor_name
- raw_value
- unit
- operating_context
- sensor_quality_state
- machine_ground_truth
- expected_screening_state
- provenance

Case-level metadata SHOULD include:
- sample_count
- sampling_rate_hz
- change_point
- affected_sensors
- dropped_samples
- latency_metadata

## 13. Acceptance Gates

Simulator V0.1 PASS requires:

1. all defined scenarios are implemented
2. fixed seeds reproduce identical outputs
3. provenance is always SIMULATED
4. no real-device or network access occurs
5. no machinery-control path exists
6. missing data is never fabricated as zero
7. sensor-quality failures remain distinct from machine anomalies
8. operating-context changes are preserved
9. mixed condition/quality cases preserve both dimensions
10. deterministic ground truth is preserved
11. tests cover scenarios A through M
12. tests cover repeatability
13. tests cover invalid configuration rejection
14. full project test suite passes
15. `git diff --check` passes

## 14. Claims Boundary

A simulator PASS means only:

`DETERMINISTIC_INDUSTRIAL_SIMULATOR_V0_1 = SOFTWARE_VALIDATED`

It does NOT mean:
- real machinery validation
- diagnosis
- root-cause proof
- causality
- failure prediction
- remaining useful life validation
- industrial safety certification
- universal machine compatibility

## 15. Next Gate

Only after this simulator specification is frozen may implementation begin.

After simulator implementation and audit, the next intended milestone is:

`INDUSTRIAL_SENSOR_QUALITY_LAYER_V0_1`

END OF SPECIFICATION
