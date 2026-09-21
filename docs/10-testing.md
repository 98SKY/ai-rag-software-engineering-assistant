# Testing Strategy

## 1. Introduction

Testing is an important part of the AI-Powered Software Engineering
Assistant because the application combines traditional software
components with AI-based retrieval and generation components.

Unlike a conventional CRUD application, testing this system requires
verification at multiple levels:

```text
Traditional Software Testing
            +
AI / Retrieval Testing
            +
RAG Behavior Testing
```

The testing strategy therefore covers:

- Document processing
- Text cleaning
- Chunking
- Embedding generation
- Vector indexing
- Semantic retrieval
- Database persistence
- REST APIs
- RAG orchestration
- LLM integration
- Source mapping
- Unsupported questions
- Frontend behavior
- Error handling
- Regression scenarios

---

# 2. Testing Objectives

The main testing objectives are:

1. Verify that documents are correctly processed.
2. Verify that text is converted into valid chunks.
3. Verify that embeddings have the expected format.
4. Verify that vector stores correctly index and retrieve chunks.
5. Verify that metadata remains associated with vectors.
6. Verify that API endpoints return valid responses.
7. Verify that the RAG pipeline generates answers using retrieved context.
8. Verify that source references correspond to retrieved chunks.
9. Verify that unsupported questions are handled appropriately.
10. Verify that frontend and backend communicate correctly.
11. Detect regressions in previously working functionality.
12. Verify important failure scenarios.

---

# 3. Testing Levels

The system is tested at several levels.

```text
                     Testing
                        |
        +---------------+---------------+
        |               |               |
        v               v               v
      Unit          Integration      End-to-End
      Tests            Tests            Tests
        |
        +-------------------------------+
                        |
                        v
                 RAG Evaluation
```

These levels serve different purposes.

---

# 4. Unit Testing

Unit tests verify individual functions or modules independently.

Important candidates include:

```text
Text cleaning

Chunk generation

Embedding generation

Vector-store configuration

Request validation

Retrieval-result mapping
```

Unit tests should be deterministic whenever possible.

---

# 5. Text Cleaning Tests

The text-cleaning function removes unwanted extraction artifacts.

Example input:

```text
"Payment   Service\x00 uses Kafka.\n\n\nNotification Service"
```

Expected cleaned result should remove the null/control character,
normalize unnecessary spaces and reduce excessive line breaks.

A conceptual test is:

```python
def test_clean_text_removes_control_characters():
    raw_text = "Payment\x00 Service"
    cleaned = clean_text(raw_text)

    assert "\x00" not in cleaned
```

Another test:

```python
def test_clean_text_reduces_excessive_newlines():
    raw_text = "Line 1\n\n\n\nLine 2"
    cleaned = clean_text(raw_text)

    assert "\n\n\n" not in cleaned
```

---

# 6. Chunking Tests

Chunking is critical because retrieved evidence is based on document
chunks.

Current configuration:

```text
chunk_size = 1000
chunk_overlap = 200
```

Tests should verify:

- Chunks are created.
- Chunk sizes follow the configured strategy.
- Adjacent chunks preserve overlap.
- Empty chunks are not produced unnecessarily.
- Short documents remain valid.

Example conceptual test:

```python
def test_short_document_creates_chunk():
    text = "Short technical document."

    chunks = chunk_text(text)

    assert len(chunks) >= 1
    assert "Short technical document." in chunks[0]
```

---

# 7. Chunk Overlap Test

Suppose:

```text
chunk_size = 1000
chunk_overlap = 200
```

The next chunk should preserve some content from the previous chunk.

Conceptually:

```text
Chunk 1
|--------------------------|

                    | overlap |

                    |--------------------------|
                              Chunk 2
```

Testing overlap helps detect regressions where important boundary
context could accidentally be removed.

---

# 8. PDF Extraction Testing

PDF processing should be tested using known PDF fixtures.

The test should verify that:

```text
PDF
 ↓
Text Extraction
 ↓
Non-empty expected content
```

For a controlled PDF containing:

```text
Apache Kafka is used for event communication.
```

the extraction test should confirm that the expected text is present
after extraction.

The test should not depend on arbitrary external PDFs whose contents
can change.

---

# 9. TXT and Markdown Extraction

