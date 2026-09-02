# E-ZERO Industrial Intelligence
## Free Read-Only Field Validation Specification V0.1

Status: PRE-REGISTERED / FIELD-VALIDATION SPECIFICATION / NOT YET AUTHORIZED

## 1. Purpose

This specification defines a controlled pathway for free real-world
read-only field validation of E-ZERO Industrial Intelligence.

The objective is to collect reproducible real-machine evidence without
granting E-ZERO any machine-control capability.

This specification does not itself authorize deployment.
Implementation and a separate safety audit are required first.

## 2. Core Boundary

The field-validation architecture MUST preserve:

READ_ONLY = TRUE
CONTROL_ALLOWED = FALSE
DIAGNOSTIC_CLAIM = FALSE
AUTONOMOUS_ACTION = FALSE

Real-machine interaction is limited to explicitly reviewed observation
and data acquisition paths.

## 3. Real-Sensor Boundary

REAL_SENSOR may become eligible only inside the separately implemented
and audited field-validation mode defined by this specification.

REAL_SENSOR evidence MUST remain distinguishable from:

- SIMULATED
- LOG_REPLAY
- MANUAL_ENTRY

No provenance class may be silently promoted to another.

## 4. Site Authorization

Before a REAL_SENSOR session begins, the user must affirm that they are
authorized by the machine/site owner or responsible operator to perform
the read-only observation.

The system must not represent this affirmation as independent proof of
ownership or legal authority.

## 5. Consent and Intended Use

Before each field-validation session, the interface must clearly state:

- E-ZERO provides read-only condition screening
- E-ZERO does not provide a confirmed diagnosis
- E-ZERO does not control the machine
- site/operator authorization is required
- outputs must not replace required safety procedures
- outputs must not be represented as certification

Acceptance must be recorded as session metadata.

## 6. No-Control Architecture

The field-validation implementation must contain no E-ZERO capability to:

- start machinery
- stop machinery
- change machine speed
- change PLC logic
- write PLC values
- change VFD parameters
- command actuators
- bypass interlocks
- clear alarms
- reset safety systems
- perform autonomous control

Where technically feasible, acquisition credentials should be
read-only and least-privilege.

Write/control credentials must not be required by the E-ZERO field
validation workflow.

## 7. Fail-Closed Requirement

If read-only status cannot be established with sufficient confidence,
REAL_SENSOR acquisition must not begin.

Unexpected writable capability, unsupported transport state, invalid
configuration, or authorization failure must fail closed.

## 8. Evidence Record

Every completed field-validation session must receive a unique session
identifier.

Evidence should preserve, where applicable:

- session identifier
- timestamp
- machine family
- sensor identities
- operating context
- provenance
- raw evidence reference
- parsed evidence
- sensor-quality state
- condition-screening state
- software/version identifier
- limitations
- evidence hash

Missing evidence must remain missing and must not be fabricated.

## 9. Evidence Integrity

Evidence records should use deterministic canonical serialization where
applicable.

Cryptographic hashes must be used to detect later evidence alteration.

A hash proves integrity relative to the hashed content.

A hash does not independently prove that a measurement was physically
correct or that the operator supplied truthful metadata.

## 10. Outcome Confirmation

Later maintenance findings may be attached as separate outcome evidence.

Outcome confirmation must preserve its source, date, and provenance.

Operator-reported or workshop-reported outcomes must not automatically
be treated as independently verified ground truth.

Screening output and later outcome evidence must remain separately
identifiable.

## 11. Sensor Quality Separation

Sensor/data quality must remain separate from machine-condition
screening.

Communication problems, missing samples, latency, invalid responses,
sensor errors, or insufficient coverage must not automatically become
machine faults.

## 12. Claims Boundary

Permitted language may include:

- observed
- measured
- screened
- anomalous pattern
- out of reference range
- sensor quality problem
- insufficient data

The field-validation system must not claim, without a separately
validated future gate:

- confirmed diagnosis
- root cause
- causality
- confirmed component failure
- failure prediction
- remaining useful life
- safety certification
- maintenance certification

## 13. Abuse Prevention

The public field-validation service must include proportionate
misuse-prevention controls.

These may include:

