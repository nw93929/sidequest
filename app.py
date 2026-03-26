import streamlit as st
import pandas as pd
from quest_data import get_quest_df

st.set_page_config(page_title="Sidequest", page_icon="⚔️", layout="centered")

# green accent theme to match our design
st.markdown("""
<style>
    .block-container { max-width: 700px; padding-top: 1rem; }
    div.stButton > button[kind="primary"] {
        background-color: #34C759;
        border: none;
        border-radius: 24px;
        font-weight: 600;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #2DB84D;
    }
    .quest-card {
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        background: white;
    }
    .quest-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 4px; }
    .quest-meta { font-size: 0.85rem; color: #888; }
    .filter-bar {
        display: flex; gap: 8px; margin-bottom: 16px;
    }
</style>
""", unsafe_allow_html=True)

if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

@st.cache_data
def load_quests():
    return get_quest_df()

# header
st.markdown("# ⚔️ Sidequest")

# filter row matching the sketch: time | distance | category
col_time, col_dist, col_cat = st.columns(3)
with col_time:
    time_filter = st.selectbox("When", ["Tonight", "Right Now", "Next 2 Hours", "Tomorrow"], label_visibility="collapsed")
with col_dist:
    max_distance = st.selectbox("Distance", ["2 mi", "5 mi", "10 mi"], index=1, label_visibility="collapsed")
with col_cat:
    cat_filter = st.selectbox("Type", ["All Types", "🎲 Games", "🏐 Sports", "🍕 Food & Drink", "🎤 Music", "🥾 Outdoors", "📚 Study"], label_visibility="collapsed")

max_dist_val = float(max_distance.replace(" mi", ""))

df = load_quests()

# apply filters
filtered = df[df["distance_mi"] <= max_dist_val]
if cat_filter != "All Types":
    filtered = filtered[filtered["category"] == cat_filter]
filtered = filtered[filtered["spots_left"] > 0]

st.caption(f"Nearby · {len(filtered)} quests")
st.divider()

# quest cards
if filtered.empty:
    st.warning("No quests match your filters. Try widening your search.")
else:
    for _, quest in filtered.iterrows():
        with st.container(border=True):
            cardLeft, cardRight = st.columns([4, 1])
            with cardLeft:
                st.markdown(f"**{quest['title']}**")
                st.caption(f"{quest['start_time']} · {quest['distance_mi']} mi · {quest['location']}")
                st.caption(f"Hosted by {quest['host']} · {quest['spots_left']} spots left")

            with cardRight:
                already_joined = quest["id"] in st.session_state.joined_quests
                if already_joined:
                    st.success("Joined!")
                else:
                    if st.button("Accept Quest", key=f"join_{quest['id']}", type="primary"):
                        st.session_state.joined_quests.append(quest["id"])
                        if quest["id"] not in st.session_state.chat_messages:
                            st.session_state.chat_messages[quest["id"]] = [
                                {
                                    "sender": quest["host"],
                                    "text": f"Hey! Welcome to {quest['title']}. See you at {quest['location']}!",
                                    "time": "Just now",
                                    "is_host": True,
                                }
                            ]
                        st.rerun()

# bottom stats
st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Nearby", len(filtered))
col2.metric("Open Spots", int(filtered["spots_left"].sum()) if len(filtered) > 0 else 0)
col3.metric("Joined", len(st.session_state.joined_quests))

# table view
with st.expander("View as table"):
    display_df = filtered[["title", "category", "location", "distance_mi", "start_time", "spots_left"]].copy()
    display_df.columns = ["Quest", "Category", "Location", "Distance (mi)", "Starts", "Spots Left"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
