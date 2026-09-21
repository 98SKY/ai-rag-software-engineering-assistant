import type {
  FormEvent,
} from "react";

interface QuestionInputProps {
  question: string;
  asking: boolean;
  hasDocuments: boolean;

  onQuestionChange: (value: string) => void;

  onSubmit: (
    event: FormEvent<HTMLFormElement>,
  ) => void;
}

function QuestionInput({
  question,
  asking,
  hasDocuments,
  onQuestionChange,
  onSubmit,
}: QuestionInputProps) {
  return (
    <form
      className="question-form"
      onSubmit={onSubmit}
    >
      <div className="question-box">
        <textarea
          value={question}
          onChange={(event) =>
            onQuestionChange(
              event.target.value,
            )
          }
          placeholder={
            hasDocuments
              ? "Ask a question about your documents..."
              : "Upload a document to begin..."
          }
          disabled={!hasDocuments || asking}
          rows={1}
        />

        <button
          type="submit"
          disabled={
            !hasDocuments ||
            asking ||
            !question.trim()
          }
        >
          {asking ? "Thinking..." : "Ask"}
        </button>
      </div>

      <p className="input-hint">
        Answers are generated from retrieved
        document context. Verify important
        information against the cited sources.
      </p>
    </form>
  );
}

export default QuestionInput;