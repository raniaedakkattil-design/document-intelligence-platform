from typing import Any


TOLERANCE = 0.01


def compare_values(
    calculated: float | None,
    reported: float | None,
    tolerance: float = TOLERANCE,
) -> dict[str, Any]:
    """
    Compare a calculated value with a reported value.

    Missing operands produce NOT_APPLICABLE.
    """

    if calculated is None or reported is None:
        return {
            "calculated": calculated,
            "reported": reported,
            "variance": None,
            "status": "NOT_APPLICABLE",
        }

    variance = round(calculated - reported, 2)

    status = "PASS" if abs(variance) <= tolerance else "FAIL"

    return {
        "calculated": calculated,
        "reported": reported,
        "variance": variance,
        "status": status,
    }


def validate_balance_sheet(
    total_assets: float | None,
    total_capital_and_liabilities: float | None,
) -> dict[str, Any]:
    """
    Balance Sheet:
    Total Assets = Total Capital and Liabilities
    """

    comparison = compare_values(
        calculated=total_assets,
        reported=total_capital_and_liabilities,
    )

    return {
        "rule": "Balance Sheet Reconciliation",
        "formula": "Total Assets = Total Capital and Liabilities",
        "inputs": {
            "total_assets": total_assets,
            "total_capital_and_liabilities": total_capital_and_liabilities,
        },
        **comparison,
    }


