# Narrative Memory & Critique Engine

## Overview

This project is a **Narrative Memory & Critique Engine** designed to support long-form fiction writing (e.g., novels of ~100k words). It addresses a core limitation of chat-based AI tools: the inability to reliably **remember**, **reason over**, and **remain consistent with** a long narrative across many chapters.

Rather than acting as an autonomous writer, this system functions as a **persistent reader, analyst, and consistency checker**. Its purpose is to help an author maintain narrative coherence, character integrity, and logical continuity over extended writing timelines.

The system is built for **long-term personal use**, experimentation with retrieval-augmented AI systems, and as a demonstration of careful system design with large language models.

---

## Design Philosophy

The project is guided by a small set of explicit principles:

- **Memory > Intelligence**  
  Long-term correctness is achieved through structured, persistent memory—not by relying on a “smarter” model.

- **Files Own Memory**  
  All narrative state lives in files. The AI never stores canon, mutates state, or owns memory.

- **AI as Analyst, Not Authority**  
  The AI provides judgment and critique only. Final decisions always remain with the user.

- **Explainability Over Automation**  
  Every stored fact, omission, or ambiguity should be inspectable and understandable.

- **Incremental Growth, No Overengineering**  
  Features are added only when real writing usage demands them.

---

## How the System Works

1. **Persistent Chapter Storage**  
   Chapters are stored as plain text files and persist across sessions.

2. **Summary-Based Memory Compression**  
   Each chapter can be summarized using an LLM, producing a lightweight representation of past content.

3. **Focused Context Retrieval**  
   When reviewing a new chapter, the system determines which past summaries are relevant and uses only that focused context—mirroring how a human editor recalls specific earlier events rather than rereading the entire manuscript.

4. **Context-Aware Critique**  
   New chapters are critiqued for consistency, logic, character behavior, and narrative coherence using retrieved summaries.

At no point does the AI act as a source of truth. All memory is explicit, file-based, and user-controlled.

---

## Development Phases

### Phase 1 – Foundation (Completed)

**Goal:** Prove that the system can persist narrative memory and critique new chapters using relevant past context.

Key features:
- Persistent file-based chapter storage
- LLM-generated chapter summaries as compressed memory
- Relevance-based retrieval of past summaries
- Context-aware critique of new chapters
- Clear separation between memory (files) and judgment (AI)

Phase-1 established that long-term narrative support is possible without relying on chat history or opaque model memory.

---

### Phase 2 – Accuracy & Structure (Completed)

**Goal:** Improve trust, accuracy, and explainability over long-term use.

Key additions:
- Structured character memory stored as JSON files
- Canonical character identities with manual alias support
- Candidate character staging for single-mention names
- Conservative pronoun resolution using recency bias
- Explicit handling of ambiguous but critical facts
- Unresolved reference tracking for titles and role-based mentions (e.g., “Mr. Whitmore”, “my master”)
- Strict append-only memory model (no silent rewrites or deletions)

Phase-2 ensures that the system **preserves uncertainty rather than guessing**, preventing long-term corruption of narrative memory.

---

### Phase 3 – Scale & Experience (Planned)

Future work will be driven by real writing needs and may include:
- Timeline annotation and contradiction alerts (advisory only)
- Promotion workflows for candidate characters
- Resolution of ambiguous facts with human or AI verification
- Explainable critique citations
- Workflow automation and usability improvements

None of these are required for the system to be useful today.

---

## What the System Explicitly Does *Not* Do

By design, the system does **not**:
- Automatically write prose
- Enforce a hard timeline
- Auto-resolve aliases, titles, or honorifics
- Rewrite or delete past memory
- Use embeddings or vector databases
- Rely on hidden model state or chat history

These constraints are intentional and preserve long-term correctness.

---

## Intended Use

This repository is intended for:
- Personal long-form fiction writing support
- Experimentation with retrieval-augmented AI systems
- Learning and demonstrating careful system design with LLMs
- Portfolio or academic reference (e.g., MS applications)

It emphasizes **deliberate design decisions** over novelty or automation.

---

## Current Status

- Phase 1 (Foundation): **Complete**
- Phase 2 (Accuracy & Structure): **Complete**
- Phase 3 (Scale & Experience): **Planned**

The system is stable, usable, and actively supporting real writing.
