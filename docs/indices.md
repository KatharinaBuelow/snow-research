## Calculation

Indices were calculated on **mistral (DKRZ)** using **CDO** (Climate Data Operators, Schulzweida, 2019).

### Required fixed fields

The following fixed fields are needed before running the area mean calculation:

- **areacella** – grid cell area
- **Land-sea mask** (common LSM: at least **50% land cover** in all models)
- **Orography**
- **Mask of accumulated snow**

### Snow indices computed

The following temporal aggregations were calculated for **snw** (snow water equivalent) and **snow days**:

- Annual means
- Seasonal means
- NDJFMA (November–April) means
- Monthly means

**Note:** The year is always defined from **September to August**.

### Snow day definition

A snow day is defined as a day with at least **3 cm of snow**:

| Variable | Threshold |
|----------|-----------|
| snw (snow water equivalent) | ≥ 9.36 kg/m² |
| snd (snow depth) | ≥ 0.03 m |

### Snow cover duration for 30 days

To provide an intuitive measure of snow cover duration, the index **SCF30D** is defined as the **fraction of a region’s area that is snow covered for at least 30 days** within a hydrological year.

### References

- Schulzweida, U. (2019): Climate Data Operators (CDO), Zenodo. https://doi.org/10.5281/zenodo.3539275