Plain text and Markdown files should also be tested.

Example fixture:

```text
test_document.txt
```

containing:

```text
The Payment Service is implemented using Spring Boot.

Apache Kafka is used for asynchronous communication between
the Payment Service and Notification Service.

Redis is used to cache frequently requested payment status data.

The service is deployed using Docker and Kubernetes.
```

The extraction result should contain the same meaningful content.

---

# 10. Embedding Service Testing

The embedding service uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The expected embedding dimension is:

```text
384
```

A basic test is:

```python
def test_embedding_dimension():
    embedding = generate_embedding(
        "Kafka is used for asynchronous messaging."
    )

    assert embedding.shape == (384,)
```

---

# 11. Embedding Data Type

The current vector implementation expects:

```text
float32
```

Therefore:

```python
def test_embedding_dtype():
    embedding = generate_embedding("Test")

    assert str(embedding.dtype) == "float32"
```

This is especially relevant for FAISS compatibility.

---

# 12. Embedding Normalization

The current embedding service requests normalized embeddings.

A normalized vector should have a norm approximately equal to:

```text
1.0
```

Conceptually:

```python
import numpy as np

def test_embedding_is_normalized():
    embedding = generate_embedding("Kafka messaging")

    norm = np.linalg.norm(embedding)

    assert np.isclose(norm, 1.0, atol=1e-5)
```

This validates an important assumption used by the FAISS
`IndexFlatIP` configuration.

---

# 13. Batch Embedding Testing

Document ingestion uses batch embedding generation.

The test should verify:

```text
3 chunks
   ↓
generate_embeddings()
   ↓
3 embeddings
```

with shape:

```text
(3, 384)
```

Example:

```python
def test_batch_embeddings():
    texts = [
        "Kafka messaging",
        "Redis caching",
        "Kubernetes deployment",
    ]

    embeddings = generate_embeddings(texts)

    assert embeddings.shape == (3, 384)
```

---

# 14. Empty Batch Test

The embedding service should safely handle an empty input list.

Expected shape:

```text
(0, 384)
```

This prevents downstream vector-store code from attempting to index
invalid input.

---

# 15. FAISS Unit Testing

The FAISS layer should verify:

- Index creation
- Correct dimension
- Embedding insertion
- Index persistence
- Index loading
- Vector count

Example conceptual test:

```python
index = create_index()

assert index.d == 384
assert index.ntotal == 0
```

After adding three vectors:

```text
index.ntotal = 3
```

should hold.

---

# 16. FAISS Persistence Test

A persistence test can:

```text
Create Index
     ↓
Add Vectors
     ↓
Save Index
     ↓
Reload Index
     ↓
Verify Vector Count
```

This ensures the local index survives application restarts.

Tests should use a temporary test path rather than modifying the
developer's main FAISS index.

---

# 17. Astra Integration Testing

Astra testing is an integration test because it communicates with an
external cloud service.

The test can:

```text
Create controlled chunk
        ↓
Generate embedding
        ↓
Insert into test collection
        ↓
Query related text
        ↓
Verify chunk appears in results
```

For example:

```text
Indexed:

"Apache Kafka is used for asynchronous communication."

Query:

"How do services communicate asynchronously?"
```

The test should verify that the expected chunk is present in the
retrieved result set.

---

# 18. Separate Test Data

Tests should not pollute the normal project knowledge base.

Where practical, use:

```text
Test database

Test vector index

Test Astra collection

Test document fixtures
```

rather than production/development data.

For example:

```text
software_engineering_chunks_test
```

could be used for integration testing.

---

# 19. Vector Store Factory Testing

The Vector Store Factory should be tested for supported
configurations.

Example:

```text
VECTOR_STORE=faiss
```

should select FAISS behavior.

```text
VECTOR_STORE=astra
```

should select Astra behavior.

An invalid configuration such as:

```text
VECTOR_STORE=unknown
```

should produce a clear error rather than silently selecting an
unexpected backend.

---

# 20. Retrieval Service Testing

The retrieval service is one of the most important modules.

A controlled retrieval test should use known documents and questions.

Example indexed content:

```text
Chunk A:
Kafka is used for asynchronous service communication.

Chunk B:
Redis caches frequently requested payment status.

Chunk C:
Kubernetes is used for deployment.
```

