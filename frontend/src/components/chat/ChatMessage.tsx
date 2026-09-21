import ReactMarkdown from "react-markdown";

import type { ChatItem } from "../../types/chat";

import RetrievalMetrics from "./RetrievalMetrics";
import SourceCard from "./SourceCard";

interface ChatMessageProps {
  item: ChatItem;
}

function ChatMessage({
  item,
}: ChatMessageProps) {
  return (
    <article className="conversation-item">
      {/* User question */}
      <div className="user-message">
        <div className="message-label">
          You
        </div>

        <p>{item.question}</p>
      </div>

      {/* Assistant response */}
      <div className="assistant-message">
        <div className="message-label">
          Assistant
        </div>

        <div className="answer-text">
          <ReactMarkdown>
            {item.response.answer}
          </ReactMarkdown>
        </div>

        {/* Retrieved sources */}
        {item.response.sources.length > 0 && (
          <div className="sources">
            <h4>Retrieved sources</h4>

            <div className="source-grid">
              {item.response.sources.map(
                (source) => (
                  <SourceCard
                    key={source.chunk_id}
                    source={source}
                  />
                ),
              )}
            </div>
          </div>
        )}

        {/* Retrieval performance */}
        <RetrievalMetrics
          retrieval={item.response.retrieval}
        />
      </div>
    </article>
  );
}

export default ChatMessage;