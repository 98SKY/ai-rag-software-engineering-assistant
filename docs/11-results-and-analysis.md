# Results and Analysis

## 1. Introduction

This chapter presents the experimental results of the
AI-Powered Intelligent Software Engineering Assistant.

The evaluation is designed to analyze the system from three major
perspectives:

1. Retrieval effectiveness
2. Generated-answer quality
3. System performance

The experiments evaluate the Retrieval-Augmented Generation pipeline
using controlled software engineering documents and questions.

The system supports two vector-search backends:

- FAISS
- Astra DB

The evaluation also compares the RAG-based approach with an LLM-only
baseline.

> **Important:** Numerical values in this document must be populated
> only after executing the corresponding experiments. No experimental
> result should be assumed or fabricated.

---

# 2. Experimental Configuration

The current implementation uses the following core configuration.

| Parameter | Configuration |
|---|---|
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2` |
| Embedding dimension | 384 |
| Default chunk size | 1000 characters |
| Default chunk overlap | 200 characters |
| Default Top-K | 5 |
| Local vector store | FAISS |
| Cloud vector store | Astra DB |
| FAISS index | `IndexFlatIP` |
| Astra similarity metric | Cosine |
| LLM provider | Groq |
| LLM model | `openai/gpt-oss-20b` |
| Backend | FastAPI |
| Metadata database | SQLite |
| Frontend | React + TypeScript |

The embeddings are normalized before vector indexing.

---

# 3. Evaluation Dataset

The evaluation dataset contains software-engineering questions with
manually verified expected evidence.

Question categories include:

```text
Direct factual
Paraphrased
Multi-chunk
Technical reasoning
Unsupported
```

Each supported question contains:

```text
Question
Expected answer
Relevant document
Relevant chunk/evidence
```

Unsupported questions intentionally contain no sufficient answer in
the indexed corpus.

---

# 4. Retrieval Evaluation

Retrieval effectiveness is measured using:

```text
Hit Rate@K
Precision@K
Recall@K
Mean Reciprocal Rank (MRR)
```

These metrics determine whether the vector-search component retrieves
the correct evidence before LLM generation.

---

# 5. Retrieval Results

The final retrieval results should be inserted after running the
evaluation scripts.

| Configuration | Hit Rate | Precision@K | Recall@K | MRR |
|---|---:|---:|---:|---:|
| FAISS | TBD | TBD | TBD | TBD |
| Astra | TBD | TBD | TBD | TBD |

### Interpretation

The analysis should discuss:

- How frequently relevant evidence was retrieved
- Whether relevant chunks appeared near the top of the ranking
- Whether irrelevant chunks were frequently included
- Differences observed between FAISS and Astra

Raw similarity scores should not be used as the primary basis for
comparing the two vector stores because their score values are not
necessarily directly comparable.

---

# 6. Top-K Experiment

The retrieval system should be evaluated using multiple Top-K values.

Recommended configurations:

```text
K = 1
K = 3
K = 5
K = 10
```

Results can be recorded as:

| Top-K | Hit Rate | Precision@K | Recall@K | MRR | Retrieval Time |
|---:|---:|---:|---:|---:|---:|
| 1 | TBD | TBD | TBD | TBD | TBD |
| 3 | TBD | TBD | TBD | TBD | TBD |
| 5 | TBD | TBD | TBD | TBD | TBD |
| 10 | TBD | TBD | TBD | TBD | TBD |

---

# 7. Top-K Analysis

The purpose of this experiment is to investigate the trade-off between
retrieving sufficient evidence and introducing irrelevant context.

A smaller K may provide:

```text
Less context
Potentially lower retrieval latency
Potential risk of missing relevant evidence
```

A larger K may provide:

```text
More potentially relevant evidence
Higher context volume
Potentially more irrelevant information
```

These are hypotheses rather than predetermined conclusions.

The final discussion should be based on measured results.

Example reporting style:

> Increasing K from [VALUE] to [VALUE] changed Recall@K from [VALUE]
> to [VALUE], while Precision@K changed from [VALUE] to [VALUE].
> Under the evaluated corpus, this indicates [OBSERVATION].

---

# 8. Chunk-Size Experiment

The effect of chunking can be evaluated using configurations such as:

| Configuration | Chunk Size | Overlap |
|---|---:|---:|
| C1 | 500 | 100 |
| C2 | 1000 | 200 |
| C3 | 1500 | 300 |

For each configuration, measure:

```text
Number of chunks
Hit Rate
Precision
Recall
MRR
Answer correctness
Groundedness
Latency
```

Results:

| Chunk Size | Overlap | Hit Rate | Recall@K | MRR | Total Time |
|---:|---:|---:|---:|---:|---:|
| 500 | 100 | TBD | TBD | TBD | TBD |
| 1000 | 200 | TBD | TBD | TBD | TBD |
| 1500 | 300 | TBD | TBD | TBD | TBD |

---

# 9. Chunking Analysis

Chunk size affects how much semantic information is contained in each
retrieval unit.

Very small chunks may separate related information.

For example:

```text
Chunk A:
The Payment Service publishes

