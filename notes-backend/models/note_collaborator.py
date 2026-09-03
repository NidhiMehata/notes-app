from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

if TYPE_CHECKING:
    from models.note import Note
    from models.user import User


class CollaboratorRole(Enum):
    viewer = "viewer"
    editor = "editor"


class NoteCollaborator(Base):
    __tablename__ = "note_collaborators"

    id: Mapped[int] = mapped_column(primary_key=True)

    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    role: Mapped[CollaboratorRole] = mapped_column(
        SAEnum(CollaboratorRole), default=CollaboratorRole.viewer
    )

    created_at: Mapped[datetime] = mapped_column()

    # relationships
    note: Mapped["Note"] = relationship(back_populates="collaborator_links")
    user: Mapped["User"] = relationship(back_populates="collaborator_links")
