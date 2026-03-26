# Sidequest

**Authors:** Thomas Blalock, Jackson Kennedy, Hudson Noyes, Nathan Wan

A Streamlit multipage app for discovering and joining spontaneous local activities near you. Built for DS 5023.

## Pages

- **Discovery Feed** (`app.py`) — Browse nearby quests, filter by time/distance/category, join activities
- **Host a Quest** (`pages/1_Host_Quest.py`) — Create and publish a new quest
- **My Quests** (`pages/2_My_Quests.py`) — View active/past quests, leave or cancel
- **Group Chat** (`pages/3_Group_Chat.py`) — Message your quest group without exchanging numbers
- **Quest Detail** (`pages/4_Quest_Detail.py`) — Full detail view with join/leave and quest analytics charts


## Visualizations

The Quest Detail page includes two Plotly charts:
- **Bar chart** showing quest counts by category
- **Scatter plot** showing distance vs open spots (sized by total group capacity)

Both respond to the quest data and give users a quick visual sense of what's available.
