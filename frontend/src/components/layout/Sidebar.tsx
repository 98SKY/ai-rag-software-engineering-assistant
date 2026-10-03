import type { ChangeEvent } from "react";

import type { Document } from "../../types/api";

import DocumentList from "../documents/DocumentList";
import DocumentUpload from "../documents/DocumentUpload";

interface SidebarProps {
  documents: Document[];
  loadingDocuments: boolean;
  uploading: boolean;
  deletingId: string | null;
  open: boolean;

  onClose: () => void;

  onFileChange: (
    event: ChangeEvent<HTMLInputElement>,
  ) => void;

  onDeleteDocument: (
    document: Document,
  ) => void;
}

function Sidebar({
  documents,
  loadingDocuments,
  uploading,
  deletingId,
  open,
  onClose,
  onFileChange,
  onDeleteDocument
}: SidebarProps) {
  return (
    <aside
      className={`sidebar ${open ? "sidebar-open" : ""
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
        deletingId={deletingId}
        onDelete={onDeleteDocument}
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