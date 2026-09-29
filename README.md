# GovAssist AI — Government Document Assistant

A document-grounded AI assistant that helps users find and understand information from indexed government documents through a conversational interface.

Built with Python, Gemini, ChromaDB and Streamlit.

## Overview

GovAssist AI uses Retrieval-Augmented Generation (RAG) to answer questions using relevant passages retrieved from an indexed government document.

The initial implementation uses the Andhra Pradesh Panchayat Raj Act, 1994, as its document source.

The application is designed to reduce reliance on general-purpose AI responses by supplying retrieved document evidence to the language model.

**Disclaimer:** GovAssist AI is an experimental information assistant. It is not an official government service or a substitute for authoritative legal advice.

## Problem Statement

Government documents can be lengthy and difficult to navigate. Finding relevant provisions often requires manually searching through multiple pages.

GovAssist AI explores how semantic search and generative AI can make document-based information easier to retrieve and understand.

## Key Features

- PDF document ingestion and text extraction.
- Page-aware text chunking with overlap.
- Metadata enrichment for document source, page and section.
- Gemini text embeddings.
- Persistent vector storage using ChromaDB.
- Semantic retrieval of relevant document chunks.
- Document-grounded answer generation.
- Conversational follow-up support.
- Streamlit chat interface with retrieved source passages.
- Retrieval, answer-quality, grounding and robustness evaluation.
- Centralized configuration, logging and isolated vector-store tests.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| User interface | Streamlit |
| Generation model | Gemini |
| Embeddings | Gemini Embedding |
| Vector database | ChromaDB |
| PDF processing | pypdf |
| Configuration | python-dotenv |
| Logging | Python logging |

The configured model identifiers are maintained in `src/config.py`.

## System Architecture

User question → Conversation context → Query embedding → ChromaDB retrieval → Retrieved document context → Gemini → Grounded answer

The application retrieves relevant document passages before generating a response. Previous conversation messages help interpret follow-up questions but are not treated as independent documentary evidence.

## Project Structure

```text
ai-government-assistant/
├── app.py
├── requirements.txt
├── .env.example
├── src/
│   ├── config.py
│   ├── logger.py
│   ├── gemini_client.py
│   ├── document_loader.py
│   ├── chunker.py
│   ├── metadata.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt_engine.py
│   ├── rag_pipeline.py
│   └── conversation.py
├── scripts/
│   ├── index_document.py
│   └── check_readiness.py
├── tests/
└── evaluation/
```

The local PDF and persistent vector database may be excluded from the public repository.

## Local Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/ai-government-assistant.git
cd ai-government-assistant
```

Create and activate a virtual environment.

On Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and configure your Gemini API key.

Place an authorized copy of the source PDF at the path configured in `src/config.py`.

Index the document:

```powershell
python -m scripts.index_document
```

Indexing requires access to the configured embedding model and may consume API quota.

Run the readiness checks:

```powershell
python -m scripts.check_readiness
```

Start the application:

```powershell
python -m streamlit run app.py
```

## Evaluation

The project includes scripts for several evaluation dimensions.

| Dimension | Evaluation |
|---|---|
| Retrieval | Section-level Hit@1, Hit@3 and Hit@5 |
| Answer completeness | Expected-keyword coverage |
| Grounding | LLM-assisted claim-support evaluation |
| Unsupported questions | Fallback-response checks |
| Robustness | Direct, paraphrased, semantic and invalid-input tests |
| Conversation | Context-dependent follow-up testing |

Evaluation scores depend on the test dataset and do not establish overall legal correctness.

**Verified results:** Add actual test counts and results after running the final evaluation suite.

## Current Limitations

- The initial implementation is designed around a single indexed government document.
- Section metadata extraction may require improvement for complex document layouts.
- Retrieval does not guarantee that a passage contains sufficient evidence.
- LLM-assisted grounding judgments require human review.
- Conversation history is maintained within the application session.
- Deployment requires a strategy for making the indexed vector database available.

## Future Improvements

- Support multiple government documents.
- Improve section-aware chunking and metadata extraction.
- Expand the evaluation dataset.
- Add document-version management.
- Introduce more robust retrieval relevance checks.
- Implement a suitable hosted or deployment-ready vector-store strategy.

## Author

**Suneel K Dandu**

AI/GenAI Application Developer.

Background in banking and government administration, with a focus on building practical AI applications for real-world problems.

## Project Status

Core application implemented. Local validation and deployment preparation are in progress.