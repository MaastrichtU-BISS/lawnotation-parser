# lawnotation-parser

Simple adapters for parsing LLM-generated annotations from GPT and Gemini into Lawnotation.

We provide three adapters:

- `LLM2LawnotationIndices`: use annotations that already include `start` and `end` offsets.
- `LLM2LawnotationAll`: match every occurrence of the annotated text in the source document.
- `LLM2LawnotationFirst`: match only the first occurrence of the annotated text.

The project also combines the GPT and Gemini annotation sets into a single Lawnotation task, ready to import.

Inside that task, both LLMs are represented as separate annotators so Lawnotation can compute agreement metrics between them.
