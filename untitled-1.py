import visa;

rm=visa.ResourceManager()
kmulti=rm.open_resource('GPIB0::2::INSTR')

k=kmulti;
print(kmulti.query("*IDN?"))
#kmulti.write("*rst;status:preset;*cls")
kmulti.write(":ARM:SOURce EXT")
print(kmulti.query(":ARM:SOURce?"))
kmulti.write("INIT:CONT ON")
kmulti.write(":VOLT:DC:RANG:AUTO ON") #changes automatic ranging
kmulti.write("VOLT:DC:RANG:UPP 10") #changes measurement range of device
print(kmulti.query("VOLT:DC:RANG:UPPer?"))
kmulti.write("DATA:FEED:PRET:SOUR EXT")
print(kmulti.query("DATA:FEED:PRET:SOURce?")) 
print(kmulti.query("INIT:CONT?"))
print(kmulti.query("DATA:DATA?"))