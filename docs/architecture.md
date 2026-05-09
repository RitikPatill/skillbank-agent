# Architecture

> **Draft** — this document will be fleshed out in M6 once the full pipeline is implemented.

## High-level flow

```
User task
  └─► Embed (MiniLM-L6)
        └─► Retrieve top-3 skills (ChromaDB)
              └─► Generate code (Claude Haiku)
                    └─► Execute (subprocess sandbox)
                          └─► Extract skills → deduplicate → persist
```

## Component notes

| Component | Technology | Notes |
|-----------|-----------|-------|
| Embedding | `sentence-transformers` MiniLM-L6-v2 | Runs fully locally, no API key required |
| Skill store | ChromaDB (local) | Persisted in `.chroma/` at runtime |
| LLM | Claude Haiku via Anthropic API | Two calls per task: generate + extract |
| Deduplication | Cosine similarity > 0.92 threshold | Prevents redundant skill entries |
| Execution | Python `subprocess`, 30 s timeout | stdout/stderr captured for feedback |
