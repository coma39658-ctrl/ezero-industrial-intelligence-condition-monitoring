# E-ZERO Industrial Intelligence
## Textile / Garment Machinery Profile Specification V0.1

Status: PRE-REGISTERED / PROFILE CONFIGURATION ONLY / NO DIAGNOSTIC CLAIM

## 1. Purpose

This specification defines the first industry-specific profile for the
E-ZERO Industrial Machinery Condition Monitoring Core V0.1.

Initial intended machinery families include:
- textile production machinery
- garment production machinery
- embroidery machines
- sewing machines
- spinning machinery
- weaving machinery
- looms
- winding machinery
- knitting machinery
- finishing/process machinery
- electric motors
- bearings
- spindles
- gearboxes
- fans and blowers
- pumps
- conveyors

This profile provides machine-context metadata and screening configuration.

It does NOT establish universal compatibility with every textile or garment
machine.

## 2. Governing Core

This profile MUST preserve the frozen boundaries of:
- Industrial Machinery Core V0.1
- Deterministic Industrial Simulator V0.1
- Industrial Sensor Quality Layer V0.1
- Industrial Replay / Log Ingestion V0.1

The profile MUST NOT weaken provenance, safety, quality, or evidence rules.

## 3. Read-Only Boundary

This profile is read-only.

It MUST NOT:
- start or stop machinery
- change machine speed
- change motor or spindle control
- write PLC logic
- change VFD parameters
- activate actuators
- bypass interlocks
- reset safety alarms
- issue maintenance-control commands
- perform autonomous control

## 4. Claims Boundary

This V0.1 profile supports condition screening only.

It does NOT establish:
- root-cause diagnosis
- component failure certainty
- causality
- remaining useful life
- maintenance certification
- safety certification
- shutdown authority
- OEM replacement
- universal textile-machine compatibility

## 5. Initial Sensor Families

This profile MAY use, where available:
- vibration
- temperature
- rpm or rotational speed
- motor current
- voltage
- power
- load
- pressure
- flow
- acoustic level
- bearing temperature
- spindle temperature
- ambient temperature
- humidity

Not every machine requires every sensor.

Missing sensors MUST NOT be fabricated.

## 6. Operating Contexts

Initial textile/garment contexts MAY include:
- OFF
- STARTUP
- IDLE
- THREADING_SETUP
- LOW_SPEED
- NORMAL_PRODUCTION
- HIGH_SPEED
- HIGH_LOAD
- TRANSIENT
- CHANGEOVER
- SHUTDOWN
- MAINTENANCE_TEST
- UNKNOWN_CONTEXT

Context MUST be preserved where known.

Changes caused by valid operating context MUST NOT automatically become
machine-fault indications.

## 7. Machine Families

Initial profile families include:

### 7.1 Rotating Drive Systems
Examples:
- electric motors
- bearings
- shafts
- couplings
- pulleys
- gearboxes

Relevant screening signals may include:
- vibration
- temperature
- rpm
- current
- power
- load

### 7.2 Spinning and Winding Systems
Examples:
- spindles
- winding heads
- rollers
- drive motors

Relevant signals may include:
- vibration
- spindle speed
- temperature
- current
- load

### 7.3 Weaving / Loom Systems
Examples:
- loom drive
- shafts
- bearings
- rollers
- fans

Relevant signals may include:
- vibration
- rpm
- temperature
- current
- power

### 7.4 Knitting Systems
Relevant signals may include:
- rpm
- vibration
- temperature
- current
- load

### 7.5 Sewing / Garment Production Machinery
Relevant signals may include:
- motor current
- speed
- vibration
- temperature
- power

### 7.6 Embroidery Machines
Relevant signals may include:
- spindle/needle drive speed
- vibration
- motor current
- temperature
- load

This profile does NOT claim that one signal uniquely identifies one component
fault.

## 8. Screening States

The profile MUST use the frozen core screening states:

- NORMAL
- OUT_OF_RANGE
- ANOMALOUS_PATTERN
- SENSOR_QUALITY_PROBLEM
- INSUFFICIENT_DATA

No profile-specific synonym may silently change these meanings.

## 9. Sensor Quality Boundary

The frozen Industrial Sensor Quality Layer remains authoritative for:
- missing samples
- dropped samples
- latency
- timeout
- no response
- sensor error
- invalid response
- non-finite values
- insufficient sampling
- suspect signal quality

