from __future__ import annotations

import pandas as pd


DEFAULT_DATA_PATH = "Updated-Product-Sales-Region.xlsx"


def load_sales_data(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """Load and lightly clean the sales dataset."""
    data = pd.read_excel(path)
    data = data.loc[:, ~data.columns.str.contains("^Unnamed")].copy()

    for column in ("Date", "OrderDate", "DeliveryDate"):
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")

    return data


def total_gross_revenue(data: pd.DataFrame) -> float:
    return float(data["Revenue (Gross)"].sum())


def total_order_count(data: pd.DataFrame) -> int:
    return int(data["OrderID"].count())


def avg_order_value(data: pd.DataFrame) -> float:
    return float(data["TotalPrice"].mean())


def revenue_by_region(data: pd.DataFrame) -> pd.Series:
    return (
        data.groupby("Region")["Revenue (Gross)"]
        .sum()
        .sort_values(ascending=False)
    )


def orders_by_region(data: pd.DataFrame) -> pd.Series:
    return data.groupby("Region")["OrderID"].count().sort_values(ascending=False)


def top_selling_products_by_revenue(
    data: pd.DataFrame,
    limit: int = 5,
) -> pd.Series:
    return (
        data.groupby("Product")["Revenue (Gross)"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )


def most_sold_products_by_qty(data: pd.DataFrame, limit: int = 5) -> pd.Series:
    return (
        data.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )


def monthly_sales_trend(data: pd.DataFrame) -> pd.Series:
    monthly = data.groupby(data["OrderDate"].dt.to_period("M"))["Revenue (Gross)"].sum()
    monthly.index = monthly.index.astype(str)
    return monthly


def revenue_by_customer_type(data: pd.DataFrame) -> pd.Series:
    return data.groupby("CustomerType")["Revenue (Gross)"].sum().sort_values(ascending=False)


def revenue_by_payment_method(data: pd.DataFrame) -> pd.Series:
    return (
        data.groupby("PaymentMethod")["Revenue (Gross)"]
        .sum()
        .sort_values(ascending=False)
    )


def dashboard_metrics(data: pd.DataFrame) -> dict[str, float]:
    return {
        "total_revenue": total_gross_revenue(data),
        "total_orders": total_order_count(data),
        "avg_order_value": avg_order_value(data),
    }
