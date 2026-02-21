'use client';

/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from 'react';
import { Upload, FileText, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface UploadStatus {
  status: 'idle' | 'uploading' | 'success' | 'error';
  message?: string;
  metadata?: any;
}

export default function UploadPanel() {
  const [uploadStatus, setUploadStatus] = useState<UploadStatus>({ status: 'idle' });
  const [dragActive, setDragActive] = useState(false);

  const handleFile = async (file: File) => {
    // Validate file type
    const allowedTypes = ['.pdf', '.docx', '.txt'];
    const fileExt = '.' + file.name.split('.').pop()?.toLowerCase();
    
    if (!allowedTypes.includes(fileExt)) {
      setUploadStatus({
        status: 'error',
        message: `Unsupported file type. Allowed: ${allowedTypes.join(', ')}`,
      });
      return;
    }

    setUploadStatus({ status: 'uploading', message: 'Uploading...' });

    try {
      const response = await apiClient.ingestDocument(file);
      setUploadStatus({
        status: 'success',
        message: response.message,
        metadata: response.metadata,
      });

      // Reset after 5 seconds
      setTimeout(() => {
        setUploadStatus({ status: 'idle' });
      }, 5000);
    } catch (error: any) {
      setUploadStatus({
        status: 'error',
        message: error.message || 'Upload failed',
      });
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);

    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) handleFile(file);
  };

  return (
    <div className="border-b bg-white p-6">
      <h2 className="text-xl font-semibold text-gray-800 mb-4">Upload Documents</h2>

      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragEnter={() => setDragActive(true)}
        onDragLeave={() => setDragActive(false)}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept=".pdf,.docx,.txt"
          onChange={handleChange}
          disabled={uploadStatus.status === 'uploading'}
        />

        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          {uploadStatus.status === 'uploading' ? (
            <>
              <Loader2 className="w-12 h-12 text-blue-500 mb-2 animate-spin" />
              <p className="text-sm text-gray-600">Uploading...</p>
            </>
          ) : uploadStatus.status === 'success' ? (
            <>
              <CheckCircle className="w-12 h-12 text-green-500 mb-2" />
              <p className="text-sm text-green-600 font-medium">
                {uploadStatus.message}
              </p>
              {uploadStatus.metadata && (
                <div className="mt-2 text-xs text-gray-500 space-y-1">
                  <p>Chunks: {uploadStatus.metadata.num_chunks}</p>
                  <p>Total in DB: {uploadStatus.metadata.total_in_db}</p>
                </div>
              )}
            </>
          ) : uploadStatus.status === 'error' ? (
            <>
              <XCircle className="w-12 h-12 text-red-500 mb-2" />
              <p className="text-sm text-red-600">{uploadStatus.message}</p>
            </>
          ) : (
            <>
              <Upload className="w-12 h-12 text-gray-400 mb-2" />
              <p className="text-sm text-gray-600 mb-1">
                Click to upload or drag and drop
              </p>
              <p className="text-xs text-gray-500">PDF, DOCX, or TXT files</p>
            </>
          )}
        </label>
      </div>
    </div>
  );
}