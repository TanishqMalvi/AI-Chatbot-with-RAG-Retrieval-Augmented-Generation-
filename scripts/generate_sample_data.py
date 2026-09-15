#!/usr/bin/env python3
"""
Generate large-scale sample data for the HealthTech RAG Assistant.

Creates comprehensive Markdown documents across multiple domains so the
chatbot can answer a wide range of employee and clinical questions.
"""

from __future__ import annotations

import random
import textwrap
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DATA_DIR.mkdir(exist_ok=True)


def write_markdown(filename: str, content: str) -> None:
    path = DATA_DIR / filename
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path} ({len(content)} chars)")


# ---------------------------------------------------------------------------
# 1. Diabetes management
# ---------------------------------------------------------------------------
diabetes_sections = [
    (
        "Overview",
        textwrap.dedent("""
        Diabetes mellitus is a chronic metabolic disease characterized by elevated blood glucose
        levels. It affects more than 500 million adults worldwide and is a major focus of
        HealthTech Inc.'s clinical knowledge base.

        ### Types
        - **Type 1:** Autoimmune destruction of pancreatic beta cells; requires insulin.
        - **Type 2:** Insulin resistance and progressive beta-cell dysfunction; lifestyle and oral agents.
        - **Gestational:** Hyperglycemia first recognized during pregnancy.
        - **MODY:** Monogenic diabetes caused by single-gene mutations.
        """),
    ),
    (
        "Diagnosis",
        textwrap.dedent("""
        ### Laboratory Criteria (ADA 2025)
        - Fasting plasma glucose ≥ 126 mg/dL
        - 2-hour plasma glucose ≥ 200 mg/dL during OGTT
        - HbA1c ≥ 6.5%
        - Random plasma glucose ≥ 200 mg/dL with classic symptoms

        ### Emerging Biomarkers
        - Fructosamine for short-term control
        - 1,5-anhydroglucitol (1,5-AG) for postprandial spikes
        - Continuous glucose monitoring (CGM) metrics: Time in Range (TIR), Glucose Management Indicator (GMI)
        """),
    ),
    (
        "Treatment Algorithms",
        textwrap.dedent("""
        ### First-Line Therapy
        Metformin remains first-line unless contraindicated. Start 500 mg daily, titrate to 2000 mg/day.

        ### Second-Line Options
        - SGLT2 inhibitors (empagliflozin, dapagliflozin) for ASCVD or CKD
        - GLP-1 receptor agonists (semaglutide, liraglutide) for weight loss and CV benefit
        - DPP-4 inhibitors (sitagliptin) as neutral add-on
        - Insulin when A1c > 10% or symptomatic hyperglycemia

        ### Combination Strategies
        Metformin + SGLT2i or GLP-1 RA is preferred for most patients with T2DM and obesity.

        ### Special Populations
        - **Elderly:** Avoid tight A1c targets (< 7.5%) if frail or limited life expectancy.
        - **Pregnancy:** Insulin is preferred; metformin may be continued in pregestational diabetes per latest ACOG guidance.
        - **CKD:** Prefer agents with renal benefit (SGLT2i, GLP-1 RA).
        """),
    ),
    (
        "Monitoring & Complications",
        textwrap.dedent("""
        ### Monitoring Schedule
        - HbA1c every 3 months if not at goal; every 6 months if stable.
        - Annual lipid panel, kidney function, retinal exam, foot exam.

        ### Complications
        - Microvascular: retinopathy, nephropathy (albuminuria), neuropathy (distal symmetric)
        - Macrovascular: MI, stroke, PAD
        - Acute: DKA (T1DM, SGLT2i-associated euglycemic DKA), HHS (T2DM)

        ### Technology
        - CGM recommended for all insulin-treated patients.
        - Insulin pumps and automated insulin delivery (AID) systems improve TIR.
        """),
    ),
]

diabetes_parts = ["# Diabetes Management Overview\n"]
for heading, body in diabetes_sections:
    diabetes_parts.append(f"## {heading}\n{body}")
diabetes_content = "\n".join(diabetes_parts)
write_markdown("diabetes_management_overview.md", diabetes_content)


# ---------------------------------------------------------------------------
# 2. Hypertension
# ---------------------------------------------------------------------------
hypertension_sections = [
    (
        "Classification",
        textwrap.dedent("""
        | Category | SBP | DBP |
        |----------|-----|-----|
        | Normal | <120 | <80 |
        | Elevated | 120–129 | <80 |
        | Stage 1 HTN | 130–139 | 80–89 |
        | Stage 2 HTN | ≥140 | ≥90 |
        | Hypertensive Crisis | >180 | >120 |
        """),
    ),
    (
        "Workup",
        textwrap.dedent("""
        - Confirm with ≥ 2 readings on ≥ 2 occasions.
        - Evaluate for secondary causes: renal artery stenosis, primary aldosteronism, pheochromocytoma.
        - Labs: CBC, CMP, fasting glucose, lipid panel, urinalysis.
        - Imaging: echocardiogram if LVH suspected; renal ultrasound if renal disease suspected.
        """),
    ),
    (
        "Pharmacotherapy",
        textwrap.dedent("""
        ### First-Line Agents
        - Thiazide diuretics (chlorthalidone)
        - ACE inhibitors (lisinopril)
        - ARBs (losartan)
        - Calcium channel blockers (amlodipine)

        ### Combination Therapy
        Start with two first-line agents for Stage 2 HTN. Preferred fixed-dose combinations:
        - ACEi + CCB
        - ARB + thiazide
        - ACEi/ARB + CCB

        ### Resistant Hypertension
        Add spironolactone 25 mg daily if BP remains above goal on 3 agents including a diuretic.
        Evaluate for secondary causes and medication nonadherence.
        """),
    ),
    (
        "Lifestyle",
        textwrap.dedent("""
        - DASH diet: fruits, vegetables, low-fat dairy, reduced saturated fat.
        - Sodium restriction < 2300 mg/day; ideal < 1500 mg/day.
        - Exercise: ≥ 150 min/week moderate-intensity aerobic activity.
        - Weight loss: 5–10% body weight can reduce SBP by 5–20 mmHg.
        - Alcohol moderation: ≤ 2 drinks/day men, ≤ 1 drink/day women.
        """),
    ),
]

