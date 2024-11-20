#!/bin/bash

cluster=$1
process=$2

# CMSSW setup etc
export SCRAM_ARCH="slc7_amd64_gcc820"
export VO_CMS_SW_DIR="/cms/base/cmssoft"
export COIN_FULL_INDIRECT_RENDERING=1

source $VO_CMS_SW_DIR/cmsset_default.sh
export HOME=/home/akobert/

cd /home/akobert/CMSSW_10_6_30_patch1/src/DeepNTuples/Ntupler/Zprime/M25/

eval `scramv1 runtime -sh`

cmsRun ntupler$2.py >& /home/akobert/CMSSW_10_6_30_patch1/src/CondorFiles/logfile_Zprime_M25_$1_$2.log
