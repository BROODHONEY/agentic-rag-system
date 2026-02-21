'use client';

import { useState, useEffect } from 'react';
import ChatInterface from '@/components/ChatInterface';
import UploadPanel from '@/components/UploadPanel';
import StatsPanel from '@/components/StatsPanel';
import { apiClient } from '@/lib/api';
import { AlertCircle, CheckCircle } from 'lucide-react';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiClient.healthCheck();
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
        console.error('API health check failed:', error);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white border-b shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Agentic RAG System</h1>
            <p className="text-sm text-gray-500">Powered by Groq & ChromaDB</p>
          </div>
          
          <div className="flex items-center gap-2">
            {apiStatus === 'online' ? (
              <>
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-green-600">API Online</span>
              </>
            ) : apiStatus === 'offline' ? (
              <>
                <AlertCircle className="w-5 h-5 text-red-500" />
                <span className="text-sm text-red-600">API Offline</span>
              </>
            ) : (
              <span className="text-sm text-gray-500">Checking...</span>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto p-4 grid grid-cols-1 lg:grid-cols-3 gap-4 h-[calc(100vh-100px)]">
        {/* Left Sidebar */}
        <div className="lg:col-span-1 space-y-4 overflow-y-auto">
          <div className="bg-white rounded-lg shadow-sm">
            <UploadPanel />
          </div>
          <StatsPanel />
        </div>

        {/* Chat Area */}
        <div className="lg:col-span-2 bg-white rounded-lg shadow-sm flex flex-col h-full">
          <ChatInterface />
        </div>
      </main>
    </div>
  );
}