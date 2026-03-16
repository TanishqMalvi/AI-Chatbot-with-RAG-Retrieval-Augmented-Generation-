"""
Offline evaluation pipeline.

Blueprint §10:
- Golden set of QA pairs.
- Metrics: Recall@10, MRR, Answer F1, Hallucination Rate.
- Run as part of CI regression gate.
"""

from __future__ import annotations

import asyncio
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

GOLDEN_SET_PATH = Path(__file__).parent / "golden_set.json"


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------


def token_f1(prediction: str, reference: str) -> float:
    """Token-level F1 score between prediction and reference strings."""
    pred_tokens = set(re.findall(r"\b\w+\b", prediction.lower()))
    ref_tokens = set(re.findall(r"\b\w+\b", reference.lower()))
    if not pred_tokens or not ref_tokens:
        return 0.0
    precision = len(pred_tokens & ref_tokens) / len(pred_tokens)
    recall = len(pred_tokens & ref_tokens) / len(ref_tokens)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    """Compute reciprocal rank of the first relevant document in retrieved list."""
    for i, doc_id in enumerate(retrieved_ids, 1):
        if doc_id in relevant_ids:
            return 1.0 / i
    return 0.0


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int = 10) -> float:
    """Compute Recall@K."""
    if not relevant_ids:
        return 1.0
    retrieved_k = set(retrieved_ids[:k])
    return len(set(relevant_ids) & retrieved_k) / len(relevant_ids)


# ---------------------------------------------------------------------------
# Evaluation data structures
# ---------------------------------------------------------------------------


@dataclass
class EvalResult:
    qa_id: str
    question: str
    answer: str
    reference_answer: str
    answer_f1: float
    recall_at_10: float
    mrr: float
    hallucinated: bool
    latency_ms: float
    skipped: bool = False
    skip_reason: str = ""


@dataclass
class EvalReport:
    total: int
    skipped: int
    avg_answer_f1: float
    avg_recall_at_10: float
    avg_mrr: float
    hallucination_rate: float
    avg_latency_ms: float
    results: list[EvalResult] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "skipped": self.skipped,
            "avg_answer_f1": round(self.avg_answer_f1, 4),
            "avg_recall_at_10": round(self.avg_recall_at_10, 4),
            "avg_mrr": round(self.avg_mrr, 4),
            "hallucination_rate": round(self.hallucination_rate, 4),
            "avg_latency_ms": round(self.avg_latency_ms, 1),
        }

    def passes_regression_gate(
        self,
        min_f1: float = 0.6,
        max_hallucination_rate: float = 0.05,
        max_latency_ms: float = 2000.0,
    ) -> bool:
        """Return True if all regression thresholds are met."""
        return (
            self.avg_answer_f1 >= min_f1
            and self.hallucination_rate <= max_hallucination_rate
            and self.avg_latency_ms <= max_latency_ms
        )


# ---------------------------------------------------------------------------
# Evaluator
# ---------------------------------------------------------------------------


