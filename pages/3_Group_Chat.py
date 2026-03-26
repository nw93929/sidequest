import streamlit as st
from datetime import datetime
from quest_data import get_quest_dict

st.set_page_config(page_title="Chat | Sidequest", page_icon="⚔️", layout="centered")

# dark header + green accent style matching the chat sketch
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
    .chat-bubble-you {
        background: #d4f5d4;
        padding: 10px 14px;
        border-radius: 16px 16px 4px 16px;
        margin-bottom: 8px;
        text-align: left;
    }
    .chat-bubble-other {
        background: #f0f0f0;
        padding: 10px 14px;
        border-radius: 16px 16px 16px 4px;
        margin-bottom: 8px;
    }
    .chat-sender { font-weight: 600; font-size: 0.85rem; }
    .chat-time { font-size: 0.75rem; color: #999; }
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

quest_db = load_quest_db()

# build list of chats the user can access
available_chats = {}
for qid in st.session_state.joined_quests:
    if qid in quest_db:
        q = quest_db[qid]
        available_chats[qid] = q['title']
    else:
        hosted_match = [q for q in st.session_state.hosted_quests if q["id"] == qid]
        if hosted_match:
            available_chats[qid] = hosted_match[0]['title']

if not available_chats:
    st.markdown("# Group Chat")
    st.write("---")
    st.write("No chats yet. Join or host a quest first — a group chat gets created automatically.")
else:
    chat_labels = list(available_chats.values())
    chat_ids = list(available_chats.keys())

    # chat selector if multiple chats
    if len(available_chats) > 1:
        selected_label = st.selectbox("Switch chat", options=chat_labels, label_visibility="collapsed")
        selected_id = chat_ids[chat_labels.index(selected_label)]
    else:
        selected_id = chat_ids[0]
        selected_label = chat_labels[0]

    # resolve quest info
    if selected_id in quest_db:
        active_quest = quest_db[selected_id]
    else:
        hosted_match = [q for q in st.session_state.hosted_quests if q["id"] == selected_id]
        active_quest = hosted_match[0] if hosted_match else None

    if active_quest:
        # dark-style header like the sketch
        st.markdown(
            f"<div style='background:#2c2c2e; color:white; padding:16px 20px; border-radius:12px; margin-bottom:12px;'>"
            f"<strong style='font-size:1.2rem;'>⚔️ {active_quest['title']}</strong><br>"
            f"<span style='font-size:0.85rem; color:#aaa;'>"
            f"{active_quest.get('spots_taken', '?')} members · Starts {active_quest['start_time']}</span></div>",
            unsafe_allow_html=True,
        )

        # green location bar like the sketch
        st.markdown(
            f"<div style='background:#e8f8e8; padding:10px 14px; border-radius:8px; margin-bottom:16px; "
            f"font-size:0.9rem;'>"
            f"📍 {active_quest['location']} · {active_quest.get('distance_mi', 0)} mi · "
            f"<em>Directions →</em></div>",
            unsafe_allow_html=True,
        )

        # seed messages if needed
        if selected_id not in st.session_state.chat_messages:
            st.session_state.chat_messages[selected_id] = [
                {
                    "sender": active_quest.get("host", "Host"),
                    "text": f"Welcome to {active_quest['title']}! See you soon.",
                    "time": "Earlier",
                    "is_host": True,
                }
            ]

        messages = st.session_state.chat_messages[selected_id]

        # render chat bubbles
        for msg in messages:
            is_you = msg["sender"] == "You"
            sender = "You" if is_you else msg["sender"]
            badge = " 👑" if msg.get("is_host") and not is_you else ""

            if is_you:
                _, msg_col = st.columns([1, 3])
                with msg_col:
                    st.markdown(
                        f"<div class='chat-bubble-you'>"
                        f"<span class='chat-sender'>{sender}</span> "
                        f"<span class='chat-time'>{msg['time']}</span><br>"
                        f"{msg['text']}</div>",
                        unsafe_allow_html=True,
                    )
            else:
                msg_col, _ = st.columns([3, 1])
                with msg_col:
                    st.markdown(
                        f"<div class='chat-bubble-other'>"
                        f"<span class='chat-sender'>{sender}{badge}</span> "
                        f"<span class='chat-time'>{msg['time']}</span><br>"
                        f"{msg['text']}</div>",
                        unsafe_allow_html=True,
                    )

        # message input bar at the bottom
        st.write("")
        input_col, send_col = st.columns([5, 1])
        with input_col:
            new_msg = st.text_input("msg", placeholder="Type a message...",
                                    key=f"chat_input_{selected_id}", label_visibility="collapsed")
        with send_col:
            send_pressed = st.button("Send", type="primary", key=f"send_{selected_id}")

        if send_pressed and new_msg.strip():
            st.session_state.chat_messages[selected_id].append({
                "sender": "You",
                "text": new_msg.strip(),
                "time": datetime.now().strftime("%I:%M %p"),
                "is_host": False,
            })
            st.rerun()
        elif send_pressed and not new_msg.strip():
            st.warning("Type a message before sending.")
