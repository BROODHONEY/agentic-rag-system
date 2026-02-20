/**
 * API client for Agentic RAG backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface QueryRequest {
  question: string;
  conversation_id?: string;
}

export interface QueryResponse {
  answer: string;
  question: string;
  conversation_id?: string;
  metadata: {
    model: string;
    tools_used: number;
  };
}

export interface StatsResponse {
  vector_store: {
    collection: string;
    document_count: number;
    persist_directory: string;
  };
  agent: {
    tools: string[];
    model: string;
    memory_enabled: boolean;
  };
}

export interface IngestResponse {
  status: string;
  message: string;
  metadata: {
    filename: string;
    num_chunks: number;
    num_documents: number;
    total_in_db: number;
  };
}

export interface HealthResponse {
  status: string;
  model: string;
  vector_store: string;
  documents: number;
}

class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseURL}/health`);
    if (!response.ok) throw new Error('Health check failed');
    return response.json();
  }

  /**
   * Get system statistics
   */
  async getStats(): Promise<StatsResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/stats`);
    if (!response.ok) throw new Error('Failed to fetch stats');
    return response.json();
  }

  /**
   * Query the RAG system
   */
  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await fetch(`${this.baseURL}/api/v1/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Query failed');
    }

    return response.json();
  }

  /**
   * Upload and ingest a document
   */
  async ingestDocument(file: File): Promise<IngestResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${this.baseURL}/api/v1/ingest`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Upload failed');
    }

    return response.json();
  }

  /**
   * Search documents directly
   */
  async search(query: string, k: number = 5) {
    const response = await fetch(
      `${this.baseURL}/api/v1/search?query=${encodeURIComponent(query)}&k=${k}`
    );
    
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  }

  /**
   * Clear conversation history
   */
  async clearConversation(conversationId: string) {
    const response = await fetch(
      `${this.baseURL}/api/v1/conversation/${conversationId}`,
      {
        method: 'DELETE',
      }
    );

    if (!response.ok) throw new Error('Failed to clear conversation');
    return response.json();
  }
}

export const apiClient = new APIClient();