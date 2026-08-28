# Lattice V1 Data Model

## System Boundary

Lattice V1 is a single-user, local-first learning system. It persists full lesson conversations, exercises, mastery state, and learning artefacts. There is no user/account table, authentication, multi-tenancy, or cloud-sync model in V1.

## Core Entities


| Entity           | Purpose                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| Track            | A learning domain, such as Distributed Systems or AI Engineering.              |
| Module           | An ordered unit within a track.                                                |
| Concept          | A teachable concept within a module.                                           |
| Learning session | One teaching interaction, with a lifecycle and module context.                 |
| Message          | An immutable, ordered message within a session.                                |
| Exercise attempt | Your answer to a named exercise, including feedback and score.                 |
| Concept mastery  | Current measured understanding of a concept.                                   |
| Artifact         | A link or file produced during learning, such as code, an RFC, or a benchmark. |

## Relationship Model

Track 1 ── * Module 1 ── * Concept

Module 1 ── * Learning session 1 ── * Message

Concept 1 ── * Exercise attempt
Concept 1 ── 1 Concept mastery

Learning session 1 ── * Artifact

## Invariants

1. A track slug is globally unique.
2. A module has a unique position within its track.
3. A concept has a unique position within its module.
4. A session belongs to exactly one module.
5. A message belongs to exactly one session.
6. Message sequence numbers are unique and strictly ordered within a session.
7. Messages are immutable after persistence.
8. A concept has at most one current mastery record.
9. Exercise attempts are append-only; feedback never overwrites the original answer.
10. Application code creates UUIDs. Postgres doesn't generate identifiers.

## Explicitly Deferred

- Authentication and multiple users.
- Semantic/vector search.
- Automated transcripts capture from a chat host.
- Agent memory summaries as a separate persistence model.
- Attachments stored in object storage.
- Soft deletion and retention policies.
