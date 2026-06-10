# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Vue 3 + Vite frontend for Documind - a document ingestion and management system. Interfaces with a FastAPI backend for document storage and retrieval.

**Stack**: Vue 3, TypeScript, PrimeVue 4 (UI), Pinia, Vue Router, Axios

## Commands

```sh
pnpm dev          # Start dev server with hot reload
pnpm build        # Type-check and build for production
pnpm lint         # Run oxlint + eslint with auto-fix
pnpm format       # Format with Prettier
pnpm type-check   # Type-check with vue-tsc
```

## API Documentation

Full API docs at `http://localhost:8000/docs#/`

### GET /documents

List all indexed documents.

**Response 200:**

```json
[{
  "filename": "string",
  "hash": "string",
  "content_type": "string",
  "size": number
}]
```

### POST /documents/ingest

Upload and index a document (PDF, TXT, MD).

**Request:** `multipart/form-data` with `file` field

**Response 200:**

```json
{ "status": "string", "points": number }
```

**Error 400:**

```json
{ "detail": "Error message" }
```

### POST /query

Query documents with RAG, returns complete JSON response.

**Request:**

```json
{ "text": "string", "model": "qwen3:8b" }
```

**Response 200:**

```json
{
  "answer": "string",
  "sources": ["string"],
  "confidence": 0.0,
  "chunks_used": 0
}
```

### POST /query/stream

Query with SSE streaming response.

**Request:** Same as `/query`

**Response:** SSE stream with `data: token\n\n` and `data: [DONE]` when finished.

**Error:**

SSE stream response with `data: [ERROR] Error detail\n\n` and `data: [DONE]` when finished.

### GET /search

Hybrid search (BM25 + vector + RRF + reranking).

**Request:** Query param `?query=string`

**Response 200:**

```json
{
  "query": "string",
  "found": true,
  "message": "string",
  "results": [{
    "text": "string",
    "source": "string",
    "doc_type": "string",
    "score": 0.0,
    "rrf_score": 0.0,
    "rerank_score": 0.0 | null
  }]
}
```

**Error 400:**

```json
{ "detail": "Error while searching query: {query}.\nError -> {error}" }
```

## Architecture

**API Base URL**: `http://localhost:8000/` (configured in `src/main.ts`)

**Source Structure**:

- `src/views/` - Route page components (HomeView, DocumentsView)
- `src/services/` - API calls (document.service.ts)
- `src/utils/checkers/` - Runtime type validation (document.checker.ts)
- `src/types/` - TypeScript interfaces (document.d.ts)
- `src/router/` - Vue Router configuration
- `@/` alias resolves to `src/`

**State**: Pinia store directory exists but is currently empty. Component state managed via Vue's `reactive()`.

## Type Checking

Uses `vue-tsc` instead of `tsc` for `.vue` file type support. The `Document` interface in `src/types/document.d.ts` defines the expected shape of document objects from the API.
