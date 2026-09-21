import type { Document } from "../../types/api";

interface DocumentCardProps {
  document: Document;
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
    </div>
  );
}

export default DocumentCard;