hypertension_parts = ["# Hypertension Overview\n"]
for heading, body in hypertension_sections:
    hypertension_parts.append(f"## {heading}\n{body}")
hypertension_content = "\n".join(hypertension_parts)
write_markdown("hypertension_overview.md", hypertension_content)


# ---------------------------------------------------------------------------
# 3. Asthma
# ---------------------------------------------------------------------------
asthma_sections = [
    (
        "Definition",
        textwrap.dedent("""
        Asthma is a heterogeneous disease characterized by chronic airway inflammation and variable
        airflow obstruction. Key features include wheezing, breathlessness, chest tightness, and
        coughing, especially at night or in the early morning.
        """),
    ),
    (
        "Severity Classification",
        textwrap.dedent("""
        | Severity | Daytime symptoms | Nighttime awakenings | SABA use | FEV1 |
        |----------|------------------|----------------------|----------|------|
        | Intermittent | ≤2x/week | ≤2x/month | ≤2x/week | >80% |
        | Mild persistent | >2x/week | 3–4x/month | >2x/week | ≥80% |
        | Moderate persistent | Daily | >1x/week | Daily | 60–79% |
        | Severe persistent | Continual | Frequent | Several/day | <60% |
        """),
    ),
    (
        "Medications",
        textwrap.dedent("""
        ### Quick-Relief
        - Albuterol 90 mcg inhalation: 2 puffs every 4–6 hours as needed.
        - Ipratropium bromide for acute severe exacerbations.

        ### Controller
        - Low-dose ICS: beclomethasone 40–80 mcg BID
        - Medium-dose ICS: fluticasone 100–250 mcg BID
        - ICS/LABA: budesonide/formoterol maintenance and reliever therapy (SMART)
        - LTRA: montelukast 10 mg nightly
        - Biologics for severe asthma:
          - Omalizumab (anti-IgE)
          - Mepolizumab (anti-IL5)
          - Dupilumab (anti-IL4R)
          - Tezepelumab (anti-TSLP)
        """),
    ),
    (
        "Action Plan",
        textwrap.dedent("""
        ### Green Zone — Stable
        - No cough, wheeze, or chest tightness.
        - Use SABA ≤ 2 days/week.
        - Continue controller meds.

        ### Yellow Zone — Caution
        - Symptoms waking patient >1 night/month.
        - SABA use >2 days/week but not daily.
        - Consider short course of oral corticosteroids (prednisone 40 mg daily × 5 days).

        ### Red Zone — Danger
        - Severe dyspnea, inability to speak in full sentences.
        - SABA not lasting 4 hours.
        - Peak flow < 50% personal best.
        - **Action:** Seek emergency care immediately; administer prednisone 40–60 mg if available.
        """),
    ),
]

asthma_parts = ["# Asthma Overview\n"]
for heading, body in asthma_sections:
    asthma_parts.append(f"## {heading}\n{body}")
asthma_content = "\n".join(asthma_parts)
write_markdown("asthma_overview.md", asthma_content)


# ---------------------------------------------------------------------------
# 4. Mental health overview
# ---------------------------------------------------------------------------
mental_health_content = textwrap.dedent("""
# Anxiety & Depression Overview

## Epidemiology
- Anxiety disorders affect ~300 million people globally.
- Major depressive disorder affects ~280 million people globally.
- Women are twice as likely to be diagnosed with anxiety or depression.
- Average onset: late teens to mid-20s for anxiety; mid-20s for depression.

## Screening Tools
- **GAD-7:** Generalized Anxiety Disorder 7-item scale. Score ≥ 10 suggests moderate anxiety.
- **PHQ-9:** Patient Health Questionnaire 9-item. Score ≥ 10 suggests moderate depression.
- **PHQ-2:** Ultra-brief screen; if positive, administer PHQ-9.

## Anxiety Disorders
### Generalized Anxiety Disorder (GAD)
- Excessive worry ≥ 6 months about multiple events.
- Associated with restlessness, fatigue, concentration problems, irritability, muscle tension, sleep disturbance.
- First-line: SSRIs (sertraline, escitalopram) or SNRIs (venlafaxine, duloxetine).
- Second-line: buspirone, hydroxyzine, cognitive behavioral therapy (CBT).

### Panic Disorder
- Recurrent unexpected panic attacks + ≥ 1 month of worry about attacks or maladaptive behavior change.
- Treatment: CBT + SSRI/SNRI.

### Social Anxiety Disorder
- Marked fear or anxiety about social situations where scrutiny may occur.
- Treatment: CBT, SSRIs, beta-blockers for performance-only anxiety.

## Depressive Disorders
### Major Depressive Disorder (MDD)
- ≥ 5 symptoms for ≥ 2 weeks: depressed mood, anhedonia, weight change, sleep disturbance, psychomotor agitation/retardation, fatigue, guilt, concentration issues, suicidality.
- First-line: SSRIs (fluoxetine, sertraline, escitalopram).
- Augmentation: bupropion, atypical antipsychotics (aripiprazole, quetiapine).

### Treatment-Resistant Depression (TRD)
- Failure to respond to ≥ 2 adequate antidepressant trials.
- Options: switch antidepressant class, augmentation, ECT, rTMS, ketamine/esketamine.

## Psychotherapy
- CBT is first-line for anxiety and mild-to-moderate depression.
- IPT effective for depression, especially with interpersonal stressors.
- DBT useful for emotional dysregulation and self-harm behaviors.

## Crisis Resources
- Always screen for suicidality using C-SSRS.
- If imminent risk: do not leave patient alone, activate emergency services, arrange urgent psychiatric evaluation.
- US Suicide & Crisis Lifeline: 988
""")
write_markdown("anxiety_depression_overview.md", mental_health_content)


