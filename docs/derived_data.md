# Derived data


## Output Variables

The following variables are processed for each Prudence region and elevation level:

| Variable | Unit |
|----------|------|
| Snow water equivalent (snw / SWE) | mm |
| Snow covered area (SCA) | % of full Prudence region |
| Number of snow days | days |

## Derived products per region and height level:

- **Timeslice per grid box** (1971–2000, 2021–2050, 2070–2099)
- **Timeslice area means** (1971–2000, 2021–2050, 2070–2099)
- **Annual timeseries** averaged over region and height level
- **Annual cycle** averaged over time slice, region, and height level

---

### Input data for horizontal plots

The input data is available on Zenodo:

[https://doi.org/10.5281/zenodo.18495851](https://doi.org/10.5281/zenodo.18495851)

### Input data for plots

Pre-processed CSV files for plotting are located in the `data/` directory:

| File | Description |
|------|-------------|
| `AF30-year_timeseries_all_level_owd.csv` | Annual AF30 timeseries per level |
| `snowcover-year_timeseries_all_level_owd.csv` | Annual snow cover timeseries |
| `snowday-year_timeseries_all_level_owd.csv` | Annual snow day timeseries |
| `DIFF-sca-year_timeseries_all_level_owd.csv` | SCA change timeseries |
| `DIFF-sd-year_timeseries_all_level_owd.csv` | Snow day change timeseries |
| `DIFF-snw-year_timeseries_all_level_owd.csv` | SWE change timeseries |
| `DIFF-pr-year_timeseries_all_level_owd.csv` | Precipitation change timeseries |
| `DIFF-tas-year_timeseries_all_level_owd.csv` | Temperature change timeseries |
| `snw_tas_pr_snowday-snowcover_NA_timeslice_areamean_all_level_owd_m2.csv` | Timeslice November-Aprilarea means |
| `snw_tas_pr_snowday-snowcover_timeslice_annualcyle_all_level_owd_norm2.csv` | Annual cycle per timeslice |
