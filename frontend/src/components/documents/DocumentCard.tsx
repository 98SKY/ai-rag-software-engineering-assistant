import type { Document } from "../../types/api";

interface DocumentCardProps {
  document: Document;
  deleting: boolean;
  onDelete: (document: Document) => void;
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(bytes / 1024).toFixed(1)} KB`;
  }

  return `${(
    bytes /
    (1024 * 1024)
  ).toFixed(1)} MB`;
}

function DocumentCard({
  document,
  deleting,
  onDelete,
}: DocumentCardProps) {
  return (
    <div className="document-card">
      <div className="document-icon">
        📄
      </div>

      <div className="document-info">
        <strong title={document.filename}>
          {document.filename}
        </strong>

        <span>
          {formatBytes(document.size)}
          {" · "}
          {document.chunk_count} chunks
        </span>
      </div>
      <button
        type="button"
        className="document-delete-button"
        disabled={deleting}
        aria-label={`Delete ${document.filename}`}
        title="Delete document"
        onClick={() => onDelete(document)}
      >
        {deleting ? (
          <span className="delete-loading">
            ...
          </span>
        ) : (
          <svg
            width="15"
            height="15"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
            aria-hidden="true"
          >
            <path d="M3 6h18" />
            <path d="M8 6V4h8v2" />
            <path d="M19 6l-1 14H6L5 6" />
            <path d="M10 11v5" />
            <path d="M14 11v5" />
          </svg>
        )}
      </button>
    </div>
  );
}

export default DocumentCard;