# ---------------------------------------------------------------------------
# 5. Benefits overview
# ---------------------------------------------------------------------------
benefits_content = textwrap.dedent("""
# Employee Benefits Overview

**Effective Date:** January 1, 2025 | **Owner:** People Operations

## Medical, Dental, and Vision
- Medical: Aetna PPO and HDHP options; HealthTech covers 85% of employee-only premium.
- Dental: Delta Dental PPO; 100% preventive, 80% basic, 50% major.
- Vision: VSP; annual exam covered, $150 frame allowance.
- HSA: up to $4,150 employee-only / $8,300 family contribution limit (2025).

## Leave Policies
- **PTO:** 20 days/year (accrues monthly).
- **Sick Leave:** Unlimited; notify manager before 10 AM.
- **Parental Leave:** 16 weeks fully paid (birthing parent); 8 weeks (non-birthing parent).
- **Bereavement:** 5 days paid for immediate family.
- **Jury Duty:** Paid leave for actual service duration.

## Retirement
- 401(k) with 4% company match, immediate vesting.
- Employees age 21+ with 1 year of service eligible.

## Learning & Development
- Annual learning stipend: $2,000 per employee for courses, conferences, books.
- Internal mentorship program: apply quarterly.
- Tuition reimbursement: up to $5,250/year for job-relevant degrees.

## Wellness
- On-site fitness center (if office-based) or $50/month fitness reimbursement.
- Mental health: free access to Modern Health; 8 therapy sessions/year included.
- Ergonomic stipend: $500 one-time for home office setup.

## Insurance
- Life insurance: 1x annual salary covered; additional coverage available.
- Disability: short-term 60% salary for 6 months; long-term 60% salary after.
- AD&D: included at no cost.

## Commuter & Remote Work
- Remote-first eligible roles receive $100/month internet reimbursement.
- Co-working space stipend: $200/month for hybrid employees.
""")
write_markdown("benefits_overview.md", benefits_content)


# ---------------------------------------------------------------------------
# 6. Engineering guidelines
# ---------------------------------------------------------------------------
engineering_content = textwrap.dedent("""
# Engineering Guidelines

**Version:** 4.1 | **Owner:** VP of Engineering

## Code Review
- All changes require at least one approval from a code owner.
- Reviews should be completed within 24 business hours.
- Focus on correctness, security, performance, and maintainability.
- Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.

## Pull Requests
- PRs should be < 400 lines when possible; split large changes.
- Include tests for new behavior; update docs for API changes.
- CI must pass: lint, type-check, unit tests, security scan.
- Link PR to ticket; summarize change, risk, and rollout plan.

## Testing
- Unit test coverage target: 80% line coverage.
- Integration tests for API endpoints and data pipelines.
- E2E tests for critical user journeys via Cypress.
- Use property-based testing for complex algorithms where feasible.

## Observability
- Instrument services with structured logging (`structlog`) and OpenTelemetry spans.
- Emit metrics for latency, error rate, saturation.
- Dashboards must include at least: p50, p95, p99 latency; request rate; error rate.
- Alerting thresholds documented in runbooks.

## Incident Response
- Severity 1: page on-call engineer, open war room within 15 min.
- Severity 2: notify team lead, resolution within 4 hours.
- Severity 3: ticket, resolution within 2 business days.
- Post-incident review required for Severity 1 and 2 within 48 hours.

## API Design
- RESTful endpoints with consistent naming: `/api/v1/<resource>`
- Request/response schemas defined with Pydantic v2.
- Pagination: cursor-based for large collections; limit default 20, max 100.
- Versioning: include version in URL path; deprecate old versions with ≥ 90 days notice.
""")
write_markdown("engineering_guidelines.md", engineering_content)


# ---------------------------------------------------------------------------
# 7. IT security policy
# ---------------------------------------------------------------------------
it_security_content = textwrap.dedent("""
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
""")
write_markdown("it_security_policy.md", it_security_content)


# ---------------------------------------------------------------------------
# 8. HR onboarding
# ---------------------------------------------------------------------------
hr_onboarding_content = textwrap.dedent("""
# HR Onboarding Guide

**Version:** 2.0 | **Effective Date:** January 1, 2025

## Before Day 1
- Send welcome email with first-day details and parking instructions.
- Provision laptop, monitor, keyboard, mouse, and headset.
- Create accounts: Okta, Slack, GitHub, AWS IAM, VPN, email.
- Assign buddy for first 30 days.

## First Week
- Complete new-hire paperwork: I-9, W-4, emergency contacts.
- Attend benefits enrollment session.
- Review code of conduct and security awareness training.
- Set up development environment per engineering guidelines.

## First Month
- Complete role-specific training modules.
- Shadow at least 2 customer support calls (customer-facing roles).
- Meet with manager to set 30/60/90-day goals.
- Attend all-hands meeting.

## Ongoing
- 30/60/90-day check-ins with manager and HR business partner.
- Probation period ends at 90 days; feedback collected from buddy and peers.
- Annual review cycle begins after first 6 months.
""")
write_markdown("hr_onboarding.md", hr_onboarding_content)


