# Full-Stack PDF QA Application

## **Objective**
Develop a full-stack application that allows users to upload PDF documents and ask questions regarding the content of these documents. The backend processes the documents and utilizes natural language processing (NLP) to provide answers to users' questions.

---

## **Tools and Technologies**

### **Backend**
- Framework: FastAPI
- NLP: LangChain / LlamaIndex
- PDF Processing: PyMuPDF
- Database: SQLite (for document metadata)

### **Frontend**
- Framework: React.js

### **File Storage**
- Local filesystem for storing uploaded PDFs.

---

## **Functional Requirements**

### **1. PDF Upload**
- Users can upload PDF documents to the application.
- The system stores the PDF and optionally extracts its text for further processing.

### **2. Question Asking**
- Users can pose questions related to the content of the uploaded PDFs.
- The system processes the question and the PDF content to provide an accurate answer.

### **3. Answer Display**
- Answers are displayed in an intuitive manner.
- Users can ask follow-up or new questions about the same document.

---

## **Non-Functional Requirements**
- **Usability**: Intuitive user interface for effortless navigation.
- **Performance**: Efficient PDF processing and minimal response time for questions.

---

## **Backend Specification**

### **FastAPI Endpoints**
1. **PDF Upload Endpoint**:
   - Accepts PDF files.
   - Stores the files locally and optionally extracts the text.

2. **Question Answering Endpoint**:
   - Receives a question and identifies the relevant PDF.
   - Utilizes LangChain or LlamaIndex to generate an answer.

### **PDF Processing**
- Extract text from uploaded PDFs using PyMuPDF or a similar library.
- Process the text and questions using LangChain/LlamaIndex to enable natural language understanding.

### **Data Management**
- Store metadata about uploaded documents (e.g., filename, upload date) in a database.

---

## **Frontend Specification**

### **User Interface**
1. **PDF Upload Page**:
   - Allows users to upload PDF documents.
   - Provides visual feedback (e.g., progress bar or success message).

2. **Question & Answer Interface**:
   - Displays a text box for posing questions.
   - Dynamically shows answers and supports follow-up questions.

### **Interactivity**
- Provide clear feedback during upload and processing.
- Display error messages for unsupported file types or processing errors.

---

## **Setup Instructions**

### **1. Backend Setup**
1. Clone the repository:
   ```bash
   git clone git@github.com:haniyakonain/file-interact.git
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### **2. Frontend Setup**
1. Navigate to the frontend folder:
   ```bash
   cd pdf-qa-frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

---

## **Assignment Deliverables**
1. **Source Code**:
   - Well-structured, appropriately commented code for both backend and frontend.

2. **Documentation**:
   - Include setup instructions and API documentation.
   - Briefly explain the application architecture.

3. **Demo**:
   - Live demo or screencast showcasing:
     - PDF upload functionality.
     - Question answering feature.
     - Intuitive user interface.

---

## **Evaluation Criteria**
- **Functionality**: Meets functional and non-functional requirements.
- **Code Quality**: Clean, organized, and well-documented code.
- **Design & UX**: Intuitive and user-friendly interface.
- **Innovation**: Additional features or improvements that enhance the application.

---

## **Additional Notes**
- The application uses local storage for storing uploaded PDFs and metadata, ensuring ease of setup without relying on cloud services.
- Optimize the backend and frontend interaction for seamless user experience.

