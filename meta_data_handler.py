import datetime

import dataAcquisitionHelperFunctions as run
import datetime
from tqdm import tqdm

class meta_data_handler():
    def __init__(self, frame, plots, canvas):
        self.frame = frame
        self.metadata = [None] * 5
        self.dataAcq = None
        self.currfilename = None
        self.chanNumber = 0
        self.ifstopped = False
        self.plots = plots
        self.canvas = canvas
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
        self.dataAcq.results = []
        self.grab_meta_data()
        for i in tqdm(range(int(self.metadata[0]))):
            if i % 20 == 0:
                self.plotHist()
            if self.ifstopped == True:
                break
            else:
                self.dataAcq.collectData(channels=self.chanNumber)
        # Plot data
        self.plotHist()
        x, pd, mu, sigma = run.curveFit(self.plots[0], array = self.dataAcq.results)
        self.plots[0].plot(x,pd)
        d = float(self.metadata[4])
        sigmad = 4
        self.plots[1].errorbar(d, mu, yerr=sigma, xerr=sigmad, fmt='r+')
        #self.plots[1].set_xlim([0,400])
        #self.plots[1].set_ylim([-20e-9, 20e-9])
        self.canvas.draw()
        #self.frame.update()

    def lockin(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 4:
                break
            if widget.winfo_class() == 'Entry':
                widget.config(state = "disabled")
                counter = counter + 1
        self.ifstopped = False
        self.grab_meta_data()
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.currfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' + '_'.join(self.metadata[2:5]) + '_' + time + '.csv'
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        self.chanNumber = chanNumbers
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters= timeParams)
        self.dataAcq = dataAcq

    def stopscan(self):
        counter = 0
        self.ifstopped = True
        for widget in self.frame.winfo_children():
            if counter == 4:
                break
            if widget.winfo_class() == 'Entry':
                widget.config(state = "normal")
                counter = counter + 1
        self.dataAcq = None

    def plotHist(self):
        # try:
        self.dataAcq.plotHistogram(self.plots[0], plotParameters = None, filename = self.currfilename, counts = int(self.metadata[0]))
        self.canvas.draw()
        self.frame.update()
        # except:
        #     print("WTF IS GOING ON")
        return 0