# ---------------------------------------------------------------------------
# 9. HR salary guidelines
# ---------------------------------------------------------------------------
hr_salary_content = textwrap.dedent("""
# Salary Guidelines

**Version:** 3.0 | **Owner:** Total Rewards

## Philosophy
HealthTech Inc. aims to pay at or above the 75th percentile of the market for comparable
roles in the healthcare technology sector, adjusted for location and experience.

## Level Framework
| Level | Title | Salary Range (USD) | Equity |
|-------|-------|-------------------|--------|
| L3 | Engineer I | 110,000–140,000 | 0.05% |
| L4 | Engineer II | 140,000–180,000 | 0.10% |
| L5 | Senior Engineer | 180,000–230,000 | 0.20% |
| L6 | Staff Engineer | 230,000–290,000 | 0.35% |
| L7 | Principal Engineer | 290,000–360,000 | 0.55% |

## Promotions
- Annual promotion cycle; exceptions for exceptional performance.
- Promotion criteria: scope, impact, technical leadership, collaboration.
- Typical raise at promotion: 10–20% base increase + equity refresh.

## Performance Bonuses
- Target bonus: 15% of base salary for L4–L6.
- Individual multiplier: 0.5x–1.5x based on performance rating.
- Team/company multiplier: 0.8x–1.2x based on business results.
""")
write_markdown("hr_salary_guidelines.md", hr_salary_content)


# ---------------------------------------------------------------------------
# 10. Emergency warning signs
# ---------------------------------------------------------------------------
emergency_content = textwrap.dedent("""
# Emergency Warning Signs

**Purpose:** Quick reference for clinicians and triage staff.

## Cardiac
- Chest pain or pressure lasting > 2 minutes, especially with radiation to arm/jaw.
- Sudden severe shortness of breath at rest.
- Syncope with exertion or without warning.

## Neurological
- Sudden severe headache ("worst headache of life").
- Focal weakness, numbness, or speech difficulty.
- Vision loss in one eye (amaurosis fugax).
- Seizure without prior history.

## Respiratory
- Inability to speak in full sentences.
- Cyanosis or SpO2 < 90% on room air.
- Stridor or severe respiratory distress.

## Gastrointestinal
- Severe abdominal pain with rigidity or rebound.
- Hematemesis or hematochezia with hemodynamic instability.
- Jaundice with altered mental status (hepatic encephalopathy).

## Sepsis
- suspected infection + qSOFA ≥ 2 (RR ≥ 22, altered mentation, SBP ≤ 100).
- Lactate > 2 mmol/L.
- Initiate sepsis bundle: blood cultures, broad-spectrum antibiotics within 1 hour, 30 mL/kg crystalloid.

## Obstetric
- Vaginal bleeding with abdominal pain in 2nd/3rd trimester.
- Severe hypertension ≥ 160/110 with headache or visual changes (preeclampsia with severe features).
- Decreased fetal movement.

## Pediatric
- Fever > 40°C (104°F) in infant < 3 months.
- Respiratory rate > 60/min in infant < 1 year.
- Bulging fontanelle with altered mental status.
""")
write_markdown("emergency_warning_signs.md", emergency_content)


# ---------------------------------------------------------------------------
# 11. Medication safety
# ---------------------------------------------------------------------------
medication_safety_content = textwrap.dedent("""
# Medication Safety Overview

## High-Alert Medications
- Insulin: double-check concentration and patient identity.
- Anticoagulants: warfarin, heparin, DOACs; monitor for bleeding.
- Concentrated electrolytes: restrict storage in patient care areas.
- Opioids: assess pain and sedation scores before each dose.

## The "Five Rights"
1. Right patient
2. Right drug
3. Right dose
4. Right route
5. Right time

## Common Interactions
| Drug A | Drug B | Interaction | Management |
|--------|--------|-------------|------------|
| Warfarin | Amiodarone | Increased INR | Reduce warfarin dose by 30–50% |
| ACE inhibitor | K-sparing diuretic | Hyperkalemia | Monitor K+; avoid combination if K > 5.0 |
| Metformin | Iodinated contrast | Lactic acidosis | Hold metformin 48 hours post-contrast |
| SSRI | MAOI | Serotonin syndrome | Washout 14 days between agents |
| Statin | Gemfibrozil | Rhabdomyolysis | Avoid combination |

## Look-Alike/Sound-Alike (LASA)
- Use Tallman lettering: e.g., HYDROmorphone vs HYDROcodone.
- Separate storage look-alike medications.
- Require independent double-check for high-alike pairs.

## Adverse Event Reporting
- Report serious adverse events to FDA MedWatch within 7 calendar days.
- Document event in incident management system with timeline, patient impact, and corrective actions.
""")
write_markdown("medication_safety_overview.md", medication_safety_content)


