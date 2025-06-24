#!/usr/bin/env python3
"""
Simple test script to verify LLM functionality
"""
import os
import sys
import toml

def load_secrets():
    """Load secrets from .streamlit/secrets.toml"""
    try:
        secrets_path = ".streamlit/secrets.toml"
        if os.path.exists(secrets_path):
            return toml.load(secrets_path)
        return {}
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return {}

def test_openai():
    """Test OpenAI API connection"""
    try:
        import openai
        secrets = load_secrets()
        api_key = secrets.get("openai_api_key") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("❌ OpenAI API key not found")
            return False
        
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'Hello World'"}],
            max_tokens=10
        )
        print(f"✅ OpenAI: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI: {e}")
        return False

def test_cohere():
    """Test Cohere API connection"""
    try:
        import cohere
        secrets = load_secrets()
        api_key = secrets.get("cohere_api_key") or os.environ.get("COHERE_API_KEY")
        if not api_key:
            print("❌ Cohere API key not found")
            return False
        
        co = cohere.Client(api_key)
        response = co.generate(
            model="command-light",
            prompt="Say Hello World",
            max_tokens=10
        )
        print(f"✅ Cohere: {response.generations[0].text}")
        return True
    except Exception as e:
        print(f"❌ Cohere: {e}")
        return False

def test_groq():
    """Test Groq API connection"""
    try:
        import requests
        secrets = load_secrets()
        api_key = secrets.get("groq_api_key") or os.environ.get("GROQ_API_KEY")
        if not api_key:
            print("❌ Groq API key not found")
            return False
        
        response = requests.post(
            "https://api.groq.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": "Say Hello World"}],
                "max_tokens": 10
            },
            timeout=10
        )
        result = response.json()
        print(f"✅ Groq: {result['choices'][0]['message']['content']}")
        return True
    except Exception as e:
        print(f"❌ Groq: {e}")
        return False

def test_gemini():
    try:
        import google.generativeai as genai
        secrets = load_secrets()
        api_key = secrets.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("❌ Gemini API key not found")
            return False
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        resp = model.generate_content("Say Hello World")
        print(f"✅ Gemini: {resp.text.strip()}")
        return True
    except Exception as e:
        print(f"❌ Gemini: {e}")
        return False

def main():
    print("🧪 Testing LLM API connections...\n")
    
    tests = [test_openai, test_cohere, test_groq, test_gemini]
    results = []
    
    for test in tests:
        results.append(test())
        print()
    
    if any(results):
        print("✅ At least one LLM provider is working!")
        print("\n🎉 Your Smart Query Lab is ready with LLM features!")
    else:
        print("❌ No LLM providers are working.")
        print("Please check your API keys in .streamlit/secrets.toml")

if __name__ == "__main__":
    main() 