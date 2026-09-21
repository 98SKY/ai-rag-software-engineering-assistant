# Viva Notes

## AI-Powered Intelligent Software Engineering Assistant Using RAG

---

# 1. 30-Second Project Introduction

> My project is an AI-Powered Intelligent Software Engineering
> Assistant using Retrieval-Augmented Generation, or RAG. The system
> allows software engineering documents to be uploaded and converted
> into vector embeddings. When a developer asks a question, the system
> performs semantic retrieval to find relevant document chunks and
> supplies those chunks as context to a Large Language Model. The LLM
> then generates an answer grounded in project-specific information,
> while the application also returns the retrieved sources and
> performance metrics.

---

# 2. One-Minute Project Explanation

> Traditional Large Language Models have general knowledge but may not
> know private or project-specific software engineering information.
> They can also generate unsupported information. My project addresses
> this using Retrieval-Augmented Generation.
>
> During ingestion, uploaded PDF, TXT or Markdown documents are
> processed, cleaned and divided into overlapping chunks. I generate
> 384-dimensional embeddings using the
> `all-MiniLM-L6-v2` Sentence Transformer model and store them in
> either FAISS or Astra DB.
>
> When the user asks a question, I generate a query embedding and
> perform semantic Top-K retrieval. The relevant chunks are added to
> the prompt and sent to the configured LLM through Groq. The response
> contains the generated answer, source references and retrieval and
> generation latency.
>
> The research evaluation compares retrieval quality, RAG versus an
> LLM-only baseline, unsupported-question behavior, chunking, Top-K,
> latency, and FAISS versus Astra.

---

# 3. Problem Statement

### Question

What problem are you solving?

### Answer

Software project knowledge is distributed across technical
documentation, architecture documents, requirements and other project
artifacts.

Developers often need project-specific answers quickly.

General-purpose LLMs may not have access to this private knowledge and
may generate plausible but unsupported answers.

The project investigates whether RAG can retrieve relevant
project-specific software engineering information and use it to
generate evidence-supported answers.

---

# 4. Why AI?

The problem involves understanding natural-language questions and
finding semantically relevant information.

AI techniques are used for:

```text
Semantic embeddings

Vector similarity search

Natural-language generation
```

The project therefore combines information retrieval and generative
AI.

---

# 5. What Is RAG?

RAG means:

```text
Retrieval-Augmented Generation
```

It combines:

```text
Information Retrieval
        +
Large Language Model Generation
```

Instead of asking the LLM to answer only from its internal knowledge,
the system first retrieves relevant external information and supplies
that evidence to the LLM.

---

# 6. Why RAG Instead of Only an LLM?

An LLM may not know:

```text
Private project documentation

Recent internal architecture

Organization-specific APIs

Project-specific coding standards
```

RAG allows this knowledge to be supplied dynamically.

It also provides source evidence that can be inspected.

---

# 7. Does RAG Eliminate Hallucination?

No.

RAG can reduce unsupported generation by providing relevant evidence,
but it does not guarantee that every generated claim is supported.

Therefore, the project separately evaluates:

```text
Retrieval quality

Correctness

Groundedness

Citation accuracy

Unsupported-question behavior
```

---

# 8. Complete Architecture

```text
React + TypeScript
        |
        v
FastAPI
        |
        v
RAG Service
        |
        +----------------+
        |                |
        v                v
Embedding Service   Retrieval Service
        |                |
        |         +------+------+
        |         |             |
        v         v             v
      MiniLM    FAISS          Astra
                        |
                        v
                  Retrieved Chunks
                        |
                        v
                    RAG Context
                        |
                        v
                    LLM Service
                        |
                        v
                       Groq
                        |
                        v
              Answer + Sources + Metrics
```

---

# 9. Technology Stack

### Frontend

```text
React
TypeScript
Vite
React Markdown
```

### Backend

```text
Python
FastAPI
SQLAlchemy
SQLite
```

### AI

```text
Sentence Transformers
all-MiniLM-L6-v2
PyTorch
NumPy
```

### Vector Storage

```text
FAISS
Astra DB
```

### LLM

```text
Groq
openai/gpt-oss-20b
```

---

# 10. Why React?

React provides a component-based frontend architecture suitable for:

