import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions import NoteNotFoundError
from models.note import Note
from models.user import User
from schemas.notes import NoteCreateData, NoteUpdateData

logger = logging.getLogger(__name__)


def create_note(db: Session, note_data: NoteCreateData, current_user: User) -> Note:
    note = Note(
        title=note_data.title, content=note_data.content, owner_id=current_user.id
    )

    db.add(note)
    db.flush()

    logger.info(f"Note created with id {note.id}")

    return note


def get_note(db: Session, note_id: int, current_user: User) -> Note:
    note = db.scalar(
        select(Note).where(
            Note.id == note_id,
            Note.is_deleted.is_(False),
            Note.owner_id == current_user.id,
        )
    )

    if not note:
        raise NoteNotFoundError(f"Note with id {note_id} does not exist")
    return note


def get_all_notes_for_a_user(db: Session, current_user: User) -> list[Note]:
    notes = db.scalars(
        select(Note)
        .where(Note.owner_id == current_user.id, Note.is_deleted.is_(False))
        .order_by(Note.created_at.desc())
    ).all()
    return notes


def update_note(
    db: Session, note_id: int, note_data: NoteUpdateData, current_user: User
) -> Note:
    note = get_note(db=db, note_id=note_id, current_user=current_user)

    if note_data.title is not None:
        note.title = note_data.title

    if note_data.content is not None:
        note.content = note_data.content

    db.flush()
    logger.info(f"Note update with id {note.id}")

    return note


def delete_note(db: Session, note_id: int, current_user: User) -> None:
    note = get_note(db=db, note_id=note_id, current_user=current_user)

    note.is_deleted = True
    logger.info(f"Note deleted with id {note.id}")

    db.flush()
