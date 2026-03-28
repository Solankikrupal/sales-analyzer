from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def create_chart(
    data: pd.Series | pd.DataFrame,
    title: str = "Sales Analysis",
    kind: str = "bar",
    xlabel: str = "Category",
    ylabel: str = "Value",
    **kwargs,
):
    """Return a matplotlib figure for dashboard display."""
    fig, ax = plt.subplots(figsize=(10, 6))

    if isinstance(data, pd.Series):
        data.plot(kind=kind, ax=ax, **kwargs)
    elif isinstance(data, pd.DataFrame):
        data.plot(kind=kind, ax=ax, **kwargs)
    else:
        ax.plot(data, **kwargs)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    return fig


def get_visualization(
    sales_data: pd.Series | pd.DataFrame,
    title: str = "Sales Analysis",
    kind: str = "bar",
    xlabel: str = "Category",
    ylabel: str = "Value",
    **kwargs,
):
    return create_chart(
        sales_data,
        title=title,
        kind=kind,
        xlabel=xlabel,
        ylabel=ylabel,
        **kwargs,
    )

