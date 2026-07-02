# Diabetes Management Overview — Clinical Reference Summary

**Source basis:** American Diabetes Association, *Standards of Care in Diabetes—2026* (published as a supplement to *Diabetes Care*, January 2026). This document is a paraphrased internal summary for knowledge-base purposes only — it is not the full guideline text and should not be treated as a complete clinical reference. See "Important Notes" below.

## Overview

Diabetes management guidance is updated annually by the American Diabetes Association (ADA). The 2026 update continues a multi-year trend toward earlier and broader use of diabetes technology, and toward selecting glucose-lowering medications based on a patient's full cardiovascular, kidney, and liver risk profile — not glucose control alone.

## Key 2026 Updates (Summary)

**Technology use expanded**
Continuous glucose monitoring (CGM) and automated insulin delivery (AID) systems are now recommended earlier in the course of disease for both type 1 and type 2 diabetes, with fewer restrictions on eligibility than in prior years. AID is now the preferred insulin delivery method — rated above standard insulin pumps and multiple daily injections — for people with type 1 diabetes and for insulin-using adults and children with type 2 diabetes. This is a notably stronger recommendation than in previous editions.

**Medication selection tied to comorbidities**
GLP-1 receptor agonists are now recommended as initial therapy (not just an add-on) for adults with type 2 diabetes who also have liver fibrosis or metabolic dysfunction-associated steatotic liver disease (MASLD). The guidelines also expanded support for GLP-1-class medications in people with type 1 diabetes, which is a new development for 2026.

**Kidney disease guidance updated**
New guidance addresses glucose-lowering therapy choices for patients with chronic kidney disease, including those on dialysis. Combined use of SGLT2 inhibitors with nonsteroidal mineralocorticoid receptor antagonists (nsMRAs) may be considered for specific patients with elevated urine albumin-to-creatinine ratios, in conjunction with an RAS inhibitor. GLP-1-based therapy may also be continued or started in dialysis patients to help reduce cardiovascular risk.

**Blood pressure targets**
The guidelines reaffirm a blood pressure target below 130/80 mmHg for most adults with diabetes, with lower systolic targets considered when they can be achieved safely.

**Perioperative glycemic guidance (new)**
For elective surgery, an A1C goal below 8% within three months of the procedure is now recommended, along with a perioperative blood glucose target range of 100–180 mg/dL.

**Pediatric and prevention updates**
Updated nutrition and psychosocial screening guidance was added for children and adolescents with type 1 or type 2 diabetes. For diabetes *prevention*, the guidelines now emphasize eating patterns with the strongest supporting evidence — specifically Mediterranean and low-carbohydrate patterns — and note that certified diabetes-prevention programs can be delivered through smartphone apps, web platforms, or telehealth.

## General Care Framework (Stable Guidance)

- Diabetes care should follow a person-centered, team-based model integrating long-term management of diabetes alongside related conditions (cardiovascular, kidney, liver), with ongoing shared goal-setting between the care team and the patient.
- CGM is recommended at diagnosis and at any point thereafter for people on insulin, people on non-insulin medications that carry hypoglycemia risk, or anyone for whom CGM would meaningfully aid management — individualized to patient preference and circumstances.
- Routine monitoring (e.g., kidney function, foot checks for those with prior ulcers/amputations/sensory loss) should occur at a frequency appropriate to the patient's risk factors and current medications.

## Important Notes — Read Before Deploying

1. **This is a paraphrased summary, not the authoritative source.** The real ADA Standards of Care document runs to hundreds of pages with full evidence grading, dosing detail, and population-specific nuance. This summary should not be the sole basis for an AI system giving clinical guidance to real patients.
2. **Copyright:** The ADA's full Standards of Care text is copyrighted. Don't scrape or bulk-ingest the full PDF into your vector store without checking licensing terms — summaries like this one, written in original language, are safer to use as a starting point, but for production clinical use you likely need a licensed data source or a published open-access dataset.
3. **This assistant should not give individualized treatment recommendations.** Specific medication choices, dosing, and treatment plans depend on a patient's full history and should come from a licensed clinician — your guardrails layer should keep responses to general/reference information and explicitly redirect anything that sounds like "what should I personally do."
4. **Guidelines change annually.** Treat any ingested clinical content as needing a refresh cycle, not a one-time load.

## Suggested Disclaimer for Your Chat UI

Consider surfacing something like this near any clinical answer:
*"This information is for general reference only and reflects publicly summarized clinical guidelines. It is not personalized medical advice. Please consult a qualified healthcare provider for diagnosis or treatment decisions."*
