from WMCore.Configuration import Configuration
config = Configuration()
config.section_('General')
config.General.transferLogs = False
config.General.transferOutputs = True
config.General.workArea = 'crab_projects'
config.General.requestName = 'QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8-v2'
config.section_('JobType')
config.JobType.numCores = 1
config.JobType.sendExternalFolder = False
config.JobType.pyCfgParams = ['inputDataset=/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM']
config.JobType.pluginName = 'Analysis'
config.JobType.allowUndistributedCMSSW = True
config.JobType.psetName = '../QCD/700to1000/DeepNtuplizerAK8.py'
config.JobType.maxMemoryMB = 2500
config.section_('Data')
config.Data.inputDataset = '/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
config.Data.outputDatasetTag = 'DeepNtuplesAK8-QCD_RunIISummer20UL18MiniAODv2-106X_v1-v2'
config.Data.publication = False
config.Data.unitsPerJob = 1
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.allowNonValidInputDataset = True
config.Data.outLFNDirBase = '/store/user/akobert/crab_output/UL/Ntupler/QCD/700to1000/'
config.section_('Site')
config.Site.storageSite = 'T3_US_Rutgers'
config.section_('User')
config.section_('Debug')
