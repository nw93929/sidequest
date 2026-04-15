import streamlit as st
import pandas as pd
from datetime import datetime, date, time, timedelta
from styles import apply_custom_style, render_top_bar, render_bottom_nav

st.set_page_config(page_title="Host a Quest | Sidequest", page_icon="⚔️", layout="centered")
apply_custom_style()
st.markdown("<style>.field-label { font-size: 0.75rem; font-weight: 700; color: #555; letter-spacing: 0.5px; margin-bottom: 2px; }</style>", unsafe_allow_html=True)
render_top_bar("Host a Quest")

with st.sidebar:
    st.header("⚔️ Sidequest")
    st.caption("Spontaneous local activities")
    st.divider()
    st.info("💡 **Hosting tips**\n\n"
            "• Keep titles short & fun\n"
            "• Smaller groups (3-6) feel less intimidating\n"
            "• A nearby location helps people find you")

if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

# header matching sketch: Cancel on left, title centered
st.markdown(
    "<div style='display:flex; align-items:center; justify-content:center; position:relative; margin-bottom:16px;'>"
    "<span style='position:absolute; left:0; color:#888; font-size:0.9rem; cursor:pointer;'>Cancel</span>"
    "<strong style='font-size:1.3rem;'>Host a Quest</strong>"
    "</div>",
    unsafe_allow_html=True,
)

st.divider()

# quest title
st.markdown("<p class='field-label'>QUEST TITLE *</p>", unsafe_allow_html=True)
quest_title = st.text_input("title", placeholder='e.g. "Catan at my place"', max_chars=60,
                            label_visibility="collapsed")

# category chips
st.markdown("<p class='field-label'>CATEGORY</p>", unsafe_allow_html=True)
quest_category = st.radio(
    "cat", options=["🎲 Games", "🏐 Sports", "🍕 Food & Drink", "🎤 Music", "🥾 Outdoors", "📚 Study"],
    horizontal=True, label_visibility="collapsed",
)

# location with auto-fill
st.markdown("<p class='field-label'>LOCATION</p>", unsafe_allow_html=True)
quest_location = st.text_input("loc", value="Charlottesville, VA", placeholder="e.g. The Haven Brewery",
                               label_visibility="collapsed")
st.caption("📍 Current location (auto-filled)")

# when: date + time side by side
st.markdown("<p class='field-label'>WHEN</p>", unsafe_allow_html=True)
when_left, when_right = st.columns(2)
with when_left:
    quest_date = st.date_input("Date", value=date.today(), min_value=date.today(),
                               max_value=date.today() + timedelta(days=7), label_visibility="collapsed")
with when_right:
    default_time = (datetime.now() + timedelta(hours=1)).replace(minute=0, second=0)
    quest_time = st.time_input("Time", value=default_time.time(), label_visibility="collapsed")

# group cap
st.markdown("<p class='field-label'>GROUP CAP</p>", unsafe_allow_html=True)
group_size = st.slider("size", min_value=2, max_value=20, value=6, label_visibility="collapsed")

# description
st.markdown("<p class='field-label'>DESCRIPTION (optional)</p>", unsafe_allow_html=True)
quest_desc = st.text_area("desc", placeholder="Add details, vibes, what to bring...",
                          max_chars=300, height=100, label_visibility="collapsed")

st.divider()

is_valid = bool(quest_title.strip()) and bool(quest_location.strip())

# preview + publish buttons at bottom
preview_col, publish_col = st.columns(2)

with preview_col:
    if st.button("Preview", use_container_width=True):
        if not is_valid:
            st.error("Fill in **Quest Title** and **Location** first.")
        else:
            with st.container(border=True):
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
    if st.button("Publish ⚔", type="primary", use_container_width=True):
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

st.caption("Fill in the required fields above. Preview before publishing to double-check everything.")

if st.session_state.hosted_quests:
    st.divider()
    st.write("### Your Hosted Quests")
    hosted_df = pd.DataFrame(st.session_state.hosted_quests)
    displayDf = hosted_df[["title", "category", "location", "start_time", "spots_left"]].copy()
    displayDf.columns = ["Quest", "Category", "Location", "Starts", "Spots Left"]
    st.dataframe(displayDf, use_container_width=True, hide_index=True)
    st.metric("Total Hosted", len(st.session_state.hosted_quests))

render_bottom_nav("host")
