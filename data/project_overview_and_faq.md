# HealthTech RAG — Project Overview & FAQ

## What This Project Is

HealthTech RAG is an AI-powered internal knowledge assistant built for healthtech organizations. It uses Retrieval-Augmented Generation (RAG) combined with HyDE (Hypothetical Document Embeddings) to answer employee and stakeholder questions accurately, grounded in the company's own internal documents — rather than relying on a language model's general training knowledge alone.

The assistant is designed to be the first point of contact for questions about company policy, benefits, onboarding, engineering practices, IT security, product specifications, and relevant research — replacing manual searches through scattered documents, wikis, and PDFs with a single conversational interface.

## Project Goal

The core goal of this project is to make internal organizational knowledge instantly accessible and trustworthy. Specifically, the system aims to:

- Reduce the time employees spend searching for policy or process information
- Ensure answers are grounded in the company's actual, current documentation (not guesses)
- Provide a consistent, auditable source of truth across HR, engineering, IT security, and product teams
- Apply guardrails so that sensitive topics (medical data, compensation, security policy) are handled carefully and within scope
- Maintain a full audit trail of queries and responses for compliance and review

## How It Works

The system follows a Retrieval-Augmented Generation pipeline with several stages:

1. **Ingestion** — Source documents (markdown files, policies, specs, research notes) are loaded, cleaned, and chunked into retrievable passages.
2. **Embedding** — Each chunk is converted into a vector representation using a sentence-transformer embedding model (`all-MiniLM-L6-v2`), capturing semantic meaning rather than just keywords.
3. **Vector Storage** — Embeddings are persisted in a vector database (Chroma), allowing fast similarity search across the full document collection.
4. **HyDE Retrieval** — Rather than embedding the raw user query directly, the system first generates a *hypothetical answer* to the question, embeds that hypothetical answer, and uses it to search the vector store. This typically produces more relevant matches than searching with the bare question alone, especially for short or ambiguous queries.
5. **Retrieval** — The most relevant document chunks are pulled from the vector store based on similarity to the HyDE-generated embedding.
6. **Generation** — A language model (served locally via Ollama) synthesizes a final answer using only the retrieved context, reducing hallucination and keeping answers grounded in real source material.
7. **Guardrails** — Responses pass through a guardrails layer that checks for scope (e.g., the assistant should not give individualized medical advice), sensitive-topic handling, and policy compliance before being returned to the user.
8. **Audit Logging** — Every query and response is logged for traceability, supporting compliance reviews and quality monitoring over time.

## What Topics Can I Ask About?

The assistant can answer questions grounded in the documents currently loaded into its knowledge base, which typically include:

- **Company handbook** — general policies, culture, and expectations
- **HR onboarding** — new hire processes, paperwork, first-week guidance
- **Benefits overview** — health coverage, leave policy, perks
- **Salary guidelines** — compensation bands and review processes
- **Engineering guidelines** — coding standards, review process, deployment practices
- **IT security policy** — acceptable use, data handling, access control
- **Medical data policy** — how sensitive health data is collected, stored, and protected
- **Product specifications** — details on product features and roadmaps
- **Research notes** — background research relevant to the RAG system itself

If a question falls outside the loaded knowledge base, the assistant should say so rather than guessing.

## Example Questions a User Might Ask

- "What is this assistant for?"
- "How do I get started with onboarding?"
- "What benefits am I eligible for?"
- "What's our policy on handling patient data?"
- "What are the engineering code review standards?"
- "How is sensitive medical information protected in this system?"
- "What's the salary review process?"
- "What is HyDE and why does this assistant use it?"
- "Is my data safe when I use this chatbot?"
- "Who built this project and why?"

## Technical Architecture (Summary)

| Component | Role |
|---|---|
| FastAPI | Backend API serving chat and health endpoints |
| Redis | Caching layer for performance and session data |
| ChromaDB | Vector database storing document embeddings |
| Ollama | Local LLM inference for response generation |
| sentence-transformers | Embedding model for semantic search |
| spaCy | NLP preprocessing for ingestion |
| Next.js | Frontend chat interface |
| JWT Auth | Secures API access; tokens expire and require re-login |

## Data Privacy & Security

This system is built with healthtech sensitivities in mind:

- Access to the assistant requires authentication (JWT-based).
- A dedicated guardrails layer restricts the assistant from providing individualized medical diagnoses or advice — it surfaces policy and reference information only.
- An audit module logs interactions for compliance review.
- Medical and personal data handling follows the internal medical data policy, which governs storage, retention, and access control for sensitive records.

## Limitations & Disclaimers

- This assistant is an internal knowledge tool. It is **not** a substitute for professional medical advice, diagnosis, or treatment. Any health-related answers reflect internal policy documentation only, not clinical guidance.
- Answers are only as accurate and current as the documents loaded into the system. If source documents are outdated, answers may be too.
- The assistant will not speculate beyond its retrieved context. If it doesn't have relevant information, it should say so rather than fabricate an answer.

## Frequently Asked Questions

**Q: What is HealthTech RAG?**
A: It's an internal AI assistant that answers questions by retrieving information from the company's own documents and generating grounded responses, rather than relying purely on general AI knowledge.

**Q: What does "RAG" mean?**
A: Retrieval-Augmented Generation — a technique where the AI first retrieves relevant documents, then generates an answer based on that retrieved content.

**Q: What does "HyDE" mean?**
A: Hypothetical Document Embeddings — a retrieval technique where the system generates a hypothetical answer to a query first, then uses that to search for real matching documents, often improving retrieval accuracy.

**Q: Can I ask it for medical advice?**
A: It can share information from internal medical data policy and related documentation, but it is not a clinical tool and should not be used for diagnosis or treatment decisions. Always consult a qualified professional for medical concerns.

**Q: Is my conversation private?**
A: All interactions are logged for audit and compliance purposes as part of the system's design. Access requires authentication.

**Q: What should I do if the assistant gives an error or can't answer?**
A: Try rephrasing your question. If the issue persists (e.g., authentication errors), contact your system administrator — session tokens expire periodically and may require logging in again.

**Q: Who maintains this system?**
A: The internal engineering team responsible for the HealthTech RAG platform, following the engineering guidelines and deployment practices documented internally.
