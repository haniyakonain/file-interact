import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { MessageSquare } from 'lucide-react';
import DropZone from './components/PDFUpload/DropZone';
import DocumentSelect from './components/DocumentList/DocumentSelect';
import QuestionInput from './components/QuestionInput';
import AnswerList from './components/AnswerList';

const API_BASE_URL = 'http://localhost:8000';

const App = () => {
  const [state, setState] = useState({
    selectedFile: null,
    documents: [],
    selectedDocument: null,
    question: '',
    answer: '',
    loading: false,
    error: null,
    successMessage: null, // For success messages
    questionHistory: []
  });

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`);
      if (response.data.message) {
        setState(prev => ({ 
          ...prev, 
          documents: response.data.documents || response.data,
          successMessage: response.data.message
        }));
      } else {
        setState(prev => ({ ...prev, documents: response.data }));
      }
    } catch (err) {
      handleError(err, 'fetching documents');
    }
  };

  const handleError = (err, action) => {
    console.error(`Error ${action}:`, err);
    const errorMessage = err.response?.data?.message || // Check for backend error message
      err.response?.data?.detail ||
      err.message ||
      `Error ${action}`;
    setState(prev => ({ 
      ...prev, 
      error: errorMessage,
      successMessage: null,
      loading: false 
    }));
  };

  const handleFileSelect = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setState(prev => ({ 
        ...prev, 
        loading: true, 
        error: null,
        successMessage: null 
      }));
      
      const response = await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      // Display backend message if available
      setState(prev => ({
        ...prev,
        selectedFile: null,
        loading: false,
        successMessage: response.data.message || 'File uploaded successfully!'
      }));
      
      await fetchDocuments();
    } catch (err) {
      handleError(err, 'uploading file');
    }
  };

  const handleAskQuestion = async (e) => {
    e.preventDefault();
    
    if (!state.selectedDocument) {
      setState(prev => ({ 
        ...prev, 
        error: 'Please select a document first',
        successMessage: null 
      }));
      return;
    }

    if (!state.question.trim()) {
      setState(prev => ({ 
        ...prev, 
        error: 'Please enter a question',
        successMessage: null 
      }));
      return;
    }

    try {
      setState(prev => ({ 
        ...prev, 
        loading: true, 
        error: null,
        successMessage: null 
      }));

      const response = await axios.post(`${API_BASE_URL}/ask`, {
        document_id: state.selectedDocument,
        question: state.question,
      });

      // Add new Q&A to history
      const newQA = {
        question: state.question,
        answer: response.data.answer,
        timestamp: new Date().toISOString()
      };

      setState(prev => ({
        ...prev,
        answer: response.data.answer,
        loading: false,
        successMessage: response.data.message, // Display backend message
        questionHistory: [newQA, ...prev.questionHistory],
        question: ''
      }));
    } catch (err) {
      handleError(err, 'getting answer');
    }
  };

  // Clear messages after 5 seconds
  useEffect(() => {
    if (state.successMessage || state.error) {
      const timer = setTimeout(() => {
        setState(prev => ({
          ...prev,
          successMessage: null,
          error: null
        }));
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [state.successMessage, state.error]);

  return (
    <div className="min-h-screen bg-blue-500 p-8">
      <div className="max-w-4xl mx-auto">
        <nav className="bg-white shadow-md py-4 mb-8">
          <div className="flex justify-between items-center px-6">
            <h1 className="text-xl font-bold">Document Q&A System</h1>
          </div>
        </nav>

        <div className="bg-white rounded-lg shadow p-6">
          {/* Error Message */}
          {state.error && (
            <div className="mb-4 p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 flex items-center justify-between">
              <span>{state.error}</span>
              <button 
                onClick={() => setState(prev => ({ ...prev, error: null }))}
                className="text-red-700 hover:text-red-900"
              >
                ✕
              </button>
            </div>
          )}

          {/* Success Message */}
          {state.successMessage && (
            <div className="mb-4 p-4 bg-green-50 text-green-700 rounded-lg border border-green-200 flex items-center justify-between">
              <span>{state.successMessage}</span>
              <button 
                onClick={() => setState(prev => ({ ...prev, successMessage: null }))}
                className="text-green-700 hover:text-green-900"
              >
                ✕
              </button>
            </div>
          )}

          <DropZone onFileSelect={handleFileSelect} loading={state.loading}>
            <div className="text-center py-6 bg-gray-100 border-dashed border-4 border-gray-300">
              <p className="text-lg text-gray-600">Drop your PDF here or click to upload</p>
            </div>
          </DropZone>
          
          <DocumentSelect
            documents={state.documents}
            selectedDocument={state.selectedDocument}
            onSelect={(doc) => setState(prev => ({ 
              ...prev, 
              selectedDocument: doc, 
              error: null,
              successMessage: null 
            }))}
          />
          
          <QuestionInput
            value={state.question}
            onChange={(e) => setState(prev => ({ ...prev, question: e.target.value }))}
            onSubmit={handleAskQuestion}
            loading={state.loading}
          />
          
          {state.questionHistory.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Question History</h2>
              <AnswerList questions={state.questionHistory} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;