from datetime import datetime

from pydantic import BaseModel, model_serializer


class NoteCreateData(BaseModel):
    title: str
    content: str


class NoteUpdateData(BaseModel):
    title: str | None = None
    content: str | None = None


class NoteResponseData(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @model_serializer(mode="wrap")
    def serialize_model(self, handler):
        data = handler(self)

        if self.created_at.tzinfo and self.updated_at.tzinfo:
            data["updated_at"] = self.updated_at.astimezone(
                self.created_at.tzinfo
            ).isoformat()

        return data
