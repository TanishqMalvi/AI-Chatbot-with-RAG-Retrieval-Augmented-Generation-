"""Tests for retrieval utilities (ACL filter, metrics)."""

from __future__ import annotations

import pytest

from app.retrieval.retriever import RetrievedChunk, _build_acl_filter, rerank
from eval.evaluator import recall_at_k, reciprocal_rank, token_f1

# ---------------------------------------------------------------------------
# ACL filter construction
# ---------------------------------------------------------------------------


class TestACLFilter:
    def test_single_role(self):
        f = _build_acl_filter(["hr-team"])
        # Should include hr-team and all-employees
        assert f is not None
        assert "$or" in f or "access_tags" in f

    def test_all_employees_included(self):
        f = _build_acl_filter(["engineering"])
        # The filter must always include all-employees tag
        filter_str = str(f)
        assert "all-employees" in filter_str

    def test_empty_roles(self):
        f = _build_acl_filter([])
        # Even with no roles, all-employees tag must be checked
        assert f is not None
        filter_str = str(f)
        assert "all-employees" in filter_str

    def test_multiple_roles(self):
        f = _build_acl_filter(["hr-team", "admin", "engineering"])
        # $or filter with multiple tags
        assert "$or" in f


# ---------------------------------------------------------------------------
# Reranker fallback
# ---------------------------------------------------------------------------


def test_rerank_fallback_sorts_by_score():
    """When cross-encoder is unavailable, rerank should fall back to score sorting."""
    chunks = [
        RetrievedChunk("c1", "text1", 0.5, {}),
        RetrievedChunk("c2", "text2", 0.9, {}),
        RetrievedChunk("c3", "text3", 0.3, {}),
    ]
    # Patch sentence_transformers to simulate unavailability
    import sys
    original = sys.modules.get("sentence_transformers")
    sys.modules["sentence_transformers"] = None  # type: ignore

    try:
        result = rerank("test query", chunks, top_n=2)
        assert result[0].chunk_id == "c2"  # Highest score first
        assert len(result) == 2
    finally:
        if original is None:
            del sys.modules["sentence_transformers"]
        else:
            sys.modules["sentence_transformers"] = original


def test_rerank_empty_chunks():
    result = rerank("test query", [], top_n=5)
    assert result == []


# ---------------------------------------------------------------------------
# Evaluation metrics
# ---------------------------------------------------------------------------


class TestTokenF1:
    def test_perfect_match(self):
        assert token_f1("hello world", "hello world") == 1.0

    def test_no_match(self):
        assert token_f1("foo bar", "hello world") == 0.0

    def test_partial_match(self):
        f1 = token_f1("hello there world", "hello world")
        assert 0.0 < f1 < 1.0

    def test_empty_prediction(self):
        assert token_f1("", "hello world") == 0.0

    def test_case_insensitive(self):
        assert token_f1("Hello World", "hello world") == 1.0


class TestRecallAtK:
    def test_all_retrieved(self):
        assert recall_at_k(["a", "b", "c"], ["a", "b"], k=10) == 1.0

    def test_none_retrieved(self):
        assert recall_at_k(["x", "y"], ["a", "b"], k=10) == 0.0

    def test_partial_retrieval(self):
        r = recall_at_k(["a", "x", "y"], ["a", "b"], k=10)
        assert r == 0.5

    def test_empty_relevant(self):
        assert recall_at_k(["a"], [], k=10) == 1.0

    def test_k_cutoff(self):
        # Relevant doc is at position 11 (beyond k=10)
        retrieved = [f"doc{i}" for i in range(15)]
        relevant = ["doc10"]  # index 10, position 11
        assert recall_at_k(retrieved, relevant, k=10) == 0.0


class TestMRR:
    def test_first_position(self):
        assert reciprocal_rank(["a", "b", "c"], ["a"]) == 1.0

    def test_second_position(self):
        assert reciprocal_rank(["x", "a", "b"], ["a"]) == pytest.approx(0.5)

    def test_not_found(self):
        assert reciprocal_rank(["x", "y", "z"], ["a"]) == 0.0

    def test_multiple_relevant(self):
        rr = reciprocal_rank(["x", "a", "b", "c"], ["b", "a"])
        assert rr == pytest.approx(0.5)  # "a" found at position 2
