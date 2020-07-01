

# Xarray examples ([video](https://www.youtube.com/watch?v=Gb0smIc1VpM) 35:10 to end)

Mickaël Lalande (mickael.lalande@univ-grenoble-alpes.fr) - last update 18/06/2020

## Notebooks
- [quick-overview.ipynb](https://github.com/mickaellalande/MC-Toolkit/blob/master/conda_environment_xarray_xesmf_proplot/xarray/quick-overview.ipynb) ([video](https://www.youtube.com/watch?v=Gb0smIc1VpM) 35:10 to 1:13:30): allows to take in hand xarray
- [advanced-analysis.ipynb](https://github.com/mickaellalande/MC-Toolkit/blob/master/conda_environment_xarray_xesmf_proplot/xarray/advanced-analysis.ipynb) ([video](https://www.youtube.com/watch?v=Gb0smIc1VpM) 1:13:30 to end): more advanced analysis using the `utils.py` file (which includes several draft functions allowing to make climatological analyses from monthly files by taking into account the weight of the days in a month)
  - Make an ensemble mean
  - Check monthly data
  - Climatology
  - Bias analyses (regrid obs with xesmf)
  - Annual cycle
  - Trends analysis (vectorized)
  - Plots with the package Proplot

## Main packages descriptions

All these packages are not necessary, it is an example, knowing that there are many different ways to plot, regrid, etc.

- [xarray](http://xarray.pydata.org/en/stable/): to open netCDF files and do way more....
- [dask](https://dask.org/): for parallelization
- [jupyter](https://jupyter.org/): for using jupyter-notebook
- [matplotlib](https://matplotlib.org/): back-end for making plots
- [cartopy](https://scitools.org.uk/cartopy/docs/latest/): replace `basemap`, back-end for map projections
- [proplot](https://proplot.readthedocs.io/en/latest/): new plot package that I find really promising (try to have latest version because it is evolving fast)
- [xesmf](https://xesmf.readthedocs.io/en/latest/): for regridding (not easy to install sometimes)

## Install environment (with the spec-file.txt)

It is recommended not to use the **root** (base) environment so that you keep a clean installation (see the [note](https://conda-forge.org/docs/user/introduction.html) at the end of the page). If you already have an Anaconda/Miniconda it doesn't mater and just make a new environment for the examples of this repository.

Download the `spec-file.txt` and use this command to create a new *xarray* environment (you put any other name if you want):
```bash
conda create -n xarray --file spec-file.txt
conda activate xarray
```

### Some issues related with this environment

- xESFM installation: https://github.com/JiaweiZhuang/xESMF/issues/47
- xESFM NaN's: https://github.com/JiaweiZhuang/xESMF/issues/15
- Proplot colormaps: https://github.com/lukelbd/proplot/issues/123
- Proplot colorbar: https://github.com/lukelbd/proplot/issues/124

------

## Manual installation (without the spec-file.txt)

Install [**xESMF**](https://xesmf.readthedocs.io/en/latest/) first with esmpy before by itself (see this [issue](https://github.com/JiaweiZhuang/xESMF/issues/47), may be not the case anymore for future versions):
```bash
conda create -n xarray  
conda activate xarray  
conda install esmpy  
conda install xesmf dask  
```
  Test the xesmf environment:  
```bash
pip install pytest  
pytest -v --pyargs xesmf  
```
If it doesn't work I advice you to install with the spec-file.txt or give up for this package (it is for regridding). You can use CDO or another tool for regridding.

Then install other packages (xarray, pandas, numpy already installed from previous packages): 
```bash 
conda install jupyter psutil netcdf4 proplot cartopy matplotlib 
```