# ---------------------------------------------------------------------------
# 12. Cold & flu
# ---------------------------------------------------------------------------
cold_flu_content = textwrap.dedent("""
# Cold & Flu Overview

## Influenza
- Annual vaccination recommended for all persons ≥ 6 months.
- Antiviral therapy: oseltamivir 75 mg PO BID × 5 days if started within 48 hours of symptom onset.
- High-risk groups: ≥ 65 years, pregnant, chronic medical conditions, immunocompromised.

## Common Cold
- Rhinovirus most common cause.
- Supportive care: hydration, rest, analgesics for fever/pain.
- Antibiotics not indicated unless secondary bacterial infection suspected.

## COVID-19
- Test with rapid antigen or PCR.
- Antivirals for high-risk outpatients: nirmatrelvir/ritonavir within 5 days of symptom onset.
- Isolation: at least 5 days from symptom onset + afebrile 24 hours + improving symptoms.

## Symptom Management
| Symptom | Intervention |
|---------|--------------|
| Fever/pain | Acetaminophen or NSAIDs |
| Nasal congestion | Saline irrigation; oxymetazoline ≤ 3 days |
| Cough | Honey (≥ 1 year); dextromethorphan |
| Sore throat | Warm salt water gargle; lozenges |

## When to Escalate
- Persistent fever > 38.9°C (102°F) for > 3 days.
- Dyspnea at rest or hypoxemia (SpO2 < 94%).
- Chest pain, altered mental status, severe dehydration.
""")
write_markdown("cold_flu_overview.md", cold_flu_content)


# ---------------------------------------------------------------------------
# 13. Extended medical topics
# ---------------------------------------------------------------------------
covid19_content = textwrap.dedent("""
# COVID-19 Overview

## Symptoms and Testing
COVID-19 is caused by SARS-CoV-2 and can range from no symptoms to severe respiratory illness. Common symptoms include fever, cough, sore throat, nasal congestion, fatigue, headache, muscle aches, and loss of smell or taste; some people also have nausea, vomiting, or diarrhea. Use a rapid antigen or PCR test when infection is suspected, and follow current local public-health guidance.

## Long-Term Effects
Long COVID (post-COVID conditions) refers to new, returning, or ongoing symptoms lasting at least 3 months after infection. Symptoms may fluctuate and can include persistent fatigue, shortness of breath, cough, headaches, sleep problems, difficulty concentrating, dizziness, and digestive complaints. Symptoms can occur after mild or asymptomatic infection.

## Current Management
There is no single diagnostic test or treatment for Long COVID. Care focuses on a clinical evaluation, excluding other causes, validating symptoms, and addressing the most burdensome problems. Rehabilitation, pacing for post-exertional malaise, treatment of underlying conditions, and supportive services may help. Updated COVID-19 vaccination reduces the risk of severe illness and Long COVID. People at higher risk of severe acute COVID-19 should ask promptly about eligible antiviral treatment.

## When to Seek Care
Seek urgent care for trouble breathing, chest pain, confusion, bluish lips, severe dehydration, or worsening symptoms. Follow current isolation and prevention guidance from public-health authorities.
""")
write_markdown("covid19_overview.md", covid19_content)

vaccination_schedule_content = textwrap.dedent("""
# Vaccination Schedule Overview

## How Schedules Are Used
Vaccination recommendations depend on age, prior doses, pregnancy, health conditions, occupation, travel, and local guidance. Clinicians use the current CDC/ACIP child, adolescent, and adult schedules rather than relying on a single fixed list.

## Pediatric Basics
Infants commonly begin with hepatitis B at birth, followed by series such as DTaP, IPV, Hib, pneumococcal, rotavirus, and COVID-19 vaccines during early childhood. MMR, varicella, hepatitis A, and booster doses are given in toddler and preschool years. Influenza vaccination is recommended annually beginning at 6 months. Preteens commonly receive HPV and meningococcal ACWY vaccines, with a Tdap booster and additional meningococcal dosing as indicated.

## Adult Basics
Adults should receive an annual influenza vaccine and stay current with COVID-19 recommendations. A Tdap dose is followed by a tetanus/diphtheria booster every 10 years. Hepatitis B vaccination is recommended for adults through age 59 and for older adults with indications; MMR, varicella, and other vaccines depend on immunity and risk. Shingles vaccination is recommended beginning at age 50, pneumococcal vaccination at age 65 or earlier with risk factors, and RSV vaccination for eligible older adults. HPV vaccination is recommended through age 26 when not completed and may be considered through age 45 through shared decision-making.

## Practical Notes
Review the immunization record at every visit, use catch-up schedules when doses are missing, and check pregnancy, allergy, immune status, and other contraindications before vaccination.
""")
write_markdown("vaccination_schedule_overview.md", vaccination_schedule_content)

pregnancy_prenatal_care_content = textwrap.dedent("""
# Pregnancy and Prenatal Care Overview

## Goals of Care
Prenatal care supports the health of the pregnant person and fetus through risk assessment, preventive care, screening, education, and timely treatment. The first assessment should occur as early as possible, ideally before 10 weeks, and include medical and obstetric history, medications, family history, infections, immunizations, and social needs.

## Checkup Schedule
For an average-risk pregnancy, visits are commonly every 4 weeks through 28 weeks, every 2 weeks from 28 to 36 weeks, and weekly until delivery. The schedule is individualized for medical conditions, symptoms, fetal growth, or other risks; telehealth and home monitoring may supplement selected visits.

## Routine Care and Screening
Visits generally review blood pressure, weight, symptoms, fetal growth and heartbeat, urine findings, and test results. Care may include blood type and antibody screening, anemia and infection testing, genetic screening options, ultrasound assessment, gestational diabetes screening, and group B streptococcus testing later in pregnancy. Prenatal vitamins with folic acid, nutrition, physical activity, medication safety, and birth planning are reviewed.

## Common Concerns
Nausea, fatigue, heartburn, constipation, back pain, swelling, and sleep changes are common, but persistent or severe symptoms need assessment. Contact the care team urgently for vaginal bleeding, severe abdominal pain, severe headache or vision changes, fever, shortness of breath, fluid leakage, or decreased fetal movement.
""")
write_markdown("pregnancy_prenatal_care_overview.md", pregnancy_prenatal_care_content)

