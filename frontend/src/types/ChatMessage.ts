import { User } from "./User";
import { Chatbot } from "./Chatbot";

export type ChatMessage = {
  sender: User | Chatbot;
  timestamp: string;
  body: string;
  displayUserName: string;
  options?: Array<string> | Record<string, Array<string>>;
};
