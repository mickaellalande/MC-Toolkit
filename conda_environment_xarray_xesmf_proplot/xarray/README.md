

# Xarray examples

Mickaël Lalande (mickael.lalande@univ-grenoble-alpes.fr) - last update 18/06/2020

## Main packages descriptions

All these packages are not necessary, it is an example, knowing that there are many different ways to plot, regrid, etc.

- [xarray](http://xarray.pydata.org/en/stable/): to open netCDF files and do way more....
- [dask](https://dask.org/): for parallelization
- [jupyter](https://jupyter.org/): for using jupyter-notebook
- [matplotlib](https://matplotlib.org/): back-end for making plots
- [cartopy](https://scitools.org.uk/cartopy/docs/latest/): replace `basemap`, back-end for map projections
- [proplot](https://proplot.readthedocs.io/en/latest/): new plot package that I find really promising (try to have latest version because it is evolving fast)
- [xesmf](https://xesmf.readthedocs.io/en/latest/): for regridding (not easy to install sometimes)

## Install environment (with the spec-file.txt)

It is recommended not to use the **root** (base) environment so that you keep a clean installation (see the [note](https://conda-forge.org/docs/user/introduction.html) at the end of the page). If you already have an Anaconda/Miniconda it doesn't mater and just make a new environment for the examples of this repository.

Download the `spec-file.txt` and use this command to create a new *xarray* environment (you put any other name if you want):
```bash
conda create -n xarray --file spec-file.txt
conda activate xarray
```



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