cancer_screening_content = textwrap.dedent("""
# Cancer Screening Overview

## General Principles
Screening is for people without cancer symptoms. Recommendations vary by sex assigned at birth, organs present, age, family history, genetic risk, prior results, and overall health. Confirm the appropriate plan with a clinician.

## Breast Screening
For people at average risk, the USPSTF recommends screening mammography every 2 years from ages 40 through 74. People with a strong family history, a known pathogenic variant such as BRCA1 or BRCA2, prior chest radiation, or other high-risk features may need earlier and additional screening, such as breast MRI.

## Colorectal Screening
Average-risk adults should begin colorectal cancer screening at age 45 and continue through 75. Options include annual high-sensitivity FIT, stool DNA-FIT at recommended intervals, CT colonography, flexible sigmoidoscopy, or colonoscopy every 10 years when results are normal. Screening from 76 to 85 is individualized based on health, prior screening, and preferences; routine screening generally stops after 85.

## Cervical Screening
Screen ages 21 to 29 with cervical cytology every 3 years. From ages 30 to 65, options include primary high-risk HPV testing every 5 years, cotesting every 5 years, or cytology every 3 years. Screening may stop after 65 after adequate normal prior screening and no high-risk history; people with certain immunocompromising conditions or prior high-grade lesions need a different plan.

## Symptoms Still Need Evaluation
Abnormal bleeding, a new lump, unexplained weight loss, blood in stool, or persistent pain requires diagnostic evaluation rather than routine screening.
""")
write_markdown("cancer_screening_overview.md", cancer_screening_content)

migraine_headache_content = textwrap.dedent("""
# Migraine and Headache Overview

## Migraine vs Tension-Type Headache
Migraine is usually moderate to severe, throbbing or pulsating, often one-sided, and worsened by activity. Nausea, light sensitivity, sound sensitivity, or aura may occur. Tension-type headache is typically mild to moderate, bilateral, and described as pressure or a tight band, without the prominent nausea or sensory sensitivity of migraine. A sudden "worst headache," neurologic deficit, fever, neck stiffness, head injury, or a new headache after age 50 needs urgent evaluation.

## Common Triggers
Triggers vary and may include stress or let-down after stress, irregular sleep, skipped meals, dehydration, alcohol, caffeine changes, hormonal changes, strong smells, bright light, weather changes, and certain foods. A headache diary can identify patterns; triggers are not always avoidable and should not lead to unnecessarily restrictive diets.

## Management
Regular sleep, meals, hydration, physical activity, and limiting acute medication overuse support control. Mild attacks may respond to acetaminophen or an NSAID when safe; migraine-specific medicines such as triptans may be appropriate for some people. Preventive treatment can be considered when headaches are frequent, prolonged, disabling, or acute medicines are ineffective or overused. Options include lifestyle and behavioral strategies and clinician-selected medicines such as beta-blockers, topiramate, amitriptyline, or CGRP-targeted therapy.

## Follow-Up
Seek clinical review for changing patterns, new neurologic symptoms, pregnancy, or headaches that interfere with daily life.
""")
write_markdown("migraine_headache_overview.md", migraine_headache_content)


# ---------------------------------------------------------------------------
# 14. Extended medical topics
# ---------------------------------------------------------------------------
copd_content = textwrap.dedent("""
# COPD Overview

## Definition
Chronic obstructive pulmonary disease (COPD) is a preventable, treatable lung disease
characterized by persistent airflow limitation due to airway and/or alveolar abnormalities
usually caused by significant exposure to noxious particles or gases.

## Classification
- **GOLD 1 (Mild):** FEV1 ≥ 80% predicted
- **GOLD 2 (Moderate):** 50% ≤ FEV1 < 80%
- **GOLD 3 (Severe):** 30% ≤ FEV1 < 50%
- **GOLD 4 (Very Severe):** FEV1 < 30%

## Pharmacotherapy
- Bronchodilators: short-acting for rescue, long-acting for maintenance.
- LABA + LAMA preferred over LABA + ICS in most patients.
- Roflumilast for severe COPD with chronic bronchitis and frequent exacerbations.
- Macrolide prophylaxis in selected patients with frequent exacerbations.

## Non-Pharmacologic
- Smoking cessation is the most effective intervention.
- Pulmonary rehabilitation improves dyspnea and quality of life.
- Vaccinations: annual influenza, pneumococcal, COVID-19 as indicated.
""")
write_markdown("copd_overview.md", copd_content)

ckd_content = textwrap.dedent("""
# Chronic Kidney Disease Overview

## Staging
| Stage | eGFR (mL/min/1.73 m²) | Description |
|-------|------------------------|-------------|
| 1 | ≥ 90 | Normal or high GFR with kidney damage |
| 2 | 60–89 | Mild decrease |
| 3a | 45–59 | Moderate decrease |
| 3b | 30–44 | Moderate-severe decrease |
| 4 | 15–29 | Severe decrease |
| 5 | < 15 | Kidney failure |

## Management
- ACE inhibitors or ARBs for proteinuria or hypertension.
- SGLT2 inhibitors for CKD with or without diabetes (dapagliflozin, empagliflozin).
- Avoid nephrotoxins: NSAIDs, IV contrast unless essential.
- Dietary protein restriction to 0.8 g/kg/day in stages 3–5.
- Refer to nephrology when eGFR < 30 or complex management needed.

## Complications
- Anemia: EPO-stimulating agents when Hb < 10 g/dL.
- Bone-mineral disorder: phosphate binders, vitamin D analogs, calcimimetics.
- Metabolic acidosis: sodium bicarbonate when bicarbonate < 18 mEq/L.
""")
write_markdown("ckd_overview.md", ckd_content)

