# Setup & Environment

## Documentation

The documentation is built with **MkDocs**. To serve locally:

```bash
mkdocs serve
```

Then open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

To build static HTML:

```bash
mkdocs build
```

Use the environment mkdocs.yml

---

## Python Environments

> It is recommended to set up a **separate environment for each task**, as dependencies change quickly.

### General plotting (Python 3.12+)

Most scripts work with the latest Python version. Install the main dependencies:

```bash
pip install numpy pandas matplotlib cmcrameri
```
### Horizontal Plots

Use snow.yml

### Timeseries Plots

Use snow310.yml
 
### Box plots (Python 3.10 required)

As of **March 2026**, `seaborn` is better installed in a **Python 3.10** environment due to unresolved dependency conflicts with newer versions:

```bash
conda create -n snow-boxplot python=3.10
conda activate snow-boxplot
pip install seaborn pandas matplotlib
```

---

## Scientific Colour Maps

We use the perceptually uniform colour maps from [Fabio Crameri](https://www.fabiocrameri.ch/colourmaps/):

```bash
pip install cmcrameri
```

### References

- Crameri, F. (2018). Scientific colour-maps. Zenodo. [doi:10.5281/zenodo.1243862](http://doi.org/10.5281/zenodo.1243862)
- Crameri, F. (2018), Geodynamic diagnostics, scientific visualisation and StagLab 3.0, *Geosci. Model Dev.*, 11, 2541–2562, [doi:10.5194/gmd-11-2541-2018](https://doi.org/10.5194/gmd-11-2541-2018)

---

