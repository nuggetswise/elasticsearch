# 🧪 Smart Query Lab: Search Mode Comparison

A powerful Streamlit application for experimenting with different search strategies and comparing their performance.

## 🚀 Features

- **Hybrid Search**: Combine lexical (BM25) and semantic (vector) search
- **Document Upload**: Upload your own JSON document sets
- **Real-time Comparison**: See how different search strategies perform
- **AI Explanations**: Get LLM-powered insights about search strategies
- **Sample Data**: Built-in documents about search technologies

## 📋 Prerequisites

- Python 3.8+
- Streamlit
- API keys for LLM providers (optional, for AI explanations)

## 🛠️ Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys** (optional, for LLM features):
   
   Create a `.streamlit/secrets.toml` file with your API keys:
   ```toml
   # OpenAI API Key (get from https://platform.openai.com/api-keys)
   openai_api_key = "your-openai-key-here"
   
   # Cohere API Key (get from https://dashboard.cohere.ai/api-keys)
   cohere_api_key = "your-cohere-key-here"
   
   # Groq API Key (get from https://console.groq.com/keys)
   groq_api_key = "your-groq-key-here"
   
   # Google Gemini API Key (get from https://makersuite.google.com/app/apikey)
   gemini_api_key = "your-gemini-key-here"
   ```

   Or set environment variables:
   ```bash
   export OPENAI_API_KEY="your-key-here"
   export COHERE_API_KEY="your-key-here"
   export GROQ_API_KEY="your-key-here"
   export GEMINI_API_KEY="your-key-here"
   ```

## 🏃‍♂️ Running the App

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🎯 How to Use

### 1. **Basic Search**
- Enter a query in the search box
- See results ranked by different strategies
- Adjust the hybrid weight slider to balance lexical vs semantic search

### 2. **Upload Custom Data**
- Use the file uploader in the sidebar
- Upload a JSON file with your documents
- Format: List of objects with `title`, `snippet`, `date`, `author`, `tags`, `type`

### 3. **Sample Data**
- Use the built-in sample documents about search technologies
- Download the sample data to see the format
- Try the sample queries provided in the sidebar

### 4. **AI Explanations**
- Toggle the "Explain" option to get LLM-powered insights
- Learn about how different search strategies work
- Understand the pros and cons of each approach

## 📊 Sample Data Included

The app comes with 5 sample documents covering:
- **Elasticsearch Tuning Guide** - Performance optimization
- **Intro to BM25** - Lexical search ranking
- **Vector Search Primer** - Semantic search with embeddings
- **Hybrid Search Patterns** - Combining lexical + semantic
- **Scaling Search Systems** - Architecture and scaling

## 🔧 Troubleshooting

### LLM Not Working?
1. Check your API keys are valid
2. Ensure you have internet connection
3. Try different LLM providers (OpenAI, Cohere, Groq, Gemini)
4. Check the console for error messages

### Search Not Working?
1. Verify your document format is correct
2. Check that documents contain relevant content
3. Try different queries

## 🏗️ Architecture

- **Frontend**: Streamlit
- **Search**: BM25 (lexical) + Sentence Transformers (semantic)
- **LLM**: OpenAI, Cohere, Groq, Gemini (fallback chain)
- **Data**: JSON document format

## 📝 License

This project is part of the Nuggetwise Elastic collaboration. 