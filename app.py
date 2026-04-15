import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from quest_data import get_quest_df
from styles import apply_custom_style, render_top_bar, render_bottom_nav

st.set_page_config(page_title="Sidequest", page_icon="⚔️", layout="centered")
apply_custom_style()

# extra page-specific styles
st.markdown("""
<style>
    .cat-icon {
        width: 56px; height: 56px;
        border-radius: 12px;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.6rem;
    }
    .quest-card-title { font-size: 1.05rem; font-weight: 700; margin: 0; color: #1a1a1a; }
    .quest-card-meta { font-size: 0.82rem; color: #888; margin: 2px 0 0 0; }
    .cat-icon { border: 1.5px solid #d0e8d0; }
</style>
""", unsafe_allow_html=True)

CAT_ICONS = {
    "🎲 Games": ("🎲", "#d4ecd4"),
    "🏐 Sports": ("🏐", "#ddd8f0"),
    "🍕 Food & Drink": ("🍕", "#f0ddd8"),
    "🎤 Music": ("🎤", "#f0ddd8"),
    "🥾 Outdoors": ("🥾", "#d4ecd4"),
    "📚 Study": ("📚", "#f0e8d4"),
}

render_top_bar()

with st.sidebar:
    st.header("⚔️ Sidequest")
    st.caption("Spontaneous local activities")
    st.divider()
    st.write("📍 **Charlottesville, VA**")
    st.caption("Location auto-detected")

if "joined_quests" not in st.session_state:
    st.session_state.joined_quests = []
if "hosted_quests" not in st.session_state:
    st.session_state.hosted_quests = []
if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {}

@st.cache_data
def load_quests():
    return get_quest_df()

# filter pills row
col_time, col_dist, col_cat = st.columns(3)
with col_time:
    time_filter = st.selectbox("Tonight", ["Tonight", "Right Now", "Next 2 Hours", "Tomorrow"],
                               label_visibility="collapsed")
with col_dist:
    max_distance = st.selectbox("2 mi", ["2 mi", "5 mi", "10 mi"], label_visibility="collapsed")
with col_cat:
    cat_filter = st.selectbox("All Types",
                              ["All Types", "🎲 Games", "🏐 Sports", "🍕 Food & Drink", "🎤 Music", "🥾 Outdoors", "📚 Study"],
                              label_visibility="collapsed")

max_dist_val = float(max_distance.replace(" mi", ""))
df = load_quests()

# compute minutes from now for each quest using current local time
now = datetime.now()
parsed_starts = pd.to_datetime(df["start_time"], format="%I:%M %p").apply(
    lambda t: t.replace(year=now.year, month=now.month, day=now.day)
)
df = df.copy()
df["minutes_from_now"] = (parsed_starts - now).dt.total_seconds() / 60

time_limits = {
    "Right Now": 30,
    "Next 2 Hours": 120,
    "Tonight": 360,
    "Tomorrow": None,
}
limit = time_limits[time_filter]

filtered = df[df["distance_mi"] <= max_dist_val]
if cat_filter != "All Types":
    filtered = filtered[filtered["category"] == cat_filter]
filtered = filtered[filtered["spots_left"] > 0]
if limit is not None:
    filtered = filtered[filtered["minutes_from_now"] <= limit]
else:
    # tomorrow: quests more than 6 hours out
    filtered = filtered[filtered["minutes_from_now"] > 360]

st.divider()

# quest cards with icon on left like the sketch
if filtered.empty:
    st.warning("No quests match your filters. Try widening your search.")
else:
    for _, quest in filtered.iterrows():
        emoji, bg = CAT_ICONS.get(quest["category"], ("⚔️", "#f0f0f0"))

        with st.container(border=True):
            icon_col, info_col, btn_col = st.columns([0.8, 3.2, 1.5])
            with icon_col:
                st.markdown(
                    f"<div class='cat-icon' style='background:{bg};'>{emoji}</div>",
                    unsafe_allow_html=True,
                )
            with info_col:
                st.markdown(
                    f"<p class='quest-card-title'>{quest['title']}</p>"
                    f"<p class='quest-card-meta'>{quest['start_time']} · {quest['distance_mi']} mi away</p>"
                    f"<p class='quest-card-meta'>📍 {quest['location']} · {quest['spots_left']} spots left</p>",
                    unsafe_allow_html=True,
                )
            with btn_col:
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

# bottom stats bar
st.divider()
st.markdown(
    f"<div style='text-align:center; color:#888; font-size:0.9rem;'>"
    f"Nearby <strong>{len(filtered)}</strong> quests · "
    f"<strong>{int(filtered['spots_left'].sum()) if len(filtered) > 0 else 0}</strong> open spots · "
    f"<strong>{len(st.session_state.joined_quests)}</strong> joined</div>",
    unsafe_allow_html=True,
)

# table view
with st.expander("View as table"):
    display_df = filtered[["title", "category", "location", "distance_mi", "start_time", "spots_left"]].copy()
    display_df.columns = ["Quest", "Category", "Location", "Distance (mi)", "Starts", "Spots Left"]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# charts
st.divider()
st.write("### Quest Insights")

st.write("**Open spots by category**")
chart_distance = st.slider("Show quests within", 0.5, 10.0, 5.0, step=0.5, format="%.1f mi", key="chart_dist")
dist_filtered = df[df["distance_mi"] <= chart_distance]
spots_by_cat = dist_filtered.groupby("category")["spots_left"].sum().reset_index()
spots_by_cat.columns = ["Category", "Open Spots"]

fig_bar = px.bar(spots_by_cat, x="Category", y="Open Spots", color="Category", text="Open Spots")
fig_bar.update_layout(showlegend=False, height=350, margin=dict(t=10, b=10))
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True)

st.write("**Distance vs Start Time**")
all_cats = df["category"].unique().tolist()
scatter_cats = st.multiselect("Filter categories", options=all_cats, default=all_cats, key="scatter_cats")
scatter_df = df[df["category"].isin(scatter_cats)].copy() if scatter_cats else df.copy()
scatter_df["parsed_time"] = pd.to_datetime(scatter_df["start_time"], format="%I:%M %p")
scatter_df = scatter_df.sort_values("parsed_time")

fig_scatter = px.scatter(
    scatter_df, x="distance_mi", y="parsed_time",
    color="category", size="spots_left",
    labels={"distance_mi": "Distance (mi)", "parsed_time": "Start Time", "category": "Category", "spots_left": "Spots Left"},
    hover_data=["title", "location", "host", "start_time"],
)
fig_scatter.update_yaxes(tickformat="%I:%M %p")
fig_scatter.update_layout(height=350, margin=dict(t=10, b=10))
st.plotly_chart(fig_scatter, use_container_width=True)

render_bottom_nav("home")
