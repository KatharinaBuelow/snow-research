# Repository for snow-research

:snowman: The snow research is a cooperation with:

Christian Steger (ETH) 

Sven Kotlarski (Meteo Swiss)

Claas Teichmann (GERICS)

Katharina Bülow
    
This git repository holds the GERICS contribution.

## Documentation
Please consider the documentation for detailed information.

Live documentation (GitHub Pages): https://katharinabuelow.github.io/snow-research/


### Serve the documentation locally

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.


## Indice calculation has been calculated on mistral (dkrz) for "PRUDENCE REGIONS "

 - cdo has been used to calculate indices for sow water equivalent, snow cover and snowdays (annual, seasonal, NDJFMA, monthly means)
   
 - a snow day is defined as 3 cm of snow. We used snw (snow water equivalent), which most RCMs provided.
   
 - snowday:
   
   	snw >= 9.36 [kg/m²]
   
   	snd >= 0.03 [m] (snw = 0.03 m * 0.312 kg/m³)
   
 - If snw for the RCM was not provided, we used snd (snow depth) and converted it to snw by multiplying it with the density of 0.312 kg/m³.


## Create plots

Area mean input data for plotting is available for the
timeslice 1971-2000, 2021-2050, 2070-2099 and annual in:

    data/

Horizontal input data is available:
		https://doi.org/10.5281/zenodo.18495851
	
### Scripts
Scripts for plotting are stored in
	
	plotting_py/

	- TIMESERIES
	
	- ANNUAL_CYCLE
	
	- SCATTER
	
	- BOXPLOTS
  	
	- HORIZONTAL
		The horizontal plots for snow cover duration and snow water equivalent , 
		for the time slices 1971-2000, 2021-2050, 2070-2099, 
		as absolute values or difference including robustness.

## :snowflake: 

