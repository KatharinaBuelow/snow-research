# Box Plots

Box plots show the distribution of snow index changes across models for different regions, height levels, and time slices.

All scripts are located in `plotting_py/BOXPLOT/`.

---

## Input Data

Box plots use the **same input data file as the Scatter plots** (see `data/`).


## Scripts Overview

### Compare experiments for a single snow index

Plots a snow index (SCA, snow days, SWE) on each height level, for each region and time slice. Different **experiments** are compared in one plot:

```bash
python snow_cover_change_hl_box+stripplot_compare_exp.py
```

---

### Compare time slices

Plots for each combination of region, height level, and time slice to compare different **time slices**:

```bash
python snow_cover_change_hl_box+stripplot.py
```

---

## Helper Module

```
snow_plotting_tools.py
```

Contains shared plotting functions used by both scripts above.

---
