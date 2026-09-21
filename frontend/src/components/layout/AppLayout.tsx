import {
  type ChangeEvent,
  type FormEvent,
  useState,
} from "react";

import type { Document } from "../../types/api";
import type { ChatItem } from "../../types/chat";

import ChatPanel from "../chat/ChatPanel";
import Header from "./Header";
import Sidebar from "./Sidebar";

interface AppLayoutProps {
  documents: Document[];
  chat: ChatItem[];
  question: string;

  loadingDocuments: boolean;
  uploading: boolean;
  asking: boolean;

  error: string | null;

  onQuestionChange: (value: string) => void;

  onSubmit: (
    event: FormEvent<HTMLFormElement>,
  ) => void;

  onFileChange: (
    event: ChangeEvent<HTMLInputElement>,
  ) => void;

  onDismissError: () => void;
}

function AppLayout({
  documents,
  chat,
  question,
  loadingDocuments,
  uploading,
  asking,
  error,
  onQuestionChange,
  onSubmit,
  onFileChange,
  onDismissError,
}: AppLayoutProps) {
  const [sidebarOpen, setSidebarOpen] =
    useState(false);

  return (
    <div className="app-shell">
      <Sidebar
        documents={documents}
        loadingDocuments={loadingDocuments}
        uploading={uploading}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onFileChange={onFileChange}
      />

      {sidebarOpen && (
        <button
          type="button"
          className="sidebar-backdrop"
          aria-label="Close knowledge base"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      <main className="main-panel">
        <Header
          onMenuClick={() =>
            setSidebarOpen(true)
          }
        />

        {error && (
          <div className="error-banner">
            <span>{error}</span>

            <button
              type="button"
              onClick={onDismissError}
              aria-label="Dismiss error"
            >
              ×
            </button>
          </div>
        )}

        <ChatPanel
          chat={chat}
          question={question}
          asking={asking}
          hasDocuments={documents.length > 0}
          onQuestionChange={onQuestionChange}
          onSubmit={onSubmit}
        />
      </main>
    </div>
  );
}

export default AppLayout;