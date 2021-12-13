import datetime

import dataAcquisitionHelperFunctions as run
import datetime
import numpy as np
from tqdm import tqdm



class meta_data_handler():
    def __init__(self, frame, plots, canvas, fibchecks):
        self.frame = frame
        self.metadata = [None] * 6
        self.dataAcq = None
        self.currfilename = None
        self.chanNumber = 0
        self.ifstopped = False
        self.plots = plots
        self.canvas = canvas
        self.tvsd = [[]]*4
        self.fibchecks = fibchecks
        
        #counts, directory name, fiber length, Distance Away, uncertainty,  fiber name,

    def grab_meta_data(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 5:
                break
            if widget.winfo_class() == 'Entry':
                self.metadata[counter] = widget.get()
                counter = counter + 1
        for i in range(3):
            if self.fibchecks[i].get() == True:
                self.metadata[5] = 'Fiber' + str(i+1)
        print(self.metadata)

    def runNext(self):
        self.dataAcq.results = []
        self.grab_meta_data()
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.currfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' + '_'.join(self.metadata[2:6]) + '_' + time + '.csv'
        for i in tqdm(range(int(self.metadata[0]))):
            if i % 20 == 0:
                self.plotHist()
            if self.ifstopped == True:
                break
            else:
                self.dataAcq.collectData(channels=self.chanNumber)
        # Plot data
        self.plotHist()
        np.savetxt(self.currfilename, self.dataAcq.results, delimiter=",")

        x, pd, mu, sigma = run.curveFit(self.plots[0], array = self.dataAcq.results)
        self.plots[0].plot(x,pd)
        d = float(self.metadata[3])
        sigmad = float(self.metadata[4])
        self.tvsd[0] = self.tvsd[0] + [d]
        self.tvsd[1] = self.tvsd[1] + [mu]
        self.tvsd[2] = self.tvsd[2] + [sigmad]
        self.tvsd[3] = self.tvsd[3] + [sigma]
        print(self.tvsd)
        self.plots[1].plot(self.tvsd[0], self.tvsd[1], 'r+', picker=10)
        self.plots[1].errorbar(self.tvsd[0], self.tvsd[1], yerr=self.tvsd[3], xerr=self.tvsd[2], fmt='r+')
        self.canvas.draw()
        self.frame.update()
        #self.frame.update()

    def delete(self, ind):
        del seld.tvsd[ind]
        return 0

    def lockin(self):
        counter = 0
        bcounter = 0
        for widget in self.frame.winfo_children():
            if counter < 4:
                if widget.winfo_class() == 'Entry':
                    # if widget.get() == "":
                    #     print("invalid Input")
                    widget.config(state = "disabled")
                    counter = counter + 1
            if widget.winfo_class() == 'Frame':
                for w in widget.winfo_children():
                    w.config(state= "disabled")
            if widget.winfo_class() == 'Button':
                bcounter = bcounter + 1
                if bcounter == 2:
                    widget.config(state = "disabled")
                    break
        # if not threewayxor(self.fibchecks[0].get(), self.fibchecks[1].get(),self.fibchecks[2].get()):
        #     print("Invalid Input")
        self.ifstopped = False
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        self.chanNumber = chanNumbers
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters= timeParams)

        self.dataAcq = dataAcq


    def stopscan(self):
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        tvsdfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' + self.metadata[5] + '_'.join(
            self.metadata[2:4]) + '_' + time + '_TvsD' +'.csv'
        self.ifstopped = True
        np.savetxt(tvsdfilename, self.tvsd, delimiter=",")
        self.tvsd = [[None]]*4
        counter = 0
        bcounter = 0
        for widget in self.frame.winfo_children():
            if counter < 4:
                if widget.winfo_class() == 'Entry':
                    widget.config(state = "normal")
                    counter = counter + 1
            if widget.winfo_class() == 'Frame':
                for w in widget.winfo_children():
                    w.config(state= "normal")
            if widget.winfo_class() == 'Button':
                bcounter = bcounter + 1
                if bcounter == 2:
                    widget.config(state = "normal")
                    break
        self.dataAcq = None

    def plotHist(self):
        # try:
        self.dataAcq.plotHistogram(self.plots[0], plotParameters = None, filename = self.currfilename, counts = int(self.metadata[0]))
        self.canvas.draw()
        self.frame.update()
        # except:
        #     print("WTF IS GOING ON")
        return 0

def threewayxor(a, b, c):
    return (a ^ b ^ c) and (not(a and b and c))


