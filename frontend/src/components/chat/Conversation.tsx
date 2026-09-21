import {
  useEffect,
  useRef,
} from "react";

import type { ChatItem } from "../../types/chat";

import ChatMessage from "./ChatMessage";
import ThinkingIndicator from "./ThinkingIndicator";
import WelcomeState from "./WelcomeState";

interface ConversationProps {
  chat: ChatItem[];
  asking: boolean;

  onSuggestion: (question: string) => void;
}

function Conversation({
  chat,
  asking,
  onSuggestion,
}: ConversationProps) {
  const bottomRef =
    useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [chat, asking]);

  return (
    <div className="chat-scroll-area">
      <div className="conversation">
        {chat.length === 0 ? (
          <WelcomeState
            onSuggestion={onSuggestion}
          />
        ) : (
          <>
            {chat.map((item) => (
              <ChatMessage
                key={item.id}
                item={item}
              />
            ))}

            {asking && (
              <ThinkingIndicator />
            )}
          </>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}

export default Conversation;