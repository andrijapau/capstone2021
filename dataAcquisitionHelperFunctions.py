# File: dataAcquisitionHelperFunctions.py
# Author: Andrija Paurevic
# Student Number: 1003995297
# Date: October 8, 2021
# Description:

# Import modules
import pyvisa as visa
import sys, os, platform

class dataAcquisition:

    def __init__(self):
        """"""
        if platform.system() == "Windows":
            os.add_dll_directory("C:\\Program Files\\Keysight\\IO Libraries Suite\\bin")
            self.rm = visa.ResourceManager("ktvisa32")
            self.infiniiVision = rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
            self.infiniiVision.timeout = 50000
            self.debug = 0
        if platform.system() == "Darwin":
            self.rm = visa.ResourceManager("@py")
            self.infiniiVision = rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
            self.infiniiVision.timeout = 50000
            self.debug = 0
        else:
            try:
                self.rm = visa.ResourceManager("@py")
                self.infiniiVision = rm.open_resource("USB0::2391::6076::MY60101365::0::INSTR")
                self.infiniiVision.timeout = 50000
                self.debug = 0
            except:
                print("Using an unfamiliar system, please figure out how to connect to the oscilloscope!")


    def doCommand(self, command, hideParams=False):
        """"""
        if hideParams:
            (header, data) = command.split(" ", 1)
            if self.debug:
                print("\nCmd = '%s'" % header)
        else:
            if self.debug:
                print("\nCmd = '%s'" % command)
        self.infiniiVision.write("%s" % command)
        if hideParams:
            self.checkInstrumentErrors(header)
        else:
            self.checkInstrumentErrors(command)

    def checkInstrumentErrors(self, command):
        """"""
        while True:
            errorString = self.infiniiVision.query(":SYSTem:ERRor?")
            if errorString:  # If there is an error string value.
                if errorString.find("+0,", 0, 3) == -1:  # Not "No error".
                    print("ERROR: %s, command: '%s'" % (errorString, command))
                    print("Exited because of error.")
                    sys.exit(1)
                else:  # "No error"
                    break
            else:  # :SYSTem:ERRor? should always return string.
                print("ERROR: :SYSTem:ERRor? returned nothing, command: '%s'" % command)
                print("Exited because of error.")
                sys.exit(1)

    def setTriggerParameters(self):
        """"""

    def setChannelParameters(self):
        """"""

    def setTimeParameters(self):
        """"""

    def digitizeChannels(self):
        """"""

    def measureSignals(self):
        """"""

    def capture(self):
        """"""

    def analyze(self):
        """"""