stroke_content = textwrap.dedent("""
# Stroke Overview

## Types
- **Ischemic stroke:** 87% of strokes. Includes large-artery atherosclerosis, cardioembolism, small-vessel disease, and other determined/undetermined causes (TOAST classification).
- **Hemorrhagic stroke:** Intracerebral hemorrhage (ICH) or subarachnoid hemorrhage (SAH).

## Acute Management
### Ischemic
- IV alteplase within 3 hours of last known well (up to 4.5 hours in select patients).
- Mechanical thrombectomy up to 24 hours for large-vessel occlusion (anterior circulation).
- Antiplatelet: aspirin 325 mg daily after excluding hemorrhage.

### Hemorrhagic
- Reverse anticoagulation immediately if present.
- Control blood pressure: target SBP 140–160 mmHg (unless contraindicated).
- Neurosurgical evaluation for ICH > 30 mL or cerebellar hemorrhage > 3 cm with mass effect.

## Secondary Prevention
- Antiplatelet therapy: aspirin, clopidogrel, or aspirin + ER dipyridamole.
- Statin therapy for noncardioembolic ischemic stroke.
- Blood pressure control: target < 130/80 mmHg.
- Atrial fibrillation: anticoagulation with DOAC preferred over warfarin in most patients.
""")
write_markdown("stroke_overview.md", stroke_content)


# ---------------------------------------------------------------------------
# 14. Drug interaction database
# ---------------------------------------------------------------------------
drug_interactions = []
drug_pairs = [
    ("warfarin", "amiodarone", "Increased INR and bleeding risk; reduce warfarin dose by 30-50% and monitor INR closely"),
    ("warfarin", "rifampin", "Decreased anticoagulant effect; increase monitoring and adjust warfarin dose"),
    ("metformin", "furosemide", "May decrease metformin efficacy; monitor glucose"),
    ("lisinopril", "spironolactone", "Risk of hyperkalemia; monitor potassium and renal function"),
    ("sertraline", "tramadol", "Increased seizure risk and serotonin syndrome; avoid if possible"),
    ("simvastatin", "clarithromycin", "Increased risk of rhabdomyolysis; contraindicated; switch to pravastatin or rosuvastatin"),
    ("omeprazole", "clopidogrel", "Reduced antiplatelet effect of clopidogrel; consider pantoprazole instead"),
    ("amlodipine", "simvastatin", "Increased simvastatin exposure; limit simvastatin to 20 mg/day"),
    ("levothyroxine", "calcium carbonate", "Decreased levothyroxine absorption; separate doses by ≥ 4 hours"),
    ("fluconazole", "warfarin", "Enhanced anticoagulant effect; monitor INR more frequently"),
    ("ibuprofen", "lisinopril", "Reduced antihypertensive effect and renal impairment risk"),
    ("methotrexate", "ibuprofen", "Increased methotrexate toxicity; avoid NSAIDs"),
    ("allopurinol", "azathioprine", "Increased azathioprine metabolite toxicity; reduce azathioprine dose to 25-33%"),
    ("digoxin", "amiodarone", "Increased digoxin levels; reduce digoxin dose by 50% and monitor"),
    ("theophylline", "ciprofloxacin", "Increased theophylline levels and toxicity risk; monitor for seizures and arrhythmias"),
]
for a, b, effect in drug_pairs:
    drug_interactions.append(f"## {a.title()} + {b.title()}\n- **Effect:** {effect}\n- **Management:** Monitor clinical status and adjust doses as needed. Consult pharmacy for complex regimens.\n")

write_markdown("drug_interactions.md", "\n".join(["# Drug Interactions\n"] + drug_interactions))


# ---------------------------------------------------------------------------
# 15. Extended HR documents
# ---------------------------------------------------------------------------
leave_policy = textwrap.dedent("""
# Leave Policies

**Version:** 2.1 | **Effective Date:** January 1, 2025

## Paid Time Off (PTO)
- Accrual: 1.67 days/month (20 days/year).
- Carryover: up to 5 days into next calendar year; excess forfeited on January 31.
- Payout: unused PTO not paid out unless required by state law.

## Sick Leave
- Unlimited sick leave for all full-time employees.
- Notify manager before 10 AM on sick days.
- Medical certification required if absent > 5 consecutive days.

## Parental Leave
- **Birthing parent:** 16 weeks fully paid.
- **Non-birthing parent:** 8 weeks fully paid.
- Adoption/surrogacy: 8 weeks paid.
- Leave must begin within 30 days of birth or placement.

## Other Leaves
- **Bereavement:** 5 days paid for immediate family.
- **Military:** Up to 5 years protected leave per USERRA.
- **Jury Duty:** Paid leave for actual service; provide summons documentation.
- **FMLA:** Up to 12 weeks unpaid protected leave per eligibility criteria.

## State-Specific Rules
- California: CFRA and PDL apply in addition to FMLA.
- New York: Paid family leave (PFL) provides partial wage replacement.
""")
write_markdown("leave_policies.md", leave_policy)

