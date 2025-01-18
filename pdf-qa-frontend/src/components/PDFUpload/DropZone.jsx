import React from 'react';
import { Upload } from 'lucide-react';

const DropZone = ({ onFileSelect, loading }) => {
  return (
    <div className="mb-8">
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <input
          type="file"
          accept=".pdf"
          onChange={onFileSelect}
          className="hidden"
          id="pdf-upload"
        />
        <label
          htmlFor="pdf-upload"
          className="cursor-pointer flex flex-col items-center"
        >
          <Upload className="h-12 w-12 text-gray-400 mb-4" />
          <span className="text-gray-600">
            Drop your PDF here
          </span>
        </label>
      </div>
    </div>
  );
};

export default DropZone;