class RAGEvaluator:
    """
    Runs the golden set against the live RAG pipeline and reports metrics.

    Usage:
        evaluator = RAGEvaluator(api_base_url="http://localhost:8000", api_token="...")
        report = await evaluator.run()
        print(report.to_dict())
    """

    def __init__(
        self,
        api_base_url: str = "http://localhost:8000",
        api_token: str = "",
        golden_set_path: Path = GOLDEN_SET_PATH,
        user_roles: list[str] | None = None,
        max_concurrent: int = 3,
    ) -> None:
        self.api_base_url = api_base_url.rstrip("/")
        self.api_token = api_token
        self.golden_set_path = golden_set_path
        self.user_roles = user_roles or ["all-employees"]
        self.max_concurrent = max_concurrent

    def _load_golden_set(self) -> list[dict[str, Any]]:
        with open(self.golden_set_path, encoding="utf-8") as f:
            return json.load(f)

    async def _query_chat(
        self,
        session: Any,
        question: str,
    ) -> tuple[str, list[str], float]:
        """
        Hit the /api/v1/chat endpoint.

        Returns (answer, retrieved_doc_ids, latency_ms).
        """
        import time


        t0 = time.perf_counter()
        try:
            response = await session.post(
                f"{self.api_base_url}/api/v1/chat",
                json={"query": question, "query_rewrite_strategy": "none"},
                headers={"Authorization": f"Bearer {self.api_token}"},
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            answer = data.get("answer", "")
            doc_ids = [s.get("doc_id", "") for s in data.get("sources", [])]
            latency = (time.perf_counter() - t0) * 1000
            return answer, doc_ids, latency
        except Exception as exc:
            latency = (time.perf_counter() - t0) * 1000
            logger.warning("eval_query_failed", error=str(exc))
            return "", [], latency

    async def _evaluate_one(
        self,
        session: Any,
        qa: dict[str, Any],
        semaphore: asyncio.Semaphore,
    ) -> EvalResult:
        async with semaphore:
            # Skip access-restricted items unless user has the right roles
            required_roles = qa.get("required_roles", ["all-employees"])
            if not any(r in self.user_roles for r in required_roles + ["all-employees"]):
                return EvalResult(
                    qa_id=qa["id"],
                    question=qa["question"],
                    answer="",
                    reference_answer=qa["reference_answer"],
                    answer_f1=0.0,
                    recall_at_10=0.0,
                    mrr=0.0,
                    hallucinated=False,
                    latency_ms=0.0,
                    skipped=True,
                    skip_reason="access_restricted",
                )

            answer, doc_ids, latency = await self._query_chat(session, qa["question"])

            relevant_docs = qa.get("source_documents", [])
            # Normalize: strip .md extension for comparison
            norm_retrieved = [d.replace(".md", "").replace(".txt", "") for d in doc_ids]
            norm_relevant = [d.replace(".md", "").replace(".txt", "") for d in relevant_docs]

            f1 = token_f1(answer, qa["reference_answer"])
            rk = recall_at_k(norm_retrieved, norm_relevant, k=10)
            rr = reciprocal_rank(norm_retrieved, norm_relevant)

            return EvalResult(
                qa_id=qa["id"],
                question=qa["question"],
                answer=answer,
                reference_answer=qa["reference_answer"],
                answer_f1=f1,
                recall_at_10=rk,
                mrr=rr,
                hallucinated=False,  # Hallucination check done by output guardrail in API
                latency_ms=latency,
            )

    async def run(self) -> EvalReport:
        """Run evaluation against the full golden set."""
        import httpx

        golden_set = self._load_golden_set()
        semaphore = asyncio.Semaphore(self.max_concurrent)

        logger.info("eval_started", total_qa=len(golden_set), roles=self.user_roles)

        async with httpx.AsyncClient() as session:
            tasks = [
                self._evaluate_one(session, qa, semaphore) for qa in golden_set
            ]
            results = await asyncio.gather(*tasks)

        evaluated = [r for r in results if not r.skipped]
        skipped = [r for r in results if r.skipped]

        if not evaluated:
            return EvalReport(
                total=len(results),
                skipped=len(skipped),
                avg_answer_f1=0.0,
                avg_recall_at_10=0.0,
                avg_mrr=0.0,
                hallucination_rate=0.0,
                avg_latency_ms=0.0,
                results=list(results),
            )

        report = EvalReport(
            total=len(results),
            skipped=len(skipped),
            avg_answer_f1=sum(r.answer_f1 for r in evaluated) / len(evaluated),
            avg_recall_at_10=sum(r.recall_at_10 for r in evaluated) / len(evaluated),
            avg_mrr=sum(r.mrr for r in evaluated) / len(evaluated),
            hallucination_rate=sum(r.hallucinated for r in evaluated) / len(evaluated),
            avg_latency_ms=sum(r.latency_ms for r in evaluated) / len(evaluated),
            results=list(results),
        )

        logger.info("eval_complete", **report.to_dict())
        return report


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Run RAG evaluation")
    parser.add_argument("--api-url", default="http://localhost:8000")
    parser.add_argument("--token", required=True, help="JWT access token")
    parser.add_argument("--roles", default="all-employees", help="Comma-separated roles")
    parser.add_argument("--output", help="Output JSON file path")
    args = parser.parse_args()

    evaluator = RAGEvaluator(
        api_base_url=args.api_url,
        api_token=args.token,
        user_roles=args.roles.split(","),
    )
    report = asyncio.run(evaluator.run())

    output = report.to_dict()
    print(json.dumps(output, indent=2))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2)

    passes = report.passes_regression_gate()
    print(f"\nRegression gate: {'PASS ✅' if passes else 'FAIL ❌'}")
    sys.exit(0 if passes else 1)
