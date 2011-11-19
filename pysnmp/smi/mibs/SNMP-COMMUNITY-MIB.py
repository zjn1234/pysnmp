# PySNMP SMI module. Autogenerated from smidump -f python SNMP-COMMUNITY-MIB
# by libsmi2pysnmp-0.1.2 at Sat Nov 19 22:05:26 2011,
# Python version sys.version_info(major=2, minor=7, micro=2, releaselevel='final', serial=0)

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( NamedValues, ) = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
( ConstraintsIntersection, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ValueSizeConstraint, ) = mibBuilder.importSymbols("ASN1-REFINEMENT", "ConstraintsIntersection", "ConstraintsUnion", "SingleValueConstraint", "ValueRangeConstraint", "ValueSizeConstraint")
( SnmpAdminString, SnmpEngineID, ) = mibBuilder.importSymbols("SNMP-FRAMEWORK-MIB", "SnmpAdminString", "SnmpEngineID")
( SnmpTagValue, snmpTargetAddrEntry, ) = mibBuilder.importSymbols("SNMP-TARGET-MIB", "SnmpTagValue", "snmpTargetAddrEntry")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Integer32, Integer32, IpAddress, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, snmpModules, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "Integer32", "IpAddress", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "snmpModules")
( RowStatus, StorageType, ) = mibBuilder.importSymbols("SNMPv2-TC", "RowStatus", "StorageType")

# Objects

snmpCommunityMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 18)).setRevisions(("2000-03-06 00:00","1999-05-13 00:00",))
if mibBuilder.loadTexts: snmpCommunityMIB.setOrganization("SNMPv3 Working Group")
if mibBuilder.loadTexts: snmpCommunityMIB.setContactInfo("WG-email:   snmpv3@lists.tislabs.com\nSubscribe:  majordomo@lists.tislabs.com\n            In msg body:  subscribe snmpv3\n\nChair:      Russ Mundy\n            TIS Labs at Network Associates\nPostal:     3060 Washington Rd\n            Glenwood MD 21738\n            USA\nEmail:      mundy@tislabs.com\nPhone:      +1-301-854-6889\n\n\n\nCo-editor:  Rob Frye\n            CoSine Communications\nPostal:     1200 Bridge Parkway\n            Redwood City, CA 94065\n            USA\nE-mail:     rfrye@cosinecom.com\nPhone:      +1 703 725 1130\n\nCo-editor:  David B. Levi\n            Nortel Networks\nPostal:     3505 Kesterwood Drive\n            Knoxville, TN 37918\nE-mail:     dlevi@nortelnetworks.com\nPhone:      +1 423 686 0432\n\nCo-editor:  Shawn A. Routhier\n            Integrated Systems Inc.\nPostal:     333 North Ave 4th Floor\n            Wakefield, MA 01880\nE-mail:     sar@epilogue.com\nPhone:      +1 781 245 0804\n\nCo-editor:  Bert Wijnen\n            Lucent Technologies\nPostal:     Schagen 33\n            3461 GL Linschoten\n            Netherlands\nEmail:      bwijnen@lucent.com\nPhone:      +31-348-407-775")
if mibBuilder.loadTexts: snmpCommunityMIB.setDescription("This MIB module defines objects to help support coexistence\nbetween SNMPv1, SNMPv2c, and SNMPv3.")
snmpCommunityMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 18, 1))
snmpCommunityTable = MibTable((1, 3, 6, 1, 6, 3, 18, 1, 1))
if mibBuilder.loadTexts: snmpCommunityTable.setDescription("The table of community strings configured in the SNMP\nengine's Local Configuration Datastore (LCD).")
snmpCommunityEntry = MibTableRow((1, 3, 6, 1, 6, 3, 18, 1, 1, 1)).setIndexNames((1, "SNMP-COMMUNITY-MIB", "snmpCommunityIndex"))
if mibBuilder.loadTexts: snmpCommunityEntry.setDescription("Information about a particular community string.")
snmpCommunityIndex = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 1), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess("noaccess")
if mibBuilder.loadTexts: snmpCommunityIndex.setDescription("The unique index value of a row in this table.")
snmpCommunityName = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 2), OctetString()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityName.setDescription("The community string for which a row in this table\nrepresents a configuration.")
snmpCommunitySecurityName = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 3), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(1, 32))).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunitySecurityName.setDescription("A human readable string representing the corresponding\nvalue of snmpCommunityName in a Security Model\nindependent format.")
snmpCommunityContextEngineID = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 4), SnmpEngineID()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityContextEngineID.setDescription("The contextEngineID indicating the location of the\ncontext in which management information is accessed\nwhen using the community string specified by the\ncorresponding instance of snmpCommunityName.\n\nThe default value is the snmpEngineID of the entity in\nwhich this object is instantiated.")
snmpCommunityContextName = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 5), SnmpAdminString().subtype(subtypeSpec=ValueSizeConstraint(0, 32)).clone('')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityContextName.setDescription("The context in which management information is accessed\nwhen using the community string specified by the corresponding\ninstance of snmpCommunityName.")
snmpCommunityTransportTag = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 6), SnmpTagValue().clone('')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityTransportTag.setDescription("This object specifies a set of transport endpoints\nfrom which a command responder application will accept\nmanagement requests.  If a management request containing\nthis community is received on a transport endpoint other\nthan the transport endpoints identified by this object,\nthe request is deemed unauthentic.\n\nThe transports identified by this object are specified\n\n\nin the snmpTargetAddrTable.  Entries in that table\nwhose snmpTargetAddrTagList contains this tag value\nare identified.\n\nIf the value of this object has zero-length, transport\nendpoints are not checked when authenticating messages\ncontaining this community string.")
snmpCommunityStorageType = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 7), StorageType()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityStorageType.setDescription("The storage type for this conceptual row in the\nsnmpCommunityTable.  Conceptual rows having the value\n'permanent' need not allow write-access to any\ncolumnar object in the row.")
snmpCommunityStatus = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 1, 1, 8), RowStatus()).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpCommunityStatus.setDescription("The status of this conceptual row in the snmpCommunityTable.\n\nAn entry in this table is not qualified for activation\nuntil instances of all corresponding columns have been\ninitialized, either through default values, or through\nSet operations.  The snmpCommunityName and\nsnmpCommunitySecurityName objects must be explicitly set.\n\nThere is no restriction on setting columns in this table\nwhen the value of snmpCommunityStatus is active(1).")
snmpTargetAddrExtTable = MibTable((1, 3, 6, 1, 6, 3, 18, 1, 2))
if mibBuilder.loadTexts: snmpTargetAddrExtTable.setDescription("The table of mask and mms values associated with the\n\n\nsnmpTargetAddrTable.\n\nThe snmpTargetAddrExtTable augments the\nsnmpTargetAddrTable with a transport address mask value\nand a maximum message size value.  The transport address\nmask allows entries in the snmpTargetAddrTable to define\na set of addresses instead of just a single address.\nThe maximum message size value allows the maximum\nmessage size of another SNMP entity to be configured for\nuse in SNMPv1 (and SNMPv2c) transactions, where the\nmessage format does not specify a maximum message size.")
snmpTargetAddrExtEntry = MibTableRow((1, 3, 6, 1, 6, 3, 18, 1, 2, 1))
if mibBuilder.loadTexts: snmpTargetAddrExtEntry.setDescription("Information about a particular mask and mms value.")
snmpTargetAddrTMask = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 2, 1, 1), OctetString().subtype(subtypeSpec=ValueSizeConstraint(0, 255)).clone('')).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpTargetAddrTMask.setDescription("The mask value associated with an entry in the\nsnmpTargetAddrTable.  The value of this object must\nhave the same length as the corresponding instance of\nsnmpTargetAddrTAddress, or must have length 0.  An\nattempt to set it to any other value will result in\nan inconsistentValue error.\n\nThe value of this object allows an entry in the\nsnmpTargetAddrTable to specify multiple addresses.\nThe mask value is used to select which bits of\na transport address must match bits of the corresponding\ninstance of snmpTargetAddrTAddress, in order for the\ntransport address to match a particular entry in the\nsnmpTargetAddrTable.  Bits which are 1 in the mask\nvalue indicate bits in the transport address which\nmust match bits in the snmpTargetAddrTAddress value.\n\n\nBits which are 0 in the mask indicate bits in the\ntransport address which need not match.  If the\nlength of the mask is 0, the mask should be treated\nas if all its bits were 1 and its length were equal\nto the length of the corresponding value of\nsnmpTargetAddrTable.\n\nThis object may not be modified while the value of the\ncorresponding instance of snmpTargetAddrRowStatus is\nactive(1).  An attempt to set this object in this case\nwill result in an inconsistentValue error.")
snmpTargetAddrMMS = MibTableColumn((1, 3, 6, 1, 6, 3, 18, 1, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(ValueRangeConstraint(0,0),ValueRangeConstraint(484,2147483647),)).clone(484)).setMaxAccess("readcreate")
if mibBuilder.loadTexts: snmpTargetAddrMMS.setDescription("The maximum message size value associated with an entry\nin the snmpTargetAddrTable.")
snmpTrapAddress = MibScalar((1, 3, 6, 1, 6, 3, 18, 1, 3), IpAddress()).setMaxAccess("notifyonly")
if mibBuilder.loadTexts: snmpTrapAddress.setDescription("The value of the agent-addr field of a Trap PDU which\nis forwarded by a proxy forwarder application using\nan SNMP version other than SNMPv1.  The value of this\nobject SHOULD contain the value of the agent-addr field\nfrom the original Trap PDU as generated by an SNMPv1\nagent.")
snmpTrapCommunity = MibScalar((1, 3, 6, 1, 6, 3, 18, 1, 4), OctetString()).setMaxAccess("notifyonly")
if mibBuilder.loadTexts: snmpTrapCommunity.setDescription("The value of the community string field of an SNMPv1\nmessage containing a Trap PDU which is forwarded by a\na proxy forwarder application using an SNMP version\nother than SNMPv1.  The value of this object SHOULD\ncontain the value of the community string field from\nthe original SNMPv1 message containing a Trap PDU as\ngenerated by an SNMPv1 agent.")
snmpCommunityMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 18, 2))
snmpCommunityMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 18, 2, 1))
snmpCommunityMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 18, 2, 2))