Question:

```text
How do services communicate asynchronously?
```

Expected behavior:

```text
Chunk A
```

should appear among the highest-ranked results.

---

# 21. Retrieval Result Structure

The retrieval service should consistently return:

```text
chunk_id
document_id
filename
chunk_index
content
score
```

regardless of whether the active backend is:

```text
FAISS
```

or:

```text
Astra
```

This tests the vector-store abstraction.

---

# 22. Top-K Retrieval Testing

For:

```text
top_k = 3
```

the retrieval service should return at most three valid chunks.

The test should also cover cases where fewer than three chunks exist.

For example:

```text
Indexed chunks = 2
Requested K    = 5

Returned <= 2
```

This verifies correct behavior for small knowledge bases.

---

# 23. Retrieval Ranking Test

A semantic retrieval test can verify that a clearly related chunk is
ranked above unrelated content.

Example:

```text
Query:

"How is payment status cached?"
```

Relevant chunk:

```text
Redis is used to cache frequently requested payment status data.
```

Unrelated chunk:

```text
The service is deployed using Docker and Kubernetes.
```

The Redis chunk should normally rank above the deployment chunk for
this controlled example.

Such tests should avoid overly ambiguous language.

---

# 24. Database Model Testing

Database tests should verify the relationship:

```text
Document
   |
   | one-to-many
   |
   v
DocumentChunk
```

For example:

```text
Create Document
      ↓
Create 3 Chunks
      ↓
Query Document
      ↓
Verify 3 Related Chunks
```

---

# 25. FAISS Mapping Test

When FAISS is active, every indexed chunk should have a valid:

```text
faiss_index
```

Example:

```text
Chunk A -> 0
Chunk B -> 1
Chunk C -> 2
```

The mapping should correspond to vectors present in the FAISS index.

---

# 26. Astra Mapping Test

When Astra is active:

```text
faiss_index
```

can remain:

```text
NULL
```

because Astra uses chunk identifiers and stored metadata rather than
FAISS positional mapping.

This behavior should be tested explicitly.

---

# 27. API Testing

FastAPI endpoints should be tested independently of the React
frontend.

Important endpoints include:

```text
GET  /api/v1/health

GET  /api/v1/documents

POST /api/v1/documents/upload

GET  /api/v1/documents/{id}/chunks

POST /api/v1/ask
```

FastAPI's test client or an equivalent HTTP testing approach can be
used.

---

# 28. Health Endpoint Test

Example:

```python
def test_health(client):
    response = client.get("/api/v1/health")

    assert response.status_code == 200
```

The response should contain the expected health structure.

---

# 29. Document Upload Integration Test

The document upload test should verify the complete ingestion flow.

```text
Upload Test Document
       ↓
HTTP Success
       ↓
Document Created
       ↓
Chunks Created
       ↓
Embeddings Generated
       ↓
Vectors Indexed
```

The test should then verify that the uploaded document appears in:

```text
GET /api/v1/documents
```

---

# 30. Ask Endpoint Integration Test

A controlled test can first index:

```text
Apache Kafka is used for asynchronous communication between the
Payment Service and Notification Service.
```

Then send:

```json
{
  "question": "How does the Payment Service communicate with the Notification Service?",
  "top_k": 5
}
```

The response should contain:

```text
question
answer
sources
retrieval
```

The retrieved sources should include the controlled test document.

---

# 31. Ask Response Schema Test

The response should contain:

```text
question

answer

sources

retrieval
```

Each source should contain:

```text
source_number
chunk_id
document_id
filename
chunk_index
score
```

Retrieval metadata should contain:

```text
top_score
top_k_requested
chunks_retrieved
retrieval_time_ms
generation_time_ms
total_time_ms
```

Schema testing helps prevent frontend/backend contract regressions.

---

# 32. Request Validation Tests

The `/ask` endpoint should reject invalid inputs.

Examples include:

```text
Empty or too-short question

Question longer than configured maximum

top_k = 0

top_k > 10
```

For example:

```json
{
  "question": "Kafka?",
  "top_k": 0
}
```

should fail request validation because the configured minimum Top-K
is 1.

---

# 33. Unsupported File Testing

The upload endpoint should reject unsupported document formats.

For example:

```text
malware.exe
```

