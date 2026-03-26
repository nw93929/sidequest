import streamlit as st
import pandas as pd
import plotly.express as px
from quest_data import get_quest_dict, get_quest_df

st.set_page_config(page_title="Quest Detail | Sidequest", page_icon="⚔️", layout="centered")

st.markdown("""
<style>
    .block-container { max-width: 700px; padding-top: 1rem; }
    div.stButton > button[kind="primary"] {
        background-color: #34C759;
        border: none;
        border-radius: 24px;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 12px 0;
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

@st.cache_data
def load_quest_db():
    return get_quest_dict()

@st.cache_data
def load_quest_df():
    return get_quest_df()

quest_db = load_quest_db()
quest_df = load_quest_df()

# quest picker
quest_options = {qid: f"{q['title']} — {q['location']}" for qid, q in quest_db.items()}
selected_label = st.selectbox("Select a quest", options=list(quest_options.values()), label_visibility="collapsed")
selected_id = list(quest_options.keys())[list(quest_options.values()).index(selected_label)]
quest = quest_db[selected_id]

# activity photo placeholder area like the sketch
st.markdown(
    f"<div style='background:#f5f5f5; border-radius:12px; padding:40px; text-align:center; "
    f"color:#bbb; font-size:0.9rem; margin-bottom:16px;'>Activity photo / icon</div>",
    unsafe_allow_html=True,
)

# title + host info
st.markdown(f"## {quest['title']} @ {quest['location']}")
st.write(f"Hosted by **{quest['host']}** · 🟢 Active now")

st.divider()

# when / where row matching the sketch
info_left, info_right = st.columns(2)
with info_left:
    st.write("**WHEN**")
    st.write(f"Tonight, {quest['start_time']}")
with info_right:
    st.write("**WHERE**")
    st.write(f"{quest['distance_mi']} mi · {quest['location']}")

st.divider()

# attendees
with st.expander(f"ATTENDEES · {quest['spots_taken']} going · {quest['spots_left']} spots open"):
    attendees = []
    mock_names = ["Jamie R.", "Alex T.", "Morgan K.", "Sam W.", "Riley P.", "Jordan B."]
    for j in range(quest["spots_taken"]):
        name = mock_names[j % len(mock_names)]
        role = "Host" if j == 0 else "Attendee"
        attendees.append({"Name": name, "Role": role})
    st.table(pd.DataFrame(attendees))

# description
st.write("**DESCRIPTION**")
st.write(quest["description"])

st.divider()

# accept / leave button (big green button at the bottom like the sketch)
already_joined = quest["id"] in st.session_state.joined_quests

if already_joined:
    st.success("You're in! Check **Group Chat** to coordinate.")
    if st.button("Leave This Quest", key=f"leave_detail_{quest['id']}", use_container_width=True):
        st.session_state.joined_quests.remove(quest["id"])
        st.info(f'You left "{quest["title"]}".')
        st.rerun()
else:
    if quest["spots_left"] > 0:
        if st.button("✕ Accept Quest", type="primary", use_container_width=True, key=f"join_detail_{quest['id']}"):
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

# charts — bar + scatter for the rubric visualization requirement
st.divider()
st.write("### Quest Insights")

st.write("**Quests by Category**")
cat_counts = quest_df["category"].value_counts().reset_index()
cat_counts.columns = ["Category", "Count"]
fig_bar = px.bar(cat_counts, x="Category", y="Count", color="Category")
fig_bar.update_layout(showlegend=False, height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig_bar, use_container_width=True)

st.write("**Distance vs Open Spots**")
fig_scatter = px.scatter(
    quest_df, x="distance_mi", y="spots_left",
    size="spots_total", color="category",
    labels={"distance_mi": "Distance (mi)", "spots_left": "Spots Left", "category": "Category"},
    hover_data=["title", "location"],
)
fig_scatter.update_layout(height=300, margin=dict(t=10, b=10))
st.plotly_chart(fig_scatter, use_container_width=True)
