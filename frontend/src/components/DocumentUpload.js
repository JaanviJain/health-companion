import React, { useState } from 'react';
import { Upload } from 'lucide-react';

function DocumentUpload() {
  const [file, setFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;

    setProcessing(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload-document', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Upload Medical Document</h2>
      
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <Upload className="mx-auto mb-4" size={48} />
        <input
          type="file"
          onChange={handleFileChange}
          accept=".pdf,.jpg,.jpeg,.png"
          className="mb-4"
        />
        <button
          onClick={handleUpload}
          disabled={!file || processing}
          className="bg-blue-500 text-white px-6 py-2 rounded disabled:bg-gray-300"
        >
          {processing ? 'Processing...' : 'Upload & Process'}
        </button>
      </div>

      {result && (
        <div className="mt-6 p-4 bg-gray-50 rounded">
          <h3 className="font-bold mb-2">Processed Result:</h3>
          <pre className="text-sm overflow-auto">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default DocumentUpload;