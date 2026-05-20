# Timeseries Plots

Timeseries plots are located in `plotting_py/TIMESERIES/`.

Use the environment snow310.yml

---

## 30-Year Running Mean Change

These plots show the **annual mean 30-year running mean change** relative to the reference period 1971–2000.

The bandwidth used is **`pi` = 50** (interquartile range).

| Script | Description |
|--------|-------------|
| `plot_timeseries_all_rcps_region_absolut.py` | Absolute values, full region |

---

## AF30 Timeseries (Area with ≥ 30 Snow Days)

These plots show the **annual mean AF30** index (area fraction with at least 30 snow days per year) as **absolute values**.

The bandwidth used is **`pi` = 50** (interquartile range).

Unit: **% of covered area** for each region (SC, EA, AL, IP, EU).

| Script | Description |
|--------|-------------|
| `plot_timeseries_AF30_all_rcps_region.py` | AF30 per Prudence region |
