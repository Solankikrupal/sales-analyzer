# Sales Analyzer Dashboard

This project is a Streamlit-based sales dashboard that loads sales data, cleans it, analyzes it, and displays interactive charts and KPIs in a browser UI.

The codebase is organized into separate layers so each file has one job:

- `analysis.py` handles data loading, cleaning, column normalization, filtering, KPI calculation, and chart-ready aggregations.
- `visualization.py` converts analysis results into matplotlib figures.
- `app.py` builds the Streamlit dashboard, file upload flow, filters, preview table, KPI cards, and chart layout.
- `app_draft.py` keeps the earlier draft version separate for reference.

## What This Project Does

The dashboard is designed for sales datasets. It lets you:

- Upload a CSV or Excel sales file from the UI
- Preview the uploaded dataset
- Automatically clean common issues like unnamed columns
- Normalize common column names into a standard format
- Derive some missing values when possible
- Show KPI summary cards
- Filter by date and region
- Display charts for revenue and product performance
- Gracefully handle incomplete files without crashing

In simple terms, the app tries to answer:

- How much revenue did we generate?
- How many orders do we have?
- What is the average order value?
- Which regions perform best?
- Which products generate the most revenue?
- Which products sell the most quantity?
- How does revenue change over time?
- How does revenue vary by customer type or payment method?

## What KPI Means

KPI stands for `Key Performance Indicator`.

A KPI is a top-level business number used to quickly understand performance.

In this dashboard, the main KPIs are:

- `Total Revenue`: Sum of the `Revenue (Gross)` column
- `Total Orders`: Count of the `OrderID` column
- `Average Order Value`: Average of the `TotalPrice` column

These numbers appear at the top of the dashboard so a user can understand the current state of the filtered dataset immediately.

## Project Flow

The application follows this flow:

1. Load the default Excel file or an uploaded file.
2. Clean the data.
3. Standardize column names.
4. Convert date columns to datetime when present.
5. Derive missing revenue-related fields when possible.
6. Apply sidebar filters such as date range and region.
7. Calculate KPIs on the filtered data.
8. Generate chart-ready pandas `Series`.
9. Convert those results into matplotlib figures.
10. Render everything in Streamlit.

## File Structure

```text
sales-analyzer/
├── app.py
├── analysis.py
├── visualization.py
├── app_draft.py
├── Product-Sales-Region.xlsx
├── Updated-Product-Sales-Region.xlsx
└── README.md
```

## What Each File Does

### `app.py`

This is the main dashboard application.

Responsibilities:

- Configures the Streamlit page
- Shows the file upload widget
- Loads the default file when no upload is provided
- Shows a dataset preview
- Shows missing-column warnings
- Renders date and region filters
- Displays KPI metric cards
- Displays charts in a dashboard layout
- Displays filtered raw data in a tab

Important functions:

- `get_default_data()`
  Loads the default Excel dataset with caching.
- `get_uploaded_data(file_bytes, file_name)`
  Loads uploaded file data with caching.
- `format_metric(value, money=False)`
  Formats KPI values for display.
- `render_chart(...)`
  Safely renders a chart only when the required analysis result exists.
- `main()`
  Orchestrates the full dashboard.

### `analysis.py`

This file contains the data logic.

Responsibilities:

- Load CSV or Excel files
- Clean incoming data
- Rename alternative column names to standard names
- Convert date columns
- Derive missing revenue fields when possible
- Apply filters
- Compute KPIs
- Compute grouped results for charts

Important functions:

- `normalize_column_name(name)`
  Removes spaces and special characters and lowercases the name so similar columns can be matched.
- `standardize_columns(data)`
  Renames columns like `sales`, `grossrevenue`, or `qty` into the app's standard column names.
- `clean_sales_data(data)`
  Cleans the dataset and derives missing fields.
- `load_sales_data(path)`
  Loads the local Excel file.
- `load_uploaded_file(file, file_name)`
  Loads CSV or Excel uploads.
- `missing_columns(data, required)`
  Returns a list of missing columns.
- `filter_data(data, start_date, end_date, region)`
  Applies dashboard filters.