def validate_profit_and_loss(
    interest_earned: float | None,
    other_income: float | None,
    total_income: float | None,
    interest_expended: float | None,
    operating_expenses: float | None,
    provisions: float | None,
    total_expenditure: float | None,
    profit_before_minority: float | None,
    minority_interest: float | None,
    net_profit: float | None,
) -> list[dict[str, Any]]:
    """
    Profit & Loss validation rules.
    """

    results = []

    # Total Income = Interest Earned + Other Income
    if interest_earned is not None and other_income is not None:
        calculated = round(interest_earned + other_income, 2)

        comparison = compare_values(
            calculated=calculated,
            reported=total_income,
        )

        results.append({
            "rule": "Total Income Reconciliation",
            "formula": "Interest Earned + Other Income = Total Income",
            "inputs": {
                "interest_earned": interest_earned,
                "other_income": other_income,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Total Income Reconciliation",
            "formula": "Interest Earned + Other Income = Total Income",
            "inputs": {
                "interest_earned": interest_earned,
                "other_income": other_income,
            },
            "calculated": None,
            "reported": total_income,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Total Expenditure =
    # Interest Expended + Operating Expenses + Provisions
    if (
        interest_expended is not None
        and operating_expenses is not None
        and provisions is not None
    ):
        calculated = round(
            interest_expended
            + operating_expenses
            + provisions,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=total_expenditure,
        )

        results.append({
            "rule": "Total Expenditure Reconciliation",
            "formula": (
                "Interest Expended + Operating Expenses + "
                "Provisions = Total Expenditure"
            ),
            "inputs": {
                "interest_expended": interest_expended,
                "operating_expenses": operating_expenses,
                "provisions": provisions,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Total Expenditure Reconciliation",
            "formula": (
                "Interest Expended + Operating Expenses + "
                "Provisions = Total Expenditure"
            ),
            "inputs": {
                "interest_expended": interest_expended,
                "operating_expenses": operating_expenses,
                "provisions": provisions,
            },
            "calculated": None,
            "reported": total_expenditure,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Profit Before Minority =
    # Total Income - Total Expenditure
    if total_income is not None and total_expenditure is not None:
        calculated = round(
            total_income - total_expenditure,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=profit_before_minority,
        )

        results.append({
            "rule": "Profit Before Minority Reconciliation",
            "formula": "Total Income - Total Expenditure = Profit Before Minority",
            "inputs": {
                "total_income": total_income,
                "total_expenditure": total_expenditure,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Profit Before Minority Reconciliation",
            "formula": "Total Income - Total Expenditure = Profit Before Minority",
            "inputs": {
                "total_income": total_income,
                "total_expenditure": total_expenditure,
            },
            "calculated": None,
            "reported": profit_before_minority,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Net Profit =
    # Profit Before Minority - Minority Interest
    if (
        profit_before_minority is not None
        and minority_interest is not None
    ):
        calculated = round(
            profit_before_minority - minority_interest,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=net_profit,
        )

        results.append({
            "rule": "Net Profit Reconciliation",
            "formula": (
                "Profit Before Minority - Minority Interest = "
                "Net Profit"
            ),
            "inputs": {
                "profit_before_minority": profit_before_minority,
                "minority_interest": minority_interest,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Net Profit Reconciliation",
            "formula": (
                "Profit Before Minority - Minority Interest = "
                "Net Profit"
            ),
            "inputs": {
                "profit_before_minority": profit_before_minority,
                "minority_interest": minority_interest,
            },
            "calculated": None,
            "reported": net_profit,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    return results


def validate_cash_flow(
    operating_cash_flow: float | None,
    investing_cash_flow: float | None,
    financing_cash_flow: float | None,
    foreign_exchange_effect: float | None,
    net_cash_increase: float | None,
    opening_cash_balance: float | None,
    closing_cash_balance: float | None,
) -> list[dict[str, Any]]:
    """
    Cash Flow Statement validation rules.
    """

    results = []

    # Net Increase =
    # Operating + Investing + Financing + FX
    if (
        operating_cash_flow is not None
        and investing_cash_flow is not None
        and financing_cash_flow is not None
        and foreign_exchange_effect is not None
    ):
        calculated = round(
            operating_cash_flow
            + investing_cash_flow
            + financing_cash_flow
            + foreign_exchange_effect,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=net_cash_increase,
        )

        results.append({
            "rule": "Net Cash Increase Reconciliation",
            "formula": (
                "Operating + Investing + Financing + "
                "Foreign Exchange Effect = Net Cash Increase"
            ),
            "inputs": {
                "operating_cash_flow": operating_cash_flow,
                "investing_cash_flow": investing_cash_flow,
                "financing_cash_flow": financing_cash_flow,
                "foreign_exchange_effect": foreign_exchange_effect,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Net Cash Increase Reconciliation",
            "formula": (
                "Operating + Investing + Financing + "
                "Foreign Exchange Effect = Net Cash Increase"
            ),
            "inputs": {
                "operating_cash_flow": operating_cash_flow,
                "investing_cash_flow": investing_cash_flow,
                "financing_cash_flow": financing_cash_flow,
                "foreign_exchange_effect": foreign_exchange_effect,
            },
            "calculated": None,
            "reported": net_cash_increase,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Closing Balance =
    # Opening Balance + Net Increase
    if (
        opening_cash_balance is not None
        and net_cash_increase is not None
    ):
        calculated = round(
            opening_cash_balance + net_cash_increase,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=closing_cash_balance,
        )

        results.append({
            "rule": "Closing Cash Balance Reconciliation",
            "formula": (
                "Opening Cash Balance + Net Cash Increase "
                "= Closing Cash Balance"
            ),
            "inputs": {
                "opening_cash_balance": opening_cash_balance,
                "net_cash_increase": net_cash_increase,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Closing Cash Balance Reconciliation",
            "formula": (
                "Opening Cash Balance + Net Cash Increase "
                "= Closing Cash Balance"
            ),
            "inputs": {
                "opening_cash_balance": opening_cash_balance,
                "net_cash_increase": net_cash_increase,
            },
            "calculated": None,
            "reported": closing_cash_balance,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    return results


def validate_invoice(
    invoice_items: list[dict[str, Any]],
    subtotal: float | None,
    tax_amount: float | None,
    total_amount: float | None,
    cash_paid: float | None,
    change_amount: float | None,
) -> list[dict[str, Any]]:
    """
    Invoice validation rules.
    """

    results = []

    # Validate quantity × unit price = line total
    for index, item in enumerate(invoice_items, start=1):

        quantity = item.get("quantity")
        unit_price = item.get("unit_price")
        line_total = item.get("line_total")

        if (
            quantity is not None
            and unit_price is not None
            and line_total is not None
        ):
            calculated = round(quantity * unit_price, 2)

            comparison = compare_values(
                calculated=calculated,
                reported=line_total,
            )

            results.append({
                "rule": f"Invoice Line Item {index}",
                "formula": "Quantity × Unit Price = Line Total",
                "inputs": {
                    "quantity": quantity,
                    "unit_price": unit_price,
                },
                **comparison,
            })
        else:
            results.append({
                "rule": f"Invoice Line Item {index}",
                "formula": "Quantity × Unit Price = Line Total",
                "inputs": {
                    "quantity": quantity,
                    "unit_price": unit_price,
                },
                "calculated": None,
                "reported": line_total,
                "variance": None,
                "status": "NOT_APPLICABLE",
            })

    # Sum of line totals = subtotal
    line_totals = [
        item.get("line_total")
        for item in invoice_items
        if item.get("line_total") is not None
    ]

    if line_totals and subtotal is not None:
        calculated = round(sum(line_totals), 2)

        comparison = compare_values(
            calculated=calculated,
            reported=subtotal,
        )

        results.append({
            "rule": "Invoice Subtotal Reconciliation",
            "formula": "Sum of Line Totals = Subtotal",
            "inputs": {
                "line_totals": line_totals,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Invoice Subtotal Reconciliation",
            "formula": "Sum of Line Totals = Subtotal",
            "inputs": {
                "line_totals": line_totals,
            },
            "calculated": None,
            "reported": subtotal,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Subtotal + Tax = Total
    if (
        subtotal is not None
        and tax_amount is not None
        and total_amount is not None
    ):
        calculated = round(
            subtotal + tax_amount,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=total_amount,
        )

        results.append({
            "rule": "Invoice Tax Reconciliation",
            "formula": "Subtotal + Tax = Total",
            "inputs": {
                "subtotal": subtotal,
                "tax_amount": tax_amount,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Invoice Tax Reconciliation",
            "formula": "Subtotal + Tax = Total",
            "inputs": {
                "subtotal": subtotal,
                "tax_amount": tax_amount,
            },
            "calculated": None,
            "reported": total_amount,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    # Cash Paid - Total = Change
    if (
        cash_paid is not None
        and total_amount is not None
        and change_amount is not None
    ):
        calculated = round(
            cash_paid - total_amount,
            2,
        )

        comparison = compare_values(
            calculated=calculated,
            reported=change_amount,
        )

        results.append({
            "rule": "Invoice Change Reconciliation",
            "formula": "Cash Paid - Total = Change",
            "inputs": {
                "cash_paid": cash_paid,
                "total_amount": total_amount,
            },
            **comparison,
        })
    else:
        results.append({
            "rule": "Invoice Change Reconciliation",
            "formula": "Cash Paid - Total = Change",
            "inputs": {
                "cash_paid": cash_paid,
                "total_amount": total_amount,
            },
            "calculated": None,
            "reported": change_amount,
            "variance": None,
            "status": "NOT_APPLICABLE",
        })

    return results