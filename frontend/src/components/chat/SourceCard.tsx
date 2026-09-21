import type { SourceReference } from "../../types/api";

interface SourceCardProps {
  source: SourceReference;
}

function SourceCard({
  source,
}: SourceCardProps) {
  return (
    <div className="source-card">
      <div className="source-number">
        Source {source.source_number}
      </div>

      <strong title={source.filename}>
        {source.filename}
      </strong>

      <span>
        Chunk {source.chunk_index}
      </span>

      <span>
        Similarity{" "}
        {source.score.toFixed(3)}
      </span>
    </div>
  );
}

export default SourceCard;