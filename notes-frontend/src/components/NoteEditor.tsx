import { useState } from "react";
import "./NoteEditor.css";
import Toast from "./Toast";
import { deleteNote, updateNote } from "../api/notes";

type Note = {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

type NoteEditorProps = {
  note: Note | null;
  isNewNote: boolean;
  onBack: () => void;
  onSave: (title: string, content: string) => void;
};

function NoteEditor({ note, isNewNote, onBack, onSave }: NoteEditorProps) {
  const [title, setTitle] = useState(note?.title ?? "");
  const [content, setContent] = useState(note?.content ?? "");
  const [errorMessage, setErrorMessage] = useState("");
  const [saveFailed, setSaveFailed] = useState(false);

  async function saveChanges() {
    if (!note) {
      return;
    }

    const updates: { title?: string; content?: string } = {};

    if (title !== note.title) {
      updates.title = title;
    }

    if (content !== note.content) {
      updates.content = content;
    }

    if (Object.keys(updates).length === 0) {
      onBack();
      return;
    }

    try {
      await updateNote(note.id, updates);
      setSaveFailed(false);
      onBack();
    } catch (error) {
      console.error(error);
      setErrorMessage("Failed to save changes. Please save again or discard.");
      setSaveFailed(true);
    }
  }

  //   useEffect(() => {
  //     if (isNewNote || !note) {
  //       return;
  //     }

  // const timeout = setTimeout(() => {
  //   updateNote(note.id, title, content)
  //     .then(() => {
  //       console.log("Note auto-saved");
  //     })
  //     .catch((error) => {
  //       console.error(error);
  //     });
  // }, 500);

  // return () => clearTimeout(timeout);
  //   }, [title, content, note, isNewNote]);

  return (
    <main className="editor-page">
      <div className="editor-container">
        <header className="editor-header">
          <button className="back-button" disabled={saveFailed} onClick={saveChanges}>
            ← Back
          </button>

          <div className="editor-actions">
            {saveFailed && (
              <>
                <button className="discard-button" onClick={onBack}>
                  Discard & Back
                </button>
                <button className="save-button" onClick={saveChanges}>
                  Save
                </button>
              </>
            )}

            {!isNewNote && !saveFailed && note && (
              <button
                className="delete-button"
                onClick={async () => {
                  const confirmed = window.confirm(
                    "Are you sure you want to delete this note?",
                  );

                  if (!confirmed) {
                    return;
                  }

                  try {
                    await deleteNote(note.id);
                    onBack();
                  } catch (error) {
                    console.error(error);
                    setErrorMessage("Failed to delete note. Please try again.");
                  }
                }}
              >
                Delete
              </button>
            )}

            {isNewNote && (
              <>
                <button className="cancel-button" onClick={onBack}>
                  Cancel
                </button>

                <button className="save-button" onClick={() => onSave(title, content)}>
                  Save Note
                </button>
              </>
            )}
          </div>
        </header>

        <Toast
          message={errorMessage}
          onClose={() => setErrorMessage("")}
          custom_timeout={4000}
        />
        <input
          className="editor-title"
          placeholder="Note title"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />

        <textarea
          className="editor-content"
          placeholder="Start writing..."
          value={content}
          onChange={(event) => setContent(event.target.value)}
        />
      </div>
    </main>
  );
}

export default NoteEditor;
