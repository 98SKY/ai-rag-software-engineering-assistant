import type { Document } from "../../types/api";

import DocumentCard from "./DocumentCard";

interface DocumentListProps {
  documents: Document[];
  loading: boolean;
}

function DocumentList({
  documents,
  loading,
}: DocumentListProps) {
  if (loading) {
    return (
      <div className="document-list">
        <p className="muted">
          Loading documents...
        </p>
      </div>
    );
  }

  if (documents.length === 0) {
    return (
      <div className="document-list">
        <div className="empty-documents">
          <span>📄</span>
          <p>No documents indexed yet.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="document-list">
      {documents.map((document) => (
        <DocumentCard
          key={document.id}
          document={document}
        />
      ))}
    </div>
  );
}

export default DocumentList;