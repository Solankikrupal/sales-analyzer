# Big-Company Interview Questionnaire (Based on This Repo)

This questionnaire is tailored to the `sales-analyzer` project (Python + pandas + Streamlit + matplotlib). It is designed for interviews at large product and tech companies.

---

## 1) Project Understanding & Architecture

### Q1. Explain the architecture of this repository.
**Answer:**
The repo follows a clear 3-layer structure:
1. **Data/logic layer (`analysis.py`)** for loading, cleaning, standardizing columns, filtering, KPIs, and aggregations.
2. **Visualization layer (`visualization.py`)** for converting aggregated data into matplotlib figures.
3. **UI layer (`app.py`)** for Streamlit controls, file upload, filters, KPI cards, and chart rendering.

This separation keeps business logic independent from UI concerns and improves maintainability.

### Q2. Why is this separation useful in big-company codebases?
**Answer:**
It supports team scalability. Data engineers can change data logic without touching UI; frontend/dashboard developers can evolve UX without rewriting analytics logic. It also improves testability and reduces regression risk.

### Q3. If this app had to support 100x more users, what would you change first?
**Answer:**
- Replace in-memory single-process Streamlit-only flow with a service layer/API.
- Move heavy aggregations to precomputed tables or warehouse queries.
- Add caching at multiple layers (query, aggregation, chart payload).
- Add observability (latency/error dashboards).
- Introduce authentication and row-level access control.

### Q4. What are the trade-offs of using Streamlit here?
**Answer:**
**Pros:** fast delivery, low boilerplate, easy data app iteration.  
**Cons:** limited fine-grained frontend control, scaling complexity for large concurrent usage, and less standard frontend architecture than React-based stacks.

---

## 2) Data Engineering & Data Quality

### Q5. How does this project handle inconsistent input schemas?
**Answer:**
It normalizes column names by removing non-alphanumeric characters and lowercasing, then maps variants to canonical names via `CANONICAL_COLUMNS` (example: `sales`, `revenue`, `grossrevenue` → `Revenue (Gross)`).

### Q6. Why is column standardization important?
**Answer:**
In enterprise environments, data comes from multiple teams/tools with naming inconsistencies. Standardization prevents brittle downstream logic and makes dashboards resilient to schema variations.

### Q7. Describe how missing values are handled.
**Answer:**
The cleanup flow derives `Revenue (Gross)` from `Quantity * UnitPrice` when missing, or from `TotalPrice` if available. It also derives `TotalPrice` from `Revenue (Gross)` when needed. Missing required fields trigger graceful UI warnings rather than crashes.

### Q8. What data-quality checks would you add for production?
**Answer:**
- Null-rate thresholds by critical columns.
- Duplicate `OrderID` detection rules.
- Negative revenue/quantity validation.
- Date sanity checks (future date, out-of-range date).
- Drift monitoring for category values (`Region`, `PaymentMethod`).

### Q9. What’s a potential bug risk in dynamic schema mapping?
**Answer:**
Ambiguous mappings can silently map unintended columns if names are too generic. Mitigation: confidence scoring, explicit audit logs of renamed columns, and optionally requiring user confirmation for ambiguous fields.

---

## 3) Pandas, Performance, and Correctness

### Q10. Why use vectorized operations for KPI derivation?
**Answer:**
Vectorized pandas operations are much faster and cleaner than Python loops for large datasets. They leverage optimized C-level internals and reduce code complexity.

### Q11. How is time-series aggregation implemented?
**Answer:**
The app converts date columns to datetime and groups revenue by monthly period using `.dt.to_period("M")`, then sums and converts the index to string for chart labels.

### Q12. What are performance bottlenecks you expect with larger files?
**Answer:**
- File parsing (`read_csv`/`read_excel`).
- Repeated groupby operations across reruns.
- Full-data DataFrame copies during filtering.
- Matplotlib rendering overhead for high-cardinality plots.

### Q13. How would you optimize this app for million-row datasets?
**Answer:**
- Switch to Parquet + predicate pushdown.
- Offload aggregations to SQL engine/data warehouse.
- Cache pre-aggregates by filter grain.
- Sample raw preview tables.
- Use faster plotting backends or chart payload APIs instead of full matplotlib each rerun.

### Q14. Why are date conversions done with `errors="coerce"`?
**Answer:**
It prevents hard failures from bad date strings by turning invalid parses into `NaT`, enabling robust pipelines where partial data quality issues are expected.

---

## 4) Backend/API/System Design Extension Questions

### Q15. If you had to expose this as an API, what endpoints would you design?
**Answer:**
- `POST /datasets` (upload and validate dataset)
- `GET /datasets/{id}/schema` (canonical + detected schema)
- `GET /datasets/{id}/kpis?start=&end=&region=`
- `GET /datasets/{id}/charts/revenue-by-region?...`
- `GET /datasets/{id}/export?...`

