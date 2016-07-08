import serial
from time import sleep

class CVIMonochromator:
    "CVI's monochromator interface for RS232 communications"
    
    def __init__(self, deviceLabel):
        self._port = serial.Serial(deviceLabel, 
                     baudrate=9600,
                     parity=serial.PARITY_NONE,
                     stopbits=serial.STOPBITS_ONE,
                     bytesize=serial.EIGHTBITS,
                     writeTimeout = 0,
                     timeout = 0,
                     rtscts=True,
                     dsrdtr=False,
                     xonxoff=False)   
        if self._port.isOpen():
            print "\nPort is Open, that's a start, right? \n"
        else:
            print "\nPort isn't Open, nothing good is expected! \n"          
        self._cmdList = []
        self._verbose = False
    
    def setVerbose (self, state):
        self._verbose = state
                
    def dec(self):
        self._cmdList = [1]
        self._instructionExchange(-1, "dec")    
        
    def inc(self):
        self._cmdList = [7]
        self._instructionExchange(-1, "inc")      
        
    def speed(self, selectedSpeed):
        self._cmdList = [13]
        self._instructionExchange(sizeByte, "speed") 
            
    def goto(self, selectedPosition):
        self._cmdList = [16]
        self._instructionExchange(selectedPosition, "goto")
        
    def calibrate(self, selectedPosition):
        self._cmdList = [18]
        self._instructionExchange(selectedPosition, "calibrate")   

    def select(self, grating):
        self._cmdList = [26]
        self._instructionExchange(grating, "grating") 
        
    def echo(self):
        self._cmdList = [27]
        self._instructionExchange(-1, "echo")  
        
    def units(self, unitsByte):
        self._cmdList = [50]
        self._instructionExchange(unitsByte, "units")

    def order(self, orderByte):
        self._cmdList = [51]
        self._instructionExchange(orderByte, "order") 

    def zero(self):
        self._cmdList = [52]
        self._instructionExchange(1, "zero") 
        
    def step(self):
        self._cmdList = [54]
        self._instructionExchange(-1 ,"step") 
        
    def size(self, sizeByte):
        self._cmdList = [55]
        self._instructionExchange(sizeByte, "size") 

    def query(self, selectedCommand):
        self._cmdList = [56]
        self._instructionExchange(selectedCommand, "query")
        queryResponse = self._cmdList[0]*256 + self._cmdList[1]
        return queryResponse

    def type(self, selectedType):
        self._cmdList = [57]
        self._instructionExchange(selectedType, "type") 

    def readNovRam(self, address):
        self._cmdList = [156]
        self._instructionExchange(address, "readNovRam")
        return self._cmdList
        
    def reset(self):
        self._cmdList = [255, 255, 255]
        self._sendMessage()
        self._receiveMessage()

    def closeCommunication(self):
        self._port.close()
        print "\nClosing communications, leamme alone now, was about that time! \n"
         
    def dumpToFile(self, fileName):
        addressMeaning = ["The baudrate index: 0 is 9600 b/s", "Current selected grating: 1 or 2", "Zero offset high byte of machine 1, grating 1",
                          "Low byte of the above number", "Zero offset high byte of machine 1, grating 2", "Low byte of the above number", 
                          "Calibration high byte of machine 1, grating 1", "Low byte of the above number", "Calibration high byte of machine 1, grating 2",
                          "Low byte of the above number", "Groove index of grating 1; 0: = 3600 g/mm; 1: = 2400; 2: = 1800; 3:= 1200; 4: = 600; 5: = 300; 6: = 150; 7: = 75.",
                          "Groove index of grating 2. The meaning is the same as grating 1", "Blazed high byte of grating 1 in nm", "Low byte of the above number",
                          "Blazed high byte of grating 2 in nm", "Low byte of the above number", "Total gratings of machine 1", "Total gratings of machine 2. (CM112 only)",
                          "Zero offset high byte of machine 2, grating 1. (CM112 only)", "Low byte of the above number. (CM112 only)", 
                          "Zero offset high byte of machine 2, grating 2. (CM112 only)", "Low byte of the above number. (CM112 only)",
                          "Order and Type. Bit 0 (for m1g1): 1 is - order, 0 is + order; Bit 1 (for m1g2): 1 is - order, 0 is + order; Bit 4 (for grating 1): 1 is subtractive dispersion, 0 is additive dispersion; Bit 5 (for grating 2): 1 is subtractive dispersion, 0 is additive dispersion. (Bits 4,5 CM112 only)",
                          "Not used", "Current machine 1 unit  0 centimicrons, 1 nm, 2 angstroms", "Current machine 2 unit  0 centimicrons, 1 nm, 2 angstroms (CM112 only)",
                          "Serial number high byte", "Serial number low byte", "Not used", "Not used", "Not used", "Not used","AA in hex if programmed",
                          "AA in hex if programmed", "Not used"]
        
        dumpFile = open(fileName,"w")      
        for address in range (0, 34):
            lastList = self.readNovRam(address)
            sleep(0.01)
            if lastList[-1] == 24:
                element = str(lastList[-3])
            else:
                element = str(lastList[1])
            dumpFile.write ("Address "+ str(address) +":\t\t" + element +"\t\t"+ addressMeaning[address]+"\n")
                
        dumpFile.close() 

    def _instructionExchange(self, selectedCommand,cmd):
        self._encodeDataBytes(selectedCommand, cmd)
        self._sendMessage()
        self._decodeDataBytes(self._receiveMessage()) 
        
    def _encodeDataBytes(self, dataByte, cmd):
        if dataByte != -1:
            hiByte = int(dataByte / 256)
            loByte = dataByte - (256 * hiByte)
            if hiByte != 0:
                self._cmdList.append(hiByte)
            elif hiByte == 0 and cmd == "goto":
                self._cmdList.append(hiByte)  
            self._cmdList.append(loByte)
            
    def _decodeDataBytes(self, string):
        self._cmdList = []
        for i in range(0, len(string)):
            self._cmdList.append(ord(string[i]))
        if len(self._cmdList) > 1:
            if self._cmdList[-2] < 128:
                if self._verbose:
                    print "Command Accepted!"
            else:
                if self._verbose:
                    print "Command Refused!"
        if self._verbose:    
            print "RXin' this: ", self._cmdList, "\n"
              
    def _sendMessage(self):
        if self._verbose:
            print "TXin' this: ", self._cmdList
        for i in range(0, len(self._cmdList)):
            element = chr(self._cmdList[i])
            self._port.write(element)
            sleep(0.01)  
    
    def _receiveMessage(self):
        message = self._port.readline()
        #print "Received message is: ", message
        return message
     
             
if __name__ == '__main__':
           
    monoChrom = CVIMonochromator("/dev/ttyUSB0")
    
    monoChrom.echo()

    monoChrom.closeCommunication()     
       