should not be processed as a supported knowledge document.

The expected behavior should be a clear client-visible error.

---

# 34. RAG Integration Testing

The RAG integration test verifies:

```text
Question
   ↓
Embedding
   ↓
Retrieval
   ↓
Context Construction
   ↓
LLM
   ↓
Answer
   ↓
Sources
```

This is different from retrieval-only testing because it verifies the
complete question-answering pipeline.

---

# 35. Context Construction Test

Given retrieved chunks:

```text
Chunk A
Chunk B
```

the generated context should contain:

```text
[Source 1]

...

[Source 2]

...
```

Source numbering should remain consistent with the source metadata
returned by the API.

---

# 36. Source Mapping Test

Suppose the answer context uses:

```text
[Source 1]
```

The returned source list should map Source 1 to the same chunk used
when constructing the prompt.

This is important for citation traceability.

---

# 37. Unsupported Question Testing

The test corpus should include questions whose answers do not exist
in the indexed documents.

Example:

```text
Does the candidate have production experience building blockchain
applications using Rust?
```

when the documents contain no such information.

The expected behavior is an abstention such as:

```text
The available documents do not provide enough information.
```

rather than fabrication.

Because LLM output can vary, the automated test should avoid relying
only on an exact sentence match.

---

# 38. Why Exact LLM String Matching Is Fragile

The model could produce:

```text
The available documents do not provide enough information.
```

or:

```text
The provided context does not mention Rust blockchain experience.
```

Both may represent acceptable abstention behavior.

Therefore:

```python
assert answer == "exact sentence"
```

can be unnecessarily fragile for LLM tests.

RAG evaluation should use semantic or human-labelled criteria where
appropriate.

---

# 39. Mocking the LLM

Many integration tests should not require a real LLM API request.

The LLM service can be mocked.

For example:

```text
RAG Service
    |
    v
Mock LLM
    |
    v
Known deterministic answer
```

Advantages include:

- Faster tests
- No API cost
- No network dependency
- Deterministic output
- Easier failure testing

Real LLM calls should be reserved for selected end-to-end and
evaluation tests.

---

# 40. Mocking Astra

Unit tests should generally not depend on a live Astra service.

The Astra client can be mocked for tests of:

```text
Retrieval mapping

Error handling

Vector-store selection
```

Separate integration tests can communicate with the actual test
collection.

This creates:

```text
Unit Test
   ->
Mock Astra
```

and:

```text
Integration Test
   ->
Real Astra Test Collection
```

---

# 41. Frontend Testing

Frontend testing should verify important user workflows.

Examples include:

```text
Document list renders

Upload button works

Question can be submitted

Loading indicator appears

Answer renders

Markdown renders

Sources render

Metrics render

Errors are displayed
```

---

# 42. Responsive UI Testing

The application is designed for:

```text
Desktop

Tablet

Mobile
```

Important responsive behaviors include:

### Desktop

```text
Sidebar visible
Chat area independently scrollable
Question input remains at bottom
```

### Mobile

```text
Sidebar becomes drawer
Menu button opens sidebar
Backdrop closes sidebar
Conversation uses available viewport
Input remains accessible
```

---

# 43. Chat Scroll Testing

One specific UI requirement is:

> The browser page itself should not scroll during normal chat use.

Instead:

```text
Conversation Area
      |
      v
Internal Scroll
```

while:

```text
Question Input
```

remains at the bottom of the chat panel.

This should be manually verified on:

```text
Desktop browser

Tablet-sized viewport

Mobile-sized viewport
```

---

# 44. Document List Scroll Testing

The document list should scroll independently when many files are
uploaded.

The desired layout is:

```text
Sidebar
   |
   +-- Upload Area
   |
   +-- Scrollable Document List
```

The entire application should not expand vertically because of a
large number of documents.

---

# 45. Error-State Testing

Frontend error handling should be tested for:

```text
Backend unavailable

Upload failure

Ask failure

Invalid response

Network interruption
```

The application should display a useful error rather than silently
failing.

---

# 46. Regression Testing

Regression testing ensures that changes do not reintroduce previously
resolved problems.

This is particularly important because the project has already
identified real integration issues.

---

# 47. FAISS / SQLite Synchronization Regression

During development, a mismatch occurred:

