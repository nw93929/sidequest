import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from quest_data import SUBCATEGORIES

st.set_page_config(
    page_title="Host a Quest | Sidequest", page_icon="⚔️", layout="centered",
)

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

st.info("📝 Step 1 of 2 — Fill in quest details")

quest_title = st.text_input(
    "QUEST TITLE *",
    placeholder='e.g. "Catan at my place"',
    max_chars=60,
    key="host_title",
)

st.write("**CATEGORY**")
quest_category = st.radio(
    "Category",
    options=list(SUBCATEGORIES.keys()),
    horizontal=True,
    label_visibility="collapsed",
    key="host_category",
)

quest_location = st.text_input(
    "LOCATION *",
    value="Charlottesville, VA",
    placeholder="e.g. The Haven Brewery",
    key="host_location",
)
st.caption("📍 Current location (auto-filled)")

st.write("**WHEN**")
when_left, when_right = st.columns(2)
with when_left:
    quest_date = st.date_input(
        "Date",
        value=date.today(),
        min_value=date.today(),
        max_value=date.today() + timedelta(days=7),
        label_visibility="collapsed",
        key="host_date",
    )
with when_right:
    default_time = (datetime.now() + timedelta(hours=1)).replace(
        minute=0, second=0,
    )
    quest_time = st.time_input(
        "Time", value=default_time.time(),
        label_visibility="collapsed",
        key="host_time",
    )

st.write("**GROUP CAP**")
group_size = st.slider(
    "Group size", min_value=2, max_value=20, value=6,
    label_visibility="collapsed",
    key="host_group_size",
)

quest_desc = st.text_area(
    "DESCRIPTION (optional)",
    placeholder="Add details, vibes, what to bring…",
    max_chars=300, height=100,
    key="host_desc",
)

show_advanced = st.toggle("Show advanced options", key="host_advanced")
if show_advanced:
    st.write("**ADVANCED OPTIONS**")
    adv1, adv2 = st.columns(2)
    with adv1:
        st.checkbox("Allow +1s", value=True, key="host_plus_ones")
    with adv2:
        st.checkbox("Require host approval", value=False, key="host_approval")
    st.text_input(
        "Accessibility notes",
        placeholder="e.g. Wheelchair accessible, no stairs",
        key="host_accessibility",
    )

st.divider()

validation_errors = []

if quest_title.strip() and len(quest_title.strip()) < 3:
    validation_errors.append("Quest title must be at least 3 characters.")

if quest_date == date.today() and quest_time < datetime.now().time():
    validation_errors.append("Start time cannot be in the past.")

for err in validation_errors:
    st.error(err)

has_required = bool(quest_title.strip()) and bool(quest_location.strip())

# preview + publish buttons at bottom
preview_col, publish_col = st.columns(2)

with preview_col:
    if st.button("Preview", use_container_width=True, key="host_preview"):
        if not has_required:
            st.error("Fill in **Quest Title** and **Location** first.")
        elif validation_errors:
            st.error("Fix the errors above before previewing.")
        else:
            st.info("📋 Step 2 of 2 — Review and publish")
            st.write("---")
            st.write(f"### {quest_category.split(' ')[0]} {quest_title}")
            st.write(
                f"**When:** {quest_date.strftime('%a, %b %d')} at "
                f"{quest_time.strftime('%I:%M %p')}"
            )
            st.write(f"**Where:** 📍 {quest_location}")
            st.write(f"**Group size:** up to {group_size}")
            st.write("**Hosted by:** You")
            if quest_desc.strip():
                st.caption(quest_desc)
            else:
                st.caption("_No description._")

with publish_col:
    if st.button(
        "Publish ⚔️", type="primary",
        use_container_width=True, key="host_publish",
    ):
        if not quest_title.strip():
            st.error("**Title** is required.")
            st.stop()
        if not quest_location.strip():
            st.error("**Location** is required.")
            st.stop()
        if validation_errors:
            st.error("Fix the errors above before publishing.")
            st.stop()

        with st.status("Publishing your quest…", expanded=True) as status:
            st.write("Validating quest details…")
            st.write("Creating group chat…")
            new_quest = {
                "id": 100 + len(st.session_state.hosted_quests),
                "title": quest_title,
                "category": quest_category,
                "activity_type": "",
                "location": quest_location,
                "distance_mi": 0.0,
                "start_time": quest_time.strftime("%I:%M %p"),
                "date": quest_date.strftime("%a, %b %d"),
                "host": "You",
                "spots_total": group_size,
                "spots_taken": 1,
                "spots_left": group_size - 1,
                "description": (
                    quest_desc if quest_desc.strip()
                    else f"Come join {quest_title}!"
                ),
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
            st.write("Publishing to nearby users…")
            status.update(label="Quest published!", state="complete")

        st.success(f'**"{quest_title}"** is live! People nearby can see it.')
        st.balloons()

st.caption("*Format: select a powerfield. Preview it to check — your quest'll be public once published.*")

if st.session_state.hosted_quests:
    st.divider()
    st.write("### Your Hosted Quests")
    hosted_df = pd.DataFrame(st.session_state.hosted_quests)
    disp = hosted_df[
        ["title", "category", "location", "start_time", "spots_left"]
    ].copy()
    disp.columns = ["Quest", "Category", "Location", "Starts", "Spots Left"]
    st.dataframe(disp, use_container_width=True, hide_index=True)
    st.metric("Total Hosted", len(st.session_state.hosted_quests))

render_bottom_nav("host")
