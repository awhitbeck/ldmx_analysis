# Don't email batch job log
export LSB_JOB_REPORT_MAIL=N

export SOFTWARE_HOME=/nfs/slac/g/ldmx/software

#################
# LDMX analysis #
#################
export PYTHONPATH=$PYTHONPATH:/nfs/slac/g/ldmx/users/whitbeck/dos_electrones/ldmx_analysis/Utils

##############
#   python   #
##############
export PATH=$SOFTWARE_HOME/Python-2.7.12/pyinstall_gcc6.3.1/bin:$PATH
export LD_LIBRARY_PATH=$SOFTWARE_HOME/Python-2.7.12/pyinstall_gcc6.3.1/lib:$LD_LIBRARY_PATH
export PYTHONHOME=$SOFTWARE_HOME/Python-2.7.12/pyinstall_gcc6.3.1

############
#   ROOT   #
############
export ROOTDIR=$SOFTWARE_HOME/root/build_gcc6.3.1_new
source $ROOTDIR/bin/thisroot.sh
