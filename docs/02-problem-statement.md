# Problem Statement

## 1. Background

Modern software engineering projects generate and maintain a large
amount of technical information throughout the software development
lifecycle.

This information may exist across:

- Software requirement documents
- System architecture documents
- API specifications
- Development guidelines
- Coding standards
- Technical design documents
- Project documentation
- Deployment instructions
- Troubleshooting guides
- Source-code-related documentation
- Developer notes

As a software project grows, locating relevant information from these
documents becomes increasingly difficult.

Developers may need to manually search multiple documents before
finding the information required to understand a system, implement a
feature, investigate an issue, or make a technical decision.

---

## 2. Existing Problem

Traditional document search systems primarily depend on exact keyword
matching.

For example, a document may contain:

> "Apache Kafka is used for asynchronous communication between the
> Payment Service and Notification Service."

A developer may instead ask:

> "How does the Payment Service communicate with the Notification
> Service?"

Although both sentences represent the same information, they do not
contain exactly the same words.

A keyword-based search system may therefore provide incomplete or
poorly ranked results.

Semantic retrieval provides an alternative approach by representing
both documents and questions as numerical vector embeddings. Similar
meanings can therefore be identified even when different wording is
used.

---

## 3. Limitations of General-Purpose LLMs

Large Language Models can generate useful answers to general software
engineering questions.

However, a general-purpose LLM may not have access to:

- Private project documentation
- Organization-specific architecture
- Internal APIs
- Project-specific coding standards
- Recent requirement changes
- Internal design decisions
- Uploaded technical documents

If a question requires information that is not available to the model,
the generated response may be incomplete or unsupported by the
project's actual documentation.

For software engineering applications, it is therefore important to
connect answer generation with project-specific knowledge.

---

## 4. Research Problem

The central problem addressed by this project is:

> How can Retrieval-Augmented Generation be used to build an
> intelligent software engineering assistant that retrieves relevant
> information from project-specific technical documents and generates
> answers grounded in the retrieved evidence?

The project investigates the combination of:

1. Document processing
2. Text chunking
3. Vector embeddings
4. Semantic information retrieval
5. Vector databases
6. Large Language Models
7. Retrieval-Augmented Generation

---

## 5. Proposed Approach

The proposed system provides an AI-powered interface through which
software engineering documents can be uploaded and queried using
natural language.

The system performs two major operations.

### 5.1 Knowledge Ingestion

Uploaded documents are:

1. Validated
2. Stored
3. Converted into text
4. Cleaned
5. Divided into smaller chunks
6. Converted into vector embeddings
7. Indexed in a vector store
8. Associated with document metadata

### 5.2 Knowledge Retrieval and Answer Generation

When a user submits a question:

1. The question is converted into a vector embedding.
2. Semantic similarity search is performed.
3. The most relevant document chunks are retrieved.
4. Retrieved chunks are assembled into contextual information.
5. The question and context are supplied to a Large Language Model.
6. The model generates an answer using the supplied context.
7. The response includes references to the retrieved sources.

This architecture is known as Retrieval-Augmented Generation (RAG).

---

## 6. Research Motivation

The motivation for this project is to improve access to technical
knowledge within software engineering environments.

Instead of requiring developers to manually inspect multiple
documents, the proposed assistant allows them to interact with
technical documentation using natural-language questions.

The system is designed to investigate whether RAG can provide:

- Better access to project-specific knowledge
- Semantically relevant document retrieval
- Evidence-backed answers
- Improved traceability through source references
- Reduced dependence on the LLM's general knowledge
- Better handling of information unavailable to the base model

---

## 7. Research Objectives

### Primary Objective

To design and implement an AI-powered Software Engineering Assistant
using Retrieval-Augmented Generation for answering questions from
project-specific technical documents.

### Secondary Objectives

The project aims to:

- Develop a document ingestion pipeline.
- Extract and clean textual information from uploaded documents.
- Investigate text chunking for semantic retrieval.
- Generate vector embeddings from document chunks.
- Implement semantic similarity search.
- Integrate vector-storage technologies.
- Integrate an LLM with retrieved document context.
- Generate answers grounded in retrieved evidence.
- Provide references to the source documents.
- Measure retrieval and generation latency.
- Evaluate retrieval relevance.
- Evaluate answer correctness and groundedness.
- Compare RAG-based generation with an LLM-only baseline.
- Investigate the effect of retrieval parameters such as Top-K.
- Investigate the effect of chunking configuration.

---

## 8. Research Questions

The project can investigate the following research questions.

### RQ1

Does Retrieval-Augmented Generation improve answers to
project-specific software engineering questions compared with using
an LLM without retrieved project context?

### RQ2

How effectively can semantic vector search retrieve relevant
information from software engineering documents?

### RQ3

How does the number of retrieved chunks (Top-K) affect answer quality
and system performance?

### RQ4

How does document chunking affect retrieval quality?

### RQ5

How effectively does the RAG system avoid unsupported answers when
the requested information is absent from the indexed documents?

### RQ6

What are the retrieval and generation latency characteristics of the
implemented RAG architecture?

### RQ7

How do different vector-store implementations behave within the same
RAG architecture?

---

## 9. Scope

The current system focuses on textual software engineering knowledge.

Supported document formats currently include:

- PDF
- TXT
- Markdown

The system performs semantic retrieval over extracted textual
content.

The current implementation includes:

- React and TypeScript frontend
- FastAPI backend
- Sentence Transformer embeddings
- FAISS vector retrieval
- Astra DB vector retrieval
- SQLite metadata storage
- Groq-based LLM generation
- Source references
- Retrieval metrics

---

## 10. Limitations of the Current Scope

The current project does not attempt to replace developers or make
software engineering decisions autonomously.

The system acts as an information retrieval and question-answering
assistant.

The current prototype primarily focuses on textual documents and does
not yet provide complete semantic understanding of:

- Complex diagrams
- Images
- Video
- Audio
- Entire source-code repositories
- Runtime application state

These capabilities may be investigated as future extensions.

---

## 11. Expected Outcome

The expected outcome is a functional RAG-based Software Engineering
Assistant capable of:

1. Accepting software engineering documents.
2. Building a searchable semantic knowledge base.
3. Retrieving relevant information for natural-language questions.
4. Generating answers using retrieved context.
5. Showing evidence associated with generated answers.
6. Recording performance information for experimental analysis.

The final research evaluation will determine the effectiveness and
limitations of the proposed approach rather than assuming that RAG is
always superior to conventional LLM-based question answering.