import type { ChangeEvent } from "react";

interface DocumentUploadProps {
  uploading: boolean;

  onFileChange: (
    event: ChangeEvent<HTMLInputElement>,
  ) => void;
}

function DocumentUpload({
  uploading,
  onFileChange,
}: DocumentUploadProps) {
  return (
    <label className="upload-button">
      <input
        type="file"
        accept=".pdf,.txt,.md"
        disabled={uploading}
        onChange={onFileChange}
      />

      {uploading
        ? "Indexing document..."
        : "+ Add document"}
    </label>
  );
}

export default DocumentUpload;