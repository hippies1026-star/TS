from finance_engine import (
    calculate_runway,
    calculate_survival_floor,
    calculate_investable_cash,
    apply_risk_preference,
)
from forecast_engine import build_cash_forecast, forecast_summary


def execute_tool(name: str, arguments: dict):
    if name == "calculate_runway":
        return calculate_runway(
            current_cash=arguments["current_cash"],
            monthly_revenue=arguments["monthly_revenue"],
            monthly_expense=arguments["monthly_expense"],
        )

    if name == "calculate_survival_floor":
        return calculate_survival_floor(
            monthly_revenue=arguments["monthly_revenue"],
            monthly_expense=arguments["monthly_expense"],
            horizon_months=arguments["horizon_months"],
            revenue_stress_percent=arguments["revenue_stress_percent"],
            expense_stress_percent=arguments["expense_stress_percent"],
            emergency_months=arguments["emergency_months"],
        )

    if name == "calculate_investable_cash":
        return calculate_investable_cash(
            current_cash=arguments["current_cash"],
            survival_floor=arguments["survival_floor"],
        )

    if name == "apply_risk_preference":
        return apply_risk_preference(
            maximum_investable_cash=arguments["maximum_investable_cash"],
            preference=arguments["preference"],
        )

    if name == "calculate_forecast_summary":
        rows = build_cash_forecast(
            current_cash=arguments["current_cash"],
            monthly_revenue=arguments["monthly_revenue"],
            monthly_expense=arguments["monthly_expense"],
            plans=arguments.get("plans", []),
            as_of=arguments["as_of"],
            months=arguments.get("months", 18),
            revenue_stress_percent=arguments.get("revenue_stress_percent", 0),
            expense_stress_percent=arguments.get("expense_stress_percent", 0),
        )
        summary = forecast_summary(rows, arguments.get("survival_floor", 0))
        summary["plan_event_months"] = [
            {"month": row["Month"], "events": row["Events"]}
            for row in rows
            if row["Events"] != "-"
        ]
        return summary

    return {"error": f"알 수 없는 Tool: {name}"}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_runway",
            "description": "현재 현금과 월 현금흐름을 이용해 Burn Rate와 Runway를 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_cash": {"type": "number"},
                    "monthly_revenue": {"type": "number"},
                    "monthly_expense": {"type": "number"},
                },
                "required": ["current_cash", "monthly_revenue", "monthly_expense"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_survival_floor",
            "description": "스트레스 시나리오와 비상예비자금을 고려해 최소 현금보유액을 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "monthly_revenue": {"type": "number"},
                    "monthly_expense": {"type": "number"},
                    "horizon_months": {"type": "integer"},
                    "revenue_stress_percent": {"type": "number"},
                    "expense_stress_percent": {"type": "number"},
                    "emergency_months": {"type": "integer"},
                },
                "required": [
                    "monthly_revenue", "monthly_expense", "horizon_months",
                    "revenue_stress_percent", "expense_stress_percent", "emergency_months"
                ],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_investable_cash",
            "description": "현재 현금에서 최소 현금보유액을 제외해 최대 운용가능자금을 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_cash": {"type": "number"},
                    "survival_floor": {"type": "number"},
                },
                "required": ["current_cash", "survival_floor"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_risk_preference",
            "description": "최대 운용가능자금에 사용자의 자금운용 성향을 적용한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "maximum_investable_cash": {"type": "number"},
                    "preference": {
                        "type": "string",
                        "enum": ["매우 보수적", "보수적", "균형형", "적극적", "매우 적극적"],
                    },
                },
                "required": ["maximum_investable_cash", "preference"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_forecast_summary",
            "description": "등록된 사업계획과 스트레스 조건을 반영해 향후 현금예측 요약을 계산한다. 사업계획의 현금영향을 묻는 질문에 사용한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "current_cash": {"type": "number"},
                    "monthly_revenue": {"type": "number"},
                    "monthly_expense": {"type": "number"},
                    "as_of": {"type": "string", "description": "YYYY-MM"},
                    "months": {"type": "integer"},
                    "revenue_stress_percent": {"type": "number"},
                    "expense_stress_percent": {"type": "number"},
                    "survival_floor": {"type": "number"},
                    "plans": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "type": {"type": "string"},
                                "title": {"type": "string"},
                                "date": {"type": "string"},
                                "amount": {"type": "number"},
                                "detail": {"type": "string"},
                            },
                            "required": ["type", "title", "date", "amount"],
                        },
                    },
                },
                "required": ["current_cash", "monthly_revenue", "monthly_expense", "as_of", "plans"],
            },
        },
    },
]
