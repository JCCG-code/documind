# DocuMind — Proyecto Final de Ciclo 1

## "AI Engineer Foundation"

**Autor:** JCCG  
**Fecha de entrega:** 4 semanas desde el inicio del proyecto  
**Nivel objetivo:** Junior/Mid AI Engineer  
**Repositorio:** github.com/JCCG-code/documind

---

## 1. Contexto y Motivación

Durante el Ciclo 1 del AI Engineering Procedure has aprendido a construir los bloques fundamentales de un sistema LLM en producción: tool calling, structured outputs, SSE streaming, RAG con hybrid search y reranking, observabilidad con Langfuse, evals con RAGAS, y prompt engineering avanzado.

DocuMind es la demostración de que dominas todos estos bloques de forma integrada. No es un tutorial — es un sistema real que resuelve un problema concreto tuyo: **buscar y consultar documentación técnica propia de forma inteligente**.

El problema que resuelve: como desarrollador acumulas documentación en múltiples formatos (PDFs, Markdown, TXT). Encontrar información específica en ese corpus es lento y frustrante con búsqueda por keywords. DocuMind permite hacerlo con lenguaje natural y obtener respuestas precisas basadas en tus propios documentos.

---

## 2. Descripción del Sistema

DocuMind es una API REST con capacidades RAG production-ready que permite:

1. **Indexar** documentos propios (PDF, TXT, Markdown) en una base de datos vectorial
2. **Consultar** ese corpus en lenguaje natural y obtener respuestas fundamentadas
3. **Streamear** las respuestas en tiempo real via SSE
4. **Observar** cada request con trazas completas en Langfuse
5. **Evaluar** la calidad del sistema con un eval suite de mínimo 20 preguntas

---

## 3. Features Obligatorias

Todas las features son obligatorias. El proyecto no se considera completo sin alguna de ellas.

### 3.1 Ingesta de Documentos

- Soporte para PDF, TXT y Markdown
- Chunking con `RecursiveCharacterTextSplitter` (chunk_size=512, overlap=50)
- Metadata por chunk: fuente, fecha de indexado, tipo de documento
- Deduplicación: no indexar el mismo documento dos veces
- Endpoint: `POST /documents/ingest`

### 3.2 Hybrid Search

- Embeddings con `nomic-embed-text` via Ollama
- Vector store: Qdrant (Docker local)
- BM25 con `rank-bm25`
- Reciprocal Rank Fusion (RRF, k=60) para combinar resultados
- Reranking con `cross-encoder/ms-marco-MiniLM-L-6-v2`
- Endpoint: `POST /search`

### 3.3 RAG Pipeline con SSE Streaming

- Recuperación hybrid search + reranking
- System prompt con instrucción de no alucinar
- Respuesta streameada token a token via SSE
- Structured output con Pydantic para metadata de la respuesta
- Endpoint: `POST /query/stream`

### 3.4 Structured Outputs

- Cada respuesta incluye: `answer`, `sources`, `confidence`, `chunks_used`
- Validación con Pydantic v2
- Endpoint no-streaming: `POST /query` devuelve JSON completo

### 3.5 Observabilidad con Langfuse

- Traza completa por cada request: retrieval span, build_prompt span, llm_response generation
- Input/output en cada span
- `user_id` y `session_id` propagados
- Cost tracking configurado (aunque sea Ollama local)

### 3.6 Eval Suite con RAGAS

- Mínimo 20 preguntas sobre los documentos indexados
- Métricas: `faithfulness`, `answer_relevancy`, `context_precision`
- LLM evaluador: Groq API (llama-3.3-70b-versatile)
- Script ejecutable: `uv run python evals/run_evals.py`
- Resultados guardados en `evals/results/` con timestamp

### 3.7 LLM-as-Judge

- Evaluación de respuestas individuales con `judge_response()`
- Scores: accuracy, relevance, completeness, overall_score
- Integrado opcionalmente en el pipeline de eval

---

## 4. Features Opcionales (bonus)

Estas features no son obligatorias pero suman al portfolio:

- Endpoint `GET /documents` — lista documentos indexados con metadata
- Endpoint `DELETE /documents/{id}` — eliminar documento del índice
- Re-indexado automático cuando cambia un archivo
- Dashboard simple con FastAPI + Jinja2 mostrando métricas del sistema
- Integración con Langfuse Prompt Management para versionar prompts

---

## 5. Stack Tecnológico

