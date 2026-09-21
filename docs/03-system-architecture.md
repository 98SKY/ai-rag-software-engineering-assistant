# System Architecture

## 1. Architecture Overview

The AI-Powered Software Engineering Assistant follows a layered
client-server architecture combined with a Retrieval-Augmented
Generation pipeline.

The major architectural components are:

1. Presentation Layer
2. API Layer
3. Document Processing Layer
4. Embedding Layer
5. Vector Retrieval Layer
6. Metadata Persistence Layer
7. RAG Orchestration Layer
8. LLM Generation Layer

---

## 2. High-Level Architecture

```mermaid
flowchart LR

    U[User]

    FE[React + TypeScript Frontend]

    API[FastAPI Backend]

    DP[Document Processing]

    EMB[Sentence Transformer<br/>all-MiniLM-L6-v2]

    VS{Vector Store}

    FAISS[(FAISS)]

    ASTRA[(Astra DB)]

    SQL[(SQLite)]

    RAG[RAG Service]

    LLM[Groq LLM]

    U --> FE
    FE -->|REST API| API

    API --> DP
    DP --> EMB

    EMB --> VS

    VS --> FAISS
    VS --> ASTRA

    API --> SQL

    API --> RAG

    RAG --> EMB
    RAG --> VS
    RAG --> LLM

    LLM --> RAG
    RAG --> API
    API --> FE
    FE --> U