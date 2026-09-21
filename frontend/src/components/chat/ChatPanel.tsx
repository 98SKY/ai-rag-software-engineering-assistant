import type {
  FormEvent,
} from "react";

import type { ChatItem } from "../../types/chat";

import Conversation from "./Conversation";
import QuestionInput from "./QuestionInput";

interface ChatPanelProps {
  chat: ChatItem[];
  question: string;
  asking: boolean;
  hasDocuments: boolean;

  onQuestionChange: (value: string) => void;

  onSubmit: (
    event: FormEvent<HTMLFormElement>,
  ) => void;
}

function ChatPanel({
  chat,
  question,
  asking,
  hasDocuments,
  onQuestionChange,
  onSubmit,
}: ChatPanelProps) {
  return (
    <section className="chat-panel">
      <Conversation
        chat={chat}
        asking={asking}
        onSuggestion={onQuestionChange}
      />

      <QuestionInput
        question={question}
        asking={asking}
        hasDocuments={hasDocuments}
        onQuestionChange={onQuestionChange}
        onSubmit={onSubmit}
      />
    </section>
  );
}

export default ChatPanel;