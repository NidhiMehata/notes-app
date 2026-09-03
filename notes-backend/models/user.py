from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

if TYPE_CHECKING:
    from models.note import Note
    from models.note_collaborator import NoteCollaborator


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # relationships
    owned_notes: Mapped[list["Note"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )
    shared_notes: Mapped[list["Note"]] = relationship(
        secondary="note_collaborators",
        primaryjoin="User.id == NoteCollaborator.user_id",
        secondaryjoin="NoteCollaborator.note_id == Note.id",
        back_populates="collaborators",
        viewonly=True,
    )
    collaborator_links: Mapped[list["NoteCollaborator"]] = relationship(
        back_populates="user"
    )
