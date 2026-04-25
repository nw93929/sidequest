import streamlit as st
import pandas as pd
from quest_data import get_quest_dict
from styles import apply_custom_style, render_top_bar, render_bottom_nav

# Mock attendee names for demo purposes
MOCK_ATTENDEE_NAMES = [
    "Jamie R.", "Alex T.", "Morgan K.", "Sam W.", "Riley P.",
    "Jordan B.", "Casey M.", "Quinn L.", "Dakota F.", "Avery S.",
]

st.set_page_config(page_title="Quest Detail | Sidequest", page_icon="⚔️", layout="centered")
apply_custom_style()

st.markdown("""
<style>
    .detail-header {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 12px; font-size: 0.9rem; color: #888;
    }
    .photo-placeholder {
        background: #d4ecd4;
        border-radius: 14px;
        padding: 48px 0;
        text-align: center;
        color: #666;
        font-size: 0.85rem;
        margin-bottom: 16px;
    }
    .field-label {
        font-size: 0.7rem; font-weight: 700; color: #aaa;
        letter-spacing: 0.5px; margin-bottom: 2px;
    }
    .info-box {
        background: #f8fdf8;
        border: 1px solid #d0e8d0;
        border-radius: 10px;
        padding: 12px 14px;
        text-align: center;
    }
    .info-box-label { font-size: 0.7rem; color: #aaa; font-weight: 600; }
    .info-box-value { font-size: 0.95rem; font-weight: 600; margin-top: 2px; }
    .avatar-row {
        display: flex; gap: 6px; margin: 8px 0;
    }
    .avatar {
        width: 32px; height: 32px;
        border-radius: 50%;
        background: #e0e0e0;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 600; color: #666;
    }
    .map-placeholder {
        background: #e8f0e8;
        border: 1px solid #c0d8c0;
        border-radius: 10px;
        padding: 30px 0;
        text-align: center;
        color: #6a9a6a;
        font-size: 0.85rem;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚔️ Sidequest")
    st.caption("Spontaneous local activities")

if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

@st.cache_data
def load_quest_db():
    return get_quest_dict()

quest_db = load_quest_db()

quest_options = {qid: f"{q['title']} — {q['location']}" for qid, q in quest_db.items()}
selected_label = st.selectbox("Select a quest", options=list(quest_options.values()),
                              label_visibility="collapsed", key="quest_picker")
selected_id = list(quest_options.keys())[list(quest_options.values()).index(selected_label)]
quest = quest_db[selected_id]

st.markdown(
    "<div class='detail-header'>"
    "<span>← Back</span>"
    "<span>Share ↗</span>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(f"## {quest['title']} @ {quest['location']}")
st.write(f"Hosted by **{quest['host']}** · 🟢 Active now")

st.divider()

info_left, info_right = st.columns(2)
with info_left:
    st.write("**WHEN**")
    st.write(f"Tonight, {quest['start_time']}")
with info_right:
    st.write("**WHERE**")
    st.write(f"{quest['distance_mi']} mi · {quest['location']}")

st.divider()

with st.expander(f"ATTENDEES · {quest['spots_taken']} going · {quest['spots_left']} spots open"):
    attendees = []
    for j in range(quest["spots_taken"]):
        name = MOCK_ATTENDEE_NAMES[j % len(MOCK_ATTENDEE_NAMES)]
        role = "Host" if j == 0 else "Attendee"
        attendees.append({"Name": name, "Role": role})
    st.table(pd.DataFrame(attendees))

st.write("**DESCRIPTION**")
st.write(quest["description"])

# mini map placeholder like the sketch
st.markdown("<div class='map-placeholder'>📍 Mini Map Preview</div>", unsafe_allow_html=True)

st.divider()

already_joined = quest["id"] in st.session_state.joined_quests

if already_joined:
    st.success("You're in! Check **Group Chat** to coordinate.")
    if st.button("Leave This Quest", key=f"leave_detail_{quest['id']}", use_container_width=True):
        st.session_state.joined_quests.remove(quest["id"])
        st.info(f'You left "{quest["title"]}".')
        st.rerun()
else:
    if quest["spots_left"] > 0:
        if st.button("⚔ Accept Quest", type="primary", use_container_width=True, key=f"join_detail_{quest['id']}"):
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
            st.success(f'You joined **"{quest["title"]}"**!')
            st.balloons()
    else:
        st.error("This quest is full.")

render_bottom_nav("detail")
