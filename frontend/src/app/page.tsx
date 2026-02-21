'use client';

import { useState, useEffect, useRef } from 'react';
import ChatInterface from '@/components/ChatInterface';
import UploadPanel from '@/components/UploadPanel';
import StatsPanel from '@/components/StatsPanel';
import DocumentsPanel, { DocumentsPanelRef } from '@/components/DocumentsPanel';
import { apiClient } from '@/lib/api';
import { AlertCircle, CheckCircle, Loader2 } from 'lucide-react';

export default function Home() {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const documentsPanelRef = useRef<DocumentsPanelRef>(null);

  const handleUploadSuccess = () => {
    // Refresh documents panel after successful upload
    documentsPanelRef.current?.refresh();
  };

  useEffect(() => {
    const checkHealth = async () => {
      try {
        await apiClient.healthCheck();
        setApiStatus('online');
      } catch (error) {
        setApiStatus('offline');
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30s

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-[#f8f6f0]">
      {/* Header - Library Style */}
      <header className="library-card-dark sticky top-0 z-10 border-b-4 border-[#d4af37]">
        <div className="max-w-[1600px] mx-auto px-6 py-5 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-[#d4af37] ornament" style={{ fontFamily: 'Georgia, serif' }}>
              Agentic RAG Library
            </h1>
            <p className="text-sm text-[#e8e4d8] mt-2 italic">Powered by Groq & Vector Intelligence</p>
          </div>
          
          <div className="flex items-center gap-3">
            {apiStatus === 'checking' ? (
              <>
                <Loader2 className="w-5 h-5 text-[#d4af37] animate-spin" />
                <span className="text-sm text-[#e8e4d8]">Checking API...</span>
              </>
            ) : apiStatus === 'online' ? (
              <>
                <div className="flex items-center gap-2 px-4 py-2 bg-[#2d5016] rounded-lg border-2 border-[#d4af37]">
                  <CheckCircle className="w-5 h-5 text-[#d4af37]" />
                  <span className="text-sm font-medium text-[#e8e4d8]">Library Online</span>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-center gap-2 px-4 py-2 bg-[#800020] rounded-lg border-2 border-[#d4af37]">
                  <AlertCircle className="w-5 h-5 text-[#d4af37]" />
                  <span className="text-sm font-medium text-[#e8e4d8]">Library Offline</span>
                </div>
              </>
            )}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-[1600px] mx-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 h-[calc(100vh-140px)]">
          
          {/* Left Sidebar - Upload & Stats */}
          <div className="lg:col-span-3 space-y-6 overflow-y-auto">
            {/* Upload Panel */}
            <div className="library-card rounded-xl overflow-hidden">
              <UploadPanel onUploadSuccess={handleUploadSuccess} />
            </div>
            
            {/* Documents Panel */}
            <div className="library-card rounded-xl overflow-hidden">
              <DocumentsPanel ref={documentsPanelRef} />
            </div>
            
            {/* Stats Panel */}
            <StatsPanel />
          </div>

          {/* Right Side - Chat */}
          <div className="lg:col-span-9 library-card rounded-xl overflow-hidden border-4 border-[#8b4513]">
            <ChatInterface />
          </div>
        </div>
      </main>
    </div>
  );
}