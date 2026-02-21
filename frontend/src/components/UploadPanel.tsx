'use client';

import { useState } from 'react';
import { Upload, FileText, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { apiClient } from '@/lib/api';

interface UploadStatus {
  status: 'idle' | 'uploading' | 'success' | 'error';
  message?: string;
  metadata?: {
    filename: string;
    num_chunks: number;
    num_documents: number;
    total_in_db: number;
  };
}

interface UploadPanelProps {
  onUploadSuccess?: () => void;
}

export default function UploadPanel({ onUploadSuccess }: UploadPanelProps) {
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

      // Notify parent of successful upload
      onUploadSuccess?.();

      // Reset after 5 seconds
      setTimeout(() => {
        setUploadStatus({ status: 'idle' });
      }, 5000);
    } catch (error) {
      setUploadStatus({
        status: 'error',
        message: error instanceof Error ? error.message : 'Upload failed',
      });
      
      // Reset after 5 seconds
      setTimeout(() => {
        setUploadStatus({ status: 'idle' });
      }, 5000);
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
    <div className="p-6">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="w-5 h-5 text-blue-600" />
        <h2 className="text-lg font-semibold text-gray-800">Upload Documents</h2>
      </div>

      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-all ${
          dragActive
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400 bg-gray-50'
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
              <Loader2 className="w-10 h-10 text-blue-500 mb-2 animate-spin" />
              <p className="text-sm text-gray-600">Uploading...</p>
            </>
          ) : uploadStatus.status === 'success' ? (
            <>
              <CheckCircle className="w-10 h-10 text-green-500 mb-2" />
              <p className="text-sm text-green-600 font-medium mb-1">Success!</p>
              {uploadStatus.metadata && (
                <div className="text-xs text-gray-500 space-y-0.5">
                  <p>{uploadStatus.metadata.num_chunks} chunks created</p>
                  <p>{uploadStatus.metadata.total_in_db} total in database</p>
                </div>
              )}
            </>
          ) : uploadStatus.status === 'error' ? (
            <>
              <XCircle className="w-10 h-10 text-red-500 mb-2" />
              <p className="text-sm text-red-600">{uploadStatus.message}</p>
            </>
          ) : (
            <>
              <Upload className="w-10 h-10 text-gray-400 mb-2" />
              <p className="text-sm text-gray-600 mb-1">
                Click or drag to upload
              </p>
              <p className="text-xs text-gray-500">PDF, DOCX, or TXT</p>
            </>
          )}
        </label>
      </div>
    </div>
  );
}