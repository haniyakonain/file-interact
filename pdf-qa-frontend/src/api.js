const backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000'; // Default to localhost if env variable is not set

export const uploadPDF = async (file) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${backendUrl}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    throw new Error('Failed to upload PDF');
  }

  return await response.json();
};

export const askQuestion = async (question, documentId) => {
  const response = await fetch(`${backendUrl}/ask-question`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, documentId }),
  });

  if (!response.ok) {
    throw new Error('Failed to fetch answer');
  }

  return await response.json();
};
