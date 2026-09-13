
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
