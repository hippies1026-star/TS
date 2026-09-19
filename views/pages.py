import re

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from agent import analyze_company
from data.demo_company import DEMO_CLIENT
from data.runtime_store import (
    get_demo_data,
    get_policy,
    get_settings,
    log_event,
    reset_runtime_state,
    sync_total_cash,
)
from finance_engine import (
    apply_risk_preference,
    calculate_investable_cash,
    calculate_runway,
    calculate_survival_floor,
)
from forecast_engine import build_cash_forecast, forecast_summary


def eok(value):
    return float(value) / 100_000_000


def won(value):
    return f"₩{float(value):,.0f}"


def page_title(title, description):
    st.html(
        f"""
        <div class="page-title">{title}</div>
        <div class="page-subtitle">{description}</div>
        """
    )


def finance_results():
    data = get_demo_data()
    policy = get_policy()
    f = data["financials"]

    runway = calculate_runway(
        f["total_cash"],
        f["avg_cash_inflow_3m"],
        f["avg_cash_outflow_3m"],
    )

    survival = calculate_survival_floor(
        monthly_revenue=f["avg_cash_inflow_3m"],
        monthly_expense=f["avg_cash_outflow_3m"],
        horizon_months=policy["horizon_months"],
        revenue_stress_percent=policy["revenue_stress_percent"],
        expense_stress_percent=policy["expense_stress_percent"],
        emergency_months=policy["emergency_months"],
    )

    investable_result = calculate_investable_cash(
        f["total_cash"], survival["survival_floor"]
    )

    preference = apply_risk_preference(
        investable_result["maximum_investable_cash"],
        policy["risk_preference"],
    )

    return {
        "runway": runway,
        "survival": survival,
        "investable": investable_result,
        "preference": preference,
    }


def _forecast_rows(stressed=False, months=18):
    data = get_demo_data()
    policy = get_policy()
    f = data["financials"]

    return build_cash_forecast(
        current_cash=f["total_cash"],
        monthly_revenue=f["avg_cash_inflow_3m"],
        monthly_expense=f["avg_cash_outflow_3m"],
        plans=data["plans"],
        as_of=data.get("as_of", "2026-09"),
        months=months,
        revenue_stress_percent=(policy["revenue_stress_percent"] if stressed else 0),
        expense_stress_percent=(policy["expense_stress_percent"] if stressed else 0),
    )


def _forecast_figure(base_rows, stress_rows, floor):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[row["Month"] for row in base_rows],
            y=[row["Projected Cash"] for row in base_rows],
            mode="lines+markers",
            name="Base Forecast",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[row["Month"] for row in stress_rows],
            y=[row["Projected Cash"] for row in stress_rows],
            mode="lines",
            name="Stress Forecast",
            line={"dash": "dot"},
        )
    )
    fig.add_hline(
        y=floor,
        line_dash="dash",
        annotation_text="Survival Floor",
    )
    fig.update_layout(
        height=390,
        margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        yaxis_title="Cash (KRW)",
        xaxis_title=None,
    )
    return fig


def _ai_context(question, scenario_override=None):
    data = get_demo_data()
    settings = get_settings()
    policy = get_policy().copy()
    if scenario_override:
        policy.update(scenario_override)
    f = data["financials"]

    return f"""
회사: {settings['company_name']}
대표: {settings['representative']}
기준월: {data.get('as_of', '2026-09')}
직원수: {DEMO_CLIENT['employee_count']}명

현재 재무데이터:
- 총 현금: {f['total_cash']}원
- 월평균 현금유입: {f['avg_cash_inflow_3m']}원
- 월평균 현금지출: {f['avg_cash_outflow_3m']}원
- 매출채권: {f['accounts_receivable']}원
- 매입채무: {f['accounts_payable']}원
- 부채: {f['debt']}원

현재 Treasury Policy:
{policy}

등록 사업계획:
{data['plans']}

사용자 질문:
{question}

사업계획의 현금영향이 관련되면 calculate_forecast_summary Tool까지 사용해 판단하라.
"""


# =========================================================
# OVERVIEW
# =========================================================

def overview():
    data = get_demo_data()
    settings = get_settings()
    results = finance_results()
    f = data["financials"]
    runway = results["runway"]
    floor = results["survival"]["survival_floor"]
    investable = results["investable"]["maximum_investable_cash"]
    recommended = results["preference"]["recommended_deployment"]

    page_title(
        f"Good morning, {settings['representative']}",
        f"{settings['company_name']}의 자금상태와 생존여력을 한눈에 확인하세요.",
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Cash", f"{eok(f['total_cash']):.2f}억원")
    runway_text = "현금창출" if runway["runway_months"] is None else f"{runway['runway_months']:.1f}개월"
    c2.metric("Runway", runway_text)
    c3.metric("Survival Floor", f"{eok(floor):.2f}억원")
    c4.metric("Investable Cash", f"{eok(investable):.2f}억원")

    if results["investable"]["cash_shortfall"] > 0:
        st.error(
            f"현재 현금이 Survival Floor보다 {eok(results['investable']['cash_shortfall']):.2f}억원 부족합니다. "
            "신규 운용보다 현금보강이 우선입니다."
        )
    else:
        st.success(
            f"Survival Floor를 보호한 뒤 최대 {eok(investable):.2f}억원을 운용할 수 있으며, "
            f"현재 {results['preference']['preference']} 정책상 권고 운용액은 {eok(recommended):.2f}억원입니다."
        )

    st.subheader("Cash Outlook")
    base_rows = _forecast_rows(False)
    stress_rows = _forecast_rows(True)
    st.plotly_chart(
        _forecast_figure(base_rows, stress_rows, floor),
        use_container_width=True,
    )

    base_summary = forecast_summary(base_rows, floor)
    stress_summary = forecast_summary(stress_rows, floor)
    a, b, c = st.columns(3)
    a.metric("18M Base Ending Cash", f"{eok(base_summary['ending_cash']):.2f}억원")
    b.metric("18M Stress Ending Cash", f"{eok(stress_summary['ending_cash']):.2f}억원")
    c.metric("Stress Floor Breach", stress_summary["first_below_floor"] or "없음")


# =========================================================
# CASH POSITION
# =========================================================

def cash_position():
    data = get_demo_data()
    page_title("Cash Position", "연결된 금융계좌를 수정하면 모든 재무 계산에 즉시 반영됩니다.")

    st.metric("Total Connected Cash", f"{eok(data['financials']['total_cash']):.2f}억원")

    for i, account in enumerate(data["accounts"]):
        with st.container(border=True):
            a, b, c = st.columns([2, 1.5, 0.7])
            a.write(f"**{account['bank']}**")
            a.caption(account["name"])
            b.write(f"**{won(account['balance'])}**")
            b.caption(account["account"])
            c.success("Connected")

            with st.expander("Manage Demo Data"):
                new_balance = st.number_input(
                    "데모 계좌 잔액",
                    min_value=0,
                    value=int(account["balance"]),
                    step=10_000_000,
                    key=f"account_balance_{i}",
                )
                if st.button("Update & Recalculate", key=f"update_account_{i}"):
                    old = account["balance"]
                    account["balance"] = int(new_balance)
                    sync_total_cash()
                    log_event(
                        f"{account['bank']} 잔액 변경: {won(old)} → {won(new_balance)}"
                    )
                    st.success("계좌잔액과 전체 재무지표가 다시 계산되었습니다.")
                    st.rerun()


# =========================================================
# FORECAST
# =========================================================

def forecast():
    results = finance_results()
    floor = results["survival"]["survival_floor"]
    policy = get_policy()

    page_title(
        "Forecast",
        "등록된 사업계획을 실제 월별 현금흐름에 반영한 18개월 Base / Stress Forecast입니다.",
    )

    st.caption(
        "가정: Hiring·Revenue는 예정월부터 매월 반복되고, Expense·Funding은 예정월에 한 번 반영됩니다. "
        f"Stress는 매출 -{policy['revenue_stress_percent']}%, 비용 +{policy['expense_stress_percent']}%입니다."
    )

    base_rows = _forecast_rows(False)
    stress_rows = _forecast_rows(True)
    st.plotly_chart(_forecast_figure(base_rows, stress_rows, floor), use_container_width=True)

    base_summary = forecast_summary(base_rows, floor)
    stress_summary = forecast_summary(stress_rows, floor)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Base Ending Cash", f"{eok(base_summary['ending_cash']):.2f}억원")
    c2.metric("Stress Ending Cash", f"{eok(stress_summary['ending_cash']):.2f}억원")
    c3.metric("Stress Minimum", f"{eok(stress_summary['minimum_cash']):.2f}억원")
    c4.metric("First Floor Breach", stress_summary["first_below_floor"] or "없음")

    table = pd.DataFrame(base_rows)
    st.dataframe(table, use_container_width=True, hide_index=True)


# =========================================================
# SURVIVAL FLOOR
# =========================================================

def survival_floor():
    results = finance_results()
    survival = results["survival"]
    investable = results["investable"]
    preference = results["preference"]
    policy = get_policy()

    page_title("Survival Floor", "기업 생존에 필요한 보호현금과 운용 가능한 잉여현금을 분리합니다.")

    a, b, c = st.columns(3)
    a.metric("Survival Floor", f"{eok(survival['survival_floor']):.2f}억원")
    b.metric("Maximum Investable", f"{eok(investable['maximum_investable_cash']):.2f}억원")
    c.metric("Recommended Deployment", f"{eok(preference['recommended_deployment']):.2f}억원")

    d1, d2, d3 = st.columns(3)
    d1.metric("Stressed Monthly Burn", f"{eok(survival['stressed_monthly_burn']):.2f}억원")
    d2.metric("Operating Requirement", f"{eok(survival['operating_requirement']):.2f}억원")
    d3.metric("Emergency Reserve", f"{eok(survival['emergency_reserve']):.2f}억원")

    st.info(
        f"현재 정책: {policy['horizon_months']}개월 생존기간 · 매출 -{policy['revenue_stress_percent']}% · "
        f"비용 +{policy['expense_stress_percent']}% · 비상예비자금 {policy['emergency_months']}개월 · "
        f"운용성향 {policy['risk_preference']}"
    )


# =========================================================
# BUSINESS PLANS
# =========================================================

def business_plans():
    data = get_demo_data()
    page_title("Business Plans", "채용·투자·펀딩·신규매출 계획을 Forecast와 AI CFO에 연결합니다.")

    for i, plan in enumerate(list(data["plans"])):
        with st.container(border=True):
            a, b, c = st.columns([3, 1, 0.45])
            a.write(f"**{plan['title']}**")
            a.caption(f"{plan['type']} · {plan['date']} · {plan['detail']}")
            if plan["amount"] >= 0:
                b.success(f"+{eok(plan['amount']):.2f}억원")
            else:
                b.error(f"{eok(plan['amount']):.2f}억원")
            if c.button("삭제", key=f"delete_plan_{i}"):
                removed = data["plans"].pop(i)
                log_event(f"사업계획 삭제: {removed['title']}")
                st.rerun()

    st.subheader("새 계획 추가")
    with st.form("add_business_plan", clear_on_submit=True):
        plan_type = st.selectbox("계획 유형", ["Hiring", "Funding", "Expense", "Revenue"])
        title = st.text_input("계획명")
        date_value = st.text_input("예정 시점", placeholder="2027-01")
        amount_abs = st.number_input("월/일회성 현금영향 절대금액 (원)", min_value=0, value=0, step=10_000_000)
        detail = st.text_input("설명")
        submitted = st.form_submit_button("사업계획 추가")

    if submitted:
        if not title.strip():
            st.error("계획명을 입력해 주세요.")
        elif not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", date_value.strip()):
            st.error("예정 시점은 YYYY-MM 형식으로 입력해 주세요.")
        elif amount_abs <= 0:
            st.error("현금영향 금액은 0보다 커야 합니다.")
        else:
            signed_amount = -abs(amount_abs) if plan_type in {"Hiring", "Expense"} else abs(amount_abs)
            data["plans"].append(
                {
                    "type": plan_type,
                    "title": title.strip(),
                    "date": date_value.strip(),
                    "amount": signed_amount,
                    "detail": detail.strip() or "사용자 등록 계획",
                }
            )
            log_event(f"사업계획 추가: {title.strip()}")
            st.success("사업계획이 Forecast와 AI CFO 컨텍스트에 반영되었습니다.")
            st.rerun()


# =========================================================
# SCENARIO LAB
# =========================================================

def scenario_lab():
    policy = get_policy()
    data = get_demo_data()
    f = data["financials"]

    page_title("Scenario Lab", "스트레스 가정을 바꾸고 Survival Floor와 현금예측을 동시에 비교합니다.")

    revenue_stress = st.slider("매출 감소", 0, 60, int(policy["revenue_stress_percent"]), 5)
    expense_stress = st.slider("비용 증가", 0, 50, int(policy["expense_stress_percent"]), 5)
    emergency_months = st.slider("비상예비자금", 0, 6, int(policy["emergency_months"]), 1)

    result = calculate_survival_floor(
        f["avg_cash_inflow_3m"],
        f["avg_cash_outflow_3m"],
        policy["horizon_months"],
        revenue_stress,
        expense_stress,
        emergency_months,
    )
    investable = calculate_investable_cash(f["total_cash"], result["survival_floor"])

    scenario_rows = build_cash_forecast(
        current_cash=f["total_cash"],
        monthly_revenue=f["avg_cash_inflow_3m"],
        monthly_expense=f["avg_cash_outflow_3m"],
        plans=data["plans"],
        as_of=data.get("as_of", "2026-09"),
        months=18,
        revenue_stress_percent=revenue_stress,
        expense_stress_percent=expense_stress,
    )
    summary = forecast_summary(scenario_rows, result["survival_floor"])

    c1, c2, c3 = st.columns(3)
    c1.metric("Scenario Survival Floor", f"{eok(result['survival_floor']):.2f}억원")
    c2.metric("Investable Cash", f"{eok(investable['maximum_investable_cash']):.2f}억원")
    c3.metric("18M Ending Cash", f"{eok(summary['ending_cash']):.2f}억원")

    if summary["first_below_floor"]:
        st.warning(f"이 시나리오에서는 {summary['first_below_floor']}부터 Survival Floor를 하회합니다.")
    else:
        st.success("18개월 Forecast 내에서 Survival Floor 하회가 관측되지 않습니다.")

    left, right = st.columns(2)
    if left.button("현재 시나리오를 정책에 적용", type="primary", use_container_width=True):
        policy["revenue_stress_percent"] = revenue_stress
        policy["expense_stress_percent"] = expense_stress
        policy["emergency_months"] = emergency_months
        log_event(
            f"Stress scenario 적용: 매출 -{revenue_stress}%, 비용 +{expense_stress}%, 비상자금 {emergency_months}개월"
        )
        st.success("Overview, Survival Floor, Forecast, AI CFO에 적용되었습니다.")
        st.rerun()

    if right.button("AI Scenario 분석", use_container_width=True):
        with st.spinner("AI가 시나리오를 분석 중입니다..."):
            response = analyze_company(
                _ai_context(
                    "이 스트레스 시나리오에서 기업의 생존 위험과 우선 액션을 분석해라.",
                    {
                        "revenue_stress_percent": revenue_stress,
                        "expense_stress_percent": expense_stress,
                        "emergency_months": emergency_months,
                    },
                )
            )
        st.markdown(response)


# =========================================================
# AI CFO
# =========================================================

def ai_cfo():
    page_title("AI CFO", "현재 재무데이터·사업계획·Treasury Policy를 함께 읽는 TreaSurv Agent입니다.")

    history = st.session_state.ai_history
    for message in history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("예: 개발자 3명을 더 채용해도 Survival Floor를 지킬 수 있을까?")
    if question:
        history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("TreaSurv가 재무 Tool과 사업계획을 함께 분석 중입니다..."):
                answer = analyze_company(_ai_context(question))
            st.markdown(answer)
        history.append({"role": "assistant", "content": answer})
        log_event("AI CFO 분석 실행", actor="TreaSurv AI")


# =========================================================
# TREASURY POLICY
# =========================================================

def treasury_policy():
    results = finance_results()
    policy = get_policy()
    floor = results["survival"]["survival_floor"]
    investable = results["investable"]["maximum_investable_cash"]
    recommended = results["preference"]["recommended_deployment"]

    page_title("Treasury Policy", "현재 스트레스 가정과 운용성향을 바탕으로 생성된 생존기반 자금관리 정책입니다.")

    if st.session_state.policy_approved_at:
        st.success(f"● APPROVED · {st.session_state.policy_approved_at}")
    else:
        st.info("● DRAFT POLICY")

    a, b, c = st.columns(3)
    a.metric("Survival Floor", f"{eok(floor):.2f}억원")
    b.metric("Maximum Deployable", f"{eok(investable):.2f}억원")
    c.metric("Recommended Deployment", f"{eok(recommended):.2f}억원")

    st.write("**Policy Rules**")
    st.write(
        f"- 목표 생존기간: {policy['horizon_months']}개월  \n"
        f"- 스트레스: 매출 -{policy['revenue_stress_percent']}%, 비용 +{policy['expense_stress_percent']}%  \n"
        f"- 비상예비자금: {policy['emergency_months']}개월  \n"
        f"- 운용성향: {policy['risk_preference']}  \n"
        "- Survival Floor 이하 현금은 운용 금지"
    )

    if st.button("Approve Current Policy", type="primary"):
        from datetime import datetime

        st.session_state.policy_approved_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        log_event("Treasury Policy 승인")
        st.success("현재 정책이 승인되어 Audit Log에 기록되었습니다.")
        st.rerun()


# =========================================================
# INTEGRATIONS
# =========================================================

def integrations():
    data = get_demo_data()
    page_title("Integrations", "TreaSurv가 사용하는 기업 데이터 연결 상태입니다.")
    for integration in data["integrations"]:
        with st.container(border=True):
            a, b = st.columns([4, 1])
            a.write(f"**{integration['name']}**")
            a.caption(integration["type"])
            b.success(integration["status"])
    st.warning("Prototype Environment: 연결상태와 계좌정보는 시연용 데이터입니다.")


# =========================================================
# REPORTS
# =========================================================

def reports():
    data = get_demo_data()
    page_title("Reports", "현재 세션의 재무데이터로 즉시 생성되는 데모 보고서 스냅샷입니다.")

    for i, report in enumerate(data["reports"]):
        with st.container(border=True):
            a, b = st.columns([4, 1])
            a.write(f"**{report}**")
            a.caption("Generated by TreaSurv")
            if b.button("View", key=f"report_{i}"):
                st.session_state.active_report = report

    active = st.session_state.get("active_report")
    if active:
        results = finance_results()
        f = data["financials"]
        st.subheader(active)
        st.write(
            f"현재 현금은 **{eok(f['total_cash']):.2f}억원**, "
            f"Survival Floor는 **{eok(results['survival']['survival_floor']):.2f}억원**, "
            f"최대 운용가능자금은 **{eok(results['investable']['maximum_investable_cash']):.2f}억원**입니다."
        )
        st.caption("공모전 프로토타입에서는 PDF 내보내기 대신 실시간 스냅샷을 제공합니다.")


# =========================================================
# TEAM
# =========================================================

def team():
    data = get_demo_data()
    page_title("Team", "회사 계정의 접근 권한과 팀원을 관리합니다.")
    st.dataframe(pd.DataFrame(data["team"]), use_container_width=True, hide_index=True)

    with st.expander("Invite Member (Demo)"):
        with st.form("invite_member", clear_on_submit=True):
            name = st.text_input("이름")
            role = st.text_input("역할", placeholder="Finance Analyst")
            permission = st.selectbox("권한", ["Viewer", "Admin"])
            invite = st.form_submit_button("초대")
        if invite:
            if name.strip() and role.strip():
                data["team"].append({"name": name.strip(), "role": role.strip(), "permission": permission})
                log_event(f"팀원 초대: {name.strip()}")
                st.success("데모 팀원으로 추가되었습니다.")
                st.rerun()
            else:
                st.error("이름과 역할을 입력해 주세요.")


# =========================================================
# AUDIT
# =========================================================

def audit_log():
    data = get_demo_data()
    page_title("Audit Log", "사용자·AI·시스템의 주요 재무 의사결정을 기록합니다.")
    for log in data["logs"]:
        with st.container(border=True):
            st.write(f"**{log['action']}**")
            st.caption(f"{log['time']} · {log['actor']}")


# =========================================================
# SETTINGS
# =========================================================

def settings():
    app_settings = get_settings()
    policy = get_policy()
    page_title("Settings", "데모 기업 정보와 기본 Treasury Policy를 설정합니다.")

    preferences = ["매우 보수적", "보수적", "균형형", "적극적", "매우 적극적"]
    currencies = ["KRW", "USD", "EUR"]

    with st.form("settings_form"):
        company_name = st.text_input("회사명", value=app_settings["company_name"])
        representative = st.text_input("대표자", value=app_settings["representative"])
        currency = st.selectbox("기준 통화", currencies, index=currencies.index(app_settings["currency"]))
        risk_preference = st.selectbox(
            "기본 운용성향",
            preferences,
            index=preferences.index(policy["risk_preference"]),
        )
        save = st.form_submit_button("Save Settings", type="primary")

    if save:
        app_settings["company_name"] = company_name.strip() or app_settings["company_name"]
        app_settings["representative"] = representative.strip() or app_settings["representative"]
        app_settings["currency"] = currency
        policy["risk_preference"] = risk_preference
        log_event("Settings 및 기본 운용성향 변경")
        st.success("설정이 저장되고 관련 재무 권고가 다시 계산됩니다.")
        st.rerun()

    st.divider()
    a, b = st.columns(2)
    if a.button("Reset Demo Data", use_container_width=True):
        reset_runtime_state()
        log_event("Demo data reset", actor="TreaSurv System")
        st.rerun()
    if b.button("로그아웃", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