### Q16. How would you ensure data isolation for enterprise customers?
**Answer:**
Use tenant-aware storage keys, token-based auth, row-level authorization policies, encrypted storage, audit logs, and strict separation in cache keys.

### Q17. How would you version data contracts?
**Answer:**
Define schema versions and transformation contracts. Support backward compatibility through a normalization layer and deprecate old contracts with observability-driven migration windows.

---

## 5) Testing & Reliability

### Q18. What tests are most important for this codebase?
**Answer:**
- Unit tests for normalization and canonical mapping.
- Tests for KPI calculations with edge datasets.
- Tests for filter boundaries (date/region).
- Regression tests for known malformed input files.
- Smoke test for Streamlit app startup.

### Q19. Give one edge-case test for `filter_data`.
**Answer:**
Test where dataset has no `OrderDate` but has `Date`, and ensure the date filter still works. Also test where both are absent and function returns unfiltered data without crashing.

### Q20. How would you improve observability?
**Answer:**
Add structured logging for upload metadata, schema mapping results, missing-column warnings, aggregation timing, and user-selected filters. Track metrics like p95 chart generation time and error rates by file type.

---

## 6) Security, Governance, and Compliance

### Q21. What security risks exist in file-upload analytics apps?
**Answer:**
- Malicious or oversized file uploads.
- PII leakage in previews/logs.
- Unauthorized dataset access.
- Formula injection risks if exporting to spreadsheet formats.

Mitigations include file-size/type limits, content scanning, redaction policies, auth controls, and secure audit trails.

### Q22. How would you handle PII in this dashboard?
**Answer:**
Classify fields, mask or hash sensitive columns, restrict access by role, avoid logging raw PII, and provide governance tags for every dataset/column.

---

## 7) Behavioral + Ownership (Frequently Asked by Big Companies)

### Q23. Tell me about a time you improved data quality in a messy pipeline.
**Answer (template):**
Use STAR:
- **Situation:** inconsistent column naming and broken dashboards.
- **Task:** reduce failures and improve trust in KPIs.
- **Action:** built canonical schema mapping, added validation checks, created fallback derivations.
- **Result:** reduced dashboard breakage and improved analysis turnaround.

### Q24. Describe a trade-off you made between speed and correctness.
**Answer (template):**
Explain how you first shipped a minimal robust path (e.g., essential KPIs + warnings) and then iterated with stricter validation and performance improvements while monitoring user impact.

### Q25. How do you influence cross-functional teams?
**Answer (template):**
Align on metric definitions early, document schema contracts, expose data-quality dashboards, and run regular syncs with product, analytics, and engineering.

---

## 8) Hands-on Coding Questions + Model Answers

### Q26. Write a function to return top N products by revenue safely when columns may be missing.
**Answer:**
```python
import pandas as pd

def safe_top_products_by_revenue(df: pd.DataFrame, n: int = 5):
    required = {"Product", "Revenue (Gross)"}
    if not required.issubset(df.columns):
        return None
    return (
        df.groupby("Product")["Revenue (Gross)"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
    )
```

### Q27. Add robust numeric conversion for revenue columns.
**Answer:**
```python
for col in ["Quantity", "UnitPrice", "TotalPrice", "Revenue (Gross)"]:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors="coerce")
```
This avoids string/object issues before aggregation.

### Q28. How would you prevent divide-by-zero when adding margin % KPI?
**Answer:**
```python
margin_pct = None
if revenue and revenue != 0:
    margin_pct = profit / revenue
```
Or use vectorized `where` conditions in pandas for row-level computations.

---

## 9) Advanced Discussion Prompts

### Q29. How do you define a “single source of truth” for KPIs?
**Answer:**
Maintain shared metric definitions in code + documentation, version them, and compute KPIs in one trusted layer reused by dashboards and APIs.

### Q30. If leadership questions KPI accuracy, how do you respond?
**Answer:**
Provide metric lineage: raw columns → transformations → filters → aggregation logic. Reproduce numbers on a frozen sample, compare with source systems, and highlight any known caveats transparently.

---

## Quick Interviewer Use Guide

- Start with **Q1–Q4** for architecture clarity.
- Use **Q5–Q14** for data and pandas depth.
- Use **Q15–Q22** for senior/system-level ownership.
- Use **Q23–Q25** for behavioral signals.
- Use **Q26–Q30** for practical coding + leadership depth.

If you want, this can be converted into:
1. **Fresher version** (easy),
2. **SDE-2/Data Engineer version** (medium),
3. **Staff/Principal analytics platform version** (hard).