expense_policy = textwrap.dedent("""
# Expense Reimbursement Policy

**Version:** 1.4 | **Effective Date:** January 1, 2025

## Submitting Expenses
- Use Expensify for all reimbursable expenses.
- Submit within 30 days of incurring the expense.
- Receipts required for all expenses > $25.

## Approval Thresholds
- **< $50:** Manager approval only.
- **$50–$500:** Manager + VP approval.
- **> $500:** CFO approval required.

## Acceptable Expenses
- Travel: airfare, train, mileage (IRS rate), lodging, meals (per diem applies).
- Software/tools: must be pre-approved for amounts > $100.
- Conferences: registration, travel, hotel; manager approval required.

## Unacceptable Expenses
- Alcohol (except client entertainment with VP approval).
- Personal entertainment or vacations.
- Traffic fines or parking tickets.
- First-class airfare without VP approval.
""")
write_markdown("expense_policy.md", expense_policy)


# ---------------------------------------------------------------------------
# 16. Product specs
# ---------------------------------------------------------------------------
product_spec_v2 = textwrap.dedent("""
# Product Specification v2.0

**Owner:** Product Management | **Status:** Released

## Summary
HealthTech RAG Assistant v2.0 introduces multi-tenant retrieval, HyDE query rewriting, and
cross-encoder reranking to improve answer relevance and reduce hallucination.

## Features
### Multi-Tenant Retrieval
- Documents tagged with `access_tags` and `pii_flags`.
- Queries filtered by user role at retrieval time.
- Supports row-level ACL without custom code per tenant.

### Query Rewriting
- **HyDE:** generate hypothetical answer to improve vector similarity.
- **Multi-query:** expand user query into 3 semantically diverse queries.
- Configurable strategy per request: `none`, `hyde`, `multi_query`, `both`.

### Reranking
- Cross-encoder model: `cross-encoder/ms-marco-MiniLM-L-6-v2`.
- Rerank top-20 candidates to top-6 final chunks.
- Latency budget: add ~40 ms per query.

### Guardrails
- Input: PII redaction + prompt injection detection.
- Output: confidence scoring + citation enforcement + optional hallucination check.

## Non-Functional Requirements
- P95 latency: < 2 seconds for end-to-end chat.
- Availability: 99.9% uptime excluding planned maintenance.
- Data retention: audit logs 6 years; embeddings retained indefinitely unless deleted by tenant.
""")
write_markdown("product_spec_v2.md", product_spec_v2)


# ---------------------------------------------------------------------------
# 17. Research paper
# ---------------------------------------------------------------------------
research_content = textwrap.dedent("""
# Research Paper: Retrieval-Augmented Generation for Clinical Question Answering

## Abstract
We evaluated a RAG pipeline combining dense retrieval, cross-encoder reranking, and
large language models for clinical question answering. Our system achieved a 12% absolute
improvement in exact match accuracy over a standalone LLM baseline on a proprietary
medical QA dataset.

## Methods
- **Retriever:** OpenAI text-embedding-3-large, top-k=20.
- **Reranker:** BAAI/bge-reranker-large, top-n=6.
- **Generator:** GPT-4o-mini with system prompt enforcing citation use.
- **Dataset:** 2,500 clinical questions spanning internal medicine, pediatrics, and emergency medicine.

## Results
| Metric | LLM Only | RAG Pipeline |
|--------|----------|--------------|
| Exact Match | 34.2% | 46.8% |
| F1 Score | 41.5% | 53.7% |
| Citation Precision | N/A | 89.4% |
| Latency (P95) | 1.1s | 1.8s |

## Conclusion
RAG significantly improves accuracy and traceability for clinical QA. HyDE query rewriting
provided marginal gains on complex questions. Cross-encoder reranking was the highest-impact
component.
""")
write_markdown("research_paper_rag.md", research_content)


# ---------------------------------------------------------------------------
# 18. Project overview / FAQ
# ---------------------------------------------------------------------------
faq_content = textwrap.dedent("""
# Project Overview & FAQ

## What is the HealthTech RAG Assistant?
The HealthTech RAG Assistant is an internal AI chatbot that answers employee questions
about company policies, HR benefits, clinical guidelines, and medical research using
retrieval-augmented generation.

## How do I log in?
Use any User ID and select your role on the login page. The backend issues a JWT for
authentication.

## What documents are indexed?
Documents in the `/data` directory are ingested on startup or via the `/api/v1/ingest`
endpoint. Supported formats: PDF, TXT, Markdown.

## Who can access which documents?
Access is controlled by `access_tags` and role membership. For example, salary guidelines
are tagged for `admin`, while medical policies require `compliance-team`.

## How accurate is the chatbot?
The system uses a hybrid retrieval pipeline with cross-encoder reranking and guardrails
to enforce citation use and confidence thresholds. If it cannot find a high-confidence
answer, it will say so.

## How do I report incorrect answers?
Use the thumbs-down feedback button or email the AI platform team. Include the question
and the incorrect answer so we can improve retrieval and guardrails.
""")
write_markdown("project_overview_and_faq.md", faq_content)


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
total_chars = sum(
    len(p)
    for p in [
        diabetes_content,
        hypertension_content,
        asthma_content,
        mental_health_content,
        benefits_content,
        engineering_content,
        it_security_content,
        hr_onboarding_content,
        hr_salary_content,
        emergency_content,
        medication_safety_content,
        cold_flu_content,
        covid19_content,
        vaccination_schedule_content,
        pregnancy_prenatal_care_content,
        cancer_screening_content,
        migraine_headache_content,
        copd_content,
        ckd_content,
        stroke_content,
        "\n".join(drug_interactions),
        leave_policy,
        expense_policy,
        product_spec_v2,
        research_content,
        faq_content,
    ]
)
print(f"\nDone. Generated ~{total_chars:,} characters of sample data across {len(list(DATA_DIR.glob('*.md')))} documents.")
