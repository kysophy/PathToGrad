import { createContext, useState, useContext, ReactNode } from 'react';

export interface ChatMessage {
  id: string;
  role: 'user' | 'agent';
  content: string;
}

interface ChatContextType {
  messages: ChatMessage[];
  addMessage: (message: ChatMessage) => void;
  isTyping: boolean;
  setIsTyping: (typing: boolean) => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export function ChatProvider({ children }: { children: ReactNode }) {
  // Initialize with a welcome message
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: '1', role: 'agent', content: 'Hi! I can help you generate a study plan. What do you want to focus on this semester?' }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const addMessage = (message: ChatMessage) => {
    setMessages((prev) => [...prev, message]);
  };

  return (
    <ChatContext.Provider value={{ messages, addMessage, isTyping, setIsTyping }}>
      {children}
    </ChatContext.Provider>
  );
}

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error("useChat must be used within a ChatProvider");
  return context;
};