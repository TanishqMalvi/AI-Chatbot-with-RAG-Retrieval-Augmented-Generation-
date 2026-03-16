# HealthTech Inc. – IT Security Policy

**Version:** 4.1 | **Effective Date:** February 1, 2025
**Owner:** Chief Information Security Officer (CISO)
**Classification:** Internal – All Employees
**Access Tags:** all-employees

---

## 1. Purpose & Scope

This policy establishes the minimum security requirements for all HealthTech employees,
contractors, and systems that store, process, or transmit company or patient data.
Non-compliance may result in disciplinary action up to and including termination.

---

## 2. Acceptable Use of Company Systems

### 2.1 Authorized Use
Company systems (laptops, cloud accounts, SaaS tools) may only be used for legitimate
business purposes. Incidental personal use is permitted provided it does not:
- Consume significant bandwidth or storage
- Expose company systems to malware or unauthorized access
- Violate this policy or any applicable law

### 2.2 Prohibited Activities
- Installing unauthorized software without IT approval
- Circumventing security controls (VPN bypass, MFA disablement)
- Sharing login credentials with any person, including colleagues
- Connecting to public Wi-Fi without the company VPN active
- Accessing, copying, or transmitting patient data outside approved systems

---

## 3. Access Control

### 3.1 Principle of Least Privilege
All access grants follow the principle of least privilege. Employees receive only the minimum
access required for their role. Access is reviewed quarterly by team leads.

### 3.2 Authentication Requirements
- All systems: Multi-Factor Authentication (MFA) required.
- Preferred MFA: Hardware security key (YubiKey 5 Series).
- Acceptable MFA: TOTP app (Google Authenticator, Authy).
- SMS OTP is **not** acceptable for any system handling PHI.

### 3.3 Password Policy
- Minimum 16 characters; managed via 1Password.
- Passwords must be unique per service (no reuse).
- Rotation required only upon suspected compromise.

### 3.4 Privileged Access
- Production root/admin access requires just-in-time (JIT) approval via HashiCorp Vault.
- All privileged sessions are logged and reviewed weekly by the Security team.

---

## 4. Data Classification

| Class | Examples | Controls |
|-------|---------|---------|
| **Public** | Marketing materials, press releases | No restriction |
| **Internal** | This policy, product roadmaps | Authenticated access only |
| **Confidential** | Source code, financial data, contracts | Need-to-know + encryption |
| **Restricted (PHI/PII)** | Patient records, salary data | Strict ACL + audit log + encryption |

---

## 5. Encryption Standards

| Context | Requirement |
|---------|------------|
| Data at rest | AES-256-GCM |
| Data in transit | TLS 1.3 (TLS 1.2 minimum) |
| Secrets management | HashiCorp Vault or AWS KMS |
| Laptop disk | FileVault (macOS) / BitLocker (Windows) |

No sensitive data may be stored in unencrypted form on any device or service.

---

## 6. Incident Response

### 6.1 What to Report
- Lost or stolen devices
- Suspected phishing or social engineering
- Unauthorized system access
- Data breach or exposure of PHI/PII

### 6.2 How to Report
1. Email security@healthtech.io with subject: **SECURITY INCIDENT – [brief description]**
2. Call the 24/7 Security Hotline: 1-888-SEC-HTEC
3. For active intrusions: immediately disconnect from the network and call the hotline.

**Report within 1 hour of discovery.** HIPAA Breach Notification Rule requires HealthTech to
notify affected patients within 60 days; internal reporting SLA is 1 hour.

### 6.3 Response Timelines

| Severity | Initial Response | Containment Target |
|---------|----------------|-------------------|
| Critical | 15 minutes | 1 hour |
| High | 30 minutes | 4 hours |
| Medium | 2 hours | 24 hours |
| Low | 1 business day | 5 business days |

---

## 7. Third-Party Vendor Security

All vendors with access to company systems or data must:
1. Complete a security questionnaire (CAIQ or SIG Lite).
2. Maintain SOC 2 Type II certification (or equivalent).
3. Sign a Data Processing Agreement (DPA) before access is granted.
4. Undergo annual re-assessment.

---

## 8. Compliance References

- HIPAA Security Rule (45 CFR Part 164)
- NIST Cybersecurity Framework 2.0
- SOC 2 Trust Service Criteria
- GDPR Article 32 (Security of Processing)
- California CMIA (Confidentiality of Medical Information Act)

---

*Violations of this policy should be reported to security@healthtech.io or the anonymous
Ethics Hotline: 1-800-ETHICS-1.*

*This policy is reviewed and updated annually or after any material security incident.*
