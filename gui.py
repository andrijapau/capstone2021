from tkinter import *
import guiHelperFunctions as gui
import numpy as np
from left_frame import *
import dataAcquisitionHelperFunctions as dataAcq

### TEST DATA ###
xData = np.linspace(0,10,1000)
yData = np.random.rand(1000,1)
#################

# Create application window
window, w, h = gui.createWindow()
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
rightFrame = Frame(window,bg="RED")
plots = [None] * 2
plots[0], plots[1], canvas = gui.initPlotFigures(rightFrame)
leftFrame, metadatahandler = create_left_frame(window, plots, canvas)

leftFrame.grid(row=0,column=0, padx=20, pady=50)
rightFrame.grid(row=0,column=1, padx=20, pady=50)




#region leftframe
# Create browse button for choosing file save location
gui.plotData(plots[1],xData,yData)

#endregion

# Main loop to open GUI window
window.mainloop()