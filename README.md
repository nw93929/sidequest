# Sidequest

**Authors:** Thomas Blalock, Jackson Kennedy, Hudson Noyes, Nathan Wan

A Streamlit multipage app for discovering and joining spontaneous local activities near you. Built for DS 5023.

## Pages

- **Discovery Feed** (`app.py`) — Browse nearby quests, filter by time/distance/category, join activities
- **Host a Quest** (`pages/1_Host_Quest.py`) — Create and publish a new quest
- **My Quests** (`pages/2_My_Quests.py`) — View active/past quests, leave or cancel
- **Group Chat** (`pages/3_Group_Chat.py`) — Message your quest group without exchanging numbers
- **Quest Detail** (`pages/4_Quest_Detail.py`) — Full detail view with join/leave actions
- **Sidekick** (`pages/5_Sidekick.py`) — Gemini-powered in-app assistant that recommends quests, answers questions about the feed, etc.

## Setup

1. `pip install -r requirements.txt`
2. Create `.streamlit/secrets.toml` and add your Gemini API key (free at https://aistudio.google.com/apikey):
   ```toml
   [api]
   GEMINI_API_KEY = "your-key-here"
   ```
3. `streamlit run app.py`
