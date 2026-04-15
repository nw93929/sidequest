import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from quest_data import get_quest_df, SUBCATEGORIES
from styles import apply_custom_style, render_top_bar

st.set_page_config(page_title="Sidequest", page_icon="⚔️", layout="centered")
apply_custom_style()

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

# Initialize filter session state
if "filter_time" not in st.session_state:
    st.session_state.filter_time = "Tonight"
if "filter_distance" not in st.session_state:
    st.session_state.filter_distance = "5 mi"
if "filter_category" not in st.session_state:
    st.session_state.filter_category = "All Types"
if "filter_subtype" not in st.session_state:
    st.session_state.filter_subtype = "All"
if "advanced_mode" not in st.session_state:
    st.session_state.advanced_mode = False
if "filter_host" not in st.session_state:
    st.session_state.filter_host = "All Hosts"
if "filter_min_spots" not in st.session_state:
    st.session_state.filter_min_spots = 1


@st.cache_data
def load_quests():
    return get_quest_df()


WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")


# Cache weather for 10 minutes — weather doesn't change rapidly and the free
# OpenWeatherMap tier allows only 1,000 calls/day, so a 10-min TTL keeps us
# well within that limit even with frequent page refreshes.
@st.cache_data(ttl=600)
def fetch_weather(city):
    """Fetch current weather from OpenWeatherMap for *city*."""
    if not WEATHER_API_KEY:
        return {"error": "no_key",
                "message": "No API key configured. Add OPENWEATHER_API_KEY to .env."}

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "imperial"}

    try:
        resp = requests.get(url, params=params, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            if not data or "main" not in data:
                return {"error": "empty",
                        "message": "Your search returned no results. Try broader terms."}
            return data
        elif resp.status_code == 401:
            return {"error": "auth",
                    "message": "API key is missing or invalid."}
        elif resp.status_code == 404:
            return {"error": "not_found",
                    "message": "No results found for your search."}
        elif resp.status_code == 429:
            return {"error": "rate_limit",
                    "message": "API limit reached. Please wait a minute and try again."}
        elif resp.status_code >= 500:
            return {"error": "server",
                    "message": "The service is temporarily unavailable. "
                               "Please try again later."}
        else:
            return {"error": "unknown",
                    "message": f"Unexpected error (HTTP {resp.status_code})."}

    except requests.exceptions.Timeout:
        return {"error": "timeout",
                "message": "Could not connect. Check your internet connection."}
    except requests.exceptions.ConnectionError:
        return {"error": "connection",
                "message": "Could not connect. Check your internet connection."}
    except Exception:
        return {"error": "unknown",
                "message": "An unexpected error occurred."}


def reset_filters():
    """on_click callback — resets every filter widget back to its default."""
    st.session_state["filter_time"] = "Tonight"
    st.session_state["filter_distance"] = "5 mi"
    st.session_state["filter_category"] = "All Types"
    st.session_state["filter_subtype"] = "All"
    st.session_state["advanced_mode"] = False
    if "filter_host" in st.session_state:
        st.session_state["filter_host"] = "All Hosts"
    if "filter_min_spots" in st.session_state:
        st.session_state["filter_min_spots"] = 1
    st.toast("Filters cleared!")


def on_category_change():
    """on_change callback — clears the dependent activity-type dropdown when
    the parent category changes, because sub-types are category-specific."""
    st.session_state["filter_subtype"] = "All"


st.markdown("# ⚔️ Sidequest")

with st.expander("🌤️ Current Weather", expanded=False):
    weather_city = st.text_input(
        "City",
        value="Charlottesville",
        key="weather_city",
        placeholder="Enter a city to check the weather…",
    )
    if weather_city.strip():
        with st.spinner("Fetching weather…"):
            weather = fetch_weather(weather_city.strip())

        if "error" in weather:
            if weather["error"] == "no_key":
                st.info(weather["message"])
            elif weather["error"] in ("empty", "not_found"):
                st.warning(weather["message"])
            else:
                st.error(weather["message"])
        else:
            st.success(f"Weather loaded for {weather.get('name', weather_city)}!")
            wcol1, wcol2, wcol3, wcol4 = st.columns(4)
            wcol1.metric("Temp", f"{weather['main']['temp']:.0f}°F")
            wcol2.metric("Feels Like", f"{weather['main']['feels_like']:.0f}°F")
            wcol3.metric("Humidity", f"{weather['main']['humidity']}%")
            wcol4.metric("Wind", f"{weather['wind']['speed']:.0f} mph")

            condition = weather["weather"][0]["main"].lower()
            desc = weather["weather"][0]["description"]
            if condition in ("rain", "drizzle", "thunderstorm", "snow"):
                st.warning(
                    f"⚠️ Current conditions: {desc}. "
                    "Outdoor quests may be affected!"
                )
            else:
                st.info(f"Conditions: {desc} — great for outdoor activities!")
    else:
        st.warning("Enter a city to check the weather.")

advanced_mode = st.toggle("Advanced filters", key="advanced_mode")

col_time, col_dist, col_cat = st.columns(3)
with col_time:
    # key="filter_time" — enables reset_filters() callback to clear this widget
    time_filter = st.selectbox(
        "When",
        ["Tonight", "Right Now", "Next 2 Hours", "Tomorrow"],
        key="filter_time",
        label_visibility="collapsed",
    )
with col_dist:
    # key="filter_distance" — enables reset_filters() callback to clear this widget
    max_distance = st.selectbox(
        "Distance",
        ["2 mi", "5 mi", "10 mi"],
        key="filter_distance",
        label_visibility="collapsed",
    )
with col_cat:
    # key="filter_category" — enables the on_change callback that clears the
    # dependent activity-type dropdown whenever the category changes
    cat_filter = st.selectbox(
        "Type",
        ["All Types"] + list(SUBCATEGORIES.keys()),
        key="filter_category",
        label_visibility="collapsed",
        on_change=on_category_change,
    )

if cat_filter != "All Types":
    subtype_options = ["All"] + SUBCATEGORIES.get(cat_filter, [])
else:
    subtype_options = ["All"]

subtype_filter = st.selectbox(
    "Activity type",
    subtype_options,
    key="filter_subtype",
    disabled=(cat_filter == "All Types"),
)

if advanced_mode:
    df_for_hosts = load_quests()
    adv_col1, adv_col2 = st.columns(2)
    with adv_col1:
        host_options = ["All Hosts"] + sorted(
            df_for_hosts["host"].unique().tolist()
        )
        st.selectbox("Host", host_options, key="filter_host")
    with adv_col2:
        st.number_input(
            "Min spots open", min_value=1, max_value=12,
            key="filter_min_spots",
        )

st.button("Reset Filters", on_click=reset_filters, key="reset_btn")

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
if subtype_filter != "All":
    filtered = filtered[filtered["activity_type"] == subtype_filter]
if advanced_mode:
    host_val = st.session_state.get("filter_host", "All Hosts")
    if host_val != "All Hosts":
        filtered = filtered[filtered["host"] == host_val]
    min_spots_val = st.session_state.get("filter_min_spots", 1)
    if min_spots_val > 1:
        filtered = filtered[filtered["spots_left"] >= min_spots_val]
filtered = filtered[filtered["spots_left"] > 0]
if limit is not None:
    filtered = filtered[filtered["minutes_from_now"] <= limit]
else:
    # tomorrow: quests more than 6 hours out
    filtered = filtered[filtered["minutes_from_now"] > 360]

st.divider()

if filtered.empty:
    st.warning("No quests match your filters. Try widening your search.")
else:
    for _, quest in filtered.iterrows():
        with st.container(border=True):
            cardLeft, cardRight = st.columns([4, 1])
            with cardLeft:
                st.markdown(f"**{quest['title']}**")
                st.caption(
                    f"{quest['start_time']} · {quest['distance_mi']} mi · "
                    f"{quest['location']}"
                )
                st.caption(
                    f"Hosted by {quest['host']} · {quest['spots_left']} spots "
                    f"left · {quest['activity_type']}"
                )
            with cardRight:
                already_joined = quest["id"] in st.session_state.joined_quests
                if already_joined:
                    st.success("Joined!")
                else:
                    if st.button(
                        "Accept Quest",
                        key=f"join_{quest['id']}",
                        type="primary",
                    ):
                        st.session_state.joined_quests.append(quest["id"])
                        if quest["id"] not in st.session_state.chat_messages:
                            st.session_state.chat_messages[quest["id"]] = [
                                {
                                    "sender": quest["host"],
                                    "text": (
                                        f"Hey! Welcome to {quest['title']}. "
                                        f"See you at {quest['location']}!"
                                    ),
                                    "time": "Just now",
                                    "is_host": True,
                                }
                            ]
                        st.rerun()

st.divider()
col1, col2, col3 = st.columns(3)
col1.metric("Nearby", len(filtered))
col2.metric(
    "Open Spots",
    int(filtered["spots_left"].sum()) if len(filtered) > 0 else 0,
)
hosted_ids = {q["id"] for q in st.session_state.hosted_quests}
joined_non_hosted = [qid for qid in st.session_state.joined_quests if qid not in hosted_ids]
col3.metric("Joined", len(joined_non_hosted))

with st.expander("View as table"):
    display_df = filtered[
        ["title", "category", "activity_type", "location",
         "distance_mi", "start_time", "spots_left"]
    ].copy()
    display_df.columns = [
        "Quest", "Category", "Activity", "Location",
        "Distance (mi)", "Starts", "Spots Left",
    ]
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()
st.write("### Quest Insights")

st.write("**Open spots by category**")
chart_distance = st.slider(
    "Show quests within", 0.5, 10.0, 5.0,
    step=0.5, format="%.1f mi", key="chart_dist",
)
dist_filtered = df[df["distance_mi"] <= chart_distance]
spots_by_cat = (
    dist_filtered.groupby("category")["spots_left"].sum().reset_index()
)
spots_by_cat.columns = ["Category", "Open Spots"]

fig_bar = px.bar(
    spots_by_cat, x="Category", y="Open Spots",
    color="Category", text="Open Spots",
)
fig_bar.update_layout(showlegend=False, height=350, margin=dict(t=10, b=10))
fig_bar.update_traces(textposition="outside")
st.plotly_chart(fig_bar, use_container_width=True, key="chart_bar")

st.write("**Distance vs Start Time**")
all_cats = df["category"].unique().tolist()
scatter_cats = st.multiselect(
    "Filter categories", options=all_cats, default=all_cats,
    key="scatter_cats",
)

if not scatter_cats:
    st.warning("Pick at least one category to display the chart.")
    # Create empty scatter plot instead of stopping execution
    fig_scatter = px.scatter()
    fig_scatter.update_layout(
        title="No categories selected",
        xaxis_title="Distance (mi)",
        yaxis_title="Start Time",
        height=350,
        margin=dict(t=40, b=10)
    )
else:
    scatter_df = df[df["category"].isin(scatter_cats)].copy()
    scatter_df["parsed_time"] = pd.to_datetime(
        scatter_df["start_time"], format="%I:%M %p",
    )
    scatter_df = scatter_df.sort_values("parsed_time")

    fig_scatter = px.scatter(
        scatter_df, x="distance_mi", y="parsed_time",
        color="category", size="spots_left",
    labels={
        "distance_mi": "Distance (mi)",
        "parsed_time": "Start Time",
        "category": "Category",
        "spots_left": "Spots Left",
    },
    hover_data=["title", "location", "host", "start_time"],
)
fig_scatter.update_yaxes(tickformat="%I:%M %p")
fig_scatter.update_layout(height=350, margin=dict(t=10, b=10))
st.plotly_chart(fig_scatter, use_container_width=True, key="chart_scatter")
