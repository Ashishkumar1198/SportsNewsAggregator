from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "your-newsapi-key")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")
if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY is not set")

genai.configure(api_key=GEMINI_API_KEY)

# Define sports-related keywords
SPORTS_KEYWORDS = {
    "cricket", "football", "soccer", "tennis", "ipl", "premier league", "bundesliga",
    "hockey", "basketball", "volleyball", "badminton", "sports", "match", "score",
    "tournament", "player", "team", "league"
}

def is_sports_related(query):
    """Check if the query is related to sports by looking for keywords."""
    query = query.lower()
    return any(keyword in query for keyword in SPORTS_KEYWORDS)

def fetch_sports_news(category="sports", limit=6):
    """Fetch sports news from NewsAPI."""
    url = f"https://newsapi.org/v2/everything?q={category} india sports&apiKey={NEWSAPI_KEY}&language=en&sortBy=publishedAt&domains=timesofindia.indiatimes.com,espn.in,indiatoday.in,ndtv.com&pageSize={limit}"
    response = requests.get(url)
    print(f"News API Response: {response.status_code}, {response.text}")
    articles = response.json().get("articles", [])
    return [{
        "title": a["title"],
        "description": a["description"] or "No Description",
        "url": a["url"],
        "image": a["urlToImage"] or "https://via.placeholder.com/300x200?text=No+Image",
        "source": a["source"]["name"]
    } for a in articles]

def get_chatbot_response(user_input):
    """Generate a chatbot response using Gemini API, limited to sports queries."""
    if not is_sports_related(user_input):
        return "Sorry, I can only assist with sports-related queries. Please ask about cricket, football, tennis, or other sports topics!"

    news = fetch_sports_news(user_input)
    if not news:
        prompt = f"User asked: '{user_input}'. I couldn’t find recent Indian sports news. Provide a helpful response."
    else:
        prompt = f"User asked: '{user_input}'. Here’s the latest Indian sports news: {news[0]['title']} - {news[0]['description']}. Provide a concise response and suggest the link for more info: {news[0]['url']}."
    print(f"Prompt: {prompt}")
    try:
        models = genai.list_models()
        print("Available models:", [model.name for model in models])
        if not models:
            return "No models available. Please check your API key and access."
        model = genai.GenerativeModel(models[0].name)
        response = model.generate_content(prompt, generation_config={
            "temperature": 0.7,
            "max_output_tokens": 200
        })
        print(f"Response: {response.text}")
        return response.text
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return f"Sorry, I encountered an error while processing your request: {str(e)}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/news")
def get_news():
    category = request.args.get("category", "sports")
    limit = int(request.args.get("limit", 6))
    return jsonify(fetch_sports_news(category, limit))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    response = get_chatbot_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)