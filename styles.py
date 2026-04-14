import streamlit as st

# shared styles pulled from our wireframe sketches (styles2)
# dark bars #1a1a1a, green accent #7eff8a, DM Sans font
def apply_custom_style():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

        * { font-family: 'DM Sans', sans-serif; }

        /* dark top bar */
        .top-bar {
            background: #1a1a1a;
            padding: 12px 20px;
            border-radius: 0 0 16px 16px;
            margin: -1rem -1rem 16px -1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .top-bar-title {
            font-size: 1.3rem;
            font-weight: 800;
            font-style: italic;
            color: #7eff8a;
        }
        .top-bar-icon {
            width: 34px; height: 34px;
            border-radius: 50%;
            background: none;
            border: 1.5px solid #7eff8a;
            display: flex; align-items: center; justify-content: center;
            color: #7eff8a; font-size: 0.85rem; font-weight: 700;
        }

        /* dark bottom nav bar */
        .bottom-nav {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 700px;
            background: #1a1a1a;
            padding: 10px 0 14px 0;
            border-radius: 16px 16px 0 0;
            display: flex;
            justify-content: space-around;
            align-items: center;
            z-index: 999;
        }
        .nav-item {
            text-align: center;
            font-size: 0.68rem;
            color: #888;
            text-decoration: none;
        }
        .nav-item.active { color: #7eff8a; font-weight: 700; }
        .nav-icon { font-size: 1.2rem; display: block; margin-bottom: 2px; }

        /* bottom padding so content doesn't hide behind the nav */
        .block-container { padding-bottom: 80px !important; }

        /* primary buttons: dark bg with green text (like "Accept Quest" in sketches) */
        div.stButton > button[kind="primary"] {
            background-color: #1a1a1a;
            border: 2px solid #1a1a1a;
            border-radius: 24px;
            font-weight: 600;
            color: #7eff8a;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #333;
            border-color: #333;
        }

        /* secondary buttons: outlined */
        div.stButton > button[kind="secondary"] {
            background-color: #fff;
            border: 2px solid #1a1a1a;
            border-radius: 24px;
            font-weight: 600;
            color: #1a1a1a;
        }

        .block-container { max-width: 700px; padding-top: 0rem; }
    </style>
    """, unsafe_allow_html=True)


def render_top_bar(title="⚔ <i>Sidequest</i>"):
    st.markdown(
        f"<div class='top-bar'>"
        f"<span class='top-bar-title'>{title}</span>"
        f"<div class='top-bar-icon'>L</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_bottom_nav(active_page="home"):
    pages = [
        ("home", "🏠", "Feed"),
        ("host", "➕", "Host"),
        ("quests", "⚔", "My Quests"),
        ("chat", "💬", "Chat"),
        ("detail", "🔍", "Detail"),
    ]
    items = ""
    for key, icon, label in pages:
        cls = "nav-item active" if key == active_page else "nav-item"
        items += f"<div class='{cls}'><span class='nav-icon'>{icon}</span>{label}</div>"

    st.markdown(f"<div class='bottom-nav'>{items}</div>", unsafe_allow_html=True)
