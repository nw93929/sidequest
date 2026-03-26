import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta

st.set_page_config(page_title="Host a Quest | Sidequest", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 700px; padding-top: 1rem; }
    div.stButton > button[kind="primary"] {
        background-color: #34C759;
        border: none;
        border-radius: 24px;
        font-weight: 600;
    }
    div.stButton > button[kind="primary"]:hover { background-color: #2DB84D; }
</style>
""", unsafe_allow_html=True)

if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

st.markdown("# Host a Quest")

# quest title
quest_title = st.text_input("QUEST TITLE *", placeholder='e.g. "Catan at my place"', max_chars=60)

# category as horizontal radio chips like the sketch
st.write("**CATEGORY**")
quest_category = st.radio(
    "Category", options=["🎲 Games", "🏐 Sports", "🍕 Food & Drink", "🎤 Music", "🥾 Outdoors", "📚 Study"],
    horizontal=True, label_visibility="collapsed",
)

# location with auto-fill note
quest_location = st.text_input("LOCATION", value="Charlottesville, VA", placeholder="e.g. The Haven Brewery")
st.caption("📍 Current location (auto-filled)")

# when: date + time side by side
st.write("**WHEN**")
when_left, when_right = st.columns(2)
with when_left:
    quest_date = st.date_input("Date", value=date.today(), min_value=date.today(),
                               max_value=date.today() + timedelta(days=7), label_visibility="collapsed")
with when_right:
    default_time = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)
    quest_time = st.time_input("Time", value=default_time.time(), label_visibility="collapsed")

# group cap slider
st.write("**GROUP CAP**")
group_size = st.slider("Group size", min_value=2, max_value=20, value=6, label_visibility="collapsed")

quest_desc = st.text_area("DESCRIPTION (optional)", placeholder="Add details, vibes, what to bring...",
                          max_chars=300, height=100)

st.divider()

is_valid = bool(quest_title.strip()) and bool(quest_location.strip())

preview_col, publish_col = st.columns(2)

with preview_col:
    if st.button("Preview", use_container_width=True):
        if not is_valid:
            st.error("Fill in **Quest Title** and **Location** first.")
        else:
            st.write("---")
            st.write(f"### {quest_category.split(' ')[0]} {quest_title}")
            st.write(f"**When:** {quest_date.strftime('%a, %b %d')} at {quest_time.strftime('%I:%M %p')}")
            st.write(f"**Where:** 📍 {quest_location}")
            st.write(f"**Group size:** up to {group_size}")
            st.write(f"**Hosted by:** You")
            if quest_desc.strip():
                st.caption(quest_desc)
            else:
                st.caption("_No description._")

with publish_col:
    if st.button("Publish ✕", type="primary", use_container_width=True):
        if not is_valid:
            st.error("**Title** and **Location** are required.")
        else:
            new_quest = {
                "id": 100 + len(st.session_state.hosted_quests),
                "title": quest_title,
                "category": quest_category,
                "location": quest_location,
                "distance_mi": 0.0,
                "start_time": quest_time.strftime("%I:%M %p"),
                "date": quest_date.strftime("%a, %b %d"),
                "host": "You",
                "spots_total": group_size,
                "spots_taken": 1,
                "spots_left": group_size - 1,
                "description": quest_desc if quest_desc.strip() else f"Come join {quest_title}!",
            }
            st.session_state.hosted_quests.append(new_quest)
            st.session_state.joined_quests.append(new_quest["id"])
            st.session_state.chat_messages[new_quest["id"]] = [
                {
                    "sender": "You",
                    "text": f"I just created {quest_title}. See you there!",
                    "time": "Just now",
                    "is_host": True,
                }
            ]
            st.success(f'**"{quest_title}"** is live! People nearby can see it.')
            st.balloons()

if st.session_state.hosted_quests:
    st.divider()
    st.write("### Your Hosted Quests")
    hosted_df = pd.DataFrame(st.session_state.hosted_quests)
    displayDf = hosted_df[["title", "category", "location", "start_time", "spots_left"]].copy()
    displayDf.columns = ["Quest", "Category", "Location", "Starts", "Spots Left"]
    st.dataframe(displayDf, use_container_width=True, hide_index=True)
    st.metric("Total Hosted", len(st.session_state.hosted_quests))