Chunk B:
events through Apache Kafka...
```

Larger chunks preserve more context but may also contain information
unrelated to the question.

The experiment therefore investigates the balance between:

```text
Context preservation
        vs
Retrieval specificity
```

The final conclusion should be derived from the measured experiment.

---

# 10. RAG Answer Quality

Retrieval alone does not determine whether the generated answer is
correct.

The generated answers are evaluated using:

```text
Correctness
Groundedness / Faithfulness
Answer relevance
Citation accuracy
```

A possible manual scoring scheme is:

```text
2 = Good / fully satisfies criterion
1 = Partial
0 = Incorrect / unsupported
```

---

# 11. Answer Correctness Results

| System | Correct | Partial | Incorrect | Average Score |
|---|---:|---:|---:|---:|
| LLM Only | TBD | TBD | TBD | TBD |
| RAG | TBD | TBD | TBD | TBD |

The final analysis should examine whether access to project-specific
retrieved context changes answer correctness.

---

# 12. Groundedness Results

| System | Fully Grounded | Partially Grounded | Unsupported | Average |
|---|---:|---:|---:|---:|
| LLM Only | TBD | TBD | TBD | TBD |
| RAG | TBD | TBD | TBD | TBD |

For RAG, groundedness should be evaluated against the retrieved
evidence.

Retrieval similarity alone must not be treated as proof that an answer
is grounded.

---

# 13. Citation Accuracy

For RAG responses, the returned source references should be checked
against the claims made in the answer.

The metric can be calculated as:

```text
Citation Accuracy =
Correct Supporting Citations
----------------------------
Total Evaluated Citations
```

Results:

| Configuration | Correct Citations | Total Citations | Accuracy |
|---|---:|---:|---:|
| RAG | TBD | TBD | TBD |

A citation should count as correct only when the referenced evidence
actually supports the corresponding answer.

---

# 14. Unsupported Question Results

Unsupported questions evaluate whether the assistant invents
information when sufficient evidence is absent.

Possible outcomes are:

```text
Correct abstention
Incorrect unsupported answer
Ambiguous response
```

Results:

| System | Unsupported Questions | Correct Abstentions | Unsupported Answers | Abstention Accuracy |
|---|---:|---:|---:|---:|
| LLM Only | TBD | TBD | TBD | TBD |
| RAG | TBD | TBD | TBD | TBD |

---

# 15. False Abstention Analysis

The system should not simply refuse every uncertain question.

Supported questions must therefore also be checked for false
abstentions.

```text
False Abstention Rate =
Supported questions incorrectly refused
----------------------------------------
Total supported questions
```

Results:

| System | Supported Questions | False Abstentions | Rate |
|---|---:|---:|---:|
| RAG | TBD | TBD | TBD |

This prevents an overly conservative system from appearing successful
on unsupported-question evaluation.

---

# 16. LLM-Only vs RAG

The primary experimental comparison is:

```text
LLM Only

Question
   |
   v
LLM
   |
   v
Answer
```

versus:

```text
RAG

Question
   |
   v
Retrieval
   |
   v
Project Context
   |
   v
LLM
   |
   v
Answer
```

The same generation model should be used where practical so that the
major experimental difference is the availability of retrieved
project-specific context.

---

# 17. LLM-Only vs RAG Results

| Metric | LLM Only | RAG |
|---|---:|---:|
| Correctness | TBD | TBD |
| Groundedness | TBD | TBD |
| Answer Relevance | TBD | TBD |
| Correct Abstention | TBD | TBD |
| Unsupported Answer Rate | TBD | TBD |
| Average Total Latency | TBD | TBD |

The final analysis should identify measured improvements and
trade-offs without assuming that RAG must outperform the baseline on
every metric.

---

# 18. FAISS vs Astra Experiment

Both vector stores use the same embedding model.

For a controlled comparison, keep fixed:

```text
Documents
Question dataset
Embedding model
Chunking configuration
Top-K
```

and change:

```text
Vector Store
```

Results:

| Metric | FAISS | Astra |
|---|---:|---:|
| Hit Rate@K | TBD | TBD |
| Precision@K | TBD | TBD |
| Recall@K | TBD | TBD |
| MRR | TBD | TBD |
| Mean Retrieval Time | TBD | TBD |
| Median Retrieval Time | TBD | TBD |

---

# 19. FAISS vs Astra Analysis

The analysis should focus on:

```text
Retrieval relevance
Ranking
Latency
Persistence architecture
Metadata handling
Operational complexity
```

FAISS uses:

```text
Vector position
        +