# Augmentions
snmpTargetAddrEntry, = mibBuilder.importSymbols("SNMP-TARGET-MIB", "snmpTargetAddrEntry")
snmpTargetAddrEntry.registerAugmentions(("SNMP-COMMUNITY-MIB", "snmpTargetAddrExtEntry"))
snmpTargetAddrExtEntry.setIndexNames(*snmpTargetAddrEntry.getIndexNames())

# Groups

snmpCommunityGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 18, 2, 2, 1)).setObjects(("SNMP-COMMUNITY-MIB", "snmpCommunitySecurityName"), ("SNMP-COMMUNITY-MIB", "snmpCommunityTransportTag"), ("SNMP-COMMUNITY-MIB", "snmpCommunityStorageType"), ("SNMP-COMMUNITY-MIB", "snmpTargetAddrMMS"), ("SNMP-COMMUNITY-MIB", "snmpTargetAddrTMask"), ("SNMP-COMMUNITY-MIB", "snmpCommunityName"), ("SNMP-COMMUNITY-MIB", "snmpCommunityContextEngineID"), ("SNMP-COMMUNITY-MIB", "snmpCommunityStatus"), ("SNMP-COMMUNITY-MIB", "snmpCommunityContextName"), )
if mibBuilder.loadTexts: snmpCommunityGroup.setDescription("A collection of objects providing for configuration\nof community strings for SNMPv1 (and SNMPv2c) usage.")
snmpProxyTrapForwardGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 18, 2, 2, 3)).setObjects(("SNMP-COMMUNITY-MIB", "snmpTrapAddress"), ("SNMP-COMMUNITY-MIB", "snmpTrapCommunity"), )
if mibBuilder.loadTexts: snmpProxyTrapForwardGroup.setDescription("Objects which are used by proxy forwarding applications\nwhen translating traps between SNMP versions.  These are\nused to preserve SNMPv1-specific information when\n\n\ntranslating to SNMPv2c or SNMPv3.")

# Compliances

snmpCommunityMIBCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 18, 2, 1, 1)).setObjects(("SNMP-COMMUNITY-MIB", "snmpCommunityGroup"), )
if mibBuilder.loadTexts: snmpCommunityMIBCompliance.setDescription("The compliance statement for SNMP engines which\nimplement the SNMP-COMMUNITY-MIB.")
snmpProxyTrapForwardCompliance = ModuleCompliance((1, 3, 6, 1, 6, 3, 18, 2, 1, 2)).setObjects(("SNMP-COMMUNITY-MIB", "snmpProxyTrapForwardGroup"), )
if mibBuilder.loadTexts: snmpProxyTrapForwardCompliance.setDescription("The compliance statement for SNMP engines which\ncontain a proxy forwarding application which is\ncapable of forwarding SNMPv1 traps using SNMPv2c\nor SNMPv3.")

# Exports

# Module identity
mibBuilder.exportSymbols("SNMP-COMMUNITY-MIB", PYSNMP_MODULE_ID=snmpCommunityMIB)

# Objects
mibBuilder.exportSymbols("SNMP-COMMUNITY-MIB", snmpCommunityMIB=snmpCommunityMIB, snmpCommunityMIBObjects=snmpCommunityMIBObjects, snmpCommunityTable=snmpCommunityTable, snmpCommunityEntry=snmpCommunityEntry, snmpCommunityIndex=snmpCommunityIndex, snmpCommunityName=snmpCommunityName, snmpCommunitySecurityName=snmpCommunitySecurityName, snmpCommunityContextEngineID=snmpCommunityContextEngineID, snmpCommunityContextName=snmpCommunityContextName, snmpCommunityTransportTag=snmpCommunityTransportTag, snmpCommunityStorageType=snmpCommunityStorageType, snmpCommunityStatus=snmpCommunityStatus, snmpTargetAddrExtTable=snmpTargetAddrExtTable, snmpTargetAddrExtEntry=snmpTargetAddrExtEntry, snmpTargetAddrTMask=snmpTargetAddrTMask, snmpTargetAddrMMS=snmpTargetAddrMMS, snmpTrapAddress=snmpTrapAddress, snmpTrapCommunity=snmpTrapCommunity, snmpCommunityMIBConformance=snmpCommunityMIBConformance, snmpCommunityMIBCompliances=snmpCommunityMIBCompliances, snmpCommunityMIBGroups=snmpCommunityMIBGroups)

# Groups
mibBuilder.exportSymbols("SNMP-COMMUNITY-MIB", snmpCommunityGroup=snmpCommunityGroup, snmpProxyTrapForwardGroup=snmpProxyTrapForwardGroup)

# Compliances
mibBuilder.exportSymbols("SNMP-COMMUNITY-MIB", snmpCommunityMIBCompliance=snmpCommunityMIBCompliance, snmpProxyTrapForwardCompliance=snmpProxyTrapForwardCompliance)
