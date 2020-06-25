# Set a conda environment and Jupyter-Notebook

Mickaël Lalande (mickael.lalande@univ-grenoble-alpes.fr) - last update 18/06/2020

This is some recommendations based on my own experience, feel free not to follow each steps and/or don't hesitate to give update to this doc to improve it!

## General installation

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
**Tip**: You can add `conda activate my_env` in your .bashrc so you don't have to activate it every time.

**Tip 2**: Use screen not to get disconnected!

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



## CICLAD specifications (with CLIMAF)

You need to get a "port" from jerome.servonnat@lsce.ipsl.fr before to use Jupyter-Notebook.

Connect to CICLAD: `ssh -XY mlalande@ciclad.ipsl.jussieu.fr` or CLIMSERV: `ssh -XY mlalande@camelot.ipsl.polytechnique.fr`

```bash
qsub -IVX -l mem=9g,vmem=9g,walltime=06:00:00
module load climaf
climaf-notebook
```

Follow the instructions



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
