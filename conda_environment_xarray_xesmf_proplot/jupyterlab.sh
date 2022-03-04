#!/bin/bash
# original file in $CLIMAF/bin/climaf-notebook after doing module load climaf (written by Philippe Weill)
# this file made 29/07/2020 by Mickaël Lalande (mickael.lalande@univ-grenoble-alpes.fr)

myport=$( grep $USER  /ciclad-home/jservon/Evaluation/CliMAF/climaf_installs/climaf_1.2.12/bin/cmip6.notebook.txt | awk '{print $2 }' )

SHORT_HOST="$(hostname -s)"
echo
case $SHORT_HOST in
    ciclad-ng|ciclad2|loholt*|camelot)
    echo -e  "\033[1;31mplease do not run this on login node $SHORT_HOST use:\033[m"
    echo -e  "First, submit an interactive session then load module and run notebook:" 
    echo -e  "\033[1;31mYou could cut and past the 2 command line under:\033[m"
    echo -e  "qsub -IVX -l nodes=1:ppn=4,mem=16g,vmem=16g,walltime=04:00:00"
    echo -e  "jupyter lab"
    exit 1 ;;
    ciclad*) SSH_TUNNEL="ssh -L ${myport}:${SHORT_HOST}:${myport} ${USER}@ciclad2.ipsl.jussieu.fr" ;;
    merlin*) SSH_TUNNEL="ssh -L ${myport}:${SHORT_HOST}:${myport} ${USER}@loholt2.ipsl.polytechnique.fr" ;;
esac
if netstat -at | grep -w $myport > /dev/null
then 
   echo "You already have a jupyter lab running" 
   echo "only one per user could be running" 
   lsof|grep "$myport (LISTEN)" 
   exit 1
fi
echo
echo -e "\033[1;31m FIRST STEP: Open your port \033[m"
echo "     - open a terminal on your computer (!! not on Ciclad, Loholt, Cerbere, Idefix... on your local machine)"
echo "     - and connect to the Mesocenter with this blue command: "
echo -e "\033[1;34m $SSH_TUNNEL \033[m"
echo
echo -e "\033[1;31m And keep this terminal open until the end of your jupyter session. \033[m"
echo 

#jupyter lab --no-browser --port=${myport} --ip=$SHORT_HOST 

# Already set in ~/.jupyter/jupyter_notebook_config.py
# https://stackoverflow.com/questions/42848130/why-i-cant-access-remote-jupyter-notebook-server
# c.NotebookApp.allow_origin = '*'
# c.NotebookApp.ip = '0.0.0.0'
# c.NotebookApp.port = 7227
# c.NotebookApp.open_browser = False

jupyter lab
