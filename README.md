# Reddit AI Summarizer

A full-stack project showcasing an AI-powered Reddit thread summarization tool. The frontend, built with Next.js (App Router), delivers real-time responses via WebSocket communication and the ChatGPT API's streaming capabilities. The backend, a Flask application, handles the AI processing and is deployed on Railway.

**Check out the live app here**: [Live Demo](https://reddit-ai-summarizer-ui.vercel.app/)

![Screenshot 2025-01-11 at 6 12 43 PM](https://github.com/user-attachments/assets/fab003ea-0279-47e2-99a0-e8fe94dea15d)
---

## Features

- **Paste and Analyze**: Simply paste a Reddit URL and ask a question about the thread.
- **AI-Powered Summaries**: Get concise, intelligent summaries of the thread and its comments powered by the chatGPT API.
- **Real-Time Updates**: Enjoy a smooth user experience with responses streamed in real time.

---

## Tech Stack

### Frontend:

- **Framework**: Next.js (App Router)
- **Deployment**: Vercel

### Backend:

- **Framework**: Flask
- **Deployment**: Railway
- **Real-Time Communication**: WebSockets
- **AI Backend**: ChatGPT API (streaming mode)

---

## How It Works

1. **Input a Reddit URL**: Paste the link to a Reddit thread into the input field.
2. **Ask a Question**: Provide a specific question or prompt to tailor the summarization.

3. **AI Summarization**: Receive streaming responses based on the scraped Reddit post and its comments.

