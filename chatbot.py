from flask import Flask, render_template, request, jsonify
import requests
import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

NEWS_API_KEY = os.getenv('NEWS_API_KEY') or "0e02f78193994486add1be208a610be1"
CRIC_API_KEY = os.getenv('CRIC_API_KEY') or "7f3e7f3c-ee87-4bdd-94ad-fb628452280b"

# Configure Gemini AI
genai.configure(api_key="AIzaSyCziI364ohNNapov2s_-C_A5-PII_XKLE4")
model = genai.GenerativeModel('gemini-1.5-pro')

# System prompt for sports-focused responses
SYSTEM_PROMPT = """
You are "SportsGenius", an AI assistant specialized in sports news and information, with a focus on the Indian Premier League (IPL) and other major sports. Your knowledge is continuously updated to the current date, April 08, 2025, and beyond.

Your expertise includes:
- Live scores and match updates
- Player statistics and transfers
- Tournament schedules and results
- Sports news and analysis
- Historical sports data

Sports you cover: Football (EPL, La Liga, Champions League), Cricket (IPL, International), Tennis (Grand Slams), Basketball (NBA), and other major sports.

For non-sports queries, respond: "I specialize only in sports. Please ask about football, cricket, tennis, etc."

When responding:
- Provide concise, accurate, and up-to-date information based on the current date, April 08, 2025.
- Use Markdown syntax: **bold headings** for sections (e.g., **Match Updates**) and - for bullet points.
- Include relevant statistics or specifics (e.g., scores, dates, player names) when available.
- Do not include placeholders, examples, or internal notes (e.g., "this is hypothetical" or "example data").
- Focus only on the requested sport (e.g., IPL for IPL queries) unless otherwise specified.
"""

chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    try:
        # Add timestamp to message
        timestamp = time.strftime("%H:%M", time.localtime())
        
        # Generate response using Gemini
        # response = model.generate_content(
        #     SYSTEM_PROMPT + f"\n\nUser: {user_message}\nSportsGenius:"
        # )

        # Decide source based on keywords
        if 'cricket' in user_message or 'ipl' in user_message:
            response = get_cricket_scores()
        # elif 'football' in user_message or 'epl' in user_message or 'barcelona' in user_message:
        #     response = get_football_info(user_message)
        elif 'news' in user_message or 'update' in user_message:
            response = get_sports_news()
        else:
            response = model.generate_content(
            SYSTEM_PROMPT + f"\n\nUser: {user_message}\nSportsGenius:"
        )
        
        # Clean and format the response
        bot_response = response.text.strip()
        # Replace newlines with Markdown bullet points outside the f-string
        formatted_response = bot_response.replace('\n', '\n- ')
        # Apply the fallback formatting if no Markdown is detected
        if not bot_response.startswith("**"):
            bot_response = f"**Latest IPL News**\n- {formatted_response}"
        
        # Add to chat history
        chat_entry = {
            'user': user_message,
            'bot': bot_response,
            'time': timestamp
        }
        chat_history.append(chat_entry)
        
        # Keep only last 10 messages
        if len(chat_history) > 10:
            chat_history.pop(0)
            
        return jsonify({
            'status': 'success',
            'response': bot_response,
            'time': timestamp
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'response': f"Sorry, I encountered an error: {str(e)}"
        })
    
def get_cricket_scores():
    url = f"https://cricapi.com/api/matches?apikey={CRIC_API_KEY}"
    r = requests.get(url)
    matches = r.json().get("matches", [])
    
    for match in matches:
        if match.get("matchStarted") and "India" in match.get("team-1", "") or "India" in match.get("team-2", ""):
            return f"*Live Cricket Score*\n- {match['team-1']} vs {match['team-2']}\n- Match: {match.get('type')}\n- Status: {match.get('date')}"

    return "No live cricket matches found."


def get_sports_news():
    url = f"https://newsapi.org/v2/top-headlines?category=sports&language=en&apiKey={NEWS_API_KEY}"
    r = requests.get(url)
    articles = r.json().get("articles", [])[:5]

    if not articles:
        return "No sports news found."

    response = "*Top Sports Headlines*\n"
    for article in articles:
        response += f"- [{article['title']}]({article['url']})\n"

    return response.strip()

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request, jsonify
# import requests
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import time
# import re

# # Load environment variables
# load_dotenv()

# # Flask app setup
# app = Flask(__name__)

# # API Key placeholders (replace in .env or set directly here)
# NEWS_API_KEY = os.getenv('NEWS_API_KEY') or "0e02f78193994486add1be208a610be1"
# CRIC_API_KEY = os.getenv('CRIC_API_KEY') or "7f3e7f3c-ee87-4bdd-94ad-fb628452280b"
# #THESPORTSDB_API_KEY = os.getenv('THESPORTSDB_API_KEY') or "YOUR_THESPORTSDB_KEY"