```text
Document upload

Document listing

Chat interface

Source display

Retrieval metrics
```

TypeScript provides static typing for frontend API contracts.

---

# 11. Why FastAPI?

FastAPI fits the project because the AI and retrieval stack is
implemented in Python.

It provides:

```text
REST API development

Pydantic validation

Async-capable API framework

Automatic OpenAPI documentation
```

It also integrates naturally with Python AI libraries.

---

# 12. Why Not Spring Boot?

Spring Boot could also implement the API layer.

However, the embedding, FAISS and AI ecosystem used by this project is
Python-oriented.

Using FastAPI reduces integration complexity between the API and AI
components.

This is a technology choice for this implementation rather than a
claim that FastAPI is universally superior.

---

# 13. What Embedding Model Do You Use?

```text
sentence-transformers/all-MiniLM-L6-v2
```

The output dimension is:

```text
384
```

---

# 14. What Is an Embedding?

An embedding is a numerical representation of text.

Example:

```text
"Kafka is used for asynchronous communication"

        ↓ Embedding Model

[0.021, -0.081, ..., 0.043]

        384 dimensions
```

Semantically related text should be represented relatively close in
the embedding space according to the selected model.

---

# 15. Why Semantic Search Instead of Keyword Search?

Keyword search depends strongly on exact terms.

For example:

Document:

```text
Apache Kafka is used for asynchronous communication.
```

Question:

```text
How do the services exchange messages?
```

The wording is different even though the concepts are related.

Semantic embeddings allow retrieval based on meaning rather than only
exact word matching.

---

# 16. What Is Chunking?

Chunking divides a large document into smaller searchable sections.

Current configuration:

```text
chunk_size = 1000 characters
chunk_overlap = 200 characters
```

Each chunk is independently embedded.

---

# 17. Why Use Overlap?

Overlap helps preserve context around chunk boundaries.

Without overlap:

```text
Chunk 1:
The Payment Service communicates

Chunk 2:
using Apache Kafka...
```

Important information may be separated.

Overlap preserves some information between neighboring chunks.

---

# 18. What Is Top-K?

Top-K is the number of highest-ranked chunks requested from semantic
retrieval.

Current default:

```text
K = 5
```

The project plans to experimentally compare values such as:

```text
1
3
5
10
```

---

# 19. What Is FAISS?

FAISS is used as the local vector-search implementation.

The project uses:

```text
IndexFlatIP
```

with normalized embeddings.

The index contains 384-dimensional vectors.

---

# 20. Why IndexFlatIP?

The embeddings are normalized.

For unit-normalized vectors, inner-product ranking corresponds to
cosine-similarity-style ranking.

`IndexFlatIP` also performs exact search over the stored vectors,
which is appropriate for the current research-scale corpus.

---

# 21. What Is Astra DB?

Astra DB provides the project's cloud vector-storage alternative.

The current collection stores:

```text
Chunk ID

Document ID

Filename

Chunk index

Content

384-dimensional vector
```

Semantic search can therefore return both similarity information and
chunk metadata.

---

# 22. Why Both FAISS and Astra?

Supporting both allows the project to study two vector-storage
approaches.

FAISS represents a local vector index.

Astra represents a managed remote vector database.

The architecture abstracts them so the RAG layer receives a common
retrieval result.

---

# 23. FAISS vs Astra Architecture

FAISS:

```text
Vector
  |
  v
FAISS Position
  |
  v
SQLite Mapping
  |
  v
Chunk Metadata
```

Astra:

```text
Vector Search
    |
    v
Vector + Chunk Metadata
```

This is one of the important architectural differences in the
implementation.

---

# 24. Can You Compare FAISS and Astra Similarity Scores Directly?

Not reliably as a universal confidence measure.

Even when retrieval ranking is similar, different backends can expose
different numerical score behavior.

Therefore, I compare them primarily using:

```text
Relevant evidence retrieved

Rank

Hit Rate

Precision

Recall

MRR

Latency
```

rather than simply comparing raw score magnitudes.

---

# 25. What Is SQLite Used For?

SQLite stores structured application metadata.

Examples:

```text
Documents

Document chunks

Filename

Chunk count

Chunk content

FAISS mapping
```

---

# 26. Explain Document and DocumentChunk

The relationship is:

