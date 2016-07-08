from CVIMonochromator import CVIMonochromator

monoChrom = CVIMonochromator("/dev/ttyUSB0")
    
monoChrom.echo()

def printHelp():
    print "\nKeys to perform operations:\n"
    print " 'g' goes to the selected wavelenght"
    print " 'i' increments one step\n 'I' increments continuosly"
    print " 'd' decrements one step\n 'D' decrements continuosly"
    print " 'z' sets zero position\n 'c' calibrates the monochromator"
    print " 's' selects the grating"
    print " 'u' sets the current machine units"
    print " 'q' queries for determined function"
    print " 'p' prints Non-Volatile Memory into a file\n 'v' switches verbose mode ON/OFF"
    print " 'x' exits this awesome piece of software\n"

def printQueryHelp():
    print "\nQuery commands:\n"
    print " 'p' returns current position of the grating"
    print " 'm' returns current working mode"
    print " 'd' returns grating's density"
    print " 'b' returns current blaze of the grating"
    print " 'g' returns current selected grating"
    print " 's' returns current set speed"
    print " 't' returns current step size"
    print " 'n' returns number of gratings of the monochromator"
    print " 'u' returns current units"
    print " 'S' returns the serial number of the monochromator" 
    print " 'x' gets back to main menu"
    
print "Welcome to the almost-manual CVI monochromator control!\n"  
cmd = 0
while (cmd!='x'):
    cmd = raw_input("\nType command in: ('h' for help) ")  
    if cmd == 'g':
        wavelenght = int(raw_input("\nType in the desired wavelenght: "))
        print "\nGoing there!"
        monoChrom.goto(wavelenght)
    elif cmd == 'i':
        print "\nIncrementing one step!"
        monoChrom.inc()  
    elif cmd == 'I':
        print "\nIncrementing continuosly until Ctrl-C is pressed!"
        try:
            while True:
                monoChrom.inc()
        except KeyboardInterrupt:
            pass    
    elif cmd == 'd':
        print "\nDecrementing one step!"
        monoChrom.dec()     
    elif cmd == 'D':
        print "\nDecrementing continuosly until Ctrl-C is pressed!"
        try:
            while True:
                monoChrom.dec()
        except KeyboardInterrupt:
            pass  
    elif cmd == 'z':
        print "\nSetting zero!"
        monoChrom.zero()
    elif cmd == 'c':
        wavelenght = int(raw_input("\nType in the desired wavelenght: "))
        print "\nCalibrating now!"
        monoChrom.calibrate(wavelenght)     
    elif cmd == 'p':
        fileName = raw_input("\nType the name of the file: ")
        print "\nDumping Non-Volatile Memory into file!"
        monoChrom.dumpToFile(fileName)       
    elif cmd == 's':
        grating = raw_input("\nType the number of the grating '1' or '2': ")
        grating = int(grating)
        if grating == 1 or grating== 2:
            print "\nSelecting grating ", grating
            monoChrom.select(grating)
        else:
            print "\nOnly '1' or '2' are valid options here!"   
    elif cmd == 'u':
        units = int(raw_input("Select  '0'- centimicrons, '1' - nanometers or '2' - angstroms: "))
        if units == 0 or units == 1 or units == 2:
            print "\nSetting units!"
            monoChrom.units(units)
        else:
            print "\nOnly '0', '1' or '2' are valid options here!"     
    elif cmd == 'q':
        query = 'h'
        while (query =='h' or query != 'x'):
            query = raw_input("\nType query command in: ('h' for help) ")
            if query == 'p':
                print "\nCurrent Position: ", monoChrom.query(0)
            elif query == 'm':
                if(monoChrom.query(1)==0):
                    print "\nThe monochromator is working in Single mode"
                elif(monoChrom.query(1)==1):
                    print "\nThe monochromator is working in Additive mode"
                elif(monoChrom.query(1)==254):
                    print "\nThe monochromator is working in single mode"
                else:
                    print "\nUnknown response from the working mode query"
            elif query == 'd':
                print "\nThe current gratings has ", monoChrom.query(2), " Grooves/mm"
            elif query == 'b':
                print "\nThe current blaze is ", monoChrom.query(3)
            elif query == 'g':
                print "\nThe current grating is ", monoChrom.query(4)
            elif query == 's':
                print "\nSpeed is set at ", monoChrom.query(5)
            elif query == 't':
                print "\nThe step size is set at ", monoChrom.query(6)
            elif query == 'n':
                print "\nThis monochromator has ", monoChrom.query(13), " gratings"
            elif query == 'u':
                if monoChrom.query(14) == 0:
                    print "\nCurrent units are centimicrons"
                elif monoChrom.query(14) == 1:
                    print "\nCurrent units are nanometers"
                elif monoChrom.query(14) == 2:
                    print "\nCurrent units are Angstroms"
                else:
                    print "\nUnknown response from the units query command!"
            elif query == 'S':
                print "\nThe serial number number of this monochromator is: ", monoChrom.query(19)
            elif query == 'h':
                printQueryHelp()
            elif query == 'x':
                print "\nBack to main menu!"
            else:
                print "\nNot a valid query command!"
                query = 'h'        
    elif cmd == 'v':
        monoChrom.setVerbose(not monoChrom._verbose)
        print "\nIt is", monoChrom._verbose, "that verbose mode is ON now"
    elif cmd == 'x':
        print "\nLooks like you're quitting, okay... CYA!"    
    elif cmd == 'h':
        printHelp()    
    else:
        print "\nJust don't get it, try another command dude!"
        
monoChrom.closeCommunication()  