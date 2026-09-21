interface WelcomeStateProps {
  onSuggestion: (question: string) => void;
}

function WelcomeState({
  onSuggestion,
}: WelcomeStateProps) {
  return (
    <div className="welcome-state">
      <div className="welcome-icon">
        ✦
      </div>

      <h3>
        Ask your engineering knowledge base
      </h3>

      <p>
        Upload technical documents and ask
        questions. Answers are generated from
        retrieved evidence rather than general
        model knowledge.
      </p>

      <div className="suggestion-grid">
        <button
          type="button"
          onClick={() =>
            onSuggestion(
              "Summarize the backend architecture.",
            )
          }
        >
          Summarize the backend architecture
        </button>

        <button
          type="button"
          onClick={() =>
            onSuggestion(
              "What technologies are used in this project?",
            )
          }
        >
          What technologies are used?
        </button>

        <button
          type="button"
          onClick={() =>
            onSuggestion(
              "How do the services communicate?",
            )
          }
        >
          How do the services communicate?
        </button>
      </div>
    </div>
  );
}

export default WelcomeState;