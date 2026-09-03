from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

if TYPE_CHECKING:
    from models.note_collaborator import NoteCollaborator
    from models.user import User


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    is_deleted: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    # relationships
    owner: Mapped["User"] = relationship(back_populates="owned_notes")
    collaborators: Mapped[list["User"]] = relationship(
        secondary="note_collaborators",
        primaryjoin="Note.id == NoteCollaborator.note_id",
        secondaryjoin="NoteCollaborator.user_id == User.id",
        back_populates="shared_notes",
        viewonly=True,
    )
    collaborator_links: Mapped[list["NoteCollaborator"]] = relationship(
        back_populates="note", cascade="all, delete-orphan"
    )
