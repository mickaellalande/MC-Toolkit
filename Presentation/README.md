

# Presentation
The goal of this repository is to give support materials for the meetings at IGE about tools: MC-Toolkit (MC stand for Mardi-Café, Modelisation&Climate,... who knows?), in additions of a Slack channel. 

- Tuesday 07/04: [Presentation](https://github.com/mickaellalande/MC-Toolkit/tree/master/Presentation)
	-  [MC-Toolkit meetings presentation.pdf](https://github.com/mickaellalande/MC-Toolkit/blob/master/Presentation/MC-Toolkit%20meetings%20presentation.pdf)
	- [CLIMAF_example.ipynb](https://github.com/mickaellalande/MC-Toolkit/blob/master/Presentation/CLIMAF_example.ipynb) (this is only a teaser next meeting will be on CLIMAF)
	- [xarray_example.ipynb](https://github.com/mickaellalande/MC-Toolkit/blob/master/Presentation/xarray_example.ipynb) (this is only a teaser a next meeting will be dedicated to xarray, if you still want to run this example see bellow)


## Recommended installation for xarray example

0. **Main packages descriptions**:
- [xarray](http://xarray.pydata.org/en/stable/): to open netCDF files and do way more....
- [dask](https://dask.org/): for parallelization
- [jupyter](https://jupyter.org/): for using jupyter-notebook
- [matplotlib](https://matplotlib.org/): backend for making plots
- [cartopy](https://scitools.org.uk/cartopy/docs/latest/): replace `basemap`, backend for map projections
- [proplot](https://proplot.readthedocs.io/en/latest/): new plot package that I find really promissing (try to have lastest version because it is evolving fast)
- [xesmf](https://xesmf.readthedocs.io/en/latest/): for regridding


2.  **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)**:
(if you don't already have an installation of Anaconda/Miniconda -> Miniconda is lighter and allows to only install the packages that you need)

If you are on a cluster, try to install it on a different path than the default one (usually it takes some spaces and it is not recommander to have it in your *home*), otherwise make the default installation and put `yes` anytime it ask something.
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
sh Miniconda3-latest-Linux-x86_64.sh 
source ~/.bashrc  
```
You should have a `(base)` in front of your line in your terminal, that correspond to the **root** environment.
  
2.  **Add [conda-forge](https://conda-forge.org/docs/user/introduction.html)** and **update** your installation (optionnal but I recommend):  
```bash
conda config --add channels conda-forge  
conda config --set channel_priority strict  
conda update -n base -c defaults conda  
```
  3. **Create an xarray environment**:

It is recommanded not to use the **root** (base) environment so that you keep a clean installation (see the [note](https://conda-forge.org/docs/user/introduction.html) at the end of the page). If you already have an Anaconda/Miniconda it doesn't mater and just make a new environment for the examples of this repository.

Download the `spec-file.txt` and use this command to create a new *xarray* environment (you put any other name if you want):
```bash
conda create -n xarray --file spec-file.txt
conda activate xarray
```
You can finish here. Then launch Jupyter-Notebook in a terminal with: `jupyter-notebook`


3. **(bis) If you wish to make a manual installation** with updated packages (without the spec-file.txt):

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
If it doesn't work I advice you to install with the spec-file.txt (3. above) or give up for this package (it is for regridding). You can use CDO or another tool for regridding.
  
Then install other packages (xarray, pandas, numpy already isntalled from previous packages): 
```bash 
conda install jupyter psutil netcdf4 proplot cartopy matplotlib 
```
## **Usefull commands** for Anaconda/Miniconda:
* Save environment ([https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)): 
```bash 
conda list --explicit > spec-file.txt  
conda create --name myenv --file spec-file.txt  
```

* Remove environment ([https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#removing-an-environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#removing-an-environment)):  
```bash 
conda remove --name myenv --all  
conda info --envs 
```

* Update environment:
```bash
conda update -n base -c defaults conda
conda update --all
```