```text
FAISS vectors = 18

SQLite chunks = 9
```

This caused some FAISS results to point to vectors without matching
SQLite metadata.

A regression check should verify:

```text
FAISS ntotal
      =
Number of valid mapped FAISS chunks
```

for a controlled clean test dataset.

Example:

```python
assert index.ntotal == mapped_chunk_count
```

This test is specifically relevant to the current architecture.

---

# 48. Retrieval Count Regression

The previous synchronization issue caused:

```text
top_k requested = 5

valid chunks returned = 3
```

even though enough vectors appeared to exist.

A controlled regression test should:

```text
Index at least 5 valid chunks
        ↓
Request Top-5
        ↓
Verify 5 valid chunks are resolved
```

This helps detect mapping corruption.

---

# 49. Database Reset Testing

If development or experiments reset the database, the corresponding
vector index must also be handled consistently.

An unsafe reset is:

```text
Delete SQLite Database

Keep Existing FAISS Index
```

because the vectors no longer have valid relational mappings.

A safe experimental reset should treat:

```text
SQLite metadata
+
FAISS index
```

as related state.

---

# 50. Vector Store Switching Test

Because the application supports:

```text
VECTOR_STORE=faiss
```

and:

```text
VECTOR_STORE=astra
```

both configurations should be tested.

The same high-level operation should work:

```text
Upload
   ↓
Index
   ↓
Ask
   ↓
Retrieve
   ↓
Answer
```

regardless of the configured backend.

---

# 51. Performance Testing

Performance testing should collect:

```text
retrieval_time_ms

generation_time_ms

total_time_ms
```

Tests should be performed over multiple questions rather than a
single request.

Possible measurements include:

```text
Mean

Median

Minimum

Maximum

Standard deviation

P95
```

when the number of observations is sufficient.

---

# 52. Cold vs Warm Execution

The first embedding request may include model initialization.

Therefore:

```text
Cold Request
```

can be significantly slower than:

```text
Warm Request
```

Testing should either:

1. perform a warm-up before performance measurements, or
2. report cold-start performance separately.

This avoids misleading latency conclusions.

---

# 53. Load Testing

Basic load testing can evaluate how the API behaves under multiple
requests.

Example scenarios:

```text
1 concurrent request

5 concurrent requests

10 concurrent requests
```

Possible observations include:

```text
Response latency

Error rate

Resource usage
```

Large-scale load testing is not necessarily required for the current
research prototype, but a small controlled test can identify obvious
limitations.

---

# 54. Security-Oriented Tests

Although security is not the primary research objective, basic tests
should include:

```text
Unsupported file upload

Very large question input

Invalid Top-K

Malformed request

Missing required fields
```

Secrets must never be stored in:

```text
Git repository

Frontend source code

API responses
```

Credentials should remain in environment configuration.

---

# 55. Manual Testing Checklist

Before a project demonstration, manually verify:

```text
[ ] Backend starts successfully

[ ] Frontend starts successfully

[ ] Health endpoint works

[ ] Existing documents load

[ ] New TXT upload works

[ ] New PDF upload works

[ ] Uploaded document is chunked

[ ] Embeddings are indexed

[ ] Supported question returns answer

[ ] Correct document appears in sources

[ ] Retrieval metrics appear

[ ] Unsupported question does not fabricate obvious information

[ ] Chat scroll works

[ ] Question field remains accessible

[ ] Mobile sidebar works

[ ] No secrets appear in browser or Git
```

---

# 56. Example Functional Test

## Test Case ID

```text
FT-RAG-001
```

## Objective

Verify that a known project-specific question retrieves the correct
document.

## Preconditions

The knowledge base contains:

```text
test_document.txt
```

with the statement:

```text
Apache Kafka is used for asynchronous communication between the
Payment Service and Notification Service.
```

## Input

```text
How does the Payment Service communicate with the Notification
Service?
```

## Expected Retrieval

```text
test_document.txt
```

should appear in the retrieved sources.

## Expected Answer

The answer should identify:

```text
Apache Kafka
```

and:

```text
asynchronous communication
```

without adding unsupported architecture details.

---

# 57. Example Unsupported Test

## Test Case ID

```text
FT-RAG-002
```

## Objective

Verify behavior when the indexed documents do not contain the answer.

## Input

