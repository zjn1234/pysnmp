from pysnmp.proto import rfc1157, rfc1902, rfc1905, rfc3411, error
from pysnmp.proto.api import v2c  # backend is always SMIv2 compliant
from pysnmp.proto.proxy import rfc2576
import pysnmp.smi.error
from pysnmp import debug

# 3.2
class CommandResponderBase:
    acmID = 3  # default MIB access control method to use
    pduTypes = ()

    def __init__(self, snmpEngine, snmpContext):
        snmpEngine.msgAndPduDsp.registerContextEngineId(
            snmpContext.contextEngineId, self.pduTypes, self.processPdu
            )
        self.snmpContext = snmpContext # for unregistration
        self.__pendingReqs = {}

    def handleMgmtOperation(
        self, snmpEngine, stateReference, contextName, PDU, (acFun, acCtx)
        ): pass
        
    def close(self, snmpEngine):
        snmpEngine.msgAndPduDsp.unregisterContextEngineId(
            self.snmpContext.contextEngineId, self.pduTypes
            )

    def sendRsp(self, snmpEngine, stateReference,
                     errorStatus, errorIndex, varBinds):
        ( messageProcessingModel,
          securityModel,
          securityName,
          securityLevel,
          contextEngineId,
          contextName,
          pduVersion,
          PDU,
          origPdu,
          maxSizeResponseScopedPDU,
          statusInformation ) = self.__pendingReqs[stateReference]

        del self.__pendingReqs[stateReference]

        debug.logger & debug.flagApp and debug.logger('sendRsp: stateReference %s, errorStatus %s, errorIndex %s, varBinds %s' % (stateReference, errorStatus, errorIndex, varBinds))
        
        v2c.apiPDU.setErrorStatus(PDU, errorStatus)
        v2c.apiPDU.setErrorIndex(PDU, errorIndex)
        v2c.apiPDU.setVarBinds(PDU, varBinds)

        # Agent-side API complies with SMIv2
        if messageProcessingModel == 0:
            PDU = rfc2576.v2ToV1(PDU, origPdu)
        
        # 3.2.6
        try:
            snmpEngine.msgAndPduDsp.returnResponsePdu(
                snmpEngine,
                messageProcessingModel,
                securityModel,
                securityName,
                securityLevel,
                contextEngineId,
                contextName,
                pduVersion,
                PDU,
                maxSizeResponseScopedPDU,
                stateReference,
                statusInformation
                )
        except error.StatusInformation, why:
            debug.logger & debug.flagApp and debug.logger('sendRsp: stateReference %s, statusInformation %s' % (stateReference, why))
            snmpSilentDrops, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMPv2-MIB', 'snmpSilentDrops')
            snmpSilentDrops.syntax = snmpSilentDrops.syntax + 1

    _getRequestType = rfc1905.GetRequestPDU.tagSet
    _getNextRequestType = rfc1905.GetNextRequestPDU.tagSet
    _setRequestType = rfc1905.SetRequestPDU.tagSet
    _counter64Type = rfc1902.Counter64.tagSet
    
    def processPdu(
        self,
        snmpEngine,
        messageProcessingModel,
        securityModel,
        securityName,
        securityLevel,
        contextEngineId,
        contextName,
        pduVersion,
        PDU,
        maxSizeResponseScopedPDU,
        stateReference
        ):

        # Agent-side API complies with SMIv2
        if messageProcessingModel == 0:
            origPdu = PDU
            PDU = rfc2576.v1ToV2(PDU)
        else:
            origPdu = None
        
        # 3.2.1
        if not rfc3411.readClassPDUs.has_key(PDU.tagSet) and \
           not rfc3411.writeClassPDUs.has_key(PDU.tagSet):
            raise error.ProtocolError('Unexpected PDU class %s' % PDU.tagSet)
        
        # 3.2.2 --> no-op

        # 3.2.4
        rspPDU = v2c.apiPDU.getResponse(PDU)
        
        statusInformation = {}
        
        self.__pendingReqs[stateReference] = (
            messageProcessingModel,
            securityModel,
            securityName,
            securityLevel,
            contextEngineId,
            contextName,
            pduVersion,
            rspPDU,
            origPdu,
            maxSizeResponseScopedPDU,
            statusInformation
            )

        acCtx = (
            snmpEngine, securityModel, securityName, securityLevel,
            contextName, PDU.getTagSet()
            )

        # 3.2.5
        varBinds = v2c.apiPDU.getVarBinds(PDU)
        errorStatus, errorIndex = 'noError', 0

        debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, varBinds %s' % (stateReference, varBinds))
        
        try:
            self.handleMgmtOperation(
                snmpEngine, stateReference,
                contextName, PDU, (self.__verifyAccess, acCtx)
                )
        # SNMPv2 SMI exceptions
        except pysnmp.smi.error.GenError, errorIndication:
            debug.logger & debug.flagApp and debug.logger('processPdu: stateReference %s, errorIndication %s' % (stateReference, errorIndication))
            if errorIndication.has_key('oid'):
                # Request REPORT generation
                statusInformation['oid'] = errorIndication['oid'] 
                statusInformation['val'] = errorIndication['val']

        # PDU-level SMI errors
        except pysnmp.smi.error.NoAccessError, errorIndication:
            errorStatus, errorIndex = 'noAccess', errorIndication['idx'] + 1
        except pysnmp.smi.error.WrongTypeError, errorIndication:
            errorStatus, errorIndex = 'wrongType', errorIndication['idx'] + 1
        except pysnmp.smi.error.WrongValueError, errorIndication:
            errorStatus, errorIndex = 'wrongValue', errorIndication['idx'] + 1
        except pysnmp.smi.error.NoCreationError, errorIndication:
            errorStatus, errorIndex = 'noCreation', errorIndication['idx'] + 1
        except pysnmp.smi.error.InconsistentValueError, errorIndication:
            errorStatus, errorIndex = 'inconsistentValue', errorIndication['idx'] + 1
        except pysnmp.smi.error.ResourceUnavailableError, errorIndication:
            errorStatus, errorIndex = 'resourceUnavailable', errorIndication['idx'] + 1
        except pysnmp.smi.error.CommitFailedError, errorIndication:
            errorStatus, errorIndex = 'commitFailedError', errorIndication['idx'] + 1
        except pysnmp.smi.error.UndoFailedError, errorIndication:
            errorStatus, errorIndex = 'undoFailedError', errorIndication['idx'] + 1
        except pysnmp.smi.error.AuthorizationError, errorIndication:
            errorStatus, errorIndex = 'authorizationError', errorIndication['idx'] + 1
        except pysnmp.smi.error.NotWritableError, errorIndication:
            errorStatus, errorIndex = 'notWritable', errorIndication['idx'] + 1
        except pysnmp.smi.error.InconsistentNameError, errorIndication:
            errorStatus, errorIndex = 'inconsistentName', errorIndication['idx'] + 1
        except pysnmp.smi.error.SmiError, errorIndication:
            errorStatus, errorIndex = 'genErr', len(varBinds) and 1 or 0
        except pysnmp.error.PySnmpError, errorIndication:
            errorStatus, errorIndex = 'genErr', len(varBinds) and 1 or 0
        else:
            return
        
        self.sendRsp(
            snmpEngine, stateReference, errorStatus, errorIndex, varBinds
            )

    def __verifyAccess(self, name, syntax, idx, viewType,
                       (snmpEngine, securityModel, securityName,
                        securityLevel, contextName, pduType)
                       ):
        try:
            snmpEngine.accessControlModel[self.acmID].isAccessAllowed(
                snmpEngine, securityModel, securityName,
                securityLevel, viewType, contextName, name
                )
        # Map ACM errors onto SMI ones
        except error.StatusInformation, statusInformation:
            debug.logger & debug.flagApp and debug.logger('__verifyAccess: name %s, statusInformation %s' % (name, statusInformation))
            errorIndication = statusInformation['errorIndication']
            # 3.2.5...
            if errorIndication == 'noSuchView' or \
               errorIndication == 'noAccessEntry' or \
               errorIndication == 'noGroupName':
                raise pysnmp.smi.error.AuthorizationError(
                    name=name, idx=idx
                    )
            elif errorIndication == 'otherError':
                raise pysnmp.smi.error.GenError(name=name, idx=idx)
            elif errorIndication == 'noSuchContext':
                snmpUnknownContexts, = snmpEngine.msgAndPduDsp.mibInstrumController.mibBuilder.importSymbols('__SNMP-TARGET-MIB', 'snmpUnknownContexts')
                snmpUnknownContexts.syntax = snmpUnknownContexts.syntax + 1
                # Request REPORT generation
                raise pysnmp.smi.error.GenError(
                    name=name, idx=idx,
                    oid=snmpUnknownContexts.name,
                    val=snmpUnknownContexts.syntax
                    )
            elif errorIndication == 'notInView':
                return 1
            else:
                raise error.ProtocolError(
                    'Unknown ACM error %s' % errorIndication
                    )
        else:
            # rfc2576: 4.1.2.1
            if securityModel == 1 and \
               syntax is not None and \
               self._counter64Type == syntax.getTagSet() and \
               self._getNextRequestType == pduType:
                # This will cause MibTree to skip this OID-value
                raise pysnmp.smi.error.NoAccessError(name=name, idx=idx)
        
class GetCommandResponder(CommandResponderBase):
    pduTypes = ( rfc1905.GetRequestPDU.tagSet, )

    # rfc1905: 4.2.1
    def handleMgmtOperation(
        self, snmpEngine, stateReference, contextName, PDU, (acFun, acCtx)
        ):
        # rfc1905: 4.2.1.1
        mgmtFun = self.snmpContext.getMibInstrum(contextName).readVars
        self.sendRsp(
            snmpEngine, stateReference, 0, 0, mgmtFun(
                v2c.apiPDU.getVarBinds(PDU), (acFun, acCtx)
                )
            )

class NextCommandResponder(CommandResponderBase):
    pduTypes = ( rfc1905.GetNextRequestPDU.tagSet, )

    # rfc1905: 4.2.2
    def handleMgmtOperation(
        self, snmpEngine, stateReference, contextName, PDU, (acFun, acCtx)
        ):
        # rfc1905: 4.2.2.1
        mgmtFun = self.snmpContext.getMibInstrum(contextName).readNextVars
        self.sendRsp(
            snmpEngine, stateReference, 0, 0, mgmtFun(
                v2c.apiPDU.getVarBinds(PDU), (acFun, acCtx)
                )
            )
        
class BulkCommandResponder(CommandResponderBase):
    pduTypes = ( rfc1905.GetBulkRequestPDU.tagSet, )
    maxVarBinds = 64
    
    # rfc1905: 4.2.3
    def handleMgmtOperation(
        self, snmpEngine, stateReference, contextName, PDU, (acFun, acCtx)
        ):
        nonRepeaters = v2c.apiBulkPDU.getNonRepeaters(PDU)
        if nonRepeaters < 0:
            nonRepeaters = 0
        maxRepetitions = v2c.apiBulkPDU.getMaxRepetitions(PDU)
        if maxRepetitions < 0:
            maxRepetitions = 0

        reqVarBinds = v2c.apiPDU.getVarBinds(PDU)

        N = min(int(nonRepeaters), len(reqVarBinds))
        M = int(maxRepetitions)
        R = max(len(reqVarBinds)-N, 0)

        if R: M = min(M, self.maxVarBinds/R)

        debug.logger & debug.flagApp and debug.logger('handleMgmtOperation: N %d, M %d, R %d' % (N, M, R))

        mgmtFun = self.snmpContext.getMibInstrum(contextName).readNextVars
        
        if N:
            rspVarBinds = mgmtFun(reqVarBinds[:N], (acFun, acCtx))
        else:
            rspVarBinds = []

        varBinds = reqVarBinds[-R:]
        while M and R:
            rspVarBinds.extend(
                mgmtFun(varBinds, (acFun, acCtx))
                )
            varBinds = rspVarBinds[-R:]
            M = M - 1

        if len(rspVarBinds):
            self.sendRsp(
                snmpEngine, stateReference, 0, 0, rspVarBinds
                )
        else:
            raise pysnmp.smi.error.SmiError()

class SetCommandResponder(CommandResponderBase):
    pduTypes = ( rfc1905.SetRequestPDU.tagSet, )

    # rfc1905: 4.2.5
    def handleMgmtOperation(
        self, snmpEngine, stateReference, contextName, PDU, (acFun, acCtx)
        ):
        mgmtFun = self.snmpContext.getMibInstrum(contextName).writeVars
        # rfc1905: 4.2.5.1-13
        try:
            self.sendRsp(
                snmpEngine, stateReference, 0, 0, mgmtFun(
                    v2c.apiPDU.getVarBinds(PDU), (acFun, acCtx)
                    )
                )
        except ( pysnmp.smi.error.NoSuchObjectError,
                 pysnmp.smi.error.NoSuchInstanceError ), errorIndication:
            e = pysnmp.smi.error.NotWritableError()
            e.update(errorIndication)
            raise e
