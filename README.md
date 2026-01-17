Narrative Memory, Critique & Editorial Engine
Overview

This project is a Narrative Memory, Critique & Editorial Engine designed to support long-form fiction writing (e.g., novels of 100k+ words). It addresses a core limitation of chat-based AI tools: the inability to persist narrative memory, maintain long-term consistency, and provide grounded editorial judgment across many chapters and writing sessions.

Rather than acting as an autonomous writer, the system functions as a persistent reader, analyst, and editor. It helps an author maintain narrative coherence, character integrity, tonal consistency, and stylistic quality over extended writing timelines.

The system is built for serious personal writing, retrieval-augmented AI experimentation, and as a demonstration of careful, explainable LLM system design suitable for academic or portfolio presentation.

Core Design Philosophy

The project is guided by explicit, non-negotiable principles:

Memory Over Intelligence
Long-term correctness comes from structured, persistent memory—not from relying on a “smarter” model.

Files Own Canon
All narrative state lives in files. The AI never owns, mutates, or silently rewrites canon.

AI as Editor, Not Authority
The system provides critique, judgment, and suggestions. Final decisions always remain with the author.

Explainability Over Automation
Every judgment is grounded in inspectable sources. Ambiguity is preserved, not resolved by guessing.

Incremental, Usage-Driven Growth
Features are added only when real writing demands them—no speculative overengineering.

How the System Works

Persistent Chapter Storage
Chapters are stored as plain text files and persist across sessions.

Summary-Based Memory Compression
Each chapter can be summarized using an LLM, producing a compressed, durable representation of past narrative content.

Focused Context Retrieval
When reviewing a chapter, the system retrieves only relevant summaries and character memory—mirroring how a human editor recalls specific prior events instead of rereading the entire manuscript.

Structured Narrative Memory
Characters, aliases, unresolved references, and ambiguous facts are stored explicitly using JSON files.

Human-Grade Editorial Evaluation
Chapters are evaluated across multiple craft dimensions (prose, pacing, character consistency, emotional depth, etc.), followed by a strengths-first editorial critique written in a controlled human voice.

Opt-In Line Editing
Grammar and clarity edits are performed only when explicitly requested, preserve authorial voice, and present before/after comparisons with explanations.

At no point does the AI act as a source of truth. All memory and canon are explicit, inspectable, and user-controlled.

Development Phases
Phase 1 — Foundation (Completed)

Goal: Prove that persistent narrative memory and context-aware critique are possible without relying on chat history.

Key features:

File-based chapter storage

LLM-generated chapter summaries as compressed memory

Relevance-based retrieval of past summaries

Context-aware chapter critique

Clear separation between memory (files) and judgment (AI)

Phase 2 — Accuracy & Structure (Completed)

Goal: Ensure long-term correctness, trust, and explainability.

Key features:

Structured per-character memory (JSON)

Alias and naming awareness

Candidate character staging for single-mention names

Conservative pronoun resolution

Explicit storage of ambiguous but critical facts

Unresolved reference tracking (titles, honorifics, role-based mentions)

Append-only memory model (no silent mutation)

This phase ensures uncertainty is preserved rather than hallucinated.

Phase 3 — Editorial Judgment & Craft Evaluation (Completed)

Goal: Enable human-grade editorial judgment comparable to a serious fiction editor.

Implemented features:

Multi-criteria chapter scoring with justification

Structured editorial critique with:

strengths-first analysis

weaknesses and missed opportunities

concrete revision examples

Configurable editorial tone (e.g., sharp friend, senior editor, professor)

Interactive editorial Q&A mode for targeted questions

Opt-in grammar and line-level editing with before/after explanations

Replayable mock mode for demos and cost-controlled reuse

Strict grounding in stored memory (no invented critique)

Phase 3 transforms the system from a consistency checker into a true editorial engine.

What the System Explicitly Does Not Do

By design, the system does not:

Automatically write prose

Enforce a hard timeline

Auto-resolve ambiguity or canon

Rewrite or delete narrative memory

Rely on embeddings or vector databases

Depend on hidden model state or chat history

These constraints preserve long-term narrative correctness.

Intended Use

This repository is intended for:

Long-form fiction writers seeking sustained editorial support

Retrieval-augmented AI experimentation

Learning careful, explainable LLM system design

Portfolio or academic evaluation (e.g., MS applications)

The emphasis is on design discipline, correctness, and explainability, not automation spectacle.

Current Status

Phase 1 — Foundation: Complete

Phase 2 — Accuracy & Structure: Complete

Phase 3 — Editorial Judgment & Craft Evaluation: Complete

Phase 4 — Workflow & Usability: Planned

The system is stable, usable, and actively supporting real writing.

One-Sentence Summary

This project is a file-backed, explainable editorial engine that persistently remembers long-form fiction and provides human-grade critique, evaluation, and line editing without ever owning or mutating narrative canon.