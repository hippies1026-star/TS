from datetime import date


def _parse_year_month(value: str):
    try:
        year_text, month_text = str(value).strip().split("-", 1)
        year = int(year_text)
        month = int(month_text)
        if month < 1 or month > 12:
            return None
        return year, month
    except (TypeError, ValueError):
        return None


def _add_months(year: int, month: int, offset: int):
    index = year * 12 + (month - 1) + offset
    return index // 12, index % 12 + 1


def _month_index(as_of: str, target: str):
    start = _parse_year_month(as_of)
    end = _parse_year_month(target)
    if not start or not end:
        return None

    start_index = start[0] * 12 + (start[1] - 1)
    end_index = end[0] * 12 + (end[1] - 1)

    # M1 is the month immediately after the as-of month.
    return end_index - start_index - 1


def build_cash_forecast(
    current_cash: float,
    monthly_revenue: float,
    monthly_expense: float,
    plans: list,
    as_of: str,
    months: int = 18,
    revenue_stress_percent: float = 0,
    expense_stress_percent: float = 0,
):
    """
    Build a deterministic monthly cash forecast.

    Prototype assumptions:
    - Hiring: recurring monthly cash outflow from the plan month onward.
    - Revenue: recurring monthly cash inflow from the plan month onward.
    - Expense: one-time cash outflow in the plan month.
    - Funding: one-time cash inflow in the plan month.
    """

    revenue_factor = max(0, 1 - revenue_stress_percent / 100)
    expense_factor = 1 + expense_stress_percent / 100

    base_revenue = monthly_revenue * revenue_factor
    base_expense = monthly_expense * expense_factor

    start = _parse_year_month(as_of)
    if not start:
        today = date.today()
        start = (today.year, today.month)

    recurring_revenue = 0.0
    recurring_expense = 0.0
    cash = float(current_cash)

    rows = []

    for month_idx in range(months):
        year, month = _add_months(start[0], start[1], month_idx + 1)
        month_key = f"{year:04d}-{month:02d}"

        one_time_change = 0.0
        events = []

        for plan in plans:
            if _month_index(as_of, plan.get("date")) != month_idx:
                continue

            plan_type = plan.get("type", "")
            amount = float(plan.get("amount", 0))
            title = plan.get("title", plan_type)

            if plan_type == "Hiring":
                recurring_expense += abs(amount) * expense_factor
                events.append(f"{title} (월간 비용 반영)")
            elif plan_type == "Revenue":
                recurring_revenue += max(0, amount) * revenue_factor
                events.append(f"{title} (월간 매출 반영)")
            elif plan_type == "Expense":
                one_time_change -= abs(amount) * expense_factor
                events.append(title)
            elif plan_type == "Funding":
                one_time_change += abs(amount)
                events.append(title)
            else:
                one_time_change += amount
                events.append(title)

        monthly_inflow = base_revenue + recurring_revenue
        monthly_outflow = base_expense + recurring_expense
        net_change = monthly_inflow - monthly_outflow + one_time_change
        cash += net_change

        rows.append(
            {
                "Month": month_key,
                "Projected Cash": round(cash),
                "Monthly Inflow": round(monthly_inflow),
                "Monthly Outflow": round(monthly_outflow),
                "One-time Plan Impact": round(one_time_change),
                "Net Change": round(net_change),
                "Events": ", ".join(events) if events else "-",
            }
        )

    return rows


def forecast_summary(rows: list, survival_floor: float = 0):
    if not rows:
        return {
            "ending_cash": 0,
            "minimum_cash": 0,
            "minimum_cash_month": None,
            "months_below_floor": 0,
            "first_below_floor": None,
        }

    minimum_row = min(rows, key=lambda row: row["Projected Cash"])
    below = [row for row in rows if row["Projected Cash"] < survival_floor]

    return {
        "ending_cash": rows[-1]["Projected Cash"],
        "minimum_cash": minimum_row["Projected Cash"],
        "minimum_cash_month": minimum_row["Month"],
        "months_below_floor": len(below),
        "first_below_floor": below[0]["Month"] if below else None,
    }
