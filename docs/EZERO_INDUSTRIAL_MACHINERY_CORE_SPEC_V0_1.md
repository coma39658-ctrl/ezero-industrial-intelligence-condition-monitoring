# E-ZERO Industrial Machinery Condition Monitoring Core V0.1

Status: PRE-REGISTERED / READ-ONLY CONDITION SCREENING / NO DIAGNOSTIC CLAIM

## 1. Purpose

E-ZERO Industrial Machinery Core V0.1 defines a vendor-neutral, read-only
condition-screening foundation for industrial machinery.

Initial intended sectors include:
- textile factories
- garment factories
- embroidery machinery
- spinning, weaving and processing machinery
- cement plants
- fertilizer plants
- oil refineries
- oil and gas operations
- rice mills
- edible-oil / ghee processing plants
- pumps
- compressors
- electric motors
- bearings
- spindles
- fans and blowers
- gearboxes
- conveyors
- rotating machinery
- other industrial and heavy machinery

This V0.1 does not claim universal compatibility with every machine or industry.

## 2. Core Principle

The system observes and screens measured condition data.

It MUST distinguish:
- measurement
- reference-range screening
- anomaly indication
- statistical evidence
- diagnosis
- causality
- physical proof

An anomaly is not automatically a fault diagnosis.
A correlation is not automatically causality.
A screening result is not automatically root-cause proof.

## 3. Read-Only Boundary

V0.1 is read-only.

It MUST NOT:
- start or stop machinery
- change speed or load
- alter PLC logic
- write to controllers
- change VFD parameters
- open or close valves
- activate actuators
- reset alarms
- clear fault history
- bypass interlocks
- override safety systems
- perform autonomous control
- issue maintenance-control commands

Any future control or actuation capability requires a separate reviewed
specification and explicit safety gate.

## 4. Initial Sensor Families

The core may accept, where available:
- vibration
- temperature
- RPM / rotational speed
- shaft speed
- motor current
- voltage
- electrical power
- pressure
- flow
- torque
- acoustic signal
- oil temperature
- oil pressure
- bearing temperature
- process temperature
- humidity
- load
- machine-state metadata

Not every machine is expected to provide every sensor.

Missing sensor data MUST NOT be fabricated as zero.

## 5. Provenance

Every observation MUST preserve provenance.

Initial provenance categories:
- REAL_SENSOR
- SIMULATED
- LOG_REPLAY
- MANUAL_ENTRY
- VIDEO_ESTIMATE

SIMULATED, LOG_REPLAY, MANUAL_ENTRY or VIDEO_ESTIMATE data MUST NOT be
silently promoted to REAL_SENSOR.

## 6. Sensor / Data Quality States

At minimum, the system MUST distinguish:
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

Transport or sensor-quality problems MUST NOT automatically become machinery
fault indications.

## 7. Core Screening Outputs

V0.1 outputs are limited to:
- NORMAL
- OUT_OF_RANGE
- ANOMALOUS_PATTERN
- SENSOR_QUALITY_PROBLEM
- INSUFFICIENT_DATA

These are screening states, not root-cause diagnoses.

## 8. Operating Context

Where available, observations SHOULD preserve operating context such as:
- OFF
- STARTUP
- IDLE
- LOW_LOAD
- NORMAL_LOAD
- HIGH_LOAD
- TRANSIENT
- SHUTDOWN
- UNKNOWN_CONTEXT

Machine-specific context may be added by later profiles.

## 9. Evidence Levels

Initial evidence ladder:
- L1 MEASURED
- L2 REFERENCE_SCREENED
- L3 PATTERN_SUPPORTED
- L4 MULTISENSOR_SUPPORTED
- L5 MAINTENANCE_CONFIRMED
- L6 INDEPENDENTLY_VALIDATED

No higher evidence level may be claimed without its required supporting
evidence.

## 10. Industry Profiles

The shared core MUST remain industry-neutral.

Industry-specific behavior will be defined through separate profiles, for
example:
- TEXTILE_GARMENT_PROFILE
- EMBROIDERY_MACHINE_PROFILE
- CEMENT_PLANT_PROFILE
- FERTILIZER_PLANT_PROFILE
- OIL_GAS_PROFILE
- REFINERY_PROFILE
- RICE_MILL_PROFILE
- EDIBLE_OIL_GHEE_PROFILE
- ROTATING_MACHINERY_PROFILE

A profile MUST NOT weaken core evidence, provenance or safety boundaries.

## 11. Transport and Sensor Quality Boundary

Latency, dropped samples, packet loss, intermittent sensors, communication
timeouts and malformed data MUST be classified separately from machine
condition.

The system MUST avoid treating communication-quality degradation as physical
machinery degradation without additional evidence.

## 12. Diagnostics Boundary

V0.1 does NOT establish:
- root cause
- component failure certainty
- causality
- remaining useful life
- safety certification
- maintenance certification
- regulatory compliance
- shutdown authority
- autonomous maintenance decisions

These require separate future validation gates.

## 13. Development Sequence

The intended sequence is:

1. freeze this Core V0.1 specification
2. build deterministic simulator
3. build sensor-quality layer
4. build replay/log ingestion
5. create synthetic benchmark datasets
6. validate screening outputs
7. create first industry profile
8. test real non-critical sensor logs
9. obtain maintenance-confirmed datasets
10. perform preregistered validation
11. only then evaluate diagnostic or predictive extensions

No step may silently convert synthetic evidence into real industrial proof.

## 14. Initial Commercial Boundary

V0.1 may be presented as:
- read-only condition screening
- evidence-preserving sensor analysis
- industrial anomaly screening
- research and development tooling

It MUST NOT be presented as:
- certified machinery diagnosis
- guaranteed failure prediction
- universal predictive maintenance
- safety-critical shutdown system
- replacement for OEM/PLC protection systems
- independently validated industrial diagnosis

## 15. Versioning Rule

Any change to safety boundaries, provenance, output semantics, evidence levels,
diagnostic claims, control authority, or validation criteria requires a new
specification version.

END OF SPECIFICATION
