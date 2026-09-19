from copy import deepcopy
from datetime import datetime

import streamlit as st

from data.demo_store import DEMO_DATA
from data.demo_company import DEMO_CLIENT


DEFAULT_POLICY = {
    "horizon_months": 12,
    "revenue_stress_percent": 20,
    "expense_stress_percent": 10,
    "emergency_months": 2,
    "risk_preference": "균형형",
}

DEFAULT_SETTINGS = {
    "company_name": DEMO_CLIENT["company_name"],
    "representative": DEMO_CLIENT["representative"],
    "currency": "KRW",
}


def initialize_runtime_state():
    """Create per-session demo state so edits are isolated and survive reruns."""
    if "demo_data" not in st.session_state:
        st.session_state.demo_data = deepcopy(DEMO_DATA)

    if "treasury_policy" not in st.session_state:
        st.session_state.treasury_policy = deepcopy(DEFAULT_POLICY)

    if "app_settings" not in st.session_state:
        st.session_state.app_settings = deepcopy(DEFAULT_SETTINGS)

    if "policy_approved_at" not in st.session_state:
        st.session_state.policy_approved_at = None

    if "ai_history" not in st.session_state:
        st.session_state.ai_history = []

    sync_total_cash()


def get_demo_data():
    initialize_runtime_state()
    return st.session_state.demo_data


def get_policy():
    initialize_runtime_state()
    return st.session_state.treasury_policy


def get_settings():
    initialize_runtime_state()
    return st.session_state.app_settings


def sync_total_cash():
    if "demo_data" not in st.session_state:
        return

    data = st.session_state.demo_data
    accounts = data.get("accounts", [])
    if accounts:
        data["financials"]["total_cash"] = round(
            sum(float(account.get("balance", 0)) for account in accounts)
        )


def log_event(action: str, actor: str = "가태용"):
    data = get_demo_data()
    data.setdefault("logs", []).insert(
        0,
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "action": action,
            "actor": actor,
        },
    )


def reset_runtime_state():
    st.session_state.demo_data = deepcopy(DEMO_DATA)
    st.session_state.treasury_policy = deepcopy(DEFAULT_POLICY)
    st.session_state.app_settings = deepcopy(DEFAULT_SETTINGS)
    st.session_state.policy_approved_at = None
    st.session_state.ai_history = []
    sync_total_cash()