A sensor-quality problem MUST NOT automatically become a textile machinery
fault indication.

## 10. Provenance Boundary

The profile MUST preserve provenance exactly.

Initial supported provenance categories include:
- SIMULATED
- LOG_REPLAY
- MANUAL_ENTRY
- VIDEO_ESTIMATE
- REAL_SENSOR

SIMULATED or LOG_REPLAY evidence MUST NOT be silently promoted to REAL_SENSOR.

## 11. Evidence Levels

The profile MUST use the frozen industrial evidence ladder:

- L1 MEASURED
- L2 REFERENCE_SCREENED
- L3 PATTERN_SUPPORTED
- L4 MULTISENSOR_SUPPORTED
- L5 MAINTENANCE_CONFIRMED
- L6 INDEPENDENTLY_VALIDATED

A profile configuration alone cannot raise an evidence level.


## 12. Profile Configuration Rules

Machine-specific configuration MUST be explicit.

Configuration MAY include:
- machine_family
- machine_model
- sensor list
- sensor units
- expected sampling rate
- reference ranges
- operating contexts
- machine speed/load bands
- sensor-quality thresholds

Unknown values MUST remain unknown.

No configuration field may be silently guessed.

## 13. Reference Range Rules

Reference ranges MUST be treated as configuration data.

They MUST NOT be presented as universal limits across all:
- textile machines
- garment machines
- embroidery machines
- motors
- bearings
- spindles
- OEMs
- operating environments

Where OEM or maintenance documentation exists, provenance of the reference
range SHOULD be preserved.

An OUT_OF_RANGE result is screening evidence only.

## 14. Multisensor Interpretation Boundary

A coordinated pattern across multiple valid sensors MAY support:

`ANOMALOUS_PATTERN`

or a higher evidence level when independently supported.

However, multisensor agreement does NOT automatically establish:
- root cause
- component identity
- causality
- imminent failure
- required shutdown

## 15. Mixed Quality / Condition Evidence

The system MUST preserve machine-condition and data-quality dimensions
separately.

Example:

machine_screening = `ANOMALOUS_PATTERN`
sensor_quality = `SUSPECT_SIGNAL_QUALITY`

A quality limitation MUST NOT erase valid anomaly evidence.

An anomaly indication MUST NOT hide poor sensor quality.

## 16. Initial Profile Use

This V0.1 profile MAY be used with:
- SIMULATED data
- LOG_REPLAY data
- explicitly reviewed MANUAL_ENTRY data
- VIDEO_ESTIMATE data where limitations are preserved

REAL_SENSOR use requires a separately reviewed real-data step.

## 17. Security / Privacy Boundary

Customer or factory data is private by default.

Public profile code or documentation MUST NOT expose:
- factory-identifying information
- customer names
- machine serial numbers unless explicitly approved
- internal network details
- PLC/VFD credentials
- proprietary maintenance data
- confidential production data

## 18. Acceptance Gates

Textile / Garment Machinery Profile V0.1 PASS requires:

1. profile preserves all frozen core safety boundaries
2. profile remains read-only
3. no actuator or control path exists
4. no PLC/VFD write path exists
5. canonical screening states are unchanged
6. canonical quality states are unchanged
7. provenance is preserved
8. SIMULATED and LOG_REPLAY cannot become REAL_SENSOR
9. evidence ladder is preserved
10. reference ranges are explicit configuration
11. machine-family mappings are deterministic
12. missing sensors are not fabricated
13. operating context is preserved
14. sensor-quality problems remain distinct from machine anomalies
15. mixed quality/condition evidence preserves both dimensions
16. invalid configuration fails closed
17. dedicated profile tests pass
18. full project regression passes
19. `git diff --check` passes

## 19. Claims Boundary

A PASS means only:

`TEXTILE_GARMENT_MACHINERY_PROFILE_V0_1 = SOFTWARE_VALIDATED`

It does NOT establish:
- real textile factory validation
- real garment factory validation
- diagnosis
- root cause
- causality
- failure prediction
- remaining useful life validation
- safety certification
- maintenance certification
- universal machine compatibility

## 20. Next Gate

Only after this specification is frozen may implementation begin.

After implementation and audit, the next intended milestone is:

`INDUSTRIAL_END_TO_END_DEMO_FLOW_V0_1`

This future demo flow must remain non-diagnostic and evidence-preserving.

END OF SPECIFICATION
