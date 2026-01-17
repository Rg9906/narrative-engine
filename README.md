Narrative Memory & Critique Engine

This project is a Narrative Memory & Critique Engine built to support long-form fiction writing such as novels. It is designed to solve a core limitation of chat-based AI tools: the inability to reliably remember, reason over, and stay consistent with a long narrative across many chapters.

Instead of relying on temporary chat context, this system stores chapters permanently, generates summaries as compressed memory, retrieves only relevant past information, and critiques new chapters for consistency, logic, and character integrity. The goal is not to write prose automatically, but to act as a persistent reader and analyst that helps the author maintain narrative coherence over time.

The system works by treating files as the source of truth. Chapters are stored as plain text and persist across sessions. Each chapter can be summarized using an LLM, creating a lightweight representation of past events. When a new chapter is reviewed, the system determines which past chapters are relevant and critiques the new text using only that focused context. This mirrors how a human editor recalls specific earlier events rather than rereading the entire book.

The AI is used strictly for judgement and analysis. It does not store memory, decide canon, or mutate state. All memory is owned and controlled by the system, and all final decisions remain with the user. The design emphasizes explainability, long-term correctness, and incremental growth rather than automation or novelty.

This project is built incrementally and intentionally avoids overengineering. It does not use vector databases, embeddings, or complex orchestration in its initial scope. The current implementation prioritizes clarity, stability, and real-world usability over scale. Future extensions may include character profiles, timeline checks, or hybrid rule-based analysis, but none of these are required for the system to be useful today.

This repository is intended for personal long-form writing support, experimentation with retrieval-augmented AI systems, and learning system design principles. It may also serve as a portfolio or academic project demonstrating thoughtful use of large language models as analytical tools rather than autonomous agents.

Current status: Scope-1 core functionality is complete and stable. Further development will be driven by actual writing usage rather than speculative features.