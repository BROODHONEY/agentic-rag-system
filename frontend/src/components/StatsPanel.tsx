'use client';

import { useState, useEffect } from 'react';
import { Database, Brain, RefreshCw, FileText, Zap, HardDrive, Cpu, Settings } from 'lucide-react';
import { apiClient, StatsResponse } from '@/lib/api';

export default function StatsPanel() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadStats = async (isManual = false) => {
    if (isManual) {
      setRefreshing(true);
    }
    
    try {
      const data = await apiClient.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadStats();
    // Refresh every 60 seconds (less frequent)
    const interval = setInterval(() => loadStats(), 60000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="library-card p-6 rounded-xl">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-[#e8e4d8] rounded w-1/2"></div>
          <div className="h-4 bg-[#e8e4d8] rounded w-3/4"></div>
          <div className="h-4 bg-[#e8e4d8] rounded w-2/3"></div>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="library-card p-6 rounded-xl">
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-2">
          <Settings className="w-5 h-5 text-[#8b4513]" />
          <h3 className="text-lg font-semibold text-[#3e2723]" style={{ fontFamily: 'Georgia, serif' }}>
            Library System
          </h3>
        </div>
        <button
          onClick={() => loadStats(true)}
          disabled={refreshing}
          className="p-1.5 text-[#8b4513] hover:text-[#d4af37] hover:bg-[#e8e4d8] rounded-lg transition-colors disabled:opacity-50"
          title="Refresh stats"
        >
          <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
        </button>
      </div>

      <div className="space-y-3">
        {/* Vector Store Type */}
        <div className="bg-gradient-to-br from-[#e8e4d8] to-[#f8f6f0] p-4 rounded-lg border-2 border-[#8b4513]/20">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-[#8b4513] rounded-lg">
              <Database className="w-5 h-5 text-[#f8f6f0]" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-[#3e2723] mb-2" style={{ fontFamily: 'Georgia, serif' }}>
                Vector Database
              </p>
              <div className="space-y-1 text-xs text-[#3e2723]">
                <div className="flex justify-between items-center">
                  <span className="text-[#8b4513]">Type:</span>
                  <span className="font-bold text-[#d4af37] bg-[#3e2723] px-2 py-0.5 rounded">
                    {stats.vector_store.type || 'CHROMA'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Documents:</span>
                  <span className="font-semibold">{stats.vector_store.document_count}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Collection:</span>
                  <span className="font-medium truncate max-w-[120px]" title={stats.vector_store.collection}>
                    {stats.vector_store.collection}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Storage Location */}
        <div className="bg-gradient-to-br from-[#e8e4d8] to-[#f8f6f0] p-4 rounded-lg border-2 border-[#8b4513]/20">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-[#2d5016] rounded-lg">
              <HardDrive className="w-5 h-5 text-[#f8f6f0]" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-[#3e2723] mb-2" style={{ fontFamily: 'Georgia, serif' }}>
                Storage
              </p>
              <div className="space-y-1 text-xs text-[#3e2723]">
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Location:</span>
                  <span className="font-medium text-right truncate max-w-[140px]" title={stats.vector_store.persist_directory}>
                    {stats.vector_store.persist_directory?.includes('Cloud') ? '☁️ Cloud' : '💾 Local'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Embedding:</span>
                  <span className="font-medium truncate max-w-[120px]" title={stats.vector_store.embedding_model}>
                    {stats.vector_store.embedding_model?.split('/').pop() || 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Agent Info */}
        <div className="bg-gradient-to-br from-[#e8e4d8] to-[#f8f6f0] p-4 rounded-lg border-2 border-[#8b4513]/20">
          <div className="flex items-start gap-3">
            <div className="p-2 bg-[#800020] rounded-lg">
              <Brain className="w-5 h-5 text-[#f8f6f0]" />
            </div>
            <div className="flex-1">
              <p className="text-sm font-semibold text-[#3e2723] mb-2" style={{ fontFamily: 'Georgia, serif' }}>
                AI Agent
              </p>
              <div className="space-y-1 text-xs text-[#3e2723]">
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Model:</span>
                  <span className="font-medium">{stats.agent.model?.split('-')[0] || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Tools:</span>
                  <span className="font-medium">{stats.agent.tools?.length || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Memory:</span>
                  <span className="font-medium">
                    {stats.agent.memory_enabled ? '✓ Enabled' : '✗ Disabled'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Temperature:</span>
                  <span className="font-medium">{stats.agent.temperature ?? 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-[#8b4513]">Top-K:</span>
                  <span className="font-medium">{stats.agent.top_k ?? 5}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Badge */}
        <div className="pt-3 border-t-2 border-[#8b4513]/20">
          <div className="flex items-center justify-center gap-2 text-xs text-[#8b4513]">
            <Zap className="w-3.5 h-3.5 text-[#d4af37]" />
            <span className="font-medium italic">
              Powered by Groq & {stats.vector_store.type || 'ChromaDB'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}