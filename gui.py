from tkinter import *
import guiHelperFunctions as gui
import numpy as np
from left_frame import *

### TEST DATA ###
xData = np.linspace(0,10,1000)
yData = np.random.rand(1000,1)
#################

# Create application window
window, w, h = gui.createWindow()
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
leftFrame, metadatahandler = create_left_frame(window)
rightFrame = Frame(window,bg="RED")

leftFrame.grid(row=0,column=0, padx=20, pady=50)
rightFrame.grid(row=0,column=1, padx=20, pady=50)




#region leftframe
# Create browse button for choosing file save location

plots = gui.initPlotFigures(rightFrame)
gui.plotHistogram(plots[0],yData)
gui.plotData(plots[1],xData,yData)


#endregion

# Main loop to open GUI window
window.mainloop()