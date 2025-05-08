# PDF Chat Agent

An intelligent PDF chat application that allows users to upload PDF documents and ask questions about their content. The application uses advanced AI techniques to understand and respond to queries about the uploaded documents.

## Features

- PDF document upload and processing
- Intelligent question answering about PDF content
- Real-time chat interface
- Text-to-speech capability
- Conversation history tracking
- User-specific document management

## Tech Stack

### Backend
- FastAPI
- LangChain
- OpenAI GPT-3.5
- Qdrant Vector Database
- Python 3.9+

### Frontend
- React
- Axios
- Web Speech API
- Modern CSS

## Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- OpenAI API key
- Docker and Docker Compose (for containerized deployment)

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pdf-chat-agent.git
cd pdf-chat-agent
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn app:app --reload --port 3001
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Start Qdrant (vector database):
```bash
docker-compose up qdrant
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001

## Project Structure

```
pdf-chat-agent/
├── backend/
│   ├── app.py
│   ├── graph_builder1.py
│   ├── graph_builder2.py
│   ├── llm_response.py
│   ├── retrieved_ans.py
│   ├── state_schema.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── docker-compose.yml
└── README.md
```

## Usage

1. Open the application in your web browser
2. Upload a PDF document using the upload button
3. Start asking questions about the content of your PDF
4. Use the text-to-speech feature to listen to responses
5. Remove the PDF when done

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-3.5 API
- LangChain for the AI framework
- Qdrant for the vector database 