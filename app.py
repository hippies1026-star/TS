import streamlit as st

from components.styles import apply_global_styles
from components.sidebar import render_sidebar
from data.demo_company import DEMO_COMPANY, DEMO_CLIENT
from data.runtime_store import initialize_runtime_state
from views import pages


st.set_page_config(
    page_title="TreaSurv",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()
initialize_runtime_state()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def show_login():
    _, center, _ = st.columns([1, 1.05, 1])

    with center:
        st.html("""
        <div class="login-wrapper">
            <div class="login-logo">TS</div>
            <div class="login-brand">TreaSurv</div>
            <div class="login-tagline">Survival-Based AI CFO</div>
        </div>
        """)

        with st.container(border=True):
            st.html("""
            <div class="login-title">로그인</div>
            <div class="login-description">기업의 생존기반 자금관리 대시보드에 접속하세요.</div>
            """)

            email = st.text_input("회사 이메일", value="demo@treasurv.ai", placeholder="name@company.com")
            password = st.text_input("비밀번호", value="demo1234", type="password")

            if st.button("로그인", type="primary", use_container_width=True):
                if email == DEMO_CLIENT["demo_email"] and password == DEMO_CLIENT["demo_password"]:
                    st.session_state.logged_in = True
                    st.rerun()
                st.error("이메일 또는 비밀번호가 올바르지 않습니다.")

            st.html("""
            <div class="login-divider"><span></span><p>또는</p><span></span></div>
            """)

            social1, social2 = st.columns(2)
            social1.button("Google Workspace", use_container_width=True, disabled=True)
            social2.button("Microsoft", use_container_width=True, disabled=True)
            st.caption("소셜 로그인은 프로토타입 환경에서는 비활성화되어 있습니다.")

        st.html("""
        <div class="demo-notice">Prototype Environment · 실제 인증 서버와 연결되지 않은 데모 로그인입니다.</div>
        """)


if not st.session_state.logged_in:
    show_login()
    st.stop()

menu = render_sidebar()

ROUTES = {
    "Overview": pages.overview,
    "Cash Position": pages.cash_position,
    "Forecast": pages.forecast,
    "Survival Floor": pages.survival_floor,
    "Business Plans": pages.business_plans,
    "Scenario Lab": pages.scenario_lab,
    "AI CFO": pages.ai_cfo,
    "Treasury Policy": pages.treasury_policy,
    "Integrations": pages.integrations,
    "Reports": pages.reports,
    "Team": pages.team,
    "Audit Log": pages.audit_log,
    "Settings": pages.settings,
}
ROUTES.get(menu, pages.overview)()

st.html(
    f"""
    <div class="global-footer">
        <div><strong>{DEMO_COMPANY['legal_name_kr']}</strong>&nbsp;·&nbsp;대표 {DEMO_COMPANY['representative']}</div>
        <div class="footer-meta">사업자등록번호 {DEMO_COMPANY['business_number']} ({DEMO_COMPANY['business_number_note']})&nbsp;·&nbsp;{DEMO_COMPANY['headquarters']} ({DEMO_COMPANY['headquarters_note']})</div>
        <div class="footer-links">이용약관 <span>·</span> 개인정보처리방침 <span>·</span> AI 이용 안내 <span>·</span> 보안 정책</div>
        <div class="footer-copy">© 2026 TreaSurv Labs Inc.</div>
        <div class="footer-prototype">Prototype Notice — 금융기관 연동, 기업정보 및 일부 서비스 기능은 시연을 위해 구성된 데모입니다.</div>
    </div>
    """
)
