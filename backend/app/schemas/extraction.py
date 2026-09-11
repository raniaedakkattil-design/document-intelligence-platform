from pydantic import BaseModel, Field


class LineItem(BaseModel):
    category: str | None = None
    item: str | None = None
    schedule: str | None = None
    period_1: str | None = None
    value_1: float | None = None
    period_2: str | None = None
    value_2: float | None = None
    page_number: int | None = None
    source_text: str | None = None


class InvoiceItem(BaseModel):
    description: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    line_total: float | None = None
    tax_rate: float | None = None
    page_number: int | None = None
    source_text: str | None = None


class BalanceSheetExtraction(BaseModel):
    document_type: str = "Balance Sheet"
    company_name: str | None = None
    document_date: str | None = None
    reporting_period_1: str | None = None
    reporting_period_2: str | None = None
    currency: str | None = None
    unit: str | None = None

    line_items: list[LineItem] = Field(default_factory=list)

    total_assets_period_1: float | None = None
    total_assets_period_2: float | None = None
    total_capital_and_liabilities_period_1: float | None = None
    total_capital_and_liabilities_period_2: float | None = None


class ProfitLossExtraction(BaseModel):
    document_type: str = "Profit and Loss"
    company_name: str | None = None
    document_date: str | None = None
    reporting_period_1: str | None = None
    reporting_period_2: str | None = None
    currency: str | None = None
    unit: str | None = None

    line_items: list[LineItem] = Field(default_factory=list)

    interest_earned_period_1: float | None = None
    interest_earned_period_2: float | None = None

    other_income_period_1: float | None = None
    other_income_period_2: float | None = None

    total_income_period_1: float | None = None
    total_income_period_2: float | None = None

    interest_expended_period_1: float | None = None
    interest_expended_period_2: float | None = None

    operating_expenses_period_1: float | None = None
    operating_expenses_period_2: float | None = None

    provisions_period_1: float | None = None
    provisions_period_2: float | None = None

    total_expenditure_period_1: float | None = None
    total_expenditure_period_2: float | None = None

    profit_before_minority_period_1: float | None = None
    profit_before_minority_period_2: float | None = None

    minority_interest_period_1: float | None = None
    minority_interest_period_2: float | None = None

    net_profit_period_1: float | None = None
    net_profit_period_2: float | None = None


class CashFlowExtraction(BaseModel):
    document_type: str = "Cash Flow Statement"
    company_name: str | None = None
    document_date: str | None = None
    reporting_period_1: str | None = None
    reporting_period_2: str | None = None
    currency: str | None = None
    unit: str | None = None

    line_items: list[LineItem] = Field(default_factory=list)

    operating_cash_flow_period_1: float | None = None
    operating_cash_flow_period_2: float | None = None

    investing_cash_flow_period_1: float | None = None
    investing_cash_flow_period_2: float | None = None

    financing_cash_flow_period_1: float | None = None
    financing_cash_flow_period_2: float | None = None

    foreign_exchange_effect_period_1: float | None = None
    foreign_exchange_effect_period_2: float | None = None

    net_cash_increase_period_1: float | None = None
    net_cash_increase_period_2: float | None = None

    opening_cash_balance_period_1: float | None = None
    opening_cash_balance_period_2: float | None = None

    closing_cash_balance_period_1: float | None = None
    closing_cash_balance_period_2: float | None = None


class InvoiceExtraction(BaseModel):
    document_type: str = "Invoice"
    company_name: str | None = None
    invoice_number: str | None = None
    document_date: str | None = None
    currency: str | None = None
    unit: str | None = None

    seller_name: str | None = None
    buyer_name: str | None = None

    invoice_items: list[InvoiceItem] = Field(default_factory=list)

    subtotal: float | None = None
    tax_amount: float | None = None
    tax_rate: float | None = None
    tax_included: bool | None = None
    total_amount: float | None = None
    cash_paid: float | None = None
    change_amount: float | None = None

    page_number: int | None = None
    source_text: str | None = None