DEMO_FINANCIALS = {
    "total_cash": 1_032_440_000,

    "avg_cash_inflow_3m": 108_400_000,
    "avg_cash_outflow_3m": 136_700_000,

    "payroll": 71_300_000,
    "fixed_operating_costs": 29_800_000,

    "accounts_receivable": 184_200_000,
    "accounts_payable": 92_800_000,

    "debt_outstanding": 150_000_000,

    "last_sync": "2026-09-20 01:30",
}


DEMO_ACCOUNTS = [
    {
        "institution": "KB국민은행",
        "type": "운영계좌",
        "balance": 643_200_000,
        "masked_account": "123-456-******",
        "status": "Connected",
    },
    {
        "institution": "신한은행",
        "type": "예비자금 계좌",
        "balance": 389_240_000,
        "masked_account": "110-***-******",
        "status": "Connected",
    },
]


DEMO_INTEGRATIONS = [
    {
        "name": "KB국민은행",
        "category": "Banking",
        "status": "Connected",
    },
    {
        "name": "신한은행",
        "category": "Banking",
        "status": "Connected",
    },
    {
        "name": "법인카드",
        "category": "Card",
        "status": "Connected",
    },
    {
        "name": "Accounting ERP",
        "category": "Accounting",
        "status": "Synced",
    },
]