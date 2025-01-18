import React from 'react';

const DocumentSelect = ({ documents, selectedDocument, onSelect }) => {
  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold mb-4">Select Document</h2>
      <select
        value={selectedDocument || ''}
        onChange={(e) => onSelect(e.target.value)}
        className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="">Select a document</option>
        {documents.map((doc) => (
          <option key={doc.id} value={doc.id}>
            {doc.filename}
          </option>
        ))}
      </select>
      <div className="text-sm text-gray-500 mt-2">
        {documents.length === 0 ? 'No documents uploaded yet' : `${documents.length} document(s) available`}
      </div>
    </div>
  );
};

export default DocumentSelect;