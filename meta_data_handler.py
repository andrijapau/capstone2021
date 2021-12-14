import datetime

import dataAcquisitionHelperFunctions as run
import datetime
import numpy as np
import tkinter as tk
from tqdm import tqdm



def invalidinput():
    win = tk.Toplevel()
    win.wm_title("Bad Input")

    l = tk.Label(win, text="Hey! No Pressure King. But did you put something wrong in here?", font=25)
    l.grid(row=0, column=0, padx=20, pady=10)

    a = tk.Button(win, text="Yeah you right mb", command=win.destroy)
    a.grid(row=1, column=0, padx=20, pady=10)

    win.mainloop()

class meta_data_handler():
    def __init__(self, frame, plots, canvas, fibchecks, save, saveall):
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
        self.save = save
        self.saveall = saveall
        
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
        self.currfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' +self.metadata[5] + '_' + '_'.join(self.metadata[2:4]) + '_' + time + '.csv'
        for i in tqdm(range(int(self.metadata[0]))):
            if i % 20 == 0:
                self.plotHist()
            if self.ifstopped == True:
                break
            else:
                self.dataAcq.collectData(channels=self.chanNumber)
        # Plot data
        self.plotHist()
        if self.save.get():
            print("im true")
            np.savetxt(self.currfilename, self.dataAcq.results, delimiter=",")

        x, pd, mu, sigma = run.curveFit(self.plots[0], array = self.dataAcq.results)
        self.plots[0].plot(x,pd)
        d = float(self.metadata[3])
        sigmad = float(self.metadata[4])
        self.tvsd[0] = self.tvsd[0] + [d]
        self.tvsd[1] = self.tvsd[1] + [mu]
        self.tvsd[2] = self.tvsd[2] + [sigmad]
        self.tvsd[3] = self.tvsd[3] + [sigma]

        self.plots[1].plot(self.tvsd[0], self.tvsd[1], 'r+', picker=10)
        self.plots[1].errorbar(self.tvsd[0], self.tvsd[1], yerr=self.tvsd[3], xerr=self.tvsd[2], fmt='r+')
        
        for artist in self.plots[1].collections:
            artist.remove()
            
        self.canvas.draw()
        self.frame.update()
        #self.frame.update()

    def delete(self, ind):
        del seld.tvsd[ind]
        return 0

    def lockin(self):
        counter = 0
        bcounter = 0
        if not threewayxor(self.fibchecks[0].get(), self.fibchecks[1].get(),self.fibchecks[2].get()):
            invalidinput()
        for widget in self.frame.winfo_children():
            if counter < 4:
                if widget.winfo_class() == 'Entry':
                    if widget.get() == "":
                        invalidinput()
                    elif counter != 1:
                        try:
                            test = float(widget.get())
                        except:
                            invalidinput()
                    counter = counter + 1

        counter = 0
        for widget in self.frame.winfo_children():
            if counter < 4:
                if widget.winfo_class() == 'Entry':
                    if widget.get() == "":
                        invalidinput()
                    widget.config(state = "disabled")
                    counter = counter + 1
            if widget.winfo_class() == 'Frame':
                for w in widget.winfo_children():
                    if w.winfo_class() == 'Checkbutton':
                        w.config(state="disabled")
                    if w.winfo_class() == 'Button':
                        if bcounter == 0:
                            w.config(state = "disabled")
                        if bcounter == 1 or bcounter == 2:
                            w.config(state = "normal")
                        bcounter = bcounter + 1


        self.ifstopped = False
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        self.chanNumber = chanNumbers
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters= timeParams)

        self.dataAcq = dataAcq



    def stopscan(self):
        if not self.metadata == [None] * 6 and self.saveall.get():
            time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            print(self.metadata)
            tvsdfilename = self.metadata[1] + '\\' + 'MATHUSLA_' + self.metadata[0] + '_' + self.metadata[5] + '_'.join(
                self.metadata[2:4]) + '_' + time + '_TvsD' +'.csv'
            np.savetxt(tvsdfilename, self.tvsd, delimiter=",")
        self.ifstopped = True
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
                    if w.winfo_class() == 'Checkbutton':
                        w.config(state="normal")
                    if w.winfo_class() == 'Button':
                        if bcounter == 0:
                            w.config(state = "normal")
                        if bcounter == 1 or bcounter == 2:
                            w.config(state = "disabled")
                        bcounter = bcounter + 1
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


