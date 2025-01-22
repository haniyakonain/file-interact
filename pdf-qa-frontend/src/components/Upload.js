import React, { useState } from 'react';
import { uploadPDF } from '../api';

const Upload = () => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    try {
      const result = await uploadPDF(file);
      setMessage('PDF uploaded successfully!');
      console.log(result);
    } catch (error) {
      setMessage('Failed to upload PDF');
      console.error(error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload PDF</button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Upload;