- `dashboard_metrics(data)`
  Returns the KPI values.
- Chart helper functions like:
  `revenue_by_region`, `top_selling_products_by_revenue`, `most_sold_products_by_qty`, `monthly_sales_trend`, `revenue_by_customer_type`, `revenue_by_payment_method`

### `visualization.py`

This file handles chart creation.

Responsibilities:

- Accept chart-ready data from `analysis.py`
- Build matplotlib figures
- Return figures to Streamlit for rendering

Important functions:

- `create_chart(...)`
  Creates a figure and plots either a pandas `Series`, a `DataFrame`, or generic data.
- `get_visualization(...)`
  Thin wrapper around `create_chart(...)`.

### `app_draft.py`

This file contains the earlier draft version of the application. It is kept separate so the cleaner modular structure in `app.py` stays focused and easier to maintain.

## Supported Input Files

The dashboard currently supports:

- `.csv`
- `.xlsx`
- `.xls`

If a file is not one of these formats, the loader raises an error.

## Expected Sales Columns

The app works best when a dataset includes columns like:

- `Revenue (Gross)`
- `OrderID`
- `OrderDate`
- `Region`
- `Product`
- `Quantity`
- `UnitPrice`
- `TotalPrice`
- `CustomerType`
- `PaymentMethod`

Not every uploaded file needs all of them. The dashboard is built to still work partially if some are missing.

## How Column Normalization Works

Different files often use different column names. For example:

- `sales`
- `revenue`
- `grossrevenue`
- `qty`
- `productname`
- `ordernumber`

The app normalizes common variations into standard internal names.

Examples:

- `sales` -> `Revenue (Gross)`
- `revenue` -> `Revenue (Gross)`
- `qty` -> `Quantity`
- `productname` -> `Product`
- `ordernumber` -> `OrderID`

This makes the dashboard more flexible when different users upload files with different naming styles.

## How Missing Data Is Handled

This project is built to avoid crashing when an uploaded file is incomplete.

### Case 1: Revenue column is missing

The code tries to derive `Revenue (Gross)`:

- If `Quantity` and `UnitPrice` exist:
  `Revenue (Gross) = Quantity * UnitPrice`
- Else if `TotalPrice` exists:
  `Revenue (Gross) = TotalPrice`

### Case 2: Total price column is missing

If `Revenue (Gross)` exists, the app sets:

- `TotalPrice = Revenue (Gross)`

### Case 3: A chart needs columns that do not exist

The chart does not render. Instead, the dashboard shows a helpful message saying the chart cannot be shown because required columns are missing.

### Case 4: KPI needs columns that do not exist

That KPI becomes `N/A` instead of failing.

### Case 5: Date filter cannot be applied

If neither `OrderDate` nor `Date` exists, no date filter is shown.

### Case 6: Region filter cannot be applied

If `Region` is missing, the region filter is skipped.

## Filters

The dashboard includes sidebar filters.

### Date Filter

The app checks for:

- `OrderDate`
- or `Date`

If either exists and contains valid values, it shows:

- `Start date`
- `End date`

These filters limit the data used for KPIs and charts.

### Region Filter

If the file contains a `Region` column, the app shows a region dropdown:

- `All`
- one entry for each detected region

Selecting a region updates all KPIs and charts.

## Charts Shown in the Dashboard

The dashboard currently includes:

- `Revenue by Region`
- `Top Products by Revenue`
- `Monthly Sales Trend`
- `Most Sold Products`
- `Revenue by Customer Type`
- `Revenue by Payment Method`

There is also a raw data tab that shows the filtered dataset table.

## How the Analysis Performs

This section explains how the code performs its work technically.

### 1. Data Loading

The app either:

- loads `Updated-Product-Sales-Region.xlsx`
- or reads a user-uploaded CSV/Excel file

### 2. Cleaning

The cleaning step:

- removes columns starting with `Unnamed`
- standardizes known alternative column names
- converts date-like columns into datetime
- derives `Revenue (Gross)` or `TotalPrice` when possible

### 3. Filtering

The filtered dataset is created after upload and cleanup.

All KPIs and charts are based on the filtered dataset, not the raw full dataset. That means the dashboard is interactive and consistent.

### 4. KPI Calculation

The KPI functions are lightweight aggregations:

- `sum()`
- `count()`
- `mean()`

These are efficient pandas operations for small-to-medium datasets.

### 5. Chart Aggregation

The chart functions use pandas `groupby()` and `sort_values()` to aggregate the data into chart-ready structures.

Examples:

- Revenue by region:
  `groupby("Region")["Revenue (Gross)"].sum()`
- Top products by revenue:
  `groupby("Product")["Revenue (Gross)"].sum().sort_values(...)`
- Monthly trend:
  group by month extracted from the date column

### 6. Visualization

The visualization layer receives already-aggregated data, so `visualization.py` stays simple and focused only on plotting.

## Performance Notes

For the current project size, performance should be good because:

- pandas aggregation is efficient for typical dashboard-sized datasets
- Streamlit caching avoids reloading and reparsing files unnecessarily
- chart rendering only happens on filtered data

The app uses `@st.cache_data` for:

- default dataset loading
- uploaded file loading

This reduces repeated work when users interact with filters.

### Current Performance Strengths

- Clean separation of UI and analysis
- Cached data loading
- Fast pandas aggregations
- Graceful handling of missing columns
- Easy to extend with new KPIs and charts

### Current Performance Limitations

- matplotlib is not the most interactive plotting library for large dashboard experiences
- very large files may still feel slow because the full file is loaded into memory
- schema detection is based on a fixed mapping and may miss unusual column names
- there is not yet a user-facing column-mapping tool for unmatched schemas

## How to Run the Project

### 1. Install dependencies

```bash
python3 -m pip install --user streamlit pandas matplotlib openpyxl
```

### 2. Start the dashboard

```bash
python3 -m streamlit run app.py
```

### 3. Open the local Streamlit URL

Streamlit will print a local URL in the terminal, usually something like:

```text
http://localhost:8501
```

Open that URL in your browser.

## How to Use the Dashboard

1. Start the Streamlit app.
2. Open the dashboard in the browser.
3. Upload a CSV or Excel file from the sidebar, or use the default file.
4. Review the dataset preview.
5. Check the warning message if columns are missing.
6. Use the date and region filters.
7. Review the KPI cards.
8. Explore the charts.
9. Inspect the filtered raw data in the `Raw Data` tab.

## Example Scenarios

### Scenario 1: A clean sales file

If the file includes standard columns like `Revenue (Gross)`, `OrderID`, `OrderDate`, `Region`, and `Product`, the full dashboard works.

### Scenario 2: Revenue missing but quantity and unit price exist

The app computes:

- `Revenue (Gross) = Quantity * UnitPrice`

Then the revenue KPIs and charts still work.

### Scenario 3: Some business columns are missing

Example:

- no `CustomerType`
- no `PaymentMethod`

Result:

- Customer Type chart will show unavailable message
- Payment Method chart will show unavailable message
- Other KPIs and charts can still work

### Scenario 4: Different naming style

Example columns:

- `sales`
- `qty`
- `productname`
- `ordernumber`

The app tries to rename these to its standard schema automatically.

## Why This Structure Is Good

This project structure is strong because it separates concerns:

- UI logic stays in `app.py`
- business/data logic stays in `analysis.py`
- plotting stays in `visualization.py`

Benefits:

- easier to debug
- easier to extend
- easier to test
- easier to swap chart libraries later
- easier to support more upload formats

## Suggested Future Improvements

Good next upgrades would be:

- manual column-mapping UI for unknown schemas
- downloadable filtered CSV
- more KPIs such as return rate, discount impact, and top salesperson
- interactive chart library like Plotly
- validation panel showing data quality issues
- automated tests for cleaning and aggregation functions
- multi-file upload and comparison view

## Summary

This codebase is a modular sales dashboard that:

- accepts uploaded sales files
- cleans and standardizes them
- computes KPIs
- filters data by date and region
- shows useful charts
- handles missing columns safely

It is already structured well for further dashboard growth, especially because the analysis, visualization, and UI layers are separated cleanly.
