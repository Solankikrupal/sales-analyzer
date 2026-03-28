from __future__ import annotations

from io import BytesIO

import streamlit as st

from analysis import (
    dashboard_metrics,
    filter_data,
    load_sales_data,
    load_uploaded_file,
    missing_columns,
    monthly_sales_trend,
    most_sold_products_by_qty,
    revenue_by_customer_type,
    revenue_by_payment_method,
    revenue_by_region,
    top_selling_products_by_revenue,
)
from visualization import get_visualization


st.set_page_config(page_title="Sales Analyzer Dashboard", layout="wide")


EXPECTED_COLUMNS = [
    "Revenue (Gross)",
    "OrderID",
    "OrderDate",
    "Region",
    "Product",
    "Quantity",
]


@st.cache_data
def get_default_data():
    return load_sales_data()


@st.cache_data
def get_uploaded_data(file_bytes: bytes, file_name: str):
    return load_uploaded_file(BytesIO(file_bytes), file_name)


def format_metric(value, money: bool = False) -> str:
    if value is None:
        return "N/A"
    if money:
        return f"${value:,.2f}"
    if isinstance(value, float):
        return f"{value:,.2f}"
    return f"{value:,}"


def render_chart(title, data, kind, xlabel, ylabel, color, **kwargs):
    st.subheader(title)
    if data is None or data.empty:
        st.info(f"`{title}` can't be shown because the uploaded file is missing the required columns.")
        return

    chart = get_visualization(
        data,
        title=title,
        kind=kind,
        xlabel=xlabel,
        ylabel=ylabel,
        color=color,
        **kwargs,
    )
    st.pyplot(chart)


def main():
    st.title("Sales Analyzer Dashboard")
    st.caption("Upload a sales file, review the KPIs, apply filters, and explore the charts that match the available columns.")

    with st.sidebar:
        st.header("Controls")
        st.write("KPI = Key Performance Indicator. These are the top summary numbers like total revenue or total orders.")
        uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"])

    if uploaded_file is not None:
        data = get_uploaded_data(uploaded_file.getvalue(), uploaded_file.name)
        st.success(f"Loaded file: {uploaded_file.name}")
    else:
        data = get_default_data()
        st.info("Using default dataset: `Updated-Product-Sales-Region.xlsx`")

    gaps = missing_columns(data, EXPECTED_COLUMNS)
    if gaps:
        st.warning(
            "Some expected sales columns are missing, so a few KPIs or charts may show `N/A`: "
            + ", ".join(gaps)
        )

    with st.expander("Dataset Preview", expanded=True):
        st.write(f"Rows: {len(data):,} | Columns: {len(data.columns):,}")
        st.dataframe(data.head(10), use_container_width=True)

    with st.sidebar:
        date_column = "OrderDate" if "OrderDate" in data.columns else "Date" if "Date" in data.columns else None

        start_date = None
        end_date = None
        if date_column and not data[date_column].dropna().empty:
            min_date = data[date_column].dropna().min().date()
            max_date = data[date_column].dropna().max().date()
            start_date = st.date_input("Start date", value=min_date, min_value=min_date, max_value=max_date)
            end_date = st.date_input("End date", value=max_date, min_value=min_date, max_value=max_date)

        region = "All"
        if "Region" in data.columns:
            region_options = ["All"] + sorted(data["Region"].dropna().astype(str).unique().tolist())
            region = st.selectbox("Region", region_options)

    filtered_data = filter_data(data, start_date=start_date, end_date=end_date, region=region)

    metrics = dashboard_metrics(filtered_data)
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", format_metric(metrics["total_revenue"], money=True))
    col2.metric("Total Orders", format_metric(metrics["total_orders"]))
    col3.metric("Average Order Value", format_metric(metrics["avg_order_value"], money=True))

    left, right = st.columns(2)

    with left:
        render_chart(
            "Revenue by Region",
            revenue_by_region(filtered_data),
            "bar",
            "Region",
            "Revenue",
            "#1f77b4",
        )
        render_chart(
            "Top Products by Revenue",
            top_selling_products_by_revenue(filtered_data),
            "bar",
            "Product",
            "Revenue",
            "#2ca02c",
        )

    with right:
        render_chart(
            "Monthly Sales Trend",
            monthly_sales_trend(filtered_data),
            "line",
            "Month",
            "Revenue",
            "#d62728",
            marker="o",
        )
        render_chart(
            "Most Sold Products",
            most_sold_products_by_qty(filtered_data),
            "bar",
            "Product",
            "Quantity",
            "#ff7f0e",
        )

    tab1, tab2, tab3 = st.tabs(["Customer Type", "Payment Method", "Raw Data"])

    with tab1:
        render_chart(
            "Revenue by Customer Type",
            revenue_by_customer_type(filtered_data),
            "bar",
            "Customer Type",
            "Revenue",
            "#9467bd",
        )

    with tab2:
        render_chart(
            "Revenue by Payment Method",
            revenue_by_payment_method(filtered_data),
            "bar",
            "Payment Method",
            "Revenue",
            "#8c564b",
        )

    with tab3:
        st.dataframe(filtered_data, use_container_width=True)


if __name__ == "__main__":
    main()
