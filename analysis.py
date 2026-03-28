from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DATA_PATH = "Updated-Product-Sales-Region.xlsx"
DATE_COLUMNS = ("Date", "OrderDate", "DeliveryDate")

CANONICAL_COLUMNS = {
    "revenuegross": "Revenue (Gross)",
    "revenue": "Revenue (Gross)",
    "grossrevenue": "Revenue (Gross)",
    "sales": "Revenue (Gross)",
    "salesamount": "Revenue (Gross)",
    "orderid": "OrderID",
    "orderno": "OrderID",
    "ordernumber": "OrderID",
    "region": "Region",
    "product": "Product",
    "productname": "Product",
    "quantity": "Quantity",
    "qty": "Quantity",
    "unitprice": "UnitPrice",
    "price": "UnitPrice",
    "totalprice": "TotalPrice",
    "ordertotal": "TotalPrice",
    "customertype": "CustomerType",
    "paymentmethod": "PaymentMethod",
    "orderdate": "OrderDate",
    "date": "Date",
    "deliverydate": "DeliveryDate",
}


def normalize_column_name(name: str) -> str:
    return "".join(char.lower() for char in name if char.isalnum())


def standardize_columns(data: pd.DataFrame) -> pd.DataFrame:
    rename_map: dict[str, str] = {}
    used_targets: set[str] = set()

    for column in data.columns:
        normalized = normalize_column_name(str(column))
        target = CANONICAL_COLUMNS.get(normalized)
        if target and target not in used_targets:
            rename_map[column] = target
            used_targets.add(target)

    return data.rename(columns=rename_map)


def clean_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    """Apply shared cleanup rules to uploaded or local datasets."""
    data = data.loc[:, ~data.columns.str.contains("^Unnamed")].copy()
    data = standardize_columns(data)

    for column in DATE_COLUMNS:
        if column in data.columns:
            data[column] = pd.to_datetime(data[column], errors="coerce")

    if "Revenue (Gross)" not in data.columns:
        if {"Quantity", "UnitPrice"}.issubset(data.columns):
            data["Revenue (Gross)"] = data["Quantity"] * data["UnitPrice"]
        elif "TotalPrice" in data.columns:
            data["Revenue (Gross)"] = data["TotalPrice"]

    if "TotalPrice" not in data.columns and "Revenue (Gross)" in data.columns:
        data["TotalPrice"] = data["Revenue (Gross)"]

    return data


def load_sales_data(path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    data = pd.read_excel(path)
    return clean_sales_data(data)


def load_uploaded_file(file, file_name: str) -> pd.DataFrame:
    suffix = Path(file_name).suffix.lower()
    if suffix == ".csv":
        data = pd.read_csv(file)
    elif suffix in {".xlsx", ".xls"}:
        data = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type. Please upload CSV or Excel.")
    return clean_sales_data(data)


def missing_columns(data: pd.DataFrame, required: list[str]) -> list[str]:
    return [column for column in required if column not in data.columns]


def has_columns(data: pd.DataFrame, required: list[str]) -> bool:
    return not missing_columns(data, required)


def filter_data(
    data: pd.DataFrame,
    start_date=None,
    end_date=None,
    region: str | None = None,
) -> pd.DataFrame:
    filtered = data.copy()

    date_column = "OrderDate" if "OrderDate" in filtered.columns else "Date" if "Date" in filtered.columns else None
    if date_column and start_date is not None:
        filtered = filtered[filtered[date_column].dt.date >= start_date]
    if date_column and end_date is not None:
        filtered = filtered[filtered[date_column].dt.date <= end_date]
    if region and region != "All" and "Region" in filtered.columns:
        filtered = filtered[filtered["Region"] == region]

    return filtered


def total_gross_revenue(data: pd.DataFrame) -> float | None:
    if not has_columns(data, ["Revenue (Gross)"]):
        return None
    return float(data["Revenue (Gross)"].sum())


def total_order_count(data: pd.DataFrame) -> int | None:
    if not has_columns(data, ["OrderID"]):
        return None
    return int(data["OrderID"].count())


def avg_order_value(data: pd.DataFrame) -> float | None:
    if not has_columns(data, ["TotalPrice"]):
        return None
    return float(data["TotalPrice"].mean())


def revenue_by_region(data: pd.DataFrame) -> pd.Series | None:
    if not has_columns(data, ["Region", "Revenue (Gross)"]):
        return None
    return data.groupby("Region")["Revenue (Gross)"].sum().sort_values(ascending=False)


def top_selling_products_by_revenue(
    data: pd.DataFrame,
    limit: int = 5,
) -> pd.Series | None:
    if not has_columns(data, ["Product", "Revenue (Gross)"]):
        return None
    return (
        data.groupby("Product")["Revenue (Gross)"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )


def most_sold_products_by_qty(data: pd.DataFrame, limit: int = 5) -> pd.Series | None:
    if not has_columns(data, ["Product", "Quantity"]):
        return None
    return (
        data.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(limit)
    )


def monthly_sales_trend(data: pd.DataFrame) -> pd.Series | None:
    date_column = "OrderDate" if "OrderDate" in data.columns else "Date" if "Date" in data.columns else None
    if date_column is None or "Revenue (Gross)" not in data.columns:
        return None

    monthly = data.groupby(data[date_column].dt.to_period("M"))["Revenue (Gross)"].sum()
    monthly.index = monthly.index.astype(str)
    return monthly


def revenue_by_customer_type(data: pd.DataFrame) -> pd.Series | None:
    if not has_columns(data, ["CustomerType", "Revenue (Gross)"]):
        return None
    return data.groupby("CustomerType")["Revenue (Gross)"].sum().sort_values(ascending=False)


def revenue_by_payment_method(data: pd.DataFrame) -> pd.Series | None:
    if not has_columns(data, ["PaymentMethod", "Revenue (Gross)"]):
        return None
    return data.groupby("PaymentMethod")["Revenue (Gross)"].sum().sort_values(ascending=False)


def dashboard_metrics(data: pd.DataFrame) -> dict[str, float | int | None]:
    return {
        "total_revenue": total_gross_revenue(data),
        "total_orders": total_order_count(data),
        "avg_order_value": avg_order_value(data),
    }
