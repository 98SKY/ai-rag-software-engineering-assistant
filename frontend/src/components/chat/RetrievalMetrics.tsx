import type {
  RetrievalMetadata,
} from "../../types/api";

interface RetrievalMetricsProps {
  retrieval: RetrievalMetadata;
}

function seconds(milliseconds: number) {
  return (milliseconds / 1000).toFixed(2);
}

function RetrievalMetrics({
  retrieval,
}: RetrievalMetricsProps) {
  return (
    <div className="metrics">
      <span>
        Retrieval{" "}
        {seconds(
          retrieval.retrieval_time_ms,
        )}
        s
      </span>

      <span>
        Generation{" "}
        {seconds(
          retrieval.generation_time_ms,
        )}
        s
      </span>

      <span>
        Total{" "}
        {seconds(
          retrieval.total_time_ms,
        )}
        s
      </span>
    </div>
  );
}

export default RetrievalMetrics;