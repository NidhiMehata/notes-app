import { useState } from "react";
import Login from "./Login";
import Notes from "./components/Notes";
import NoteEditor from "./components/NoteEditor";
import { createNote , updateNote} from "./api/notes";
import Toast from "./components/Toast";

type Note = {
  id: number;
  title: string;
  content: string;
  created_at: string;
  updated_at: string;
};

function App() {
  function handleLogout(message = "") {
    localStorage.removeItem("access_token");
    setAuthMessage(message);
    setCurrentView("list");
    setSelectedNote(null);

    setIsLoggedIn(false);
  }

  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("access_token"));

  const [currentView, setCurrentView] = useState("list");
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [authMessage, setAuthMessage] = useState("");

  if (!isLoggedIn) {
    return (
      <>
        <Login
          onLogin={() => {
            setAuthMessage("");
            setIsLoggedIn(true);
          }}
        />

        <Toast message={authMessage} onClose={() => setAuthMessage("")} />
      </>
    );
  }

  if (currentView === "new") {
    return (
      <NoteEditor
        note={null}
        isNewNote={true}
        onBack={() => setCurrentView("list")}
        onSave={async (title, content) => {
          try {
            await createNote(title, content);
            setCurrentView("list");
          } catch (error) {
            if (error instanceof Error && error.message === "Unauthorized") {
              handleLogout("Your session has expired. Please log in again.");
              return;
            }

            console.error(error);
          }
        }}
      />
    );
  }

  if (currentView === "edit" && selectedNote) {
    return (
      <NoteEditor
        note={selectedNote}
        isNewNote={false}
        onBack={() => setCurrentView("list")}
        onSave={async (title, content) => {
        try {
          await updateNote(selectedNote.id, { title, content });
          setCurrentView("list");
        } catch (error) {
          if (error instanceof Error && error.message === "Unauthorized") {
            handleLogout("Your session has expired. Please log in again.");
            return;
          }

          console.error(error);
        }
      }}
      />
    );
  }

  return (
    <Notes
      onNewNote={() => setCurrentView("new")}
      onSelectNote={(note) => {
        setSelectedNote(note);
        setCurrentView("edit");
      }}
      onLogout={() => handleLogout()}
    />
  );
}

export default App;