```text
Document
    |
    | one-to-many
    |
    v
DocumentChunk
```

One uploaded document can produce multiple chunks.

Each chunk belongs to one document.

---

# 27. Difference Between chunk_index and faiss_index

`chunk_index` means:

```text
Position of chunk inside its document
```

`faiss_index` means:

```text
Position of its vector inside FAISS
```

They are different concepts.

---

# 28. Explain Document Ingestion

```text
Upload Document
      ↓
Validate
      ↓
Extract Text
      ↓
Clean Text
      ↓
Create Chunks
      ↓
Generate Embeddings
      ↓
Store Vectors
      ↓
Store Metadata
      ↓
Document Ready
```

---

# 29. Explain Query Processing

```text
User Question
      ↓
Generate Query Embedding
      ↓
Semantic Search
      ↓
Retrieve Top-K Chunks
      ↓
Build Context
      ↓
Send Context + Question to LLM
      ↓
Generate Answer
      ↓
Return Answer + Sources + Metrics
```

---

# 30. What Is the Retrieval Service?

The Retrieval Service is responsible for finding relevant chunks.

It:

```text
Embeds the question

Selects configured vector store

Executes semantic search

Returns normalized RetrievedChunk objects
```

---

# 31. What Is the RAG Service?

The RAG Service orchestrates the complete question-answering process.

It performs:

```text
Retrieval

Context construction

LLM generation

Source mapping

Latency measurement
```

---

# 32. Retrieval Service vs RAG Service

Retrieval Service:

> Which document chunks are relevant?

RAG Service:

> Use those chunks to construct evidence and generate the final
> response.

This separation improves modularity.

---

# 33. What Is the Vector Store Factory?

The Vector Store Factory abstracts indexing based on:

```text
VECTOR_STORE
```

Supported configurations:

```text
faiss
astra
```

This prevents upload logic from containing duplicated backend-specific
vector-store code.

---

# 34. What Does Your LLM Prompt Do?

The LLM is instructed to:

```text
Use only retrieved context

Avoid inventing facts

Indicate insufficient information when necessary

Keep answers technically accurate

Reference sources where useful
```

This supports evidence-grounded generation.

---

# 35. Main API Endpoint

The main RAG endpoint is:

```text
POST /api/v1/ask
```

Example request:

```json
{
  "question": "How does the Payment Service communicate with the Notification Service?",
  "top_k": 5
}
```

---

# 36. What Does `/ask` Return?

It returns:

```text
Question

Generated answer

Retrieved sources

Top retrieval score

Requested Top-K

Chunks retrieved

Retrieval latency

Generation latency

Total latency
```

---

# 37. Why Return Sources?

Sources provide:

```text
Traceability

User verification

Debugging

Retrieval evaluation

Citation analysis
```

They allow the generated answer to be connected to retrieved evidence.

---

# 38. Why Don't You Return `grounded=true`?

Because successful retrieval does not prove that the final answer is
fully grounded.

The LLM can still add an unsupported statement.

Groundedness therefore needs separate evaluation.

---

# 39. How Do You Evaluate Retrieval?

Using:

```text
Hit Rate@K

Precision@K

Recall@K

MRR
```

with manually labelled relevant evidence.

---

# 40. Explain Precision@K

```text
Precision@K =
Relevant chunks retrieved in Top-K
----------------------------------
K
```

It measures how much of the retrieved context is relevant.

---

# 41. Explain Recall@K

```text
Recall@K =
Relevant chunks retrieved
--------------------------
Total known relevant chunks
```

It measures how much of the known relevant evidence was found.

---

# 42. Explain MRR

MRR means:

```text
Mean Reciprocal Rank
```

For one question:

```text
RR =
1 / rank of first relevant result
```

If the relevant result is rank 1:

```text
RR = 1
```

If rank 2:

```text
RR = 0.5
```

MRR averages this across questions.

---

# 43. How Do You Evaluate Answer Quality?

Using:

```text
Correctness

Groundedness

Relevance

Citation accuracy
```

Unsupported questions are evaluated separately for abstention
behavior.

---

# 44. What Is Groundedness?

Groundedness measures whether factual claims in the generated answer
are supported by the retrieved evidence.

An answer can be linguistically good but still have poor groundedness
if it contains unsupported claims.