SQLite metadata mapping
```

while Astra stores vector-related metadata with the vector record.

The experiment should not conclude that one system is universally
superior.

Results apply to the evaluated corpus, environment, configuration and
workload.

---

# 20. Latency Results

The API records:

```text
retrieval_time_ms
generation_time_ms
total_time_ms
```

Aggregated results should include:

| Metric | Mean | Median | Min | Max | Std. Dev. |
|---|---:|---:|---:|---:|---:|
| Retrieval Time | TBD | TBD | TBD | TBD | TBD |
| Generation Time | TBD | TBD | TBD | TBD | TBD |
| Total Time | TBD | TBD | TBD | TBD | TBD |

Where sufficient observations exist, P95 latency can also be reported.

---

# 21. Cold-Start Observation

The embedding model is cached after loading.

Therefore, the first request can behave differently from subsequent
requests.

Performance experiments should distinguish between:

```text
Cold Start

and

Warm Execution
```

or perform a warm-up before collecting the primary latency results.

---

# 22. Existing Functional Validation

Before the formal experimental evaluation, the implemented pipeline
was functionally validated using a controlled document describing a
Payment Service.

The document contained information including:

```text
Spring Boot
Apache Kafka
Redis
Docker
Kubernetes
```

A query asking how the Payment Service communicates with the
Notification Service retrieved the controlled document and produced an
answer identifying Apache Kafka as the asynchronous communication
mechanism.

This validates the functional pipeline:

```text
Upload
  ↓
Extraction
  ↓
Chunking
  ↓
Embedding
  ↓
Vector Indexing
  ↓
Retrieval
  ↓
LLM Generation
  ↓
Answer + Sources
```

This functional validation should not be confused with the larger
formal experimental evaluation.

---

# 23. Observed Persistence Issue During Development

An important issue was identified during development when FAISS and
SQLite became inconsistent.

At one point:

```text
FAISS vectors = 18
SQLite chunks = 9
```

Because FAISS vector positions depended on SQLite metadata mappings,
some retrieved positions could not be resolved to valid chunks.

After resetting the related persistence state consistently, the
baseline became:

```text
FAISS vectors = 9
Database chunks = 9
Mapped chunks = 9
```

This restored complete retrieval mapping.

This observation demonstrates an architectural limitation of using
independently persisted vector and metadata stores.

---

# 24. Threats to Result Validity

Results must be interpreted considering:

- Evaluation dataset size
- Quality of manual annotations
- Document diversity
- LLM response variability
- Network latency
- External API behavior
- Embedding model choice
- Chunking configuration
- Hardware/environment
- Vector-store implementation

Therefore, experimental conclusions should be scoped to the evaluated
configuration rather than generalized to every RAG system.

---

# 25. Recommended Result Visualizations

The final dissertation can include:

```text
Top-K vs Recall

Top-K vs Precision

Top-K vs Retrieval Latency

Chunk Size vs Recall

Chunk Size vs Answer Correctness

FAISS vs Astra Latency

LLM-only vs RAG Correctness

LLM-only vs RAG Groundedness

Unsupported Question Abstention Rate
```

All graphs should be generated from actual experiment results.

---

# 26. Final Analysis Template

After experiments are completed, the final discussion can follow this
structure:

### Retrieval

> Under the evaluated configuration, [CONFIGURATION] achieved
> [RESULT]. Changing Top-K from [X] to [Y] resulted in [OBSERVATION].

### Generation

> The RAG configuration achieved [RESULT] for answer correctness
> compared with [RESULT] for the LLM-only baseline.

### Groundedness

> The measured groundedness results indicate [OBSERVATION].

### Unsupported Questions

> Out of [N] unsupported questions, the RAG system correctly abstained
> on [N], corresponding to [RESULT].

### Performance

> Mean retrieval latency was [VALUE] ms, while mean generation latency
> was [VALUE] ms.

Only measured values should replace these placeholders.

---

# 27. Summary

The final analysis considers the complete RAG pipeline:

```text
                  Experimental Results
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Retrieval        Generation       Performance
          |                |                |
          v                v                v
      Hit Rate         Correctness       Latency
      Precision        Groundedness      Variability
      Recall           Relevance
      MRR              Citations
                       Abstention
```

The final conclusions will be based on experimental measurements
rather than assumptions about RAG performance.