# # Gemini AI config
# genai.configure(api_key="AIzaSyCziI364ohNNapov2s_-C_A5-PII_XKLE4")
# model = genai.GenerativeModel('gemini-1.5-pro')

# SYSTEM_PROMPT = """You are "SportsGenius", an AI assistant specialized in sports news and information, with a focus on the Indian Premier League (IPL) and other major sports. Your knowledge is continuously updated to the current date, April 08, 2025, and beyond.

#  Your expertise includes:
#  - Live scores and match updates
#  - Player statistics and transfers
#  - Tournament schedules and results
#  - Sports news and analysis
#  - Historical sports data

#  Sports you cover: Football (EPL, La Liga, Champions League), Cricket (IPL, International), Tennis (Grand Slams), Basketball (NBA), and other major sports.

#  For non-sports queries, respond: "I specialize only in sports. Please ask about football, cricket, tennis, etc."

#  When responding:
#  - Provide concise, accurate, and up-to-date information based on the current date, April 08, 2025.
#  - Use Markdown syntax: **bold headings** for sections (e.g., **Match Updates**) and - for bullet points.
#  - Include relevant statistics or specifics (e.g., scores, dates, player names) when available.
#  - Do not include placeholders, examples, or internal notes (e.g., "this is hypothetical" or "example data").
#  - Focus only on the requested sport (e.g., IPL for IPL queries) unless otherwise specified."""  

# chat_history = []

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_message = request.json['message'].lower()
#     timestamp = time.strftime("%H:%M", time.localtime())

#     try:
#         # Decide source based on keywords
#         if 'cricket' in user_message or 'ipl' in user_message:
#             response = get_cricket_scores()
#         # elif 'football' in user_message or 'epl' in user_message or 'barcelona' in user_message:
#         #     response = get_football_info(user_message)
#         elif 'news' in user_message or 'update' in user_message:
#             response = get_sports_news()
#         else:
#             response = model.generate_content(
#                 SYSTEM_PROMPT + f"\n\nUser: {user_message}\nSportsGenius:"
#             ).text.strip()

#         # Markdown formatting
#         if not response.startswith(""):
#             formatted_response = response.replace('\n','\n- ')
#             response = f"Sports Update\n- {formatted_response}"
#         # Chat history
#         chat_entry = {
#             'user': user_message,
#             'bot': response,
#             'time': timestamp
#         }
#         chat_history.append(chat_entry)
#         if len(chat_history) > 10:
#             chat_history.pop(0)

#         return jsonify({'status': 'success', 'response': response, 'time': timestamp})

#     except Exception as e:
#         return jsonify({'status': 'error', 'response': f"Sorry, something went wrong: {str(e)}"})

# # ========== 🔌 API Integration Functions ==========

# def get_cricket_scores():
#     url = f"https://cricapi.com/api/matches?apikey={CRIC_API_KEY}"
#     r = requests.get(url)
#     matches = r.json().get("matches", [])
    
#     for match in matches:
#         if match.get("matchStarted") and "India" in match.get("team-1", "") or "India" in match.get("team-2", ""):
#             return f"*Live Cricket Score*\n- {match['team-1']} vs {match['team-2']}\n- Match: {match.get('type')}\n- Status: {match.get('date')}"

#     return "No live cricket matches found."

# # def get_football_info(query):
# #     # Try to extract team name from query
# #     team = "Barcelona"
# #     match = re.search(r"(barcelona|real madrid|chelsea|manchester)", query, re.IGNORECASE)
# #     if match:
# #         team = match.group(1)

# #     url = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}/searchteams.php?t={team}"
# #     r = requests.get(url)
# #     data = r.json()
# #     if not data['teams']:
# #         return "Team not found."
    
# #     team_info = data['teams'][0]
# #     return f"*Football Team Info: {team_info['strTeam']}*\n- Stadium: {team_info['strStadium']}\n- League: {team_info['strLeague']}\n- Description: {team_info['strDescriptionEN'][:200]}..."

# def get_sports_news():
#     url = f"https://newsapi.org/v2/top-headlines?category=sports&language=en&apiKey={NEWS_API_KEY}"
#     r = requests.get(url)
#     articles = r.json().get("articles", [])[:5]

#     if not articles:
#         return "No sports news found."

#     response = "*Top Sports Headlines*\n"
#     for article in articles:
#         response += f"- [{article['title']}]({article['url']})\n"

#     return response.strip()

# if __name__ == '_main_':
#     app.run(debug=True)