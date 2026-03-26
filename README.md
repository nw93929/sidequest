# Sidequest

**Authors:** Thomas Blalock, Jackson Kennedy, Hudson Noyes, Nathan Wan

A Streamlit multipage app for discovering and joining spontaneous local activities near you. Built for DS 5023.

## Pages

- **Discovery Feed** (`app.py`) — Browse nearby quests, filter by time/distance/category, join activities
- **Host a Quest** (`pages/1_Host_Quest.py`) — Create and publish a new quest
- **My Quests** (`pages/2_My_Quests.py`) — View active/past quests, leave or cancel
- **Group Chat** (`pages/3_Group_Chat.py`) — Message your quest group without exchanging numbers
- **Quest Detail** (`pages/4_Quest_Detail.py`) — Full detail view with join/leave actions


## Visualizations

The Discovery Feed includes two interactive Plotly charts:
- **Bar chart** — open spots by category, filtered by a distance slider so users can see what's available near them
- **Scatter plot** — distance vs start time, filterable by a category multiselect so users can weigh proximity against timing

These visuals help users answer the question they should all be asking when using our app: "what should I join right now?" and additionally is interactive to adjust based on their preferences.
