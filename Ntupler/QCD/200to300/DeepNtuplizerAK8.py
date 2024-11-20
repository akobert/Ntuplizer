import FWCore.ParameterSet.Config as cms
from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import patJetCorrFactors
from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import updatedPatJets
# ---------------------------------------------------------

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

options.outputFile = 'output.root'
options.inputFiles = '/QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2/MINIAODSIM'
#options.inputFiles = '/store/mc/RunIIFall17MiniAODv2/RSGluonToTT_M-3000_TuneCP5_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/100000/E0AB2D2B-12B5-E811-8DBA-EC0D9A82260E.root'

options.maxEvents = -1

options.register('skipEvents', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "skip N events")
options.register('job', 0, VarParsing.multiplicity.singleton, VarParsing.varType.int, "job number")
options.register('nJobs', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, "total jobs")
options.register('inputDataset',
                 '',
                 VarParsing.multiplicity.singleton,
                 VarParsing.varType.string,
                 "Input dataset")
options.register('isTrainSample', True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "if the sample is used for training")
options.register('isQCD', True, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "if the sample is background for training")

options.setupTags(tag='%d', ifCond='nJobs > 1', tagArg='job')
options.parseArguments()

# ---------------------------------------------------------

process = cms.Process("DNNFiller")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary=cms.untracked.bool(False)
)

print ('Using output file ' + options.outputFile)

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string(options.outputFile))

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(options.maxEvents))

process.source = cms.Source('PoolSource',
    fileNames=cms.untracked.vstring(options.inputFiles),
    skipEvents=cms.untracked.uint32(options.skipEvents)
)


numberOfFiles = len(process.source.fileNames)
numberOfJobs = options.nJobs
jobNumber = options.job

process.source.fileNames = process.source.fileNames[jobNumber:numberOfFiles:numberOfJobs]
if options.nJobs > 1:
    print ("running over these files:")
    print (process.source.fileNames)

# ---------------------------------------------------------

process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')
# process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_data', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, '94X_mc2017_realistic_v17', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v16_L1v1', '')
print 'Using global tag', process.GlobalTag.globaltag

# ---------------------------------------------------------
from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection
#from RecoBTag.MXNet.pfDeepBoostedJet_cff import _pfDeepBoostedJetTagsAll as pfDeepBoostedJetTagsAll

useReclusteredJets = True
jetR = 0.8

bTagInfos = [
    'pfBoostedDoubleSVAK8TagInfos'
]

bTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfBoostedDoubleSecondaryVertexAK8BJetTags',
    'pfDeepDoubleBvLJetTags:probHbb',
    'pfDeepDoubleCvLJetTags:probHcc',
    'pfDeepDoubleCvBJetTags:probHcc',
    'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
    'pfMassIndependentDeepDoubleCvLJetTags:probHcc',
    'pfMassIndependentDeepDoubleCvBJetTags:probHcc',
]

#subjetBTagDiscriminators = [
#    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
#    'pfDeepCSVJetTags:probb',
#    'pfDeepCSVJetTags:probbb',
#]

subjetBTagDiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfDeepCSVJetTags:probb',
    'pfDeepCSVJetTags:probbb',
    'pfDeepCSVJetTags:probc',
    'pfDeepCSVJetTags:probudsg',
]

ak8btagdiscriminators = [
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfBoostedDoubleSecondaryVertexAK8BJetTags',
#    'pfDeepDoubleBvLJetTags:probHbb',
#    'pfDeepDoubleCvLJetTags:probHcc',
#    'pfDeepDoubleCvBJetTags:probHcc',
#    'pfMassIndependentDeepDoubleBvLJetTags:probHbb',
#    'pfMassIndependentDeepDoubleCvLJetTags:probHcc',
#    'pfMassIndependentDeepDoubleCvBJetTags:probHcc',
]

if useReclusteredJets:
    JETCorrLevels = ['L2Relative', 'L3Absolute']

    from DeepNTuples.Ntupler.jetToolbox_cff import jetToolbox
    jetToolbox(process, 'ak8', 'dummySeq', 'out', associateTask=False,
               PUMethod='Puppi', JETCorrPayload='AK8PFPuppi', JETCorrLevels=JETCorrLevels,
               Cut='pt > 100.0',
               miniAOD=True, runOnMC=True,
               addNsub=True, maxTau=3,
               addSoftDrop=True, addSoftDropSubjets=True, subJETCorrPayload='AK4PFPuppi', subJETCorrLevels=JETCorrLevels,
               #bTagDiscriminators=['pfCombinedInclusiveSecondaryVertexV2BJetTags'], subjetBTagDiscriminators=subjetBTagDiscriminators)
               bTagDiscriminators=ak8btagdiscriminators, subjetBTagDiscriminators=subjetBTagDiscriminators)

    updateJetCollection(
       process,
       jetSource=cms.InputTag('packedPatJetsAK8PFPuppiSoftDrop'),
       rParam=jetR,
       jetCorrections=('AK8PFPuppi', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
       #btagDiscriminators=bTagDiscriminators + pfDeepBoostedJetTagsAll,
       btagDiscriminators=ak8btagdiscriminators,
       btagInfos=bTagInfos,
       postfix='AK8WithPuppiDaughters',  # needed to tell the producers that the daughters are puppi-weighted
    )
    process.updatedPatJetsTransientCorrectedAK8WithPuppiDaughters.addTagInfos = cms.bool(True)
    process.updatedPatJetsTransientCorrectedAK8WithPuppiDaughters.addBTagInfo = cms.bool(True)

    srcJets = cms.InputTag('selectedUpdatedPatJetsAK8WithPuppiDaughters')
    hasPuppiWeightedDaughters = True
else:
    updateJetCollection(
       process,
       jetSource=cms.InputTag('slimmedJetsAK8'),
       rParam=jetR,
       jetCorrections=('AK8PFPuppi', cms.vstring(['L2Relative', 'L3Absolute']), 'None'),
       #btagDiscriminators=bTagDiscriminators + pfDeepBoostedJetTagsAll,
       btagDiscriminators=ak8btagdiscriminators,
       btagInfos=bTagInfos,
    )
    process.updatedPatJetsTransientCorrected.addTagInfos = cms.bool(True)
    process.updatedPatJetsTransientCorrected.addBTagInfo = cms.bool(True)

    srcJets = cms.InputTag('selectedUpdatedPatJets')
    hasPuppiWeightedDaughters = False
# ---------------------------------------------------------
from PhysicsTools.PatAlgos.tools.helpers import getPatAlgosToolsTask, addToProcessAndTask
patTask = getPatAlgosToolsTask(process)

# DeepNtuplizer
process.load("DeepNTuples.Ntupler.DeepNtuplizer_QCD_cfi")
process.deepntuplizer.jets = srcJets
process.deepntuplizer.useReclusteredJets = useReclusteredJets
process.deepntuplizer.hasPuppiWeightedDaughters = hasPuppiWeightedDaughters
#process.deepntuplizer.bDiscriminators = bTagDiscriminators + pfDeepBoostedJetTagsAll
process.deepntuplizer.bDiscriminators = ak8btagdiscriminators

#process.deepntuplizer.isQCDSample = '/QCD_' in options.inputDataset
process.deepntuplizer.isQCDSample = options.isQCD
process.deepntuplizer.isTrainSample = options.isTrainSample
if not options.inputDataset:
    # interactive running
    process.deepntuplizer.isTrainSample = False
#==============================================================================================================================#
process.p = cms.Path(process.deepntuplizer)
process.p.associate(patTask)