El stack es fijo. No se pueden sustituir componentes sin justificación técnica documentada.

| Componente         | Tecnología                  | Versión mínima |
| ------------------ | --------------------------- | -------------- |
| Lenguaje           | Python                      | 3.12+          |
| Package manager    | uv                          | latest         |
| API Framework      | FastAPI                     | 0.100+         |
| Streaming          | SSE (sse-starlette)         | latest         |
| LLM local          | Ollama + qwen3:8b           | latest         |
| Embeddings         | nomic-embed-text via Ollama | latest         |
| Vector DB          | Qdrant (Docker)             | latest         |
| Chunking           | langchain-text-splitters    | latest         |
| BM25               | rank-bm25                   | latest         |
| Reranking          | sentence-transformers       | latest         |
| Structured outputs | instructor + Pydantic v2    | latest         |
| Observabilidad     | Langfuse                    | latest         |
| Evals              | RAGAS + Groq API            | latest         |
| Linting            | ruff                        | latest         |
| Type checking      | mypy                        | latest         |
| Testing            | pytest                      | latest         |

**Modelos Ollama requeridos:**

```bash
ollama pull qwen3:8b        # LLM principal
ollama pull nomic-embed-text # Embeddings
ollama pull gemma4:e4b      # Fallback LLM
```

---

## 6. Arquitectura del Sistema

```
documind/
  src/
    documind/
      api/
        main.py              # FastAPI app
        routes/
          documents.py       # POST /documents/ingest, GET /documents
          query.py           # POST /query, POST /query/stream
          search.py          # POST /search
      rag/
        chunker.py           # RecursiveCharacterTextSplitter
        embeddings.py        # nomic-embed-text via Ollama
        indexer.py           # chunk + embed + upsert en Qdrant
        retriever.py         # búsqueda semántica pura
        hybrid_retriever.py  # BM25 + embeddings + RRF + reranking
        rag_agent.py         # pipeline RAG completo con Langfuse
      ingestion/
        pdf_loader.py        # PyMuPDF o pdfplumber
        txt_loader.py        # lectura directa
        md_loader.py         # markdown → texto plano
        file_dispatcher.py   # router por tipo de archivo
      models/
        document.py          # DocumentMetadata, IndexedDocument
        query.py             # QueryRequest, QueryResponse
        search.py            # SearchResult
        judge.py             # JudgeResponse
      observability/
        langfuse_client.py   # cliente Langfuse configurado
      prompts/
        rag_system.py        # system prompt del RAG agent
        judge.py             # LLM-as-judge prompt
      config.py              # Settings con pydantic-settings
  evals/
    run_evals.py             # script principal de evaluación
    eval_set.json            # 20+ preguntas con ground truths
    results/                 # resultados con timestamp
  tests/
    test_chunker.py
    test_retriever.py
    test_rag_agent.py
  docker-compose.yml         # Qdrant
  pyproject.toml
  README.md
  .env.example
```

---

## 7. Flujo de Datos

### Indexado (se ejecuta una vez por documento):

```
archivo (PDF/TXT/MD)
  → file_dispatcher → loader específico
  → texto plano
  → chunker → chunks con metadata
  → embeddings (nomic-embed-text)
  → Qdrant upsert
```

### Consulta (cada request del usuario):

```
query string
  → hybrid_retriever:
      → embed query (nomic-embed-text)
      → Qdrant semantic search (top-10)
      → BM25 search (todos los chunks)
      → RRF fusion
      → CrossEncoder reranking (top-5)
  → rag_agent:
      → build prompt con chunks
      → LLM call (qwen3:8b)
      → SSE streaming al cliente
  → Langfuse trace completa
```

---

## 8. Criterios de Evaluación

El proyecto se evalúa en cuatro dimensiones:

### 8.1 Funcionalidad (40%)

- [ ] Ingesta de PDF, TXT y Markdown funciona correctamente
- [ ] Hybrid search devuelve resultados relevantes
- [ ] SSE streaming funciona end-to-end
- [ ] Structured outputs validados con Pydantic
- [ ] Todos los endpoints responden correctamente

### 8.2 Calidad del RAG (25%)

- [ ] `faithfulness` ≥ 0.75 en el eval suite
- [ ] `answer_relevancy` ≥ 0.70 en el eval suite
- [ ] `context_precision` ≥ 0.80 en el eval suite
- [ ] Eval suite tiene mínimo 20 preguntas
- [ ] Script de evals ejecutable sin intervención manual

