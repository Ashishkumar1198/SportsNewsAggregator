### File Hierarchy Diagram
```
SportsNewsAggregator/
├── chatbot.py
├── requirements.txt
├── .env
├── templates/
│   └── index.html
```

### Informational and Structured README Content
Welcome to the SportsNewsAggregator repository! This project is a sports-focused chatbot application built using Flask, designed to provide users with the latest sports news and updates, with a special emphasis on the Indian Premier League (IPL) and other major sports leagues.

#### Project Overview
- **Purpose**: The SportsNewsAggregator is an AI-powered chatbot named "SportsGenius" that delivers real-time sports information, including live scores, player statistics, tournament schedules, and news updates.
- **Target Audience**: Sports enthusiasts, particularly those interested in cricket (IPL and international), football (EPL, La Liga, Champions League), tennis (Grand Slams), and basketball (NBA).
- **Current Date**: The chatbot's knowledge is updated as of April 24, 2025.

#### Features
- Provides concise, accurate sports updates using Markdown formatting.
- Integrates with Google Generative AI (Gemini-1.5-pro) for intelligent responses.
- Supports live scores, news headlines, and historical data.
- Maintains a chat history of up to 10 messages.
- Responsive web interface via a simple HTML template.

#### Installation
1. **Clone the Repository**:
   ```
   git clone https://github.com/Ashishkumar1198/SportsNewsAggregator.git
   cd SportsNewsAggregator
   ```
2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add the following (replace with your actual API keys):
     ```
     NEWS_API_KEY=your_news_api_key
     CRIC_API_KEY=your_cric_api_key
     GEMINI_API_KEY=your_gemini_api_key
     ```
3. **Install Dependencies**:
   - Ensure you have Python installed.
   - Run:
     ```
     pip install -r requirements.txt
     ```
4. **Run the Application**:
   - Execute:
     ```
     python chatbot.py
     ```
   - Access the chatbot at `http://localhost:5000` in your browser.

#### Usage
- Visit the homepage (`/`) to see the chat interface.
- Send a message via the `/chat` endpoint (POST request with JSON `{"message": "your query"}`).
- Example queries:
  - "Latest IPL scores"
  - "Football news"
  - "Tennis updates"
- Non-sports queries will receive: "I specialize only in sports. Please ask about football, cricket, tennis, etc."

#### File Structure
- `chatbot.py`: Main application file containing the Flask app, AI logic, and API integrations.
- `requirements.txt`: Lists all Python dependencies required to run the project.
- `.env`: Stores sensitive API keys and configuration settings.
- `templates/index.html`: HTML template for the chatbot's web interface.

#### Contributing
- Fork the repository.
- Create a new branch for your feature or bug fix.
- Submit a pull request with a clear description of your changes.

#### License
This project is currently unlicensed. Please contact the repository owner for usage permissions.

#### Contact
For questions or support, reach out to the repository owner via GitHub issues or the contact information provided by Ashishkumar1198.

#### Acknowledgments
- Powered by Google Generative AI for intelligent responses.
- Utilizes Flask for the web framework and various APIs for sports data.
