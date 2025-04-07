from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)


GEMINI_API_KEY = "AIzaSyCm5Xj7Ckywng6lRS_L7wwlxXFi_KNvg3c"  
NEWSAPI_KEY = "0e02f78193994486add1be208a610be1"  


if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set")
if not NEWSAPI_KEY:
    raise ValueError("NEWSAPI_KEY is not set")

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
    url = f"https://newsapi.org/v2/everything?q={category} india sports&apiKey={NEWSAPI_KEY}&language=en&sortBy=publishedAt&domains=timesofindia.indiatimes.com,espn.in,indiatimes.in,ndtv.com&pageSize={limit}"
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
    """Generate a chatbot response using Gemini API as a general conversational LLM for sports queries."""
    if not is_sports_related(user_input):
        return "I couldn’t find recent Indian sports news. Provide a helpful response."


    prompt = (
        f"Act as a conversational AI similar to ChatGPT or Gemini. Respond to the user's query: '{user_input}' "
        "with a natural, informative, and engaging tone. Provide up-to-date or general knowledge about sports, "
        "focusing on Indian sports if relevant, and limit the response to 200 words. If the query seeks real-time "
        "data (e.g., scores or schedules), acknowledge the limitation and suggest reliable sources like ESPN, "
        "NDTV Sports, or the Indian Express."
    )


    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "max_output_tokens": 200
        }
    }

    try:
       
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status() 
        result = response.json()
        
        chatbot_response = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn’t process your request.")
        print(f"Response: {chatbot_response}")
        return chatbot_response
    except Exception as e:
        print(f"Gemini API Error: {e}")
        print(f"Response Text: {getattr(response, 'text', 'No response')}")
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
