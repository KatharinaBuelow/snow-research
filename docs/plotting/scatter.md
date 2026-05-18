# Scatter Plots

Scatter plots visualise snow indices for the season **November–April**.

All scripts are located in `plotting_py/SCATTER/`.

---

## Before You Start

Before running any scatter plot script, adjust the following settings inside the script:

1. **Input directory** – path to the `data/` folder
2. **Output directory** – where figures should be saved
3. **Variable selection** – choose which snow variable to plot

---

## Scripts Overview

### Absolute values

```bash
python make_scatter_plots_6x4_sca_absolute_values.py
```

Produces 6×4 scatter plots of **absolute values** per snow index.

---

### Change values

```bash
python make_scatter_plots_change_6x4.py
```

Produces 6×4 scatter plots of **change** (future minus reference period).

---

## Helper Modules

| File | Purpose |
|------|---------|
| `scattertable.py` | :rainbow: Colors and markers for models/scenarios |
| `design_matrix_tool.py` | :scissors: Utility to clean up the data frame |
