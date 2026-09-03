import { useEffect, useState } from "react";
import { deleteNote, getNotes } from "../api/notes";
import "./Notes.css";

type Note = {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

type NotesProps = {
  onNewNote: () => void;
  onSelectNote: (note: Note) => void;
  onLogout: () => void;
};

function Notes({ onNewNote, onSelectNote, onLogout }: NotesProps) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadNotes() {
      try {
        setIsLoading(true);

        const data = await getNotes();
        setNotes(data);
      } catch (error) {
        if (error instanceof Error && error.message === "Unauthorized") {
          onLogout();
          return;
        }

        console.error(error);
      } finally {
        setIsLoading(false);
      }
    }

    loadNotes();
  }, [onLogout]);

  return (
    <main className="notes-page">
      <div className="notes-container">
        <header className="notes-header">
          <div>
            <h1 className="notes-title">My Notes</h1>
          </div>

          <div className="notes-actions">
            <button className="create-note-button" onClick={onNewNote}>
              + New Note
            </button>

            <button className="logout-button" onClick={onLogout}>
              Logout
            </button>
          </div>
        </header>

        <section className="notes-list">
          {isLoading ? (
            <p className="notes-loading">Loading notes...</p>
          ) : (
            notes.map((note) => (
              <article
                className="note-row"
                key={note.id}
                onClick={() => onSelectNote(note)}
              >
                <div className="note-info">
                  <h2 className="note-title">{note.title}</h2>

                  <p className="note-content">{note.content}</p>
                </div>

                <div className="note-date">
                  {new Date(note.created_at).toLocaleDateString()}
                </div>

                <button
                  className="note-delete-button"
                  onClick={async (event) => {
                    event.stopPropagation();

                    const confirmed = window.confirm(
                      "Are you sure you want to delete this note?",
                    );

                    if (!confirmed) {
                      return;
                    }

                    try {
                      await deleteNote(note.id);

                      setNotes((currentNotes) =>
                        currentNotes.filter(
                          (currentNote) => currentNote.id !== note.id,
                        ),
                      );
                    } catch (error) {
                      console.error(error);
                    }
                  }}
                  aria-label="Delete note"
                >
                  <svg
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  >
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6l-1 14H6L5 6" />
                    <path d="M10 11v6" />
                    <path d="M14 11v6" />
                    <path d="M9 6V4h6v2" />
                  </svg>
                </button>
              </article>
            ))
          )}
        </section>
      </div>
    </main>
  );
}

export default Notes;
