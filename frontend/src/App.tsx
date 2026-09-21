import {
  type ChangeEvent,
  type FormEvent,
  useCallback,
  useEffect,
  useState,
} from "react";

import AppLayout from "./components/layout/AppLayout";

import {
  askQuestion,
  getDocuments,
  uploadDocument,
} from "./services/api";

import type { Document } from "./types/api";
import type { ChatItem } from "./types/chat";

import "./App.css";

function App() {
  const [documents, setDocuments] = useState<Document[]>(
    [],
  );

  const [chat, setChat] = useState<ChatItem[]>([]);
  const [question, setQuestion] = useState("");

  const [loadingDocuments, setLoadingDocuments] =
    useState(true);

  const [uploading, setUploading] = useState(false);
  const [asking, setAsking] = useState(false);

  const [error, setError] = useState<string | null>(
    null,
  );

  const loadDocuments = useCallback(async () => {
    try {
      setLoadingDocuments(true);

      const result = await getDocuments();

      setDocuments(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to load documents.",
      );
    } finally {
      setLoadingDocuments(false);
    }
  }, []);

  useEffect(() => {
    void loadDocuments();
  }, [loadDocuments]);

  async function handleFileChange(
    event: ChangeEvent<HTMLInputElement>,
  ) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    try {
      setError(null);
      setUploading(true);

      await uploadDocument(file);

      await loadDocuments();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Document upload failed.",
      );
    } finally {
      setUploading(false);
      event.target.value = "";
    }
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || asking) {
      return;
    }

    try {
      setError(null);
      setAsking(true);

      const response = await askQuestion({
        question: trimmedQuestion,
        top_k: 5,
      });

      setChat((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          question: trimmedQuestion,
          response,
        },
      ]);

      setQuestion("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to generate an answer.",
      );
    } finally {
      setAsking(false);
    }
  }

  return (
    <AppLayout
      documents={documents}
      chat={chat}
      question={question}
      loadingDocuments={loadingDocuments}
      uploading={uploading}
      asking={asking}
      error={error}
      onQuestionChange={setQuestion}
      onSubmit={handleSubmit}
      onFileChange={handleFileChange}
      onDismissError={() => setError(null)}
    />
  );
}

export default App;