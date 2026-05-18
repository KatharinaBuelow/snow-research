# Repository for snow-research
# 
:snowman: The snow research is a cooperation with
Christian Steger (ETH) and Sven Kotlarski (Meteo Swiss), Claas Teichmann, Katharina Bülow
    
This git repository holds the GERICS contribution

## 1.) Documentation
Please consider the documentation for detailed information

### Serve the documentation locally

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.


### environments
it is better to set up your own envoronment for each task, because everything changes to quickly. Just in March 2026 seaborn is better to install in a python3.10 environment, otherwise  the dependencies do not work, everything else seemed fine with the latest python version.

## 2.) Indice calculation has been calculated on mistral (dkrz) for "PRUDENCE REGIONS "

 - cdo has been used to calculate indices for snw and snowdays (annual, seasonal, NDJFMA, monthly means)
 - a snow day is defined as 3 cm of snow. We used snw (snow water equivalent), which most RCMs provided.
 - snowday: snw >= 9.36 [kg/m²]; snd >= 0.03 [m] (snw = 0.03 m * 0.312 kg/m³)
 - If snw for the RCM was not provided, we used snd (snow depth) and converted it to snw by multiplying it with the density of 0.312 kg/m³.


## 3.) Making plots *plotting-py*

The data for plotting is available for the
timeslice 1971-2000, 2021-2050, 2070-2099 and annual in:

    data/

a.) ANNUAL CYCLE from September to August for the following Indices:
	* number of snow days
	* snow covered area
	* snow water equivalent

To plot all regions, time slices and scenarios, with variable y-axis, on one sheet use

		plot_annual_cycle_all_rcps_all_regions.py

Inside the code you have to select which index you like to plot.

	What means % of sca:
	The monthly values are all adjusted to months with the length of 30 days.
  * for each scenario, plotting all height levels and 4 prudence regions:
		plot_annual_cycle_all.py
  * for each region, plotting all scenarios:
		plot_annual_cycle_all_rcps_region.py
  	
b.) HORIZONTAL

The horizontal plots for snow cover duration and snow water equivalent , for the time slices 1971-2000, 2021-2050, 2070-2099, as absolute values or difference including robustness are produced with the notebook:

	hori_plot-snow.ipynb 

which uses the functions stored in 

	plotting_tools_snow.py

The input data is available:

	https://doi.org/10.5281/zenodo.18495851


	![Ensemble Mean Difference Snow Cover Duration](PLOTS/ensemble_mean_diff_snowcoverduration_all_oT_YLGrBl.png)
 
c.) SCATTER (Nov-April)

    Before starting the scripts, you need to adjust the input and output
    directory and select which variable you like to plot 

	* make_scatter_plots_6x4_sca_absolute_values.py (Scatterplots of absolute values)
	* make_scatter_plots_change_6x4.py (Scatterplots of change)
	
	:rainbow: Colors and markers are stored here:
	* scattertable.py

	This is just a function to clean up :scissors: the data frame:
	* design_matrix_tool.py

d.) BOXPLOTS:
	* uses the same input-data-file as SCATTER
	Plotting uses seaborn, which is better to install in a python3.10 environment; otherwise, some dependencies do not work at the moment (March 2026).

	Plotting routines are in plotting-py/BOXPLOT:
	
	Plots of a snow index (sca, sd, swe) on each height level, for each region and time_slice. Different experiments are compared in one plot
		
		snow_cover_change_hl_box+stripplot_compare_exp.py
	
	To compare different timeslices, plots for each region, height level, time slice, use:
	
		snow_cover_change_hl_box+stripplot.py
	
	Functions are stored here:

		snow_plotting_tools.py
	
	The directory also contains an example notebook:

		snowcover_change_hl_compare_exp_box+stripplot.ipynb
	
e.) Timeseries for annual mean 30-year running mean change:
	* plot_timeseries_all_rcps_region.py (full region)
	* plot_timeseries_all_rcps_region_levels.py (each level)

	(The bandwidth is 'pi'=95)

f.) Timeseries for annual mean AF30 (area of at least 30-days of snow cover area):
	* plot_timeseries_AF30_all_rcps_region.py
	* Absolute Values

	Unit: % of covered area for each region SC, EA, AL, IP, EU

	(The bandwidth is 'pi'=50, Interquartile range)

## :snowflake: Ideas and hints and links:

We try to use the colors from https://www.fabiocrameri.ch/colourmaps/

	   pip install cmcrameri

	   test_crameri.py

Crameri, F. (2018). Scientific colour-maps. Zenodo. http://doi.org/10.5281/zenodo.1243862

Crameri, F. (2018), Geodynamic diagnostics, scientific visualisation and StagLab 3.0, Geosci. Model Dev., 11, 2541-2562, doi:10.5194/gmd-11-2541-2018.

