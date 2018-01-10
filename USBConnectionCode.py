import sys
import usb.core
import usb.util
import UniversalLibrary;
import UniversalLibrary as UL

dev = usb.core.find(find_all = True)
for cfg in dev:  #- This is to find the id numbers from vendor for product  - have to set find(find_all = True) idVendor=0x9db, idProduct=0x9d
  sys.stdout.write('Decimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n')
  sys.stdout.write('Hexadecimal VendorID=' + hex(cfg.idVendor) + ' & ProductID=' + hex(cfg.idProduct) + '\n\n')

#if dev is None:
 #   raise ValueError('Device not found')



'''BoardNum = 0
Chan = 0
Gain = UL.UNI4VOLTS # works on USB 1208FS
EngUnits = 0 # Volts
DataValue = UL.cbFromEngUnits(BoardNum, Gain, EngUnits, 0)
UL.cbAOut(BoardNum, Chan, Gain, DataValue)
#UL.cbFlashLED(0);
'''
