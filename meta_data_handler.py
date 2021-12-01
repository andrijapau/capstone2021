import dataAcquisitionHelperFunctions as run


class meta_data_handler():
    def __init__(self, frame):
        self.frame = frame
        self.metadata = [None] * 5
        #counts, directory name, fiber name, Distance Away, fiber length

    def grab_meta_data(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == 'Entry':
                self.metadata[counter] = widget.get()
                counter = counter + 1

    def runscan(self):
        self.grab_meta_data()
        counts = int(self.metadata[0])
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters=timeParams)
        for i in tqdm(range(numOfIterations)):
            dataAcq.collectData(channels=chanNumbers)
        # Plot data
        dataAcq.plotData(plotParameters=None)