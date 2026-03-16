# HealthTech RAG Chatbot Evaluation Framework

## Evaluation Configuration
- golden_set_version: "2025-Q1"
- num_qa_pairs: 30
- domains: ["hr", "product", "security", "compliance", "engineering"]
- metrics: ["recall_at_10", "mrr", "answer_f1", "hallucination_rate"]

---

*This YAML-formatted golden set is consumed by eval/evaluator.py*
*Full 200+ QA pair set is maintained in the internal data warehouse.*

## Sample QA Pairs (JSON below)
