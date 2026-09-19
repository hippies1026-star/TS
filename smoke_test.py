from data.demo_store import DEMO_DATA
from finance_engine import (
    apply_risk_preference,
    calculate_investable_cash,
    calculate_runway,
    calculate_survival_floor,
)
from forecast_engine import build_cash_forecast, forecast_summary


def main():
    f = DEMO_DATA["financials"]
    runway = calculate_runway(
        f["total_cash"], f["avg_cash_inflow_3m"], f["avg_cash_outflow_3m"]
    )
    survival = calculate_survival_floor(
        f["avg_cash_inflow_3m"], f["avg_cash_outflow_3m"], 12, 20, 10, 2
    )
    investable = calculate_investable_cash(
        f["total_cash"], survival["survival_floor"]
    )
    recommended = apply_risk_preference(
        investable["maximum_investable_cash"], "균형형"
    )
    rows = build_cash_forecast(
        f["total_cash"],
        f["avg_cash_inflow_3m"],
        f["avg_cash_outflow_3m"],
        DEMO_DATA["plans"],
        DEMO_DATA["as_of"],
        18,
        20,
        10,
    )
    summary = forecast_summary(rows, survival["survival_floor"])

    assert runway["runway_months"] > 0
    assert survival["survival_floor"] > 0
    assert investable["maximum_investable_cash"] > 0
    assert recommended["recommended_deployment"] > 0
    assert len(rows) == 18

    print("TreaSurv smoke test: PASS")
    print("Runway:", runway)
    print("Survival Floor:", survival["survival_floor"])
    print("Investable Cash:", investable["maximum_investable_cash"])
    print("Recommended Deployment:", recommended["recommended_deployment"])
    print("Stress Forecast Summary:", summary)


if __name__ == "__main__":
    main()
