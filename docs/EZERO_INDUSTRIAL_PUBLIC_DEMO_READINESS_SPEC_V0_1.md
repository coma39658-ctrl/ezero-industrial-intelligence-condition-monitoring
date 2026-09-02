# E-ZERO Industrial Intelligence
## Industrial Public Demo Readiness Specification V0.1

Status: PRE-REGISTERED / PUBLIC-READINESS GATE / NO RELEASE AUTHORIZATION

## 1. Purpose

This specification defines the criteria that must be satisfied before the
E-ZERO Industrial Intelligence section may be published on the public website.

Passing this gate means only that the public demo is suitable for controlled
software demonstration.

It does not establish real-machine validation or diagnostic capability.

## 2. Governing Frozen Milestones

The public demo must preserve the frozen boundaries of:

- Industrial Machinery Core V0.1
- Deterministic Industrial Simulator V0.1
- Industrial Sensor Quality Layer V0.1
- Industrial Replay / Log Ingestion V0.1
- Textile / Garment Machinery Profile V0.1
- Industrial End-to-End Demo Flow V0.1

No public UI may weaken these boundaries.

## 3. Public User Experience Principle

The default public interface must follow:

`SIMPLE_FIRST / DEPTH_ON_DEMAND`

The primary user flow should be understandable without technical training.

The default view should emphasize:
- what the system can do
- what input is being used
- what result was produced
- what limitations apply

Technical evidence may be shown in an optional expanded view.

## 4. Allowed Public Demo Inputs

Initially allowed:
- SIMULATED
- LOG_REPLAY demo data approved for public use

Not authorized:
- REAL_SENSOR
- private customer logs
- confidential factory data
- live machinery connections

## 5. Public Result States

The public interface may show:

- NORMAL
- OUT_OF_RANGE
- ANOMALOUS_PATTERN
- SENSOR_QUALITY_PROBLEM
- INSUFFICIENT_DATA

These must be explained as screening states.

The public interface must not convert them into:
- diagnosis
- root cause
- causality
- confirmed component failure
- failure prediction
- RUL
- shutdown recommendation

## 6. Provenance Visibility

Every public result must clearly preserve its input provenance.

SIMULATED must be visibly distinguishable from LOG_REPLAY.

Neither may be presented as REAL_SENSOR evidence.

## 7. Sensor Quality Visibility

Sensor quality must remain visible and separate from condition screening.

Poor-quality data must not be visually hidden behind a simple green/red
condition label.

## 8. Missing Data

Missing data and missing recommended sensors must remain explicit.

The public interface must not fabricate:
- zero values
- healthy defaults
- missing sensors
- timestamps
- units
- operating context

## 9. Plain-Language Summary

The interface should provide a short non-technical summary.

The summary must remain consistent with the structured evidence.

It must not introduce stronger claims than the underlying result.

## 10. Evidence Detail

An optional expanded evidence section should be able to show:
- profile
- provenance
- sensor quality
- condition screening
- configured sensors
- missing recommended sensors
- evidence level
- limitations
- source identity where public-safe
- software validation status

## 11. Privacy and Security

Public demo content must not expose:
- credentials
- API secrets
- private customer data
- machine serial numbers without approval
- proprietary factory logs
- internal network addresses
- PLC/VFD endpoints
- unpublished control interfaces

## 12. Public Design Requirements

The industrial page should be:
- mobile-first
- fast
- visually modern
- simple to navigate
- accessible
- responsive
- clear about system status
- clear about evidence limitations

The interface should feel advanced without using misleading technical claims.

## 13. Public Navigation

The existing E-ZERO public website should expose Industrial Intelligence
through one clear top-level entry.

The industrial area may contain its own dedicated page or section.

Detailed engineering documentation should not dominate the default user view.

## 14. Technical Detail Boundary

Public-facing simplicity must not remove scientific transparency.

The user must be able to access:
- evidence status
- provenance
- limitations
- validation scope

without requiring access to proprietary implementation details.

## 15. Acceptance Gates

Industrial Public Demo Readiness V0.1 PASS requires:

1. End-to-End Demo Flow remains frozen and passing
2. full project regression passes
3. only SIMULATED and approved LOG_REPLAY are public-demo inputs
4. REAL_SENSOR remains unauthorized
5. condition and sensor-quality dimensions remain separate
6. provenance is visible
7. missing data is not fabricated
8. missing recommended sensors are not fabricated
9. no diagnostic claim is generated
10. no RUL claim is generated
11. no live-machine path exists
12. no PLC/VFD/control path exists
13. privacy-sensitive information is excluded
14. plain-language output matches structured evidence
15. technical limitations remain accessible
16. mobile/public UX is reviewed
17. public claims are evidence-backed
18. evidence registry entry is prepared before release
19. public validation log is preserved
20. final public regression passes
21. `git diff --check` passes

## 16. Release Boundary

A PASS means only:

`INDUSTRIAL_PUBLIC_DEMO_READINESS_V0_1 = READY_FOR_CONTROLLED_PUBLIC_SOFTWARE_DEMO`

It does NOT establish:
- real industrial validation
- diagnosis
- root cause
- causality
- failure prediction
- remaining useful life validation
- safety certification
- maintenance certification
- universal industrial compatibility

## 17. Release Authorization

Passing this readiness specification does not automatically publish the site.

A separate reviewed public-release step must:
- update the evidence registry
- update the public interface
- run the evidence validator
- preserve the validation log
- verify website behavior
- freeze and tag the public release

END OF SPECIFICATION
