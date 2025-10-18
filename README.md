# AI-Powered Role-Playing Chatbot

An AI-powered text-based chatbot that engages users in role-playing conversations using Large Language Models (LLM). The chatbot acts as a curious journalist/interviewer, discussing various topics while monitoring for specific keywords and evaluating user responses with detailed scoring.

## Features

- **Intelligent Conversations**: Natural dialogue powered by OpenAI's GPT models
- **Role-Playing**: Chatbot acts as a curious journalist conducting interviews
- **Keyword Monitoring**: Tracks specific topics and keywords during conversation
- **Smart Scoring**: Evaluates responses on keyword coverage, contextual relevance, and depth (0-100 scale)
- **Modern UI**: Beautiful Next.js frontend with real-time chat interface
- **Detailed Feedback**: Comprehensive breakdown of performance with actionable insights

## Topics Covered

1. **Weather** - Temperature, Humidity, Air Pressure, Wind Patterns, Precipitation
2. **Software Application Performance** - Algorithm Efficiency, Hardware Resources, Network Latency, Concurrency, Database Optimization
3. **Road Traffic** - Road Infrastructure, Traffic Volume, Traffic Signals, Accidents & Roadworks, Weather Conditions

## Architecture

### Backend (Python + Flask)

- RESTful API server
- OpenAI integration for conversation and evaluation
- Session management for multiple concurrent conversations
- Keyword detection and scoring logic

### Frontend (Next.js + React + TypeScript)

- Modern, responsive chat interface
- Real-time message display
- Comprehensive score visualization
- Tailwind CSS for styling

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 18 or higher
- OpenAI API key

### Quick Start with Scripts

The easiest way to run the application is using the provided convenience scripts:

#### 1. Setup Environment

First, create your `.env` file with your OpenAI API key:

```bash
cd backend
cp env.template .env
# Edit .env and add your OpenAI API key
```

#### 2. Start Backend

```bash
./start-backend.sh
```

This script will:

- Create a virtual environment (if needed)
- Install/update Python dependencies
- Start the Flask server on `http://localhost:5001`

#### 3. Start Frontend (in a new terminal)

```bash
./start-frontend.sh
```

This script will:

- Install Node.js dependencies (if needed)
- Start the Next.js development server on `http://localhost:3000`

#### 4. Run Tests

To test the backend functionality:

```bash
./test-backend.sh
```

This script will:

- Setup the environment (if needed)
- Run the backend test suite with a simulated conversation
- Display evaluation results

### Manual Setup

If you prefer to set up manually or need more control:

### Backend Setup

1. Navigate to the backend directory:

```bash
cd backend
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:

```bash
python3 -m pip install -r requirements.txt
```

4. Create a `.env` file in the backend directory:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

5. Start the Flask server:

```bash
python3 api.py
```

The backend will run on `http://localhost:5001`

> **Note**: We use port 5001 instead of 5001 because macOS AirPlay Receiver often occupies port 5001.

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. (Optional) Create a `.env.local` file if your backend runs on a different URL:

```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:5001/api" > .env.local
```

4. Start the development server:

