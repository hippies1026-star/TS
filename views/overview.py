import streamlit as st

from data.demo_company import (
    DEMO_CLIENT
)

from data.demo_financials import (
    DEMO_FINANCIALS,
    DEMO_ACCOUNTS
)

from finance_engine import (
    calculate_runway,
    calculate_survival_floor,
    calculate_investable_cash,
    apply_risk_preference,
)


def money_eok(value):
    return value / 100_000_000


def show():

    st.html(f"""
    <div class="page-title">
        Good morning, {DEMO_CLIENT["user_name"]}
    </div>

    <div class="page-subtitle">
        {DEMO_CLIENT["company_name"]}의 현재 자금상태와
        생존기반 자금운용 여력을 확인하세요.
    </div>
    """)


    # =====================================================
    # DEMO FINANCE ENGINE
    # =====================================================

    current_cash = DEMO_FINANCIALS[
        "total_cash"
    ]

    monthly_revenue = DEMO_FINANCIALS[
        "avg_cash_inflow_3m"
    ]

    monthly_expense = DEMO_FINANCIALS[
        "avg_cash_outflow_3m"
    ]


    runway = calculate_runway(
        current_cash,
        monthly_revenue,
        monthly_expense
    )


    survival = calculate_survival_floor(
        monthly_revenue=monthly_revenue,
        monthly_expense=monthly_expense,
        horizon_months=12,
        revenue_stress_percent=20,
        expense_stress_percent=10,
        emergency_months=2
    )


    survival_floor = survival[
        "survival_floor"
    ]


    investable = calculate_investable_cash(
        current_cash,
        survival_floor
    )


    max_investable = investable[
        "maximum_investable_cash"
    ]


    recommended = apply_risk_preference(
        max_investable,
        "균형형"
    )["recommended_deployment"]


    runway_months = runway[
        "runway_months"
    ]

    if runway_months is None:
        runway_text = "Positive CF"
    else:
        runway_text = (
            f"{runway_months:.1f}개월"
        )


    # =====================================================
    # 핵심 KPI
    # =====================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.html(f"""
        <div class="card">
            <div class="card-label">
                TOTAL CASH
            </div>

            <div class="card-value">
                {money_eok(current_cash):.2f}억원
            </div>

            <div class="card-note">
                연결된 전체 계좌 기준
            </div>
        </div>
        """)

    with c2:
        st.html(f"""
        <div class="card">
            <div class="card-label">
                RUNWAY
            </div>

            <div class="card-value">
                {runway_text}
            </div>

            <div class="card-note">
                현재 현금흐름 기준
            </div>
        </div>
        """)

    with c3:
        st.html(f"""
        <div class="card">
            <div class="card-label">
                SURVIVAL FLOOR
            </div>

            <div class="card-value purple">
                {money_eok(survival_floor):.2f}억원
            </div>

            <div class="card-note">
                생존을 위해 보호해야 할 현금
            </div>
        </div>
        """)

    with c4:
        st.html(f"""
        <div class="card">
            <div class="card-label">
                INVESTABLE CASH
            </div>

            <div class="card-value">
                {money_eok(max_investable):.2f}억원
            </div>

            <div class="card-note">
                최대 운용가능자금
            </div>
        </div>
        """)


    # =====================================================
    # 데이터 연결 상태
    # =====================================================

    st.html("""
    <div class="section-title">
        Connected Financial Data
    </div>
    """)


    for account in DEMO_ACCOUNTS:

        left, middle, right = st.columns(
            [2.2, 1.5, 0.7]
        )

        with left:

            st.write(
                f"**{account['institution']}**"
            )

            st.caption(
                account["type"]
            )

        with middle:

            st.write(
                f"₩{account['balance']:,.0f}"
            )

            st.caption(
                account[
                    "masked_account"
                ]
            )

        with right:

            st.html("""
            <span class="status-connected">
                Connected
            </span>
            """)


    st.caption(
        "마지막 동기화 · "
        + DEMO_FINANCIALS[
            "last_sync"
        ]
    )


    # =====================================================
    # 운영 권고
    # =====================================================

    st.html("""
    <div class="section-title">
        Treasury Recommendation
    </div>
    """)


    col_a, col_b = st.columns(2)

    with col_a:

        st.html(f"""
        <div class="card">

            <div class="card-label">
                RECOMMENDED DEPLOYMENT
            </div>

            <div class="card-value purple">
                {money_eok(recommended):.2f}억원
            </div>

            <div class="card-note">
                균형형 정책 기준
            </div>

        </div>
        """)


    with col_b:

        st.html("""
        <div class="card">

            <div class="card-label">
                CURRENT POLICY STATUS
            </div>

            <div class="card-value">
                LOW RISK
            </div>

            <div class="card-note">
                Survival Floor 이상 현금 확보
            </div>

        </div>
        """)


    # =====================================================
    # Demo 표시
    # =====================================================

    st.html("""
    <div class="prototype-notice">
        Prototype Environment ·
        연결된 금융기관 및 재무 데이터는
        서비스 시연을 위해 생성된 데모 데이터입니다.
    </div>
    """)