- account or session controls
- reasonable rate limits
- automated abuse detection
- duplicate/replay detection where appropriate
- server-side validation
- restricted acquisition interfaces
- misuse reporting

Security controls must not silently alter scientific evidence.

## 14. Rate Limiting

Rate limiting must protect service availability without changing
scientific results.

A rate-limited request must be reported as a service/access state and
must not be misclassified as:

- machine anomaly
- sensor failure
- healthy machine state

Limits should be documented and adjustable without changing frozen
scientific interpretation rules.

## 15. Privacy and Data Minimization

Only information necessary for validation, security, auditability, or
explicitly approved research should be retained.

The system should avoid unnecessary collection or long-term storage of:

- personal identifiers
- precise user location
- raw IP addresses
- confidential factory identifiers
- proprietary machine identifiers

Security telemetry and scientific evidence must remain logically
separable where practical.

Retention policy must be documented before public field deployment.

## 16. Secrets and Credentials

Evidence records, client applications, reports, and public repositories
must not contain:

- passwords
- API secrets
- write credentials
- PLC/VFD credentials
- private keys
- control tokens

Secrets required for infrastructure must remain outside public evidence
and source artifacts.

## 17. Public / Private Boundary

Public artifacts may include:

- specifications
- evidence methodology
- validation criteria
- public-safe schemas
- documented interfaces
- audit records
- appropriate demonstration data

Proprietary detection implementation may remain private.

Public claims must remain reproducible to the extent promised by the
published evidence.

## 18. Machine-Type Promotion Sequence

A new machine type must not silently inherit validation from another
machine family.

Preferred promotion sequence:

1. profile specification
2. simulated/synthetic validation
3. replay/log validation where available
4. read-only field-validation review
5. controlled REAL_SENSOR evidence collection
6. audit
7. claim review

## 19. Misuse Reporting

A public field-validation interface should provide a clear method for
reporting suspected misuse, unsafe representation, security issues, or
incorrect claims.

Reports must not automatically modify scientific evidence.

## 20. Free-Use Principle

The initial field-validation program may be provided without charge to
encourage independent real-world evidence collection.

Free access does not weaken:

- authorization requirements
- safety boundaries
- evidence requirements
- provenance requirements
- privacy requirements
- claims boundaries

## 21. Future Commercial Boundary

Future paid services may include separately reviewed value-added
features such as professional reporting, historical analysis,
organizational workflows, or extended evidence management.

Payment status must not change scientific interpretation of the same
underlying evidence.

No future commercial claim may exceed the available validation evidence.

## 22. Acceptance Gates

Implementation may pass this specification only if:

1. read-only architecture is demonstrated
2. no machine-control path exists
3. REAL_SENSOR mode is isolated from existing demo modes
4. provenance cannot silently drift
5. consent/authorization acknowledgement is recorded
6. invalid authorization fails closed
7. write/control credentials are not required
8. sensor quality remains separate from machine screening
9. missing data is not fabricated
10. session evidence receives a unique identifier
11. evidence integrity hashing is implemented
12. later outcome evidence remains separate from screening evidence
13. diagnostic claims remain disabled
14. rate limiting cannot create machine-state claims
15. privacy/data-minimization requirements are implemented
16. secrets are excluded from evidence/public artifacts
17. misuse reporting is available for public deployment
18. dedicated field-validation tests pass
19. full project regression passes
20. evidence validator passes
21. validation output is preserved as an audit artifact
22. git diff --check passes

## 23. Claims Boundary of PASS

A PASS establishes only:

EZERO_FREE_READ_ONLY_FIELD_VALIDATION_V0_1 = SOFTWARE_SAFETY_GATE_PASSED

It does not establish:

- successful real-machine validation
- diagnostic accuracy
- root-cause accuracy
- causal proof
- failure-prediction accuracy
- remaining-useful-life accuracy
- safety certification
- regulatory approval
- universal machine compatibility

Real-world scientific claims require accumulated field evidence and
separate analysis.

## 24. Next Gate

Only after this specification is frozen may implementation begin.

Implementation must receive its own regression evidence and audit before
any REAL_SENSOR field-validation deployment is authorized.

END OF SPECIFICATION
