# git-repository for snow-research
# 
:snowman: The snow research is a cooperation with
Christain Steger (ETH) and Sven Kotlarski (Meteo Swiss), Claas Teichmann, Katharina Bülow, Ludwig Lierhammer
    
This git repository holds the GERICS contribution


## 1.) Indice calculation have been calculated on mistral

 - cdo has been used    
 - Calculats indices for snw and snowdays: Annual, seasonal, NDJFMA, monthly Means
 - Snow day is greater than : snw =  9.36 [kg/m²] ; snd 0.03 [m] (snw = 0.03 m *0.312 kg/m3)

    Calculated Number of Snowdays: This is a day with 3 cm of snow. If you do not 
have snw for the RCM you can use snd and coverted it to snw by mulipying it with the desity of 312 kg/m³
      
## 2.) Snow research

* You need some fixed field:
    * areacella
    * land see mask (common lsm (at least 50% land cover in all modells)
    * orographie 
    * mask of accumulated snow 

### Results for Prudence Regions:

* Some model accumulate snow, which leads to unrealistic values. These Gridboxes are masked out and not included in the calculation. This finaly leads to areas which have less than 5 gridboxes for some RCMS, so they will not be used for the area mean.

       See pictute: Grid_cells_per_elev_class.png

This is the reason why you do not find the same number of simulations at each region and hight level.

* Timeslice 1971-2000, 2021-2050, 2070-2099
     
* Snow water equivalent [mm], snow covered area [%] (part of full prudence region) and number of snowdays:
    - areamean for prudence region and on different height levels for timeslices
    - timeseries per year averaged over Prudence-Region and height level
    - timeseries of 30 year running mean of annual change compared to 1971-2000  averaged over Prudence-Region and height level
    - Annual cycle averaged of time slice and prudence region and height level.

 * New Index af30, area of annual snowcover with atleast 30 snowdays/year.

 * The year is always from September to August
 

## 3.) Making plots *plotting-py*

The data for plotting is available in

    data/

preview of plots:

    https://drive.google.com/drive/folders/1xDmv63OY1dKlB8qv-CmSXQOllZQ6C4lh

a.) ANNUAL CYCLE (eg. Sept.71 till August.01) for number of snowdays and snow covered area [sca]
    What means % of sca:
    The monthly values are all adjusted to month with the length of 30 days.
  * for each scenario, plotting all hight levels and 4 prudence regions
    	plot_annual_cycle_all.py
  * for each region plotting all scenarios:
        plot_annual_cycle_all_rcps_region.py
  * all regions and sceanrios, but with variable y-axis:
    	plot_annual_cycle_all_rcps_all_regions.py
	
b.) HORIZONTAL

    * Absolute values of snow cover and change incl robustness

    * Timeslice 1971-2000, 2021-2050, 2070-2099

    * here you find a nootbook and in the notebook the link to download the data


c.) SCATTER (Nov-April)

    Before starting the scripts, you need to adjust the input and output
    directory and select which variable you like to plot 

	* make_scatter_plots_6x4_sca_absolut_values.py (Scatterplots of absolut values)
	* make_scatter_plots_change_6x4.py (Scatterplots of change)
	
	:rainbow: Colors and markers are stored here:
	* scattertable.py

	This ist just a funktion to clean up :scissors: the data frame:
	* design_matrix_tool.py

d.) Stripplot+Barplots
	plotting-routines/plotting-py:
	* snow_cover_change_hl_box+stripplot_compare_exp.py
	(make plots of sca on each hight level for each region and timeslice.
	Different experiments are compared in one plot)
	* snow_cover_change_hl_box+stripplot.py
	(makes plots for sca on each hight level for each region and experiment.
	Different timeslices are compared in the plot)
	* snow_plotting_tools.py
	(this are just tools)
	
e.) timeseries for annual mean 30-year running mean change:
  	* plot_timeseries_all_rcps_region.py (full region)
	* plot_timeseries_all_rcps_region_levels.py (each level)

	(The bandwidth is 'pi'=95)

f.) timeseries for annual mean AF30 (area of at least 30-days of snow cover area ):
  	* plot_timeseries_AF30_all_rcps_region.py
	* Absolute Values

	Unit: % of covered area for each region SC, EA, AL, IP, EU

	(The bandwidth is 'pi'=50, Inter quartile range)
	     






## :snowflake: Ideas and hints and links:

We try to use the colors from https://www.fabiocrameri.ch/colourmaps/

       pip install cmcrameri

       test_crameri.py

Crameri, F. (2018). Scientific colour-maps. Zenodo. http://doi.org/10.5281/zenodo.1243862

Crameri, F. (2018), Geodynamic diagnostics, scientific visualisation and StagLab 3.0, Geosci. Model Dev., 11, 2541-2562, doi:10.5194/gmd-11-2541-2018.


I used :information_desk_person: https://www.youtube.com/c/KimberlyFessel/videos
to learn a lot about plotting.