### 8.3 Observabilidad (20%)

- [ ] Trazas completas en Langfuse para cada request
- [ ] Spans diferenciados: retrieval, build_prompt, llm_response
- [ ] Input/output capturados en cada span
- [ ] Sin errores no capturados en el dashboard de Langfuse

### 8.4 Calidad del Código (15%)

- [ ] Estructura de carpetas sigue src-layout profesional
- [ ] Type hints en todas las funciones públicas
- [ ] Sin errores de ruff ni mypy
- [ ] README técnico con decisiones de arquitectura justificadas
- [ ] `.env.example` con todas las variables necesarias
- [ ] Docker Compose funcional para Qdrant

---

## 9. Métricas de Éxito

El proyecto se considera exitoso cuando:

```
1. uv run uvicorn documind.api.main:app --reload  → arranca sin errores
2. POST /documents/ingest con un PDF → indexa correctamente
3. POST /query/stream → responde en streaming con fuentes citadas
4. uv run python evals/run_evals.py → genera scores ≥ umbrales definidos
5. Langfuse dashboard → muestra trazas completas sin errores
```

---

## 10. Documentación de Referencia por Módulo

### Ingesta

- PyMuPDF: https://pymupdf.readthedocs.io/en/latest/
- LangChain text splitters: https://python.langchain.com/docs/how_to/recursive_text_splitter/

### RAG Core

- Qdrant Python client: https://qdrant.tech/documentation/quick-start/
- rank-bm25: https://github.com/dorianbrown/rank_bm25
- sentence-transformers CrossEncoder: https://www.sbert.net/docs/cross_encoder/usage/usage.html

### API

- FastAPI: https://fastapi.tiangolo.com/tutorial/
- SSE Starlette: https://github.com/sysid/sse-starlette

### Structured Outputs

- instructor: https://python-instructor.com
- Pydantic v2: https://docs.pydantic.dev/latest/

### Observabilidad

- Langfuse Python SDK: https://langfuse.com/docs/sdk/python/low-level-sdk

### Evals

- RAGAS: https://docs.ragas.io/en/latest/getstarted/index.html
- Groq API: https://console.groq.com/docs/openai

---

## 11. Restricciones y Reglas

1. **Sin APIs de pago para el LLM principal** — solo Ollama local. Groq está permitido exclusivamente para evals RAGAS.
2. **Sin LangChain como framework principal** — puedes usar `langchain-text-splitters` y `langchain-ollama` como utilidades, pero el pipeline RAG se construye con el SDK de Ollama directamente.
3. **Sin tutoriales copiados** — el código debe ser tuyo. Si usas código de referencia, cítalo en comentarios.
4. **Commits atómicos** — cada commit debe tener un propósito claro. Usar conventional commits: `feat:`, `fix:`, `chore:`, `docs:`.
5. **Variables de entorno** — ninguna credencial en el código. Todo en `.env` con `.env.example` versionado.

---

## 12. Entrega

**Fecha límite:** 4 semanas desde el inicio del proyecto  
**Formato de entrega:** repositorio GitHub público con:

```
README.md               → descripción, instalación, uso, decisiones técnicas
.env.example            → todas las variables necesarias
docker-compose.yml      → Qdrant configurado
evals/results/          → al menos una ejecución de evals con resultados reales
```

**El README es parte de la evaluación.** Debe incluir:

- Descripción del sistema en 2-3 párrafos
- Diagrama de arquitectura (ASCII o imagen)
- Instrucciones de instalación paso a paso
- Ejemplos de uso de la API (curl o httpie)
- Decisiones técnicas tomadas y por qué
- Resultados del eval suite con interpretación
- Limitaciones conocidas y mejoras futuras

---

## 13. Recursos de Apoyo

Durante el proyecto puedes consultar dudas en sesión semanal. Las sesiones de apoyo no son para que te expliquen cómo hacer el proyecto — son para resolver bloqueos técnicos concretos.

Ante cualquier bloqueo técnico:

1. Intenta resolverlo solo mínimo 30 minutos
2. Documenta el error exacto y lo que has intentado
3. Pregunta en la sesión de apoyo con ese contexto

**El objetivo es que seas capaz de construir este sistema de forma autónoma.** Las sesiones de formación ya te dieron todas las herramientas. Ahora toca aplicarlas.

---

_Documento generado al finalizar Ciclo 1 — AI Engineering Procedure_  
_Versión 1.0 — Mayo 2026_
