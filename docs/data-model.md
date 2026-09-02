# Lattice V1 Data Model

## System Boundary

Lattice V1 is a single-user, local-first learning system. It persists full lesson conversations, exercises, mastery state, and learning artefacts. There is no user/account table, authentication, multi-tenancy, or cloud-sync model in V1.

## Core Entities


| Entity           | Purpose                                                                        |
| ---------------- | ------------------------------------------------------------------------------ |
| Track            | A learning domain, such as Distributed Systems or AI Engineering.              |
| Module           | An ordered unit within a track.                                                |
| Concept          | A teachable concept within a module.                                           |
| Learning session | One teaching interaction, with a lifecycle and one primary concept.            |
| Message          | An immutable, ordered message within a session.                                |
| Exercise attempt | Your answer to a named exercise, including feedback and score.                 |
| Concept mastery  | Current measured understanding of a concept.                                   |
| Artifact         | A link or file produced during learning, such as code, an RFC, or a benchmark. |

## Relationship Model

Track 1 ── * Module 1 ── * Concept

Concept 1 ── * Learning session 1 ── * Message

Learning session 1 ── * Exercise attempt
Concept 1 ── 1 Concept mastery

Learning session 1 ── * Artifact

## Invariants

1. A track slug is globally unique.
2. A module has a unique position within its track.
3. A module slug is unique within its track.
4. A concept has a unique position and slug within its module.
5. A session belongs to exactly one concept; its module and track are derived through that concept.
6. A message belongs to exactly one session.
7. Message sequence numbers are positive, unique, and strictly ordered within a session.
8. Messages are immutable after persistence.
9. An exercise attempt belongs to exactly one session; its concept is derived through that session.
10. A concept has at most one current mastery record.
11. Exercise attempts are append-only; feedback never overwrites the original answer.
12. An artifact belongs to exactly one learning session; its concept is derived through that session.
13. Application code creates UUIDs. Postgres doesn't generate identifiers.

## Explicitly Deferred

- Authentication and multiple users.
- Semantic/vector search.
- Automated transcripts capture from a chat host.
- Agent memory summaries as a separate persistence model.
- Attachments stored in object storage.
- Soft deletion and retention policies.
