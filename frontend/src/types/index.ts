export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  metadata?: any;
}

export interface ChatSession {
  id: string;
  messages: Message[];
  createdAt: Date;
}