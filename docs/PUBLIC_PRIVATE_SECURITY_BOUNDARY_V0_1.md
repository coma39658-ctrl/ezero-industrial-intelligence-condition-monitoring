# E-ZERO Industrial Intelligence
## Public / Private Security Boundary V0.1

Status: PRE-REGISTERED SECURITY GOVERNANCE

## 1. Purpose

This document defines what may be published in the public repository and what
must remain private.

## 2. Public-Safe Content

The public repository MAY contain:
- frozen public specifications
- architecture summaries
- safety boundaries
- provenance definitions
- public interfaces
- synthetic examples
- synthetic benchmark datasets
- validation summaries
- non-sensitive tests
- public documentation
- reproducibility instructions that do not expose secrets
- public evidence logs approved for release

## 3. Private-Only Content

The following MUST remain private unless separately reviewed and approved:
- API keys
- access tokens
- passwords
- private keys
- certificates containing secrets
- customer credentials
- customer-identifying information
- raw customer industrial data
- proprietary machine logs
- confidential plant layouts
- internal network addresses
- industrial control credentials
- PLC/VFD write credentials
- safety-system credentials
- unpublished proprietary algorithms
- commercial scoring logic not approved for release
- private model parameters or decision rules
- internal security testing details that materially increase attack risk
- confidential partner or customer agreements
- non-public incident data

## 4. Data Boundary

Real industrial data MUST be treated as private by default.

Real data may become public only after:
1. ownership and sharing rights are confirmed
2. identifying information is removed
3. security-sensitive fields are removed
4. customer/partner approval is obtained where required
5. publication risk is reviewed

Synthetic data may be public if it does not reconstruct confidential real data.

## 5. Secret Handling

Secrets MUST NOT be committed to Git.

Secrets MUST be stored through:
- environment variables
- GitHub Secrets
- protected deployment secrets
- approved private secret stores

If a secret is accidentally committed:
1. revoke/rotate it immediately
2. remove it from active use
3. clean repository history where appropriate
4. record the security incident privately

Deleting a secret only from the latest commit is NOT sufficient.

## 6. Public Repository Rule

The public repository is NOT a secure secret store.

Anything committed and pushed to a public repository MUST be treated as
potentially permanently public.

`.gitignore` reduces accidental commits but does not protect files that were
already tracked or previously committed.

## 7. Private Development Layer

Proprietary or commercially sensitive implementation SHOULD live in a separate
private repository or private controlled workspace.

The public repository SHOULD expose only the minimum interfaces and evidence
needed for transparency, reproducibility and external review.

## 8. Industrial Safety Boundary

Public code MUST NOT expose or enable:
- unauthorized machine control
- PLC write operations
- VFD parameter changes
- safety-interlock bypass
- actuator control
- emergency shutdown override
- unrestricted industrial command passthrough
- credentials or endpoints for real industrial control systems

Read-only monitoring remains the default public boundary.

## 9. Review Before Publication

Before any new file is pushed publicly, review:
- secrets
- credentials
- customer data
- machine-identifying data
- network information
- proprietary implementation
- security-sensitive details
- licensing/IP restrictions

If uncertain, keep the material private.

## 10. Versioning Rule

Any weakening of this public/private boundary requires a new reviewed version.

END OF SECURITY BOUNDARY
