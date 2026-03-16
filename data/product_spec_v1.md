# HealthTech ClinicalAI Platform – Product Specification v1.0

**Status:** GA (Generally Available) | **Release Date:** March 2024
**Product Owner:** Dr. Priya Sharma | **Engineering Lead:** Marcus Chen
**Access Tags:** all-employees

---

## 1. Product Overview

HealthTech ClinicalAI v1.0 is an enterprise-grade clinical decision support platform that
surfaces evidence-based recommendations to physicians at the point of care. It integrates
directly into Epic and Cerner EHR systems via SMART on FHIR APIs.

**Core capabilities:**
- Differential diagnosis suggestions based on structured patient data (ICD-10, SNOMED CT)
- Drug-interaction alerts with severity scoring (A–D scale per FDA)
- Sepsis early-warning scores (SOFA, qSOFA, NEWS2)
- Readmission risk stratification (30-day, 90-day)

---

## 2. Architecture

```
┌─────────────┐    FHIR R4     ┌──────────────────┐    gRPC     ┌──────────────┐
│  EHR System │ ────────────► │  ClinicalAI API  │ ──────────► │  ML Inference│
│(Epic/Cerner)│               │  (FastAPI + MTLS) │             │  Service     │
└─────────────┘               └──────────────────┘             └──────────────┘
                                        │                               │
                                   PostgreSQL                    PyTorch Serve
                                   (patient ctx)                 (ONNX models)
```

### 2.1 Data Flow

1. EHR triggers a SMART app launch upon patient record open.
2. ClinicalAI API fetches FHIR resources (Patient, Condition, Medication, Observation).
3. Structured data is featurized and passed to ML inference microservice.
4. Recommendations are returned as FHIR CommunicationRequest resources.
5. EHR displays recommendations as CDS Hooks cards.

---

## 3. Models & Performance

| Model | Task | AUC | Sensitivity | Specificity |
|-------|------|-----|------------|------------|
| DiagnosisRanker v3 | Differential Dx top-5 | 0.91 | 88% | 84% |
| DrugInteractionNet | DDI severity | 0.95 | 93% | 91% |
| SepsisWatch | 6-hour sepsis onset | 0.88 | 82% | 90% |
| ReadmitRisk | 30-day readmission | 0.79 | 74% | 81% |

All models are validated on held-out patient populations from 3 geographically diverse health systems.

---

## 4. Compliance & Security

- **HIPAA:** BAA signed with all customers; PHI encrypted at rest (AES-256) and in transit (TLS 1.3).
- **FDA:** ClinicalAI is a Software as Medical Device (SaMD) Class II under FDA guidance.
  510(k) clearance pending for DiagnosisRanker.
- **SOC 2 Type II:** Certified annually.
- **Audit logs:** All clinical recommendations are logged with timestamp, model version, and clinician action.

---

## 5. API Reference

### POST /v1/recommendations

**Request:**
```json
{
  "patient_id": "fhir-patient-id",
  "encounter_id": "fhir-encounter-id",
  "recommendation_types": ["diagnosis", "drug_interaction", "sepsis"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "type": "diagnosis",
      "rank": 1,
      "code": "J18.9",
      "display": "Pneumonia, unspecified",
      "confidence": 0.87,
      "evidence_links": ["pmid:12345678"]
    }
  ],
  "model_versions": {"DiagnosisRanker": "3.2.1"},
  "latency_ms": 142
}
```

---

## 6. Latency SLAs

| Percentile | Target |
|-----------|--------|
| p50 | < 150ms |
| p95 | < 400ms |
| p99 | < 800ms |

---

## 7. Known Limitations (v1.0)

- Rare diseases (<1:10,000 prevalence) have limited training data; confidence is lower.
- Pediatric populations (age < 18) are not yet validated; use with clinical judgment.
- Non-English EHR notes are not processed in this version.
