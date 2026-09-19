DEMO_DATA = {

    # Fixed as-of month keeps the competition demo deterministic.
    "as_of": "2026-09",

    "financials": {
        # Total cash is synchronized from the two demo bank accounts at runtime.
        "total_cash": 1_232_440_000,
        "avg_cash_inflow_3m": 108_400_000,
        "avg_cash_outflow_3m": 136_700_000,

        "payroll": 71_300_000,
        "fixed_cost": 29_800_000,

        "accounts_receivable": 184_200_000,
        "accounts_payable": 92_800_000,

        "debt": 150_000_000,
    },


    "accounts": [
        {
            "bank": "KB국민은행",
            "name": "운영계좌",
            "balance": 643_200_000,
            "account": "123-456-******",
        },
        {
            "bank": "신한은행",
            "name": "Reserve Account",
            "balance": 589_240_000,
            "account": "110-***-******",
        },
    ],


    "plans": [
        {
            "type": "Hiring",
            "title": "개발팀 증원",
            "date": "2027-01",
            "amount": -28_000_000,
            "detail": "Software Engineer 4명 · 월 인건비 증가",
        },

        {
            "type": "Expense",
            "title": "GPU Infrastructure",
            "date": "2027-03",
            "amount": -100_000_000,
            "detail": "R&D 인프라 일회성 투자",
        },

        {
            "type": "Funding",
            "title": "Series A",
            "date": "2027-06",
            "amount": 1_000_000_000,
            "detail": "예상 지연 가능성 3개월",
        },

        {
            "type": "Revenue",
            "title": "Enterprise Product",
            "date": "2027-02",
            "amount": 50_000_000,
            "detail": "예상 월매출 증가",
        },
    ],


    "integrations": [
        {
            "name": "KB국민은행",
            "type": "Banking",
            "status": "Connected",
        },
        {
            "name": "신한은행",
            "type": "Banking",
            "status": "Connected",
        },
        {
            "name": "Corporate Card",
            "type": "Card",
            "status": "Connected",
        },
        {
            "name": "Accounting ERP",
            "type": "Accounting",
            "status": "Synced",
        },
    ],


    "team": [
        {
            "name": "가태용",
            "role": "CEO",
            "permission": "Owner",
        },
        {
            "name": "가태용",
            "role": "Finance Manager",
            "permission": "Admin",
        },
        {
            "name": "가태용",
            "role": "Accountant",
            "permission": "Viewer",
        },
        {
            "name": "TreaSurv AI",
            "role": "AI CFO Agent",
            "permission": "System",
        },
    ],


    "logs": [
        {
            "time": "Today 01:18",
            "action": "Financial data synchronized",
            "actor": "TreaSurv System",
        },
        {
            "time": "Today 00:54",
            "action": "Treasury Policy recalculated",
            "actor": "TreaSurv AI",
        },
        {
            "time": "Yesterday 22:16",
            "action": "Series A plan updated",
            "actor": "가태용",
        },
        {
            "time": "Yesterday 20:31",
            "action": "Stress scenario created",
            "actor": "가태용",
        },
    ],


    "reports": [
        "September Treasury Report",
        "Cash Position Report",
        "Runway Stress Test",
        "Board Finance Brief",
    ],
}
