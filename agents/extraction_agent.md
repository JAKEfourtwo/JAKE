# Extraction Agent

## Purpose
Extract entities, relations, and facts from raw text using local LLMs.

## Prompt Template

```markdown
You are an expert knowledge extractor.

Extract from the following text:
- Entities (with types)
- Relations (subject-predicate-object)
- Key facts

Return ONLY valid JSON.

Text:
{{text}}
```

## Usage
Integrated in `core/ingest.py`.

## Future Improvements
- Few-shot examples
- Schema-guided extraction
- Multi-pass refinement