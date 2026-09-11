from app.services.financial_validation_service import (
    validate_balance_sheet,
    validate_cash_flow,
    validate_invoice,
    validate_profit_and_loss,
)


def test_balance_sheet_pass():
    result = validate_balance_sheet(
        total_assets=4908040.84,
        total_capital_and_liabilities=4908040.84,
    )

    assert result["status"] == "PASS"
    assert result["variance"] == 0.0


def test_balance_sheet_fail():
    result = validate_balance_sheet(
        total_assets=4908040.84,
        total_capital_and_liabilities=4900000.00,
    )

    assert result["status"] == "FAIL"


def test_balance_sheet_not_applicable():
    result = validate_balance_sheet(
        total_assets=None,
        total_capital_and_liabilities=4908040.84,
    )

    assert result["status"] == "NOT_APPLICABLE"


def test_profit_and_loss():
    results = validate_profit_and_loss(
        interest_earned=348615.15,
        other_income=146847.66,
        total_income=495462.81,
        interest_expended=185491.23,
        operating_expenses=181173.91,
        provisions=49578.21,
        total_expenditure=416243.35,
        profit_before_minority=79219.46,
        minority_interest=3193.49,
        net_profit=76025.97,
    )

    assert all(result["status"] == "PASS" for result in results)


def test_cash_flow():
    results = validate_cash_flow(
        operating_cash_flow=113506.38,
        investing_cash_flow=6362.72,
        financing_cash_flow=-59004.85,
        foreign_exchange_effect=1113.90,
        net_cash_increase=61978.15,
        opening_cash_balance=249947.90,
        closing_cash_balance=311926.05,
    )

    assert all(result["status"] == "PASS" for result in results)


def test_invoice():
    results = validate_invoice(
        invoice_items=[
            {
                "quantity": 1,
                "unit_price": 1.80,
                "line_total": 1.80,
            },
            {
                "quantity": 2,
                "unit_price": 2.10,
                "line_total": 4.20,
            },
            {
                "quantity": 1,
                "unit_price": 0.20,
                "line_total": 0.20,
            },
        ],
        subtotal=6.20,
        tax_amount=None,
        total_amount=6.20,
        cash_paid=100.00,
        change_amount=93.80,
    )

    assert results[0]["status"] == "PASS"
    assert results[1]["status"] == "PASS"
    assert results[2]["status"] == "PASS"
    assert results[3]["status"] == "PASS"
    assert results[4]["status"] == "NOT_APPLICABLE"
    assert results[5]["status"] == "PASS"