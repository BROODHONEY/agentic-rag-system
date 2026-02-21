'use client';

import { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { FileText, ChevronDown, ChevronRight, Database, Hash, Loader2, Trash2, AlertTriangle, X } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface Chunk {
  id: string;
  content: string;
  metadata: Record<string, unknown>;
  embedding_dim: number;
  content_length: number;
}

interface Document {
  source: string;
  chunks: Chunk[];
  total_chunks: number;
}

interface DocumentsData {
  documents: Document[];
  total_documents: number;
  total_chunks: number;
}

export interface DocumentsPanelRef {
  refresh: () => Promise<void>;
}

const DocumentsPanel = forwardRef<DocumentsPanelRef>((props, ref) => {
  const [data, setData] = useState<DocumentsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [expandedDocs, setExpandedDocs] = useState<Set<string>>(new Set());
  const [expandedChunks, setExpandedChunks] = useState<Set<string>>(new Set());
  const [showConfirm, setShowConfirm] = useState(false);
  const [clearing, setClearing] = useState(false);
  const [deletingDoc, setDeletingDoc] = useState<string | null>(null);

  const fetchDocuments = async () => {
    try {
      setLoading(true);
      const result = await apiClient.getAllDocuments();
      setData(result);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  // Expose refresh method to parent via ref
  useImperativeHandle(ref, () => ({
    refresh: fetchDocuments,
  }), []);

  const toggleDocument = (source: string) => {
    const newExpanded = new Set(expandedDocs);
    if (newExpanded.has(source)) {
      newExpanded.delete(source);
    } else {
      newExpanded.add(source);
    }
    setExpandedDocs(newExpanded);
  };

  const toggleChunk = (chunkId: string) => {
    const newExpanded = new Set(expandedChunks);
    if (newExpanded.has(chunkId)) {
      newExpanded.delete(chunkId);
    } else {
      newExpanded.add(chunkId);
    }
    setExpandedChunks(newExpanded);
  };

  const handleClearAll = async () => {
    try {
      setClearing(true);
      await apiClient.resetVectorStore();
      setData({ documents: [], total_documents: 0, total_chunks: 0 });
      setExpandedDocs(new Set());
      setExpandedChunks(new Set());
      setShowConfirm(false);
    } catch (error) {
      console.error('Failed to clear embeddings:', error);
      alert('Failed to clear embeddings. Please try again.');
    } finally {
      setClearing(false);
    }
  };

  const handleDeleteDocument = async (source: string, e: React.MouseEvent) => {
    e.stopPropagation();
    
    if (!confirm(`Delete "${source.split('/').pop()}" and all its chunks?`)) {
      return;
    }

    try {
      setDeletingDoc(source);
      await apiClient.deleteDocument(source);
      await fetchDocuments();
    } catch (error) {
      console.error('Failed to delete document:', error);
      alert('Failed to delete document. Please try again.');
    } finally {
      setDeletingDoc(null);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Database className="w-5 h-5 text-purple-600" />
          <h2 className="text-lg font-semibold text-gray-800">Documents & Embeddings</h2>
        </div>
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 text-gray-400 animate-spin" />
        </div>
      </div>
    );
  }

  if (!data || data.documents.length === 0) {
    return (
      <div className="p-6">
        <div className="flex items-center gap-2 mb-4">
          <Database className="w-5 h-5 text-purple-600" />
          <h2 className="text-lg font-semibold text-gray-800">Documents & Embeddings</h2>
        </div>
        <div className="text-center py-8 text-gray-500 text-sm">
          No documents uploaded yet
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-purple-600" />
          <h2 className="text-lg font-semibold text-gray-800">Documents & Embeddings</h2>
        </div>
        <div className="flex items-center gap-2">
          <div className="text-xs text-gray-500">
            {data.total_documents} docs • {data.total_chunks} chunks
          </div>
          {data.total_documents > 0 && (
            <button
              onClick={() => setShowConfirm(true)}
              disabled={clearing}
              className="p-1.5 text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
              title="Clear all embeddings"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>

      {/* Confirmation Dialog */}
      {showConfirm && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-1">
              <h3 className="text-sm font-semibold text-red-900 mb-1">
                Clear All Embeddings?
              </h3>
              <p className="text-xs text-red-700 mb-3">
                This will permanently delete all {data.total_documents} documents and {data.total_chunks} chunks from the vector store. This action cannot be undone.
              </p>
              <div className="flex gap-2">
                <button
                  onClick={handleClearAll}
                  disabled={clearing}
                  className="px-3 py-1.5 bg-red-600 text-white text-xs font-medium rounded hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center gap-1"
                >
                  {clearing ? (
                    <>
                      <Loader2 className="w-3 h-3 animate-spin" />
                      Clearing...
                    </>
                  ) : (
                    'Yes, Clear All'
                  )}
                </button>
                <button
                  onClick={() => setShowConfirm(false)}
                  disabled={clearing}
                  className="px-3 py-1.5 bg-white text-gray-700 text-xs font-medium rounded border border-gray-300 hover:bg-gray-50 transition-colors disabled:opacity-50"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="space-y-2 max-h-96 overflow-y-auto">
        {data.documents.map((doc) => (
          <div key={doc.source} className="border border-gray-200 rounded-lg overflow-hidden">
            {/* Document Header */}
            <button
              onClick={() => toggleDocument(doc.source)}
              className="w-full px-4 py-3 bg-gray-50 hover:bg-gray-100 flex items-center justify-between transition-colors"
            >
              <div className="flex items-center gap-2 flex-1 min-w-0">
                {expandedDocs.has(doc.source) ? (
                  <ChevronDown className="w-4 h-4 text-gray-500 flex-shrink-0" />
                ) : (
                  <ChevronRight className="w-4 h-4 text-gray-500 flex-shrink-0" />
                )}
                <FileText className="w-4 h-4 text-blue-600 flex-shrink-0" />
                <span className="text-sm font-medium text-gray-700 truncate" title={doc.source}>
                  {doc.source.split(/[/\\]/).pop() || doc.source}
                </span>
              </div>
              <div className="flex items-center gap-2 flex-shrink-0">
                <span className="text-xs text-gray-500 bg-white px-2 py-1 rounded">
                  {doc.total_chunks} chunks
                </span>
                <button
                  onClick={(e) => handleDeleteDocument(doc.source, e)}
                  disabled={deletingDoc === doc.source}
                  className="p-1 text-red-600 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
                  title="Delete document"
                >
                  {deletingDoc === doc.source ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <X className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>
            </button>

            {/* Chunks List */}
            {expandedDocs.has(doc.source) && (
              <div className="bg-white divide-y divide-gray-100">
                {doc.chunks.map((chunk, idx) => (
                  <div key={chunk.id} className="px-4 py-2">
                    <button
                      onClick={() => toggleChunk(chunk.id)}
                      className="w-full flex items-start gap-2 text-left hover:bg-gray-50 p-2 rounded transition-colors"
                    >
                      {expandedChunks.has(chunk.id) ? (
                        <ChevronDown className="w-3 h-3 text-gray-400 mt-0.5 flex-shrink-0" />
                      ) : (
                        <ChevronRight className="w-3 h-3 text-gray-400 mt-0.5 flex-shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-medium text-gray-600">
                            Chunk {idx + 1}
                          </span>
                          <span className="text-xs text-gray-400">
                            {chunk.content_length} chars
                          </span>
                          {chunk.embedding_dim > 0 && (
                            <span className="text-xs text-purple-600 flex items-center gap-1">
                              <Hash className="w-3 h-3" />
                              {chunk.embedding_dim}D
                            </span>
                          )}
                        </div>
                        <p className="text-xs text-gray-500 line-clamp-2">
                          {chunk.content}
                        </p>
                      </div>
                    </button>

                    {/* Expanded Chunk Details */}
                    {expandedChunks.has(chunk.id) && (
                      <div className="mt-2 ml-5 p-3 bg-gray-50 rounded text-xs space-y-2">
                        <div>
                          <span className="font-medium text-gray-700">Content:</span>
                          <p className="text-gray-600 mt-1 whitespace-pre-wrap">
                            {chunk.content}
                          </p>
                        </div>
                        <div>
                          <span className="font-medium text-gray-700">Metadata:</span>
                          <pre className="text-gray-600 mt-1 overflow-x-auto">
                            {JSON.stringify(chunk.metadata, null, 2)}
                          </pre>
                        </div>
                        <div className="flex items-center gap-4 text-gray-600">
                          <span>ID: {chunk.id}</span>
                          {chunk.embedding_dim > 0 && (
                            <span>Embedding: {chunk.embedding_dim} dimensions</span>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
});

DocumentsPanel.displayName = 'DocumentsPanel';

export default DocumentsPanel;
