import datetime

import dataAcquisitionHelperFunctions as run
import datetime

class meta_data_handler():
    def __init__(self, frame):
        self.frame = frame
        self.metadata = [None] * 5
        #counts, directory name, fiber name, Distance Away, fiber length

    def grab_meta_data(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if counter == 5:
                break
            if widget.winfo_class() == 'Entry':
                self.metadata[counter] = widget.get()
                counter = counter + 1

        print(self.metadata)
    def runscan(self):
        self.grab_meta_data()
        counts = int(self.metadata[0])
        time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = self.metadata[1] + '\\' + self.metadata[0] + '_' + '_'.join(self.metadata[2:5]) + '_' + time + '.csv'
        trigParams, chanParams, timeParams, chanNumbers = run.setupOscilloscopeInput()
        dataAcq = run.dataAcquisition()
        dataAcq.prepareOscilloscope(triggerParameters=trigParams, channelParameters=chanParams,
                                    timeParameters=timeParams)
        for i in tqdm(range(numOfIterations)):
            dataAcq.collectData(channels=chanNumbers)
        # Plot data
        dataAcq.plotData(plotParameters=None, filename = filename)