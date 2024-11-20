import FWCore.ParameterSet.Config as cms
from  PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import patJetCorrFactors
from  PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cfi import updatedPatJets
from PhysicsTools.NanoAOD.common_cff import *

from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
from PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.jetSelector_cfi import selectedPatJets
from PhysicsTools.PatAlgos.tools.jetTools import addJetCollection, updateJetCollection, switchJetCollection


# ---------------------------------------------------------

from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')

#options.outputFile = 'output.root'
#options.inputFiles = '/store/mc/RunIIFall17MiniAODv2/RSGluonToTT_M-3000_TuneCP5_13TeV-pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/100000/E0AB2D2B-12B5-E811-8DBA-EC0D9A82260E.root'

# Testing on 1 file
options.outputFile = 'output.root'
options.inputFiles = 'input.root'
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
options.register('isQCD', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, "if the sample is background for training")

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


#    from RecoBTag.ONNXRuntime.pfParticleNet_cff import pfMassDecorrelatedParticleNetJetTags
#    flav_names = ["probQCDothers", "probQCDb", "probQCDbb", "probQCDc", "probQCDcc", "probXqq", "probXbb", "probXcc"]
#    pfMassDecorrelatedParticleNetJetTagsProbs = ['pfMassDecorrelatedParticleNetJetTags:' + n for n in flav_names]
#    ak8btagdiscriminators += pfMassDecorrelatedParticleNetJetTagsProbs
    
#    process.pfParticleNetTagInfosAK8WithDeepInfo.min_jet_pt = 100

    print("DEBUG: ParticleNetMD Tagging")

    JETCorrLevels = ['L2Relative', 'L3Absolute', 'L2L3Residual']

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
   
 
#    from RecoBTag.ONNXRuntime.pfParticleNet_cff import pfMassDecorrelatedParticleNetJetTags
#    process.pfParticleNetTagInfosAK8.jet_radius = 0.8
#    process.pfParticleNetTagInfosAK8.min_jet_pt = 100
#    process.pfMassDecorrelatedParticleNetJetTagsAK8ParticleNet = pfMassDecorrelatedParticleNetJetTags.clone(
#        src = 'pfParticleNetTagInfos',
#        preprocess_json = '/home/akobert/ParticleNet/training/preprocess.json',
#        model_path = '/home/akobert/ParticleNet/training/ParticleNetMD_standard.onnx',
#        preprocess_json = 'PhysicsTools/data/ParticleNet-MD/ak8/preprocess.json',
#        model_path = 'PhysicsTools/data/ParticleNet-MD/ak8/ParticleNet-MD.onnx',
#    )

#    process.selectedPatJetsAK8PFPuppiJTBTable = cms.EDProducer("SimpleCandidateFlatTableProducer", src=cms.InputTag('selectedUpdatedPatJetsAK8WithPuppiDaughters'), name=cms.string("selectedPatJetsAK8PFPuppi"), cut=cms.string(""), doc=cms.string("Selected AK8 PUPPI Jets with ParticleNet Taggers"), singleton=cms.bool(False), extension=cms.bool(False), variables=cms.PSet(P4Vars,
#	msoftdrop = Var("groomedMass()", float, doc="Corrected soft drop mass with PUPPI", precision=10),
#	msoftdrop = Var("userFloat('ak8PFJetsPuppiSoftDropMass')", float, doc='Softdrop mass', precision=10),
#        area=Var("jetArea()", float, doc="jet catchment area, for JECs", precision=10),
#        nMuons = Var("?hasOverlaps('muons')?overlaps('muons').size():0", int, doc="number of muons in the jet"),
#        muonIdx1 = Var("?overlaps('muons').size()>0?overlaps('muons')[0].key():-1", int, doc="index of first matching muon"),
#        muonIdx2 = Var("?overlaps('muons').size()>1?overlaps('muons')[1].key():-1", int, doc="index of second matching muon"),
#        electronIdx1 = Var("?overlaps('electrons').size()>0?overlaps('electrons')[0].key():-1", int, doc="index of first matching electron"),
#        electronIdx2 = Var("?overlaps('electrons').size()>1?overlaps('electrons')[1].key():-1", int, doc="index of second matching electron"),
#         nElectrons = Var("?hasOverlaps('electrons')?overlaps('electrons').size():0", int, doc="number of electrons in the jet"),
#        jetId = Var("userInt('looseId')+userInt('tightId')*2+4*userInt('tightIdLepVeto')",int,doc="Jet ID flags bit1 is loose, bit2 is tight, bit3 is tightLepVeto"),
#        nConstituents = Var("numberOfDaughters()",int,doc="Number of particles in the jet"),
#        rawFactor = Var("1.-jecFactor('Uncorrected')",float,doc="1 - Factor to get back to raw pT",precision=6),
#        tau1 = Var("userFloat('NjettinessAK8Puppi:tau1')", float, doc="Nsubjettiness (1 axis)", precision=10),
#        tau2 = Var("userFloat('NjettinessAK8Puppi:tau2')", float, doc="Nsubjettiness (2 axis)", precision=10),
#        tau3 = Var("userFloat('NjettinessAK8Puppi:tau3')", float, doc="Nsubjettiness (3 axis)", precision=10),
#	tau4 = Var("userFloat('NjettinessAK8Puppi:tau4')", float, doc="Nsubjettiness (4 axis)", precision=10),
#        n2b1 = Var("?hasUserFloat('nb1AK8PuppiSoftDrop:ecfN2')?userFloat('nb1AK8PuppiSoftDrop:ecfN2'):-99999.", float, doc="N2 with beta=1 (for jets with raw pT>250 GeV)", precision=10),
#	n3b1 = Var("?hasUserFloat('nb1AK8PuppiSoftDrop:ecfN3')?userFloat('nb1AK8PuppiSoftDrop:ecfN3'):-99999.", float, doc="N3 with beta=1 (for jets with raw pT>250 GeV)", precision=10),
#	chHEF = Var("chargedHadronEnergyFraction()", float, doc="charged Hadron Energy Fraction", precision= 6),
#        neHEF = Var("neutralHadronEnergyFraction()", float, doc="neutral Hadron Energy Fraction", precision= 6),
#        chEmEF = Var("chargedEmEnergyFraction()", float, doc="charged Electromagnetic Energy Fraction", precision= 6),
#        neEmEF = Var("neutralEmEnergyFraction()", float, doc="neutral Electromagnetic Energy Fraction", precision= 6),
#	muEF = Var("muonEnergyFraction()", float, doc="muon Energy Fraction", precision= 6),	
#	)
#    )

#    for prob in pfMassDecorrelatedParticleNetJetTagsProbs:
#        name = 'ParticleNetMD_' + prob.split(':')[1]
#        name = name.replace('QCDothers', 'QCD')
#        setattr(process.selectedPatJetsAK8PFPuppiJTBTable.variables, name, Var("bDiscriminator('%s')" % prob, float, doc=prob, precision=-1))




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
process.load("DeepNTuples.Ntupler.DeepNtuplizer_cfi")
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
