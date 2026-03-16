# HealthTech Inc. – Medical Data Handling Policy

**Version:** 2.3 | **Effective Date:** January 1, 2025
**Owner:** Chief Privacy Officer (CPO) & Chief Information Security Officer (CISO)
**Classification:** RESTRICTED – Compliance & Engineering Leads
**Access Tags:** compliance-team,engineering-leads,admin
**PII Flags:** PHI

---

## 1. Purpose

This policy defines how HealthTech Inc. collects, processes, stores, transmits, and disposes
of Protected Health Information (PHI) and Personally Identifiable Information (PII) in
compliance with:
- HIPAA Privacy Rule (45 CFR Part 164, Subpart E)
- HIPAA Security Rule (45 CFR Part 164, Subpart C)
- HITECH Act
- California CMIA (Confidentiality of Medical Information Act)
- GDPR (for EU patient data)
- CCPA (for California residents)

---

## 2. Definitions

**Protected Health Information (PHI):** Individually identifiable health information held or
transmitted by a covered entity, including names, dates, geographic data, phone numbers,
email addresses, social security numbers, health plan numbers, account numbers, diagnoses,
treatment records, and any other unique identifier.

**De-identified Data:** Data from which all 18 HIPAA Safe Harbor identifiers have been removed,
or where a qualified statistician certifies re-identification risk is very small.

**Minimum Necessary Standard:** HIPAA requires that PHI access and use be limited to the minimum
necessary to accomplish the intended purpose.

---

## 3. PHI Lifecycle

### 3.1 Collection

- PHI is collected only with explicit patient consent (or as permitted by HIPAA without consent).
- Collection is limited to the minimum data elements required.
- All data collection forms must be reviewed by the Privacy team before deployment.

### 3.2 Storage

| Storage Location | Allowed? | Requirements |
|----------------|---------|-------------|
| Production AWS (us-east-1, us-west-2) | ✅ Yes | AES-256, BAA in place |
| EU AWS (eu-west-1) | ✅ Yes | AES-256, GDPR SCCs, BAA |
| Developer laptops | ❌ No | Use synthetic data only |
| Third-party SaaS (without BAA) | ❌ Never | |
| S3 public buckets | ❌ Never | |

### 3.3 Retention

| Data Type | Retention Period | Disposal Method |
|----------|----------------|----------------|
| Patient PHI | 6 years (HIPAA minimum) | Cryptographic erasure |
| Audit logs | 6 years | Cryptographic erasure |
| De-identified research data | Indefinite | N/A |
| Synthetic / test data | Dispose when no longer needed | Standard deletion |

### 3.4 Transmission

- All PHI transmission must use TLS 1.3.
- PHI must never be sent via email or Slack.
- Use the approved Secure File Transfer (SFT) system for partner data exchange.

### 3.5 Disposal

PHI must be disposed of using:
- **Digital:** AWS KMS key rotation (cryptographic erasure) + S3 object deletion.
- **Physical:** Cross-cut shredding for any printed PHI (should be rare).

---

## 4. Access Control

### 4.1 Role-Based Access

PHI access is governed by the Role-Based Access Control (RBAC) matrix maintained by the
Security team. Access must follow the Minimum Necessary Standard.

### 4.2 Row-Level Security

Production databases enforce row-level security (RLS) policies so that queries return only
records belonging to the requesting organization's tenant.

### 4.3 Privileged Access

PHI system admin access requires:
1. Approval from the CPO or delegate.
2. Just-in-time (JIT) credential issuance via HashiCorp Vault.
3. Full session recording (AWS CloudTrail + database audit).

---

## 5. Breach Notification

### 5.1 Internal Timeline

| Step | Deadline |
|------|---------|
| Discover & contain | Immediately |
| Report to Security team | ≤ 1 hour |
| Report to CPO | ≤ 4 hours |
| Preliminary assessment | ≤ 24 hours |
| HIPAA breach determination | ≤ 72 hours |

### 5.2 External Notification

| Recipient | Deadline |
|----------|---------|
| Affected individuals | ≤ 60 days |
| HHS Office for Civil Rights | ≤ 60 days (500+ affected) / Annual report (<500) |
| Media (state-specific) | ≤ 60 days if >500 residents of a state |
| EU DPA (for GDPR breaches) | ≤ 72 hours of awareness |

---

## 6. Training Requirements

All employees with PHI access must complete:
- HIPAA Basics (annual, 60 min)
- Data Classification & Handling (annual, 45 min)
- Breach Response Simulation (annual)
- Role-specific training as assigned by the Privacy team

---

## 7. Penalties for Non-Compliance

Non-compliance with this policy may result in:
- Disciplinary action (written warning → suspension → termination)
- Civil monetary penalties up to $1.9 million per HIPAA violation category
- Criminal penalties for willful neglect: up to 10 years imprisonment

---

*This policy is reviewed annually by the CPO and CISO. All exceptions require CPO sign-off.*
*Questions: privacy@healthtech.io*
