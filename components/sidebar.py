import streamlit as st
from streamlit_option_menu import option_menu

from data.demo_company import DEMO_CLIENT
from data.runtime_store import get_settings


OPTIONS = [
    "Overview",
    "Cash Position",
    "Forecast",
    "Survival Floor",
    "Business Plans",
    "Scenario Lab",
    "AI CFO",
    "Treasury Policy",
    "Integrations",
    "Reports",
    "Team",
    "Audit Log",
    "Settings",
]

ICONS = [
    "grid",
    "wallet2",
    "graph-up-arrow",
    "shield-check",
    "calendar-event",
    "bezier2",
    "stars",
    "sliders",
    "link-45deg",
    "file-earmark-text",
    "people",
    "clock-history",
    "gear",
]


def render_sidebar():
    settings = get_settings()

    with st.sidebar:
        st.html("""
        <div class="brand">
            <div class="brand-logo">TS</div>
            <div>
                <div class="brand-name">TreaSurv</div>
                <div class="brand-sub">AI Treasury Intelligence</div>
            </div>
        </div>
        """)

        st.html(f"""
        <div class="company-box">
            <div class="company-icon">N</div>
            <div>
                <div class="company-name">{settings['company_name']}</div>
                <div class="company-type">{DEMO_CLIENT['industry']}</div>
            </div>
        </div>
        """)

        selected = option_menu(
            menu_title=None,
            options=OPTIONS,
            icons=ICONS,
            default_index=0,
            key="main_navigation",
            styles={
                "container": {"padding": "0", "background-color": "transparent"},
                "icon": {"color": "#8c819b", "font-size": "16px"},
                "nav-link": {
                    "font-size": "14px",
                    "font-weight": "520",
                    "text-align": "left",
                    "margin": "3px 0",
                    "padding": "10px 12px",
                    "border-radius": "11px",
                    "color": "#4d4458",
                    "--hover-color": "#f6f2fc",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, #f0e9ff, #f7f3ff)",
                    "color": "#6d28d9",
                    "font-weight": "720",
                },
            },
        )

        st.html("""
        <div style="border-top:1px solid #eee9f4; margin:20px 4px 16px;"></div>
        """)

        st.html(f"""
        <div class="sidebar-user">
            <div class="user-avatar">가</div>
            <div>
                <div class="user-name">{DEMO_CLIENT['user_name']}</div>
                <div class="user-role">CEO · {settings['company_name']}</div>
            </div>
        </div>
        """)

        return selected