```text
Does the system use RabbitMQ for payment communication?
```

## Preconditions

The controlled corpus contains information about Kafka but no
statement supporting RabbitMQ usage.

## Expected Behavior

The assistant should not claim that RabbitMQ is used.

It should indicate that the available documents do not support that
claim.

---

# 58. Example Retrieval Test

## Test Case ID

```text
RT-001
```

## Corpus

```text
Chunk 1:
Kafka is used for asynchronous communication.

Chunk 2:
Redis caches payment status.

Chunk 3:
Kubernetes manages deployment.
```

## Query

```text
How is payment status cached?
```

## Expected Result

The Redis chunk should appear among the highest-ranked results.

---

# 59. Test Result Documentation

Test results can be stored under:

```text
evaluation/results/
```

or a dedicated location such as:

```text
tests/results/
```

depending on whether the result is:

```text
Software verification
```

or:

```text
Research experiment
```

These should remain conceptually separate.

For example:

```text
tests/
    ->
Does the implementation behave correctly?

evaluation/
    ->
How well does the RAG approach perform?
```

---

# 60. Testing vs Evaluation

Testing and evaluation should not be treated as the same activity.

## Software Testing

Asks:

> Is the implementation functioning according to its design?

Examples:

```text
Does upload work?

Does the embedding have 384 dimensions?

Does Top-K validation work?

Does the API return the required fields?
```

## Research Evaluation

Asks:

> How effective is the implemented approach?

Examples:

```text
What is Recall@5?

How grounded are the answers?

Does RAG outperform the selected baseline on the evaluated corpus?

How does chunk size affect retrieval?
```

Both are necessary for the project.

---

# 61. Testing Pyramid for This Project

A practical testing strategy is:

```text
                  /\
                 /  \
                / E2E\
               /------\
              /Integration\
             /------------\
            /  Unit Tests  \
           /________________\
```

The majority of deterministic logic should be covered by fast unit
tests.

A smaller number of integration tests should verify:

```text
Database

Vector stores

API

RAG orchestration
```

A focused set of end-to-end tests should verify complete user
workflows.

---

# 62. Viva Questions and Answers

## How did you test your RAG system?

> I test it at multiple levels. Unit tests verify document cleaning,
> chunking and embedding behavior. Integration tests verify database
> persistence, vector indexing, semantic retrieval and API behavior.
> End-to-end tests verify the complete upload-to-question workflow.
> Separately, I use an evaluation dataset to measure retrieval and
> answer quality.

## What is the difference between testing and evaluation?

> Testing determines whether the software implementation behaves as
> designed, while evaluation measures how effective the AI approach
> is. For example, verifying that the embedding has 384 dimensions is
> a test, whereas measuring Recall@5 is an evaluation.

## How do you test an LLM when its response can change?

> I avoid exact string comparison for most LLM behavior. Deterministic
> software tests can mock the LLM, while real RAG evaluation uses
> correctness, groundedness and abstention criteria rather than
> requiring an exact sentence.

## What important bug did testing reveal?

> During development, I found that FAISS and SQLite could become
> inconsistent because they are persisted independently. In one
> development state FAISS contained 18 vectors while SQLite contained
> only 9 chunks. Some retrieved vector positions therefore had no
> metadata mapping. This led to treating vector/metadata consistency
> as an explicit regression and architectural concern.

## How do you test semantic retrieval?

> I create controlled chunks where the relevant evidence is known,
> issue semantically related questions, and verify that the expected
> chunk appears in the retrieved Top-K results. Research evaluation
> then measures this systematically using metrics such as Hit Rate,
> Precision, Recall and MRR.

---

# 63. Summary

The testing strategy covers the complete application:

```text
Document Upload
      |
      v
Text Extraction       -> Test
      |
      v
Cleaning              -> Test
      |
      v
Chunking              -> Test
      |
      v
Embedding             -> Test
      |
      v
Vector Indexing       -> Test
      |
      v
Semantic Retrieval    -> Test + Evaluate
      |
      v
Context Construction  -> Test
      |
      v
LLM Generation        -> Integration + Evaluate
      |
      v
Sources & Metrics     -> Test
      |
      v
Frontend Display      -> Test
```

This approach ensures that implementation correctness and AI-system
quality are evaluated separately but comprehensively.