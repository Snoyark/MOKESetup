# Copyright (c) 2005, California Institute of Technology
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:

#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.

#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.

#     * Neither the name of the California Institute of Technology nor
#       the names of its contributors may be used to endorse or promote
#       products derived from this software without specific prior
#       written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Author: Andrew Straw
import UniversalLibrary as UL

VtoA = 0.34
Conv = 3.17;
BoardNum = 0
Chan =5
Gain = 20 # works on USB 1208FS - UL.UNI4VOLTS  -  For KEPCO being used, gain of 20 is the best, with a 0.9 conversion (setting 10 volts gives 9 on the machine)
EngUnits = 0 # Volts

var=1

#For the Kepco 50-8M
if(Gain==20):
    Conv = 3.17
elif(Gain==23):
    Conv = (10.0-0.19)/17
elif(Gain==15):
    Conv = 5.0/13
#else:
 #   print("There's a good chance the voltage value is off the charts. Check this")
EngUnits = input("Enter the voltage: ")
DataValue = UL.cbFromEngUnits(BoardNum, Gain, EngUnits, 0)
UL.cbAOut(BoardNum, Chan, Gain, DataValue)

UL.cbAOut(BoardNum, 7, Gain, UL.cbFromEngUnits(BoardNum, Gain, 0, 0))
print(str(Gain)+" is the gain, and "+str(EngUnits)+" Is the Voltage")

#UL.cbFlashLED(0);

