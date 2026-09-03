import { apiFetch } from "./client";

export async function getNotes() {
  const response = await apiFetch("/notes");

  if (!response.ok) {
    throw new Error("Failed to fetch notes");
  }

  return response.json();
}

export async function createNote(title: string, content: string) {
  const response = await apiFetch("/notes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      title,
      content,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to create note");
  }

  return response.json();
}

export async function updateNote(
  noteId: number,
  updates: { title?: string; content?: string },
) {
  const response = await apiFetch(`/notes/${noteId}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(updates),
  });

  if (!response.ok) {
    throw new Error("Failed to update note");
  }

  return response.json();
}

export async function deleteNote(noteId: number) {
  const response = await apiFetch(`/notes/${noteId}`, {
    method: "DELETE",
  });

  if (!response.ok) {
    throw new Error("Failed to delete note");
  }
}
