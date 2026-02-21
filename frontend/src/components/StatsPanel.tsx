'use client';

import { useState, useEffect } from 'react';
import { Database, Brain, RefreshCw } from 'lucide-react';
import { apiClient, StatsResponse } from '@/lib/api';

export default function StatsPanel() {
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const loadStats = async () => {
    setLoading(true);
    try {
      const data = await apiClient.getStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  if (loading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-gray-800">System Stats</h3>
        <button
          onClick={loadStats}
          className="p-2 text-gray-500 hover:text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
        >
          <RefreshCw className="w-4 h-4" />
        </button>
      </div>

      <div className="space-y-4">
        {/* Vector Store */}
        <div className="flex items-start gap-3">
          <Database className="w-5 h-5 text-blue-500 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-gray-700">Vector Store</p>
            <p className="text-xs text-gray-500">
              Collection: {stats.vector_store.collection}
            </p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {stats.vector_store.document_count} documents
            </p>
          </div>
        </div>

        {/* Agent */}
        <div className="flex items-start gap-3">
          <Brain className="w-5 h-5 text-purple-500 mt-0.5" />
          <div>
            <p className="text-sm font-medium text-gray-700">Agent</p>
            <p className="text-xs text-gray-500">Model: {stats.agent.model}</p>
            <p className="text-xs text-gray-500">
              Tools: {stats.agent.tools.length}
            </p>
            <p className="text-xs text-gray-500">
              Memory: {stats.agent.memory_enabled ? 'Enabled' : 'Disabled'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}