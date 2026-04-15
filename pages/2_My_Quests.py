import streamlit as st
import pandas as pd
from quest_data import get_quest_dict
from styles import apply_custom_style, render_top_bar, render_bottom_nav

st.set_page_config(page_title="My Quests | Sidequest", page_icon="⚔️", layout="centered")
apply_custom_style()
st.markdown("""
<style>
    .hosting-badge {
        display: inline-block;
        background: #1a1a1a;
        color: #7eff8a;
        font-size: 0.7rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 10px;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .section-label {
        font-size: 0.7rem;
        font-weight: 700;
        color: #aaa;
        letter-spacing: 1px;
        margin: 18px 0 8px 0;
    }
</style>
""", unsafe_allow_html=True)
render_top_bar("My Quests")

with st.sidebar:
    st.header("⚔️ Sidequest")
    st.caption("Spontaneous local activities")
    st.divider()

if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}
if "left_quests" not in st.session_state:
    st.session_state.left_quests = []

@st.cache_data
def load_quest_db():
    return get_quest_dict()

quest_db = load_quest_db()

st.markdown("# My Quests")

view_mode = st.radio("View", options=["Active", "Past"], index=0, horizontal=True,
                     label_visibility="collapsed", key="my_quests_view")

active_count = len(set(st.session_state.joined_quests + [q["id"] for q in st.session_state.hosted_quests]))
tab_active, tab_past = st.tabs([f"Active ({active_count})", "Past"])

with tab_active:

    if st.session_state.hosted_quests or st.session_state.joined_quests:
        st.markdown("<p class='section-label'>TONIGHT</p>", unsafe_allow_html=True)

    # hosted quests
    if st.session_state.hosted_quests:
        for i, quest in enumerate(st.session_state.hosted_quests):
            with st.container(border=True):
                st.markdown("<span class='hosting-badge'>👑 YOU'RE HOSTING</span>", unsafe_allow_html=True)
                st.write(f"**{quest['title']}**")
                st.caption(
                    f"{quest.get('date', 'Today')} at {quest['start_time']} · "
                    f"{quest['spots_taken']} people joined"
                )
                edit_col, cancel_col = st.columns(2)
                with edit_col:
                    st.button("Edit ✏️", key=f"edit_hosted_{quest['id']}", disabled=True)
                with cancel_col:
                    if st.button("Cancel ✕", key=f"cancel_hosted_{quest['id']}"):
                        removed = st.session_state.hosted_quests.pop(i)
                        if removed["id"] in st.session_state.joined_quests:
                            st.session_state.joined_quests.remove(removed["id"])
                        st.session_state.left_quests.append({
                            "title": removed["title"],
                            "action": "Cancelled (hosted)",
                        })
                        st.warning(f'"{removed["title"]}" has been cancelled.')
                        st.rerun()

    # joined quests
    if st.session_state.joined_quests:
        joinedData = []
        for qid in st.session_state.joined_quests:
            if qid in quest_db:
                joinedData.append(quest_db[qid])
            else:
                hosted_match = [q for q in st.session_state.hosted_quests if q["id"] == qid]
                if hosted_match:
                    continue

        for quest in joinedData:
            emoji = quest["category"].split(" ")[0]
            with st.container(border=True):
                st.write(f"**{emoji} {quest['title']}**")
                st.caption(
                    f"{quest['start_time']} · 📍 {quest['location']} · {quest['distance_mi']} mi"
                )
                chat_col, leave_col = st.columns(2)
                with chat_col:
                    st.button("Chat 💬", key=f"chat_{quest['id']}", disabled=True)
                with leave_col:
                    if st.button("Leave Quest", key=f"leave_{quest['id']}"):
                        st.session_state.joined_quests.remove(quest["id"])
                        st.session_state.left_quests.append({
                            "title": quest["title"],
                            "action": "Left",
                        })
                        st.info(f'You left "{quest["title"]}".')
                        st.rerun()

    # later this week section
    st.markdown("<p class='section-label'>LATER THIS WEEK</p>", unsafe_allow_html=True)

    if not st.session_state.joined_quests and not st.session_state.hosted_quests:
        st.caption("No quests yet — explore the feed or host one!")
    else:
        st.caption("No upcoming quests scheduled for later this week.")

    # summary table
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

with tab_past:
    if st.session_state.left_quests:
        past_df = pd.DataFrame(st.session_state.left_quests)
        past_df.columns = ["Quest", "Status"]
        st.dataframe(past_df, use_container_width=True, hide_index=True)
    else:
        st.info("No past quests yet. When you leave or cancel a quest it shows up here.")

render_bottom_nav("quests")
