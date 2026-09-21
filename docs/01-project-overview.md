# AI-Powered Intelligent Software Engineering Assistant Using RAG

## 1. Project Overview

This project implements an AI-powered Software Engineering Assistant
using Retrieval-Augmented Generation (RAG).

The system allows users to upload software-engineering-related
documents such as:

- Technical documentation
- Software requirements
- Architecture documents
- API documentation
- Coding standards
- Project notes
- PDF, TXT, and Markdown files

Users can then ask natural-language questions about the uploaded
documents.

Instead of relying only on the general knowledge of a Large Language
Model (LLM), the system first retrieves relevant information from the
uploaded documents and supplies that information as context to the LLM.

The LLM generates an answer using the retrieved context and the system
also returns the document sources used to generate the response.

---

## 2. Research Area

Artificial Intelligence

Primary concepts used:

- Natural Language Processing
- Large Language Models
- Retrieval-Augmented Generation
- Semantic Search
- Vector Embeddings
- Vector Databases
- Information Retrieval

---

## 3. Problem Statement

Software engineering projects generate large amounts of technical
information distributed across requirement documents, architecture
documents, API specifications, coding standards, project notes, and
other sources.

Developers often spend significant time searching through these
documents to find information required for development,
troubleshooting, onboarding, and decision-making.

Traditional keyword search may fail when the terminology used in a
query differs from the terminology used in the documents.

General-purpose Large Language Models can answer software engineering
questions, but they may not have access to private or project-specific
information. They may also generate unsupported information when the
required knowledge is unavailable.

This project investigates whether Retrieval-Augmented Generation can
provide a more useful approach by combining semantic document
retrieval with LLM-based answer generation.

---

## 4. Proposed Solution

The proposed system provides a centralized AI assistant for querying
software engineering knowledge.

The system follows two major workflows.

### Document Ingestion

1. User uploads a document.
2. The backend extracts text from the document.
3. Extracted text is cleaned.
4. Text is divided into smaller chunks.
5. Each chunk is converted into a vector embedding.
6. Embeddings are stored in a vector store.
7. Document and chunk metadata are persisted.

### Question Answering

1. User submits a natural-language question.
2. The question is converted into an embedding.
3. Semantic search retrieves the most relevant document chunks.
4. Retrieved chunks are combined into contextual information.
5. The context and question are supplied to the LLM.
6. The LLM generates an answer based on the supplied context.
7. The API returns the answer, source references, similarity scores,
   and performance information.

---

## 5. High-Level Architecture

The system consists of the following layers:

Frontend
    |
    v
React + TypeScript
    |
    | REST API
    v
FastAPI Backend
    |
    +-----------------------------+
    |                             |
    v                             v
Document Processing          Query Processing
    |                             |
    v                             v
Chunking                   Query Embedding
    |                             |
    v                             v
Embedding Model            Semantic Retrieval
    |                             |
    +-------------+---------------+
                  |
                  v
             Vector Store
          FAISS / Astra DB
                  |
                  v
           Retrieved Context
                  |
                  v
               Groq LLM
                  |
                  v
        Grounded Answer + Sources

---

## 6. Current Technology Stack

### Frontend

- React
- TypeScript
- Vite
- CSS
- React Markdown

### Backend

- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI / RAG

Embedding model:

sentence-transformers/all-MiniLM-L6-v2

Embedding dimension:

384

Document chunk size:

1000 characters

Chunk overlap:

200 characters

Retrieval:

Top-K semantic similarity search

### Vector Stores

The system currently supports two vector-store implementations:

1. FAISS
2. DataStax Astra DB

The active implementation can be selected using:

VECTOR_STORE=faiss

or:

VECTOR_STORE=astra

### LLM

Groq API

Current model:

openai/gpt-oss-20b

---

## 7. Why Retrieval-Augmented Generation?

A normal LLM-based system follows:

Question
    |
    v
LLM
    |
    v
Answer

The model answers primarily from information available through its
existing model knowledge.

The proposed RAG system follows:

Question
    |
    v
Semantic Retrieval
    |
    v
Project Documents
    |
    v
Relevant Context
    |
    v
LLM
    |
    v
Grounded Answer

This allows the system to answer questions using project-specific
information that may not be available to the base LLM.

---

## 8. Example

Suppose a document contains:

"Apache Kafka is used for asynchronous communication between the
Payment Service and Notification Service."

The user asks:

"How does the Payment Service communicate with the Notification
Service?"

The system converts the question into an embedding and performs
semantic similarity search.

The relevant document chunk is retrieved and supplied to the LLM.

The generated answer can then state that Apache Kafka is used for
asynchronous communication, while also returning the source document
and chunk.

---

## 9. Current Features

The current prototype supports:

- PDF document upload
- TXT document upload
- Markdown document upload
- Text extraction
- Text cleaning
- Configurable chunking
- Local embedding generation
- Semantic similarity search
- FAISS vector storage
- Astra DB vector storage
- Configurable vector-store backend
- Retrieval-Augmented Generation
- Groq LLM integration
- Source references
- Similarity scores
- Retrieval latency measurement
- LLM generation latency measurement
- Total response-time measurement
- Document listing
- Document chunk inspection
- Responsive React interface
- Markdown answer rendering

---

## 10. Research Evaluation

The project will not be evaluated only on whether the application
works.

Experiments will be conducted to investigate the effectiveness of the
RAG architecture.

The evaluation can include:

- Retrieval relevance
- Answer correctness
- Groundedness / faithfulness
- Citation accuracy
- Unsupported-answer behavior
- Retrieval latency
- Generation latency
- Total response latency
- Effect of Top-K
- Effect of chunk size
- Comparison of LLM-only and RAG responses
- Comparison of FAISS and Astra retrieval behavior

---

## 11. Expected Research Comparison

Two answer-generation approaches can be compared.

### Approach A: LLM Only

Question -> LLM -> Answer

### Approach B: RAG

Question
-> Retrieve project context
-> LLM with retrieved context
-> Answer + Sources

The objective is to determine whether the RAG-based approach improves
answers for project-specific software engineering questions,
particularly in terms of evidence grounding and access to information
contained in the uploaded documents.

---

## 12. Current Project Status

Completed:

- Project architecture
- FastAPI backend
- React frontend foundation
- Document ingestion pipeline
- Text extraction
- Text cleaning
- Chunking
- Embedding generation
- FAISS integration
- Astra DB integration
- Semantic retrieval
- Groq LLM integration
- RAG answer generation
- Source references
- Performance metadata
- Responsive chat interface

In Progress / Planned:

- Source-content preview
- Improved knowledge-base management
- Document deletion and vector synchronization
- Retrieval evaluation dataset
- LLM-only baseline
- Automated evaluation
- Experimental comparison
- Result visualization
- Final dissertation