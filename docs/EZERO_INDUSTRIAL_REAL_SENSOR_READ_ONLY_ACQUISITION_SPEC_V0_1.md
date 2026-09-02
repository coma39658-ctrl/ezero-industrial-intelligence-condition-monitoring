# E-ZERO Industrial Intelligence
## Real-Sensor Read-Only Acquisition / Integration Specification V0.1

Status: PRE-REGISTERED / READ-ONLY ACQUISITION SPECIFICATION / NO LIVE DEPLOYMENT AUTHORIZATION

## 1. Purpose

This specification defines the safety and evidence requirements for future
read-only acquisition of real industrial sensor data.

The purpose is to allow controlled REAL_SENSOR evidence collection without
granting E-ZERO any machine-control capability.

This specification does not itself authorize live machine connection.

## 2. Governing Boundaries

The implementation MUST preserve:

READ_ONLY = TRUE
CONTROL_ALLOWED = FALSE
DIAGNOSTIC_CLAIM = FALSE
AUTONOMOUS_ACTION = FALSE

No acquisition path may weaken these boundaries.

## 3. REAL_SENSOR Provenance

REAL_SENSOR may be assigned only when:

- data originates from an actual physical sensor or approved machine telemetry source
- the acquisition path has been separately reviewed
- session authorization is valid
- source identity is preserved
- no provenance conversion occurs

SIMULATED, LOG_REPLAY, MANUAL_ENTRY, or VIDEO_ESTIMATE must never become
REAL_SENSOR.

## 4. Supported Acquisition Classes

Future adapters may support explicitly reviewed read-only sources such as:

- dedicated external sensors
- approved data-loggers
- read-only machine telemetry APIs
- read-only OPC UA variables
- read-only MQTT telemetry
- read-only serial/USB sensor streams
- read-only network telemetry endpoints

Each transport or protocol requires its own reviewed adapter or profile.

## 5. No Automatic Discovery

The acquisition layer MUST NOT:

- scan industrial networks automatically
- enumerate arbitrary PLCs
- probe unknown control endpoints
- auto-select first responding device
- auto-connect to unreviewed endpoints
- perform background device discovery

Endpoints and sources must be explicitly configured.

## 6. No-Control Requirement

The system MUST NOT:

- write PLC variables
- modify PLC logic
- write VFD parameters
- start or stop machinery
- change speed or load
- operate actuators
- bypass interlocks
- acknowledge or clear safety alarms
- reset safety systems
- issue maintenance-control commands
- perform autonomous control

## 7. Credential Boundary

Where credentials are required, the implementation should use
least-privilege read-only credentials.

The E-ZERO acquisition workflow MUST NOT require write/control credentials.

Credentials must not be stored in:

- evidence records
- public repositories
- public reports
- validation logs

## 8. Explicit Source Configuration

Every acquisition session must explicitly identify:

- source type
- endpoint or device identity
- sensor identity
- machine family
- expected units where known
- operating context
- session authorization

No hidden fallback source may be selected.

## 9. Session Authorization

Before acquisition begins:

- site/operator authorization must be recorded
- consent must be accepted
- acquisition mode must be explicitly read-only
- source configuration must pass validation

Failure of any gate must block acquisition.

## 10. Fail-Closed Behavior

Acquisition must fail closed when:

- endpoint configuration is invalid
- authorization is missing
- read-only status cannot be established
- unexpected write capability is required
- protocol behavior is outside the reviewed profile
- source identity changes unexpectedly
- data structure is unsupported

## 11. Sensor Quality Separation

Communication and sensor-quality problems must remain separate from
machine-condition screening.

Examples include:

- timeout
- no response
- invalid response
- missing samples
- excessive latency
- non-finite values
- insufficient coverage
- suspect signal quality

These states must not automatically become machine faults.

## 12. Missing Data

Missing values must remain missing.

The acquisition layer MUST NOT fabricate:

- zeros
- healthy defaults
- timestamps
- units
- sensor identities
- operating context

## 13. Raw Evidence Preservation

Where technically possible, preserve:

- raw received payload
- acquisition timestamp
- source identity
- transport/protocol metadata
- parsed observation
- parse status
- sensor quality
- source hash

Raw evidence must remain distinguishable from parsed evidence.

## 14. Evidence Integrity

Raw source evidence should receive a cryptographic hash.

Structured evidence should receive a separate canonical evidence hash.

Hashing establishes integrity relative to the hashed content.

It does not independently prove sensor correctness or physical truth.

## 15. Source Identity

Source identity must be stable within a session.

Unexpected endpoint, device, topic, node, or sensor identity changes must
fail closed or create an explicit new reviewed session.

## 16. Data Minimization

Only data necessary for scientific validation, safety, auditability, or
approved research should be retained.

Avoid unnecessary retention of:

- personal identifiers
- raw IP addresses
- confidential factory names
- proprietary machine identifiers
- unrelated telemetry

## 17. Public / Private Boundary

REAL_SENSOR evidence collected in field validation must not automatically
become public.

Publication requires separate approval and privacy review.

Public demonstration may continue to use SIMULATED and approved LOG_REPLAY
even when REAL_SENSOR evidence exists privately.

## 18. Rate and Load Safety

Acquisition frequency must be bounded.

The implementation must not create excessive polling or traffic that could
degrade machine, controller, gateway, or network performance.

Rate limiting or sampling limits must not be interpreted as machine-state
evidence.

## 19. Determinism

For stored raw evidence, replaying the same bytes through the same frozen
parser and configuration should produce identical parsed output.

Live sensor values themselves are not expected to repeat identically.

## 20. Claims Boundary

REAL_SENSOR acquisition alone does not establish:

- diagnosis
- root cause
- causality
- confirmed component failure
- failure prediction
- remaining useful life
- maintenance certification
- safety certification

It establishes only measured field evidence under the reviewed acquisition
conditions.

## 21. Acceptance Gates

Implementation may pass this specification only if:

1. read-only acquisition architecture is demonstrated
2. no control/write path exists
3. explicit source configuration is required
4. no automatic discovery exists
5. authorization and consent are required
6. invalid authorization fails closed
7. write/control credentials are not required
8. REAL_SENSOR provenance cannot be forged from SIMULATED or LOG_REPLAY
9. source identity is preserved
10. missing data is not fabricated
11. raw and parsed evidence remain distinct
12. source hash is preserved
13. evidence hash is preserved separately
14. sensor-quality states remain separate from machine screening
15. acquisition rate is bounded
16. privacy/data-minimization controls are documented
17. dedicated acquisition tests pass
18. full project regression passes
19. git diff --check passes
20. no live deployment occurs during software-only validation

## 22. Claims Boundary of PASS

A software-only PASS establishes only:

`INDUSTRIAL_REAL_SENSOR_READ_ONLY_ACQUISITION_V0_1 = SOFTWARE_VALIDATED`

It does NOT establish:

- successful physical sensor connection
- successful industrial network integration
- real machine validation
- diagnostic accuracy
- safety certification
- regulatory approval
- universal protocol compatibility

## 23. Next Gate

Only after this specification is frozen may implementation begin.

After software implementation and audit, a separate controlled physical
acquisition bench-validation gate is required before live industrial use.

END OF SPECIFICATION