```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Click "Start Interview" to begin a conversation
3. The chatbot will randomly select a topic and start the interview
4. Engage in 3-5 exchanges with the chatbot, answering questions naturally
5. After the conversation ends, view your detailed evaluation including:
   - Total score (0-100)
   - Breakdown by category (coverage, relevance, depth)
   - Individual keyword analysis
   - Overall feedback
6. Click "New Interview" to start another conversation

## Testing

### Running Backend Tests

The project includes a comprehensive test suite for the backend:

```bash
./test-backend.sh
```

The test script will:

- Verify the OpenAI API key configuration
- Initialize the chatbot with a random topic
- Simulate a complete conversation with 5 sample responses
- Display the evaluation results including:
  - Total score breakdown
  - Individual keyword analysis
  - Overall feedback

### Manual Testing

You can also run tests manually:

```bash
cd backend
source venv/bin/activate
python test_chatbot.py
```

### What the Tests Cover

The backend test suite validates:

- ✅ Environment configuration (API keys)
- ✅ Topic selection and initialization
- ✅ Conversation flow and response generation
- ✅ Keyword detection and tracking
- ✅ Scoring algorithm (coverage, relevance, depth)
- ✅ Evaluation and feedback generation

## API Endpoints

### `POST /api/conversation/start`

Start a new conversation with a randomly selected topic.

**Response:**

```json
{
  "session_id": "unique_session_id",
  "topic": "Weather",
  "message": "Hey! I've heard that...",
  "is_complete": false
}
```

### `POST /api/conversation/message`

Send a message in an ongoing conversation.

**Request:**

```json
{
  "session_id": "unique_session_id",
  "message": "User's response"
}
```

**Response:**

```json
{
  "message": "Bot's response",
  "is_complete": false,
  "evaluation": {...}  // Only present when is_complete is true
}
```

### `POST /api/conversation/end`

Manually end a conversation and get evaluation.

**Request:**

```json
{
  "session_id": "unique_session_id"
}
```

### `GET /api/topics`

Get list of available topics.

## Scoring System

The evaluation system scores responses on a 0-100 scale:

- **Keyword Coverage (40 points)**: How many key concepts were mentioned
- **Contextual Relevance (40 points)**: How appropriately keywords were used in context
- **Depth of Explanation (20 points)**: Level of detail and insight provided

### Score Interpretation

- 90-100: Excellent!
- 80-89: Great!
- 70-79: Good!
- 60-69: Fair
- 50-59: Needs Improvement
- 0-49: Keep Practicing

## Project Structure

```
Project/
├── backend/
│   ├── api.py              # Flask API server
│   ├── chatbot.py          # Core chatbot logic
│   ├── topics.py           # Topic definitions
│   ├── test_chatbot.py     # Backend test suite
│   ├── requirements.txt    # Python dependencies
│   └── .env               # Environment variables (create this)
├── frontend/
│   ├── components/
│   │   ├── ChatBox.tsx     # Chat interface component
│   │   └── ScoreDisplay.tsx # Score visualization component
│   ├── lib/
│   │   └── api.ts          # API client
│   ├── pages/
│   │   ├── _app.tsx        # Next.js app wrapper
│   │   └── index.tsx       # Main page
│   ├── styles/
│   │   └── globals.css     # Global styles
│   ├── package.json        # Node.js dependencies
│   ├── tsconfig.json       # TypeScript config
│   ├── tailwind.config.js  # Tailwind CSS config
│   └── next.config.js      # Next.js config
├── start-backend.sh        # Convenience script to start backend
├── start-frontend.sh       # Convenience script to start frontend
├── test-backend.sh         # Convenience script to run tests
└── README.md
```

### Convenience Scripts

The project includes three shell scripts for easy operation:

- **`start-backend.sh`** - Sets up and starts the Flask backend server
- **`start-frontend.sh`** - Sets up and starts the Next.js frontend
- **`test-backend.sh`** - Runs the backend test suite

All scripts handle dependency installation and environment setup automatically.

## Development Notes

- The backend uses GPT-3.5-turbo by default for cost efficiency. You can change to GPT-4 in `chatbot.py` for better results.
- Conversations automatically end after 5 exchanges, but this can be adjusted in the `ChatbotManager` class.
- Session data is stored in-memory. For production, consider using Redis or a database.
- The frontend uses Tailwind CSS for styling with a modern, responsive design.

## Troubleshooting

### Backend Issues

- **"OPENAI_API_KEY not found"**: Make sure you created a `.env` file with your API key
- **Module not found errors**: Ensure you activated the virtual environment and installed dependencies
- **Port 5001 already in use**: Change the port in `api.py` (line 145) and update `frontend/lib/api.ts` (line 8)

### Frontend Issues

- **API connection errors**: Verify the backend is running and the URL is correct
- **Module not found**: Run `npm install` in the frontend directory
- **Port 3000 already in use**: Next.js will automatically suggest port 3001
