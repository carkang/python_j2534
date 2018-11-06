#coding:utf-8

import sys
import J2534.dllLoader as dllloader
from J2534.dll import *
import ctypes as ct
from J2534.Define import *
import J2534.Func as Func

ptData = PassThru_Data
class baseMsg(PassThru_Msg):
    def _setData(self, data):
        print (data)
        self.DataSize = len(data)
        self.Data = ptData()
        for i in range(self.DataSize):
            self.Data[i] = data[i]
    def setID(self, ID):
        d = Func.IntToID(ID)
        self._setData(d)
    def setIDandData(self, ID, data = []):
        d = Func.IntToID(ID) + data
        self._setData(d)

class pt15765Msg(baseMsg):
    def __init__(self, TxFlag):
        self.ProtocolID = ProtocolID.ISO15765
        self.TxFlags = TxFlag
class ptMskMsg(pt15765Msg):
    pass
class ptPatternMsg(pt15765Msg):
    pass
class ptFlowControlMsg(pt15765Msg):
    pass
class ptTxMsg(baseMsg):
    def __init__(self, ProtocolID, TxFlags):
        self.ProtocolID = ProtocolID
        self.TxFlags = TxFlags
    
    
class J2534Lib():
    def __init__(self):
        self.Devices = dllloader.getDevices()
        self._module = sys.modules[__name__]
    def setDevice(self, key = 0):
        device = self.Devices[key]
        self.name = device['Name']
        self.dll = dllloader.load_dll(device['FunctionLibrary'])
        self.canlib = CanlibDll(self.dll)
    def getDevices(self):
        return self.Devices
    def __getattr__(self, name):
        try:
            return getattr(self.canlib, name)
        except AttributeError:
            raise AttributeError("{t} object has no attribute {n}".format(
                t=str(type(self)), n=name))
j2534lib = J2534Lib()


def ptOpen():
    """Open Device
    """
    DeviceId = ct.c_ulong()
    ret = j2534lib.PassThruOpen(ct.c_void_p(None), ct.byref(DeviceId))
    return ret, DeviceId.value
def ptClose(DeviceId):
    """Close Device
    
    Keyword Arguments:
        DeviceId {[int]} -- Device Id Number
    """
    ret = j2534lib.PassThruClose(DeviceId)
    return ret
def ptConnect(DeviceId, ProtocolID, Flags, BaudRate):
    """Connect

    """
    ChannelID = ct.c_ulong()
    ret = j2534lib.PassThruConnect(DeviceId, ProtocolID, Flags, BaudRate, ct.byref(ChannelID))
    return ret, ChannelID.value
def ptDisconnect(ChannelID):
    """ :TODO
    """
    ret = j2534lib.PassThruDisconnect(ChannelID)
    return ret
def ptReadMsgs(ChannelID, Msgs, NumMsgs, Timeout):
    """ :TODO
    """
    ret = j2534lib.PassThruReadMsgs(ChannelID, ct.byref(Msgs), ct.byref(NumMsgs), Timeout)
    return ret
def ptWtiteMsgs(ChannelID, Msgs, NumMsgs, Timeout):
    """[summary]
    
    Arguments:
        ChannelID {[type]} -- [description]
        Msgs {[type]} -- [description]
        NumMsgs {[type]} -- [description]
        Timeout {[type]} -- [description]
    """
    ret = j2534lib.PassThruWriteMsgs(ChannelID, ct.byref(Msgs), ct.byref(ct.c_ulong(NumMsgs)), Timeout)
    return ret
def ptStartPeriodicMsg(ChannelID, Msgs, MsgID, TimeInterval):
    """ :TODO
    """
    j2534lib.PassThruStartPeriodicMsg(ChannelID, ct.byref(Msgs), ct.byref(MsgID), TimeInterval)
def ptStopPeriodicMsg(ChannelID, MsgID):
    """ :TODO
    """
    j2534lib.PassThruStopPeriodicMsg(ChannelID, MsgID)
def ptStartMsgFilter(ChannelID, FilterType, MaskMsg, PatternMsg, FlowControlMsg):
    """ :TODO
    """
    pFilterID = ct.c_ulong()
    ret = j2534lib.PassThruStartMsgFilter(ChannelID, FilterType, ct.byref(MaskMsg), ct.byref(PatternMsg), ct.byref(FlowControlMsg), ct.byref(pFilterID))
    return ret, pFilterID.value
def ptStopMsgFilter(ChannelID, MsgID):
    """ :TODO
    """
    j2534lib.PassThruStopMsgFilter(ChannelID, MsgID)
def ptSetProgrammingVoltage(DeviceID, PinNumber, Voltage):
    """ :TODO
    """
    j2534lib.PassThruSetProgrammingVoltage(DeviceID, PinNumber, Voltage)
def ptReadVersion(DeviceId):
    """Read Dll Version Msg
    
    Keyword Arguments:
        DeviceId {[int]} -- Device Id Number
    return

    """
    FirmwareVersion = ct.create_string_buffer(80)
    DllVersion = ct.create_string_buffer(80)
    ApiVersion = ct.create_string_buffer(80)
    ret = j2534lib.PassThruReadVersion(DeviceId, FirmwareVersion, DllVersion, ApiVersion)
    return ret, FirmwareVersion.value, DllVersion.value, ApiVersion.value
def ptGetLastError():
    """ :TODO
    """
    ErrorMsg = ct.create_string_buffer(80)
    j2534lib.PassThruGetLastError(ErrorMsg)
    return ErrorMsg.value
def ptIoctl(HandleID, IoctlID, Input, Output):
    """ :TODO
    """
    j2534lib.PassThruIoctl(HandleID, IoctlID, Input, Output)
