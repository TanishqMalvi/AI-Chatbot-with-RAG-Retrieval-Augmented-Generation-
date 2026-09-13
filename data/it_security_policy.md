
# IT Security Policy

**Classification:** CONFIDENTIAL | **Owner:** CISO

## Access Control
- Principle of least privilege: grant minimum access needed.
- Admin access requires VP approval and quarterly recertification.
- Multi-factor authentication (MFA) required for all production systems.
- Password policy: ≥ 14 characters, rotated every 90 days, no reuse of last 12 passwords.

## Endpoint Security
- Company-issued devices only for PHI access.
- Disk encryption required (BitLocker/FileVault).
- EDR agent installed and kept up to date.
- USB storage disabled unless approved by security team.

## Network Security
- VPN required for remote access to internal systems.
- Segmentation: dev, staging, and production networks are isolated.
- Firewall rules reviewed quarterly.

## Vulnerability Management
- Critical CVEs patched within 7 days.
- High CVEs patched within 30 days.
- Dependency scanning in CI; ban critical/high severity in production images.

## Incident Reporting
- Report suspected incidents to security@healthtech.io within 1 hour.
- Do not attempt to investigate or remediate independently if PHI may be involved.
- Preserve evidence; do not power off systems unless instructed.

## Backup & Recovery
- Daily automated backups with 30-day retention.
- Quarterly restore tests required.
- RPO: 4 hours; RTO: 8 hours for Tier 1 systems.
