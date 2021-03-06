#coding:utf-8
import J2534
from J2534.Define import *
import sys, time

J2534.SetErrorLog(True)
devices = J2534.getDevices()
try:
    index = int(sys.argv[1], base=10)
except:
    index = 0
J2534.setDevice(index)


ret, deviceID = J2534.ptOpen()

ret, channelID = J2534.ptConnect(deviceID, ProtocolID.CAN, 0, BaudRate.B500K)


msg = J2534.ptRxMsg()

start = time.time()
while True:
    if time.time() - start > 10:
        break
    ret = J2534.ptReadMsgs(channelID, msg, 1, 100)
    if ret is 0:
        msg.show()

ret = J2534.ptDisconnect(channelID)

ret = J2534.ptClose(deviceID)
