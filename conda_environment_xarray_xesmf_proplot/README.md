# Set a conda environment and Jupyter-Notebook ([video](https://www.youtube.com/watch?v=Gb0smIc1VpM) 1:25 to 35:10)

Mickaël Lalande (mickael.lalande@univ-grenoble-alpes.fr) - last update 22/07/2020

This is some recommendations based on my own experience, feel free not to follow each steps and/or don't hesitate to give update to this doc to improve it!

> Great video from the SciPyConf 2020: https://www.youtube.com/watch?v=qn5zfdJtcYc&list=PLYx7XA2nY5Gde-6QO98KUJ9iL_WW4rgYf&index=5, they advise in particular to install also pip in any environment in order to have the pip installations included in your conda environment and they develop more about the way to share an environment with .yml files. Here is the tutorial associated: https://carpentries-incubator.github.io/introduction-to-conda-for-data-scientists/index.html
>

## General installation

/!\ **This installation does not work on CICLAD anymore, so refer to CICLAD section below** /!\ 

Updated version here: https://mickaellalande.github.io/post/tutorial/how-to-install-jupyter-notebook-on-a-server/ (only for general installation, for server specifications see below)

1. **Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)**:
   (if you don't already have an installation of Anaconda/Miniconda -> Miniconda is lighter and allows to only install the packages that you need)

If you are on a cluster, try to install it on a different path than the default one (usually it takes some spaces and it is not recommended to have it in your *home*), otherwise make the default installation and put `yes` anytime it ask something.
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
sh Miniconda3-latest-Linux-x86_64.sh 

# Change the path to a place where you can have some storage
GRICAD: [/home/lalandmi/miniconda3] >>> /bettik/lalandmi/miniconda3
CICLAD: [/home/lalandmi/miniconda3] >>> /data/mlalande/miniconda3
Jean-Zay: [/home/ufz23bm/miniconda3] >>> /gpfswork/rech/goe/ufz23bm/miniconda3

# This will automatically update your ~/.bashrc so that you can directly have conda in your path
Do you wish the installer to initialize Miniconda3
by running conda init? [yes|no]
[no] >>> yes

source ~/.bashrc  
```
You should have a `(base)` in front of your line in your terminal, that correspond to the **root** environment.

2.  **Add [conda-forge](https://conda-forge.org/docs/user/introduction.html)** and **update** your installation (optional but I recommend):  
```bash
conda config --add channels conda-forge  
conda config --set channel_priority strict  
conda update -n base -c defaults conda  
```
  3. **Create an environment**:

It is recommended not to use the **root** (base) environment so that you keep a clean installation (see the [note](https://conda-forge.org/docs/user/introduction.html) at the end of the page). 

```bash
conda create -n my_env jupyter # ... install any package you want
conda activate my_env
```
4. **Configure Jupyter**

The problem with launching Jupyter on a server is that you will have to make an ssh bridge between your machine and the server to open Jupyter directly on your internet browser. So you have to specify to Jupyter not to open a window on the server and to open Jupyter on a specific port (if needed).

There are two ways to do this, either you specify all this in your command when you run Jupyter, or you create a configuration file:

- **Command line**
  Here is an example of a command line (where XXXX would be your port number), but don’t run it yet, it would be for later!

```bash
jupyter lab --port XXXX --ip 0.0.0.0 --no-browser
```

- **Configuration file**

Alternatively, you can put this directly into a configuration file and just run the command jupyter lab (or jupyter notebook):

Create a configuration file and edit it

```bash
jupyter notebook --generate-config
gvim ~/.jupyter/jupyter_notebook_config.py
```

Uncomment these lines and modify them as follow

```bash
c.NotebookApp.allow_origin = '*'
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = XXXX
c.NotebookApp.open_browser = False
```



---

**Tip**: You can add `conda activate my_env` in your .bashrc so you don't have to activate it every time.

**Tip 2**: Use [screen](https://openclassrooms.com/fr/courses/43538-reprenez-le-controle-a-laide-de-linux/40849-executer-des-programmes-en-arriere-plan#/id/r-40848) not to get disconnected!

**Note**: Usually each computational center have their own way to use Jupyter-Notebook, however it usually uses some of their installation that is most of the time not convenient... That's why I personally prefer to install my own environment so that I have control on the packages I want to install etc.

**Note 2:** Once you have a environment set-up I advice you to save it (`conda list --explicit > spec-file.txt `) before to do any updates... sometimes you can break everything. Another option is to make versions of your environment, so that before an update or an install of a new package you can clone your environment (`conda create --name myenv_v1 --clone myenv_v0`) with a new version number for example (see https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html for more infos on environments). A good practice can be then to note which version of your environment you are using in your scripts so that you are sure to keep it to work even later.

## GRICAD specifications

1. Connect to GRICAD:

```bash
ssh lalandmi@access-ciment.imag.fr
ssh dahu
cd /bettik/lalandmi
```

2. Launch job:

```bash
oarsub -I -l nodes=1/core=16,walltime=3:00:00 --project data-ocean
```

3. Launch Jupyter on the desired environment

```bash
conda activate my_env
jupyter-notebook
```

4. Make a tunnel in your own terminal (on your personal machine):

```bash
ssh -fNL 8888:f-dahu:8888 lalandmi@access-ciment.imag.fr
```



**Note**: If you don't want to install your own Miniconda you can use their own installation and create your environment:

```bash
source /applis/environments/conda.sh
conda create -n my_env jupyter # ... install any package you want
conda activate my_env
cd /bettik/lalandmi
jupyter-notebook
```



See more: https://gricad-doc.univ-grenoble-alpes.fr/notebook/hpcnb/ (other method)



## CICLAD specifications

You need to get a "port" from `jerome.servonnat@lsce.ipsl.fr` before to use Jupyter-Notebook.

Connect to CICLAD: `ssh -XY mlalande@ciclad.ipsl.jussieu.fr` or CLIMSERV: `ssh -XY mlalande@camelot.ipsl.polytechnique.fr`

### Your own environment (recommanded for xarray, etc.)

Recent Anaconda/Miniconda does not work anymore on CICLAD (https://documentations.ipsl.fr/MESO_User/Python/python_version.html)

1) So I recommend to directly use their `conda` through: `module load python/3.8-anaconda`

Then you can create your own environment that will be stored in your `home` in a hidden folder `.conda` (only the environment size should not exceed 1 or 2 Go). You can use the [phd_v3.txt](phd_v3.txt) environment that contains most of the packages used in the [xarray](xarray) tutorial. This environment only works on CICLAD, for more general installation (on your personal machine or other server) you can use this file: https://github.com/mickaellalande/ERCA/blob/main/environment.yml (be aware that this environment starts to be a bit old).

2. So after loading conda you can install this environment (or create your own): `conda create --name phd_v3 --file phd_v3.txt`
3. Then you can follow the step 4 above to create the configuration file. 

For ease, you can add the following lines to your *bashrc* (`gvim ~/.bashrc`) so you don't have to write them every time:

```bash
module load python/3.8-anaconda
source activate phd_v3
```

The you need to launch a job, for example (adapt to your needs):

```bash
qsub -IVX -l nodes=1:ppn=4,mem=16g,vmem=16g,walltime=05:00:00
```

Then you should be able to launch Jupyter Lab. For ease you can also use the [jupyterlab.sh](jupyterlab.sh) script (that you can copy or create in your `home`):

```bash
sh jupyterlab.sh
```

That allows you to get the line to copy in your terminal (on your computer, not CICLAD) to make the SSH tunnel (without having to modify anything).

Then you can access CMIP6 data for example in the `/bdd/CMIP6` folder (or any other data in `/bdd`). For more information about the data, you can contact Guillaume LEVAVASSEUR <Guillaume.Levavasseur@ipsl.fr>. You can use `intake` or `CLIMAF` (bellow) to help you accessing data. But once you know the architecture, you can also just use the direct paths. 

Here is an example notebook: [CMIP6_CORDEX_CICLAD.ipynb](CMIP6_CORDEX_CICLAD.ipynb)



### With CLIMAF

No need to install any environment as it is already set. Be aware that you can't use all custom package with CLIMAF...

```bash
qsub -IVX -l mem=9g,vmem=9g,walltime=06:00:00
module load climaf
climaf-notebook
```

Follow the instructions

More information on CLIMAF: https://climaf.readthedocs.io/en/master/



## Jean-Zay specifications

```bash
ssh -XY ufz23bm@jean-zay-pp.idris.fr
salloc --partition=prepost --ntasks=1 --hint=nomultithread --time=10:00:00 -A goe@cpu srun --pty bash
conda activate my_env
idrjup --notebook-dir=$WORK
```

Then open the link in your browser: https://jean-zay-srv2.idris.fr (see * if you are not connecting directly from your computer), enter you login/pw from IDRIS, then click on "Envoyer" button from your Job. Write the "Mot de passe jupyter" in the browser. Enjoy!

\* If you connect via CICLAD for example you can make a tunel from your own terminal: `ssh -N -D 8080 mlalande@ciclad.ipsl.jussieu.fr` and then setting a proxy in Firefox for exemple (in Proxy network/réseau) settings:  "Manual configuration" -> Hôte SOCKS: 127.0.0.1, Port: 8080, SOCKS v5

More infos: http://www.idris.fr/eng/jean-zay/pre-post/jean-zay-jupyter-notebook-eng.html (other method)



## Trick Ghislain ([video](https://www.youtube.com/watch?v=Gb0smIc1VpM) 20:00)

To launch jupyter, I put everything in argument, which avoids the config of gricad. I'm obviously making an alias

```bash
jupyter lab --port 10345 --ip 0.0.0.0  --no-browser
```

and underneath the script to make the tunnel, I've got two, one for dahu and one for ipsl. The rest of the "ss" config is in .ssh/config.

```bash
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Provide the name of the node (should be merlinX-c)"
fi

PORT=10345  # chacun met un port different !!

ssh -o ServerAliveInterval=60 -o ServerAliveCountMax=3 -f -N -L  $PORT:$1:$PORT ipsl
```



## **Useful commands** for Anaconda/Miniconda

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
