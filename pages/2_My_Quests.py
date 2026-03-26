import streamlit as st
import pandas as pd
from quest_data import get_quest_dict

st.set_page_config(page_title="My Quests | Sidequest", page_icon="⚔️", layout="centered")

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

if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}
if "left_quests" not in st.session_state:
    st.session_state.left_quests = []

# cache quest lookup
@st.cache_data
def load_quest_db():
    return get_quest_dict()

quest_db = load_quest_db()

st.markdown("# My Quests")

view_mode = st.radio("View", options=["Active", "Past"], index=0, horizontal=True, label_visibility="collapsed")

active_count = len(st.session_state.joined_quests) + len(st.session_state.hosted_quests)
col1, col2 = st.columns(2)
col1.metric("Active", active_count)
col2.metric("Left / Cancelled", len(st.session_state.left_quests))

st.divider()

if view_mode == "Active":

    if st.session_state.hosted_quests:
        st.write("### Quests You're Hosting")
        for i, quest in enumerate(st.session_state.hosted_quests):
            with st.container(border=True):
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    st.write(f"**{quest['title']}**")
                    st.caption(
                        f"{quest.get('date', 'Today')} at {quest['start_time']} · "
                        f"📍 {quest['location']} · "
                        f"{quest['spots_taken']} joined · {quest['spots_left']} spots left"
                    )
                with col_actions:
                    with st.expander("Manage"):
                        if st.button("Cancel Quest", key=f"cancel_hosted_{quest['id']}"):
                            removed = st.session_state.hosted_quests.pop(i)
                            if removed["id"] in st.session_state.joined_quests:
                                st.session_state.joined_quests.remove(removed["id"])
                            st.session_state.left_quests.append({
                                "title": removed["title"],
                                "action": "Cancelled (hosted)",
                            })
                            st.warning(f'"{removed["title"]}" has been cancelled.')
                            st.rerun()

    if st.session_state.joined_quests:
        st.write("### Quests You've Joined")

        joinedData = []
        for qid in st.session_state.joined_quests:
            if qid in quest_db:
                joinedData.append(quest_db[qid])
            else:
                hosted_match = [q for q in st.session_state.hosted_quests if q["id"] == qid]
                if hosted_match:
                    continue

        for quest in joinedData:
            with st.container(border=True):
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    st.write(f"**{quest['title']}**")
                    st.caption(
                        f"{quest['start_time']} · 📍 {quest['location']} · "
                        f"{quest['distance_mi']} mi · Hosted by {quest['host']}"
                    )
                with col_actions:
                    if st.button("Leave", key=f"leave_{quest['id']}"):
                        st.session_state.joined_quests.remove(quest["id"])
                        st.session_state.left_quests.append({
                            "title": quest["title"],
                            "action": "Left",
                        })
                        st.info(f'You left "{quest["title"]}".')
                        st.rerun()

    if not st.session_state.joined_quests and not st.session_state.hosted_quests:
        st.write("---")
        st.write("No active quests yet. Head to the **Discovery Feed** to find something, "
                 "or **Host a Quest** to start your own.")

elif view_mode == "Past":
    if st.session_state.left_quests:
        st.write("### Past Quests")
        past_df = pd.DataFrame(st.session_state.left_quests)
        past_df.columns = ["Quest", "Status"]
        st.dataframe(past_df, use_container_width=True, hide_index=True)
    else:
        st.info("No past quests yet. When you leave or cancel a quest it shows up here.")

if st.session_state.joined_quests:
    st.divider()
    st.write("### Summary")
    summary_rows = []
    for qid in st.session_state.joined_quests:
        if qid in quest_db:
            q = quest_db[qid]
            summary_rows.append({
                "Quest": q["title"],
                "Location": q["location"],
                "Time": q["start_time"],
                "Distance (mi)": q["distance_mi"],
                "Role": "Joined",
            })
    for q in st.session_state.hosted_quests:
        summary_rows.append({
            "Quest": q["title"],
            "Location": q["location"],
            "Time": q["start_time"],
            "Distance (mi)": q["distance_mi"],
            "Role": "Hosting",
        })
    if summary_rows:
        st.table(pd.DataFrame(summary_rows))
