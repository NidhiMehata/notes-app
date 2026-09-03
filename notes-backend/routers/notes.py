from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import services.note as note_service
from database.database import get_db
from models.user import User
from schemas.notes import NoteCreateData, NoteResponseData, NoteUpdateData
from utils.auth import get_current_user

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("", response_model=list[NoteResponseData], status_code=status.HTTP_200_OK)
def get_all_notes(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    notes = note_service.get_all_notes_for_a_user(db=db, current_user=current_user)
    return notes


@router.get(
    "/{note_id}", response_model=NoteResponseData, status_code=status.HTTP_200_OK
)
def get_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    note = note_service.get_note(db=db, note_id=note_id, current_user=current_user)
    return note


@router.post("", response_model=NoteResponseData, status_code=status.HTTP_201_CREATED)
def create_note(
    note_data: NoteCreateData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    created_note = note_service.create_note(
        db=db, note_data=note_data, current_user=current_user
    )
    return created_note


@router.patch("/{note_id}", status_code=status.HTTP_200_OK)
def update_note(
    note_id: int,
    note_data: NoteUpdateData,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> NoteResponseData:

    note = note_service.update_note(
        db=db, note_id=note_id, note_data=note_data, current_user=current_user
    )
    return note


@router.delete("/{note_id}", status_code=status.HTTP_200_OK)
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    note_service.delete_note(db=db, note_id=note_id, current_user=current_user)