---

# 45. How Do You Test Hallucination?

I include questions where the indexed corpus intentionally does not
contain sufficient information.

The system should indicate insufficient evidence rather than invent an
answer.

I also inspect whether generated factual claims are supported by
retrieved chunks.

---

# 46. What Is Your Baseline?

The primary baseline is:

```text
Same LLM
+
Same Questions
+
No Retrieved Project Context
```

This is compared with:

```text
Same LLM
+
Same Questions
+
RAG Context
```

This helps isolate the effect of retrieval augmentation.

---

# 47. What Is the Independent Variable in the RAG Comparison?

For the primary LLM-only vs RAG comparison, the major changed
condition is:

```text
Availability of retrieved project-specific context
```

Other important settings should remain as consistent as practical.

---

# 48. What Top-K Values Will You Evaluate?

Recommended:

```text
K = 1
K = 3
K = 5
K = 10
```

The purpose is to measure the relationship between retrieval coverage,
irrelevant context and latency.

---

# 49. How Will You Evaluate Chunk Size?

Example configurations:

```text
500 / 100 overlap

1000 / 200 overlap

1500 / 300 overlap
```

For each configuration I can measure retrieval and answer-quality
metrics.

---

# 50. What Latency Do You Measure?

The API measures:

```text
Retrieval time

Generation time

Total time
```

This helps separate retrieval overhead from LLM generation latency.

---

# 51. Why Can the First Request Be Slow?

The embedding model is cached.

The first request may need to load the model, producing a cold-start
cost.

Later requests can reuse the loaded model.

Therefore, performance experiments should account for warm-up or
report cold starts separately.

---

# 52. What Real Problem Did You Encounter?

One important problem occurred because FAISS and SQLite are persisted
independently.

At one development stage:

```text
FAISS = 18 vectors

SQLite = 9 chunks
```

Some vector positions therefore had no valid metadata mapping.

After resetting both consistently:

```text
FAISS = 9

SQLite chunks = 9

Mapped = 9
```

retrieval mapping worked correctly.

---

# 53. What Did You Learn From That Problem?

A RAG system is not only an LLM integration problem.

It also requires reliable:

```text
Data ingestion

Vector persistence

Metadata mapping

Consistency

Failure recovery
```

The issue motivated future work around indexing status, reconciliation,
idempotent ingestion and re-indexing.

---

# 54. What Happens If Astra Insert Succeeds but SQLite Fails?

The vector store and SQLite do not share one distributed transaction.

Therefore, an Astra record could remain without corresponding
application metadata.

A future solution could use:

```text
Compensating deletion

Retry

Indexing state

Reconciliation
```

---

# 55. Why Is Your Project an M.Tech Research Project and Not Just a Chatbot?

The contribution is not simply the chat interface.

The project implements and evaluates a configurable RAG pipeline for
software-engineering knowledge.

Research variables include:

```text
RAG vs LLM-only

Top-K

Chunk size

Retrieval effectiveness

Groundedness

Unsupported questions

FAISS vs Astra

Latency
```

The objective is to experimentally analyze the behavior of the
architecture.

---

# 56. What Is Novel or Significant About the Project?

A careful answer is:

> The project does not claim to invent RAG itself. Its contribution is
> the design, implementation and experimental evaluation of a
> developer-oriented RAG assistant over project-specific software
> engineering knowledge, including retrieval evaluation, evidence
> traceability, unsupported-question behavior and configurable vector
> backends.

---

# 57. What Are the Main Limitations?

Major limitations include:

```text
Limited evaluation corpus

Simple character-based chunking

Single embedding model

No reranking

No hybrid retrieval

No full distributed transaction

Limited conversational memory

External LLM dependency

Limited source-code understanding

No complete enterprise authentication
```

---

# 58. What Is the Most Important Future Improvement?

One strong direction is:

```text
Hybrid Retrieval
+
Reranking
+
Evidence Verification
```

A future pipeline could be:

```text
Question
   ↓
Vector + Keyword Retrieval
   ↓
Reranker
   ↓
Best Evidence
   ↓
LLM
   ↓
Claim Verification
   ↓
Answer
```

---

# 59. Could You Add Source Code?

Yes.

Instead of character-based document chunks, source code could be
parsed into logical units such as:

```text
Class

Method

Function

Module
```

Embeddings and metadata could then support questions about actual
implementation.

---

# 60. Could This Be Used in an Enterprise?

The architecture provides a foundation, but production deployment
would require additional capabilities such as:

```text
Authentication

Authorization

Document-level access control

Encryption

Audit logging

Secret management

Scalable ingestion

Document lifecycle management

Monitoring
```

---

# 61. Demonstration Flow

For the final demo, use this order:

```text
1. Explain the problem

2. Show architecture

3. Start frontend and backend

4. Show existing knowledge-base documents

5. Upload a controlled technical document

6. Show successful indexing

7. Ask a supported question

8. Show answer

9. Show retrieved source

10. Show similarity and latency metrics

11. Ask a paraphrased question

12. Show semantic retrieval

13. Ask an unsupported question

14. Show abstention behavior

15. Explain FAISS/Astra switch

16. Show evaluation results
```

---

# 62. Strong Demo Question

With the controlled Payment Service document:

```text
How does the Payment Service communicate with the Notification
Service?
```

Expected evidence:

```text
Apache Kafka
```

Then ask a paraphrased version:

```text
Which technology enables asynchronous messaging between the payment
and notification services?
```

This demonstrates semantic retrieval rather than exact keyword
matching.

---

# 63. Unsupported Demo Question

Example:

```text
Which cloud provider hosts the Payment Service?
```

if the controlled document does not specify a cloud provider.

The desired behavior is to explain that the available documents do
not provide sufficient information.

---

# 64. If Examiner Asks "Why Not ChatGPT Directly?"

Answer:

> A general chatbot may not have access to private project-specific
> documentation. My system retrieves relevant information from the
> organization's indexed knowledge base at query time and supplies
> that evidence to the LLM. It can also expose which project sources
> were retrieved.

---

# 65. If Examiner Asks "Why Not Fine-Tuning?"

Answer:

> The goal is primarily to provide dynamic project knowledge rather
> than change the model's general behavior. RAG allows documents to be
> updated and retrieved without retraining the LLM. Fine-tuning and
> RAG solve different problems and could also be combined in future
> work.

---

# 66. If Examiner Asks "What Happens When a New Document Is Added?"

Answer:

```text
Upload
 ↓
Extract
 ↓
Clean
 ↓
Chunk
 ↓
Embed
 ↓
Index
 ↓
Available for Retrieval
```

The LLM itself does not need to be retrained.

---

# 67. If Examiner Asks "Where Is AI Used?"

Answer:

AI is primarily used in two places:

```text
Embedding model
    ->
Semantic representation and retrieval

Large Language Model
    ->
Natural-language answer generation
```

Vector search then operates over the embedding representations.

---

# 68. If Examiner Asks "What Is Your Main Contribution?"

Answer:

> My main contribution is an end-to-end, modular RAG architecture for
> project-specific software engineering knowledge, together with an
> evaluation framework that separates retrieval quality, generation
> quality and system performance.

---

# 69. If Examiner Asks "What Would You Do With More Time?"

Answer:

> I would expand the evaluation corpus, add source-code-aware
> ingestion, hybrid retrieval and reranking, introduce claim-level
> evidence verification, improve conversational retrieval, and
> strengthen vector/metadata consistency and enterprise security.

---

# 70. Five Points to Remember

If time is limited before the viva, remember these five points:

### 1. Problem

```text
LLMs do not automatically know private project knowledge.
```

### 2. Solution

```text
Retrieve project evidence before generation.
```

### 3. Pipeline

```text
Document
→ Chunk
→ Embed
→ Vector Store
→ Retrieve
→ LLM
→ Answer + Source
```

### 4. Research

```text
Evaluate retrieval + generation + performance.
```

### 5. Key Limitation

```text
RAG improves access to evidence but does not guarantee
hallucination-free answers.
```

---

# 71. Final Viva Closing Statement

> This project demonstrates that building a reliable software
> engineering assistant involves more than connecting an LLM to a
> user interface. The system requires document processing, semantic
> embeddings, vector retrieval, metadata management, context
> construction, evidence traceability and systematic evaluation.
> The implemented architecture provides a working foundation for
> studying how Retrieval-Augmented Generation can support
> project-specific software engineering knowledge.