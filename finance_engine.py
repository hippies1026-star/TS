def calculate_runway(
    current_cash: float,
    monthly_revenue: float,
    monthly_expense: float
):
    """
    현재 현금, 월 현금유입, 월 현금지출을 이용해
    Burn Rate와 Runway를 계산한다.
    """

    monthly_burn = monthly_expense - monthly_revenue

    if monthly_burn <= 0:
        return {
            "monthly_burn": 0,
            "runway_months": None,
            "status": "positive_cashflow"
        }

    runway_months = current_cash / monthly_burn

    return {
        "monthly_burn": round(monthly_burn),
        "runway_months": round(runway_months, 2),
        "status": "burning_cash"
    }


def calculate_survival_floor(
    monthly_revenue: float,
    monthly_expense: float,
    horizon_months: int = 12,
    revenue_stress_percent: float = 20,
    expense_stress_percent: float = 10,
    emergency_months: int = 2
):
    """
    스트레스 상황을 고려하여
    기업이 목표 기간 동안 확보해야 하는 최소 현금을 계산한다.

    현재는 프로토타입용 규칙 기반 계산이다.
    """

    # 매출 감소 시나리오
    stressed_revenue = monthly_revenue * (
        1 - revenue_stress_percent / 100
    )

    # 비용 증가 시나리오
    stressed_expense = monthly_expense * (
        1 + expense_stress_percent / 100
    )

    # 스트레스 상황의 월 현금소진액
    stressed_monthly_burn = max(
        0,
        stressed_expense - stressed_revenue
    )

    # 목표 기간 동안 필요한 운영자금
    operating_requirement = (
        stressed_monthly_burn * horizon_months
    )

    # 비상예비자금
    emergency_reserve = (
        stressed_expense * emergency_months
    )

    # Survival Floor
    survival_floor = (
        operating_requirement + emergency_reserve
    )

    return {
        "stressed_revenue": round(stressed_revenue),
        "stressed_expense": round(stressed_expense),
        "stressed_monthly_burn": round(stressed_monthly_burn),
        "operating_requirement": round(operating_requirement),
        "emergency_reserve": round(emergency_reserve),
        "survival_floor": round(survival_floor)
    }


def calculate_investable_cash(
    current_cash: float,
    survival_floor: float
):
    """
    Survival Floor를 제외한 최대 운용가능자금을 계산한다.
    """

    maximum_investable_cash = max(
        0,
        current_cash - survival_floor
    )

    cash_shortfall = max(
        0,
        survival_floor - current_cash
    )

    return {
        "maximum_investable_cash": round(
            maximum_investable_cash
        ),
        "cash_shortfall": round(
            cash_shortfall
        )
    }


def apply_risk_preference(
    maximum_investable_cash: float,
    preference: str
):
    """
    최대 운용가능자금 중 실제로 얼마를 운용할지
    사용자의 자금운용 성향에 따라 결정한다.
    """

    ratios = {
        "매우 보수적": 0.20,
        "보수적": 0.40,
        "균형형": 0.60,
        "적극적": 0.80,
        "매우 적극적": 1.00
    }

    ratio = ratios.get(preference, 0.60)

    recommended_deployment = (
        maximum_investable_cash * ratio
    )

    additional_cash_buffer = (
        maximum_investable_cash
        - recommended_deployment
    )

    return {
        "preference": preference,
        "deployment_ratio": ratio,
        "recommended_deployment": round(
            recommended_deployment
        ),
        "additional_cash_buffer": round(
            additional_cash_buffer
        )
    }


# 테스트용 코드
if __name__ == "__main__":

    current_cash = 1_000_000_000
    monthly_revenue = 100_000_000
    monthly_expense = 120_000_000

    runway = calculate_runway(
        current_cash,
        monthly_revenue,
        monthly_expense
    )

    floor = calculate_survival_floor(
        monthly_revenue,
        monthly_expense,
        horizon_months=12
    )

    investable = calculate_investable_cash(
        current_cash,
        floor["survival_floor"]
    )

    preference = apply_risk_preference(
        investable["maximum_investable_cash"],
        "균형형"
    )

    print("=== Runway ===")
    print(runway)

    print("\n=== Survival Floor ===")
    print(floor)

    print("\n=== Investable Cash ===")
    print(investable)

    print("\n=== Risk Preference ===")
    print(preference)