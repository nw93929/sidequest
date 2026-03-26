import streamlit as st
import pandas as pd
import plotly.express as px
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

# charts section
st.divider()
st.write("### Quest Insights")

# chart 1: bar chart — open spots by category, filtered by distance slider
st.write("**Open spots by category**")
chart_distance = st.slider("Show quests within", 0.5, 10.0, 5.0, step=0.5, format="%.1f mi", key="chart_dist")
dist_filtered = df[df["distance_mi"] <= chart_distance]
spots_by_cat = dist_filtered.groupby("category")["spots_left"].sum().reset_index()
spots_by_cat.columns = ["Category", "Open Spots"]

fig_bar = px.bar(spots_by_cat, x="Category", y="Open Spots", color="Category",
                 text="Open Spots")
fig_bar.update_layout(showlegend=False, height=350, margin=dict(t=10, b=10))
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

# chart 2: scatter — distance vs start time, filterable by category
st.write("**Distance vs Start Time**")
all_cats = df["category"].unique().tolist()
scatter_cats = st.multiselect("Filter categories", options=all_cats, default=all_cats, key="scatter_cats")
scatter_df = df[df["category"].isin(scatter_cats)].copy() if scatter_cats else df.copy()
scatter_df = scatter_df.sort_values("start_dt")

fig_scatter = px.scatter(
    scatter_df, x="distance_mi", y="start_dt",
    color="category", size="spots_left",
    labels={"distance_mi": "Distance (mi)", "start_dt": "Start Time", "category": "Category", "spots_left": "Spots Left"},
    hover_data=["title", "location", "host", "start_time"],
)
fig_scatter.update_yaxes(tickformat="%I:%M %p")
fig_scatter.update_layout(height=350, margin=dict(t=10, b=10))
st.plotly_chart(fig_scatter, use_container_width=True)
