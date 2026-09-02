from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID

NAMING_CONVENTION = {
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)

learning_tracks = Table(
    "learning_tracks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column("slug", String(100), nullable=False, unique=True),
    Column("title", String(255), nullable=False),
    Column("description_markdown", Text),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
)

learning_modules = Table(
    "learning_modules",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "track_id",
        UUID(as_uuid=True),
        ForeignKey("learning_tracks.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("slug", String(100), nullable=False),
    Column("title", String(255), nullable=False),
    Column("position", Integer, nullable=False),
    Column("description_markdown", Text),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint("position > 0", name="positive_position"),
    UniqueConstraint("track_id", "slug", name="track_slug"),
    UniqueConstraint("track_id", "position", name="track_position"),
)

concepts = Table(
    "concepts",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "module_id",
        UUID(as_uuid=True),
        ForeignKey("learning_modules.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("slug", String(100), nullable=False),
    Column("title", String(255), nullable=False),
    Column("position", Integer, nullable=False),
    Column("description_markdown", Text),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint("position > 0", name="positive_position"),
    UniqueConstraint("module_id", "slug", name="module_slug"),
    UniqueConstraint("module_id", "position", name="module_position")
)

learning_sessions = Table(
    "learning_sessions",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "concept_id",
        UUID(as_uuid=True),
        ForeignKey("concepts.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("title", String(255), nullable=False),
    Column("status", String(32), nullable=False, server_default=text("'planned'")),
    Column("started_at", DateTime(timezone=True)),
    Column("completed_at", DateTime(timezone=True)),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint(
        "status IN ('planned', 'in_progress', 'completed', 'abandoned')",
        name="valid_status"
    ),
    CheckConstraint(
        "completed_at IS NULL OR started_at IS NULL OR completed_at >= started_at",
        name="completion_after_start"
    ),
)

session_messages = Table(
    "session_messages",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "session_id",
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("sequence_number", Integer, nullable=False),
    Column("role", String(32), nullable=False),
    Column("content_markdown", Text, nullable=False),
    Column(
        "attributes",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    ),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint(
        "role IN ('user', 'assistant', 'system')",
        name="valid_role"
    ),
    UniqueConstraint("session_id", "sequence_number", name="session_sequence_number"),
    CheckConstraint("sequence_number > 0", name="positive_sequence_number"),
)

exercise_attempts = Table(
    "exercise_attempts",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "session_id",
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("exercise_key", String(100), nullable=False),
    Column("prompt_snapshot_markdown", Text, nullable=False),
    Column("answer_markdown", Text, nullable=False),
    Column("feedback_markdown", Text),
    Column("score", Numeric(5, 2)),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column("evaluated_at", DateTime(timezone=True)),
    CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="score_range")
)

concept_mastery = Table(
    "concept_mastery",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "concept_id",
        UUID(as_uuid=True),
        ForeignKey("concepts.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    ),
    Column("mastery_level", String(32), nullable=False, server_default=text("'unseen'")),
    Column("score", Numeric(5, 2)),
    Column("notes_markdown", Text),
    Column("last_assessed_at", DateTime(timezone=True)),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    CheckConstraint(
        "mastery_level IN ('unseen', 'learning', 'practicing', 'proficient', 'mastered')",
        name="valid_mastery_level"
    ),
    CheckConstraint("score IS NULL OR (score >= 0 AND score <= 100)", name="score_range")
)

learning_artifacts = Table(
    "learning_artifacts",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True),
    Column(
        "session_id",
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="RESTRICT"),
        nullable=False
    ),
    Column("artifact_type", String(32), nullable=False),
    Column("title", String(255), nullable=False),
    Column("uri", Text, nullable=False),
    Column("description_markdown", Text),
    Column(
        "attributes",
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb")
    ),
    Column("created_at", DateTime(timezone=True), nullable=False, server_default=func.now()),
    CheckConstraint(
        "artifact_type IN ('code', 'document', 'diagram', 'benchmark', 'link')",
        name="valid_artifact_type"
    ),
)

Index(
    "ix_learning_sessions_concept_id_status",
    learning_sessions.c.concept_id,
    learning_sessions.c.status
)

Index(
    "ix_exercise_attempts_session_id_created_at",
    exercise_attempts.c.session_id,
    exercise_attempts.c.created_at
)
