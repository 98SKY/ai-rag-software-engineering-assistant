import type { ChangeEvent } from "react";

import type { Document } from "../../types/api";

import DocumentList from "../documents/DocumentList";
import DocumentUpload from "../documents/DocumentUpload";

interface SidebarProps {
  documents: Document[];
  loadingDocuments: boolean;
  uploading: boolean;
  open: boolean;

  onClose: () => void;

  onFileChange: (
    event: ChangeEvent<HTMLInputElement>,
  ) => void;
}

function Sidebar({
  documents,
  loadingDocuments,
  uploading,
  open,
  onClose,
  onFileChange,
}: SidebarProps) {
  return (
    <aside
      className={`sidebar ${
        open ? "sidebar-open" : ""
      }`}
    >
      <div className="brand">
        <div className="brand-icon">
          AI
        </div>

        <div className="brand-copy">
          <h1>SE Assistant</h1>
          <p>RAG Knowledge Base</p>
        </div>

        <button
          type="button"
          className="sidebar-close"
          onClick={onClose}
          aria-label="Close knowledge base"
        >
          ×
        </button>
      </div>

      <div className="sidebar-section">
        <div className="section-heading">
          <span>Knowledge Base</span>

          <span className="document-count">
            {documents.length}
          </span>
        </div>

        <DocumentUpload
          uploading={uploading}
          onFileChange={onFileChange}
        />
      </div>

      <DocumentList
        documents={documents}
        loading={loadingDocuments}
      />

      <div className="sidebar-footer">
        <span className="status-dot" />
        RAG backend connected
      </div>
    </aside>
  );
}

export default Sidebar;