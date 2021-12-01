from tkinter import *
import guiHelperFunctions as gui
from left_frame import *
# Create application window
window, w, h = gui.createWindow()
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
leftFrame = create_left_frame(window)
rightFrame = Frame(window,bg="RED")

leftFrame.grid(row=0,column=0)
rightFrame.grid(row=0,column=1)



#region leftframe
# Create browse button for choosing file save location


#endregion


# Main loop to open GUI window
window.mainloop()