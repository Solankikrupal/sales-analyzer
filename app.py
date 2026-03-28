from __future__ import annotations

import streamlit as st

from analysis import (
    dashboard_metrics,
    load_sales_data,
    monthly_sales_trend,
    most_sold_products_by_qty,
    revenue_by_customer_type,
    revenue_by_payment_method,
    revenue_by_region,
    top_selling_products_by_revenue,
)
from visualization import get_visualization


st.set_page_config(page_title="Sales Analyzer Dashboard", layout="wide")


@st.cache_data
def get_data():
    return load_sales_data()


def main():
    st.title("Sales Analyzer Dashboard")
    st.caption("`analysis.py` prepares data, `visualization.py` builds charts, and `app.py` renders the dashboard.")

    data = get_data()
    metrics = dashboard_metrics(data)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${metrics['total_revenue']:,.2f}")
    col2.metric("Total Orders", f"{metrics['total_orders']:,}")
    col3.metric("Average Order Value", f"${metrics['avg_order_value']:,.2f}")

    left, right = st.columns(2)

    with left:
        st.subheader("Revenue by Region")
        region_chart = get_visualization(
            revenue_by_region(data),
            title="Revenue by Region",
            kind="bar",
            xlabel="Region",
            ylabel="Revenue",
            color="#1f77b4",
        )
        st.pyplot(region_chart)

        st.subheader("Top Products by Revenue")
        top_products_chart = get_visualization(
            top_selling_products_by_revenue(data),
            title="Top Products by Revenue",
            kind="bar",
            xlabel="Product",
            ylabel="Revenue",
            color="#2ca02c",
        )
        st.pyplot(top_products_chart)

    with right:
        st.subheader("Monthly Sales Trend")
        monthly_chart = get_visualization(
            monthly_sales_trend(data),
            title="Monthly Sales Trend",
            kind="line",
            xlabel="Month",
            ylabel="Revenue",
            marker="o",
            color="#d62728",
        )
        st.pyplot(monthly_chart)

        st.subheader("Most Sold Products")
        quantity_chart = get_visualization(
            most_sold_products_by_qty(data),
            title="Most Sold Products by Quantity",
            kind="bar",
            xlabel="Product",
            ylabel="Quantity",
            color="#ff7f0e",
        )
        st.pyplot(quantity_chart)

    tab1, tab2, tab3 = st.tabs(["Customer Type", "Payment Method", "Raw Data"])

    with tab1:
        customer_chart = get_visualization(
            revenue_by_customer_type(data),
            title="Revenue by Customer Type",
            kind="bar",
            xlabel="Customer Type",
            ylabel="Revenue",
            color="#9467bd",
        )
        st.pyplot(customer_chart)

    with tab2:
        payment_chart = get_visualization(
            revenue_by_payment_method(data),
            title="Revenue by Payment Method",
            kind="bar",
            xlabel="Payment Method",
            ylabel="Revenue",
            color="#8c564b",
        )
        st.pyplot(payment_chart)

    with tab3:
        st.dataframe(data, use_container_width=True)


if __name__ == "__main__":
    main()
