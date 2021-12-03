import datetime

import dataAcquisitionHelperFunctions as run
import datetime

class meta_data_handler():
    def __init__(self, frame):
        self.frame = frame
        self.metadata = [None] * 5
        self.dataAcq = None
        self.currfilename = None
        #counts, directory name, fiber name, fiber length, Distance Away

    def grab_meta_data(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 5:
                break
            if widget.winfo_class() == 'Entry':
                self.metadata[counter] = widget.get()
                counter = counter + 1


    def runNext(self):
        self.grab_meta_data()
        for i in tqdm(range(int(self.metadata[0]))):
            self.dataAcq.collectData(channels=chanNumbers)
        # Plot data
        #dataAcq.plotData(plotParameters=None, filename = filename)

    def lockin(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 4:
                break
            if widget.winfo_class() == 'Entry':
                widget.config(state = "disabled")
                counter = counter + 1

        self.grab_meta_data()
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.currfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' + '_'.join(self.metadata[2:5]) + '_' + time + '.csv'
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters=timeParams)
        self.dataAcq = dataAcq

    def stopscan(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 4:
                break
            if widget.winfo_class() == 'Entry':
                widget.config(state = "normal")
                counter = counter + 1
        self.dataAcq = None

    def plotHist(self, plot):
        try:
            self.dataAcq.plotHistogram(plot, plotparamter = None, filename = self.currfilename, binsize = int(sqrt(self.metadata[0])))
        except:
            print("WTF IS GOING ON")
        return 0