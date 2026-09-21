import type { AskResponse } from "./api";

export interface ChatItem {
  id: string;
  question: string;
  response: AskResponse;
}