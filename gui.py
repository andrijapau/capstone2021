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
fig, plots[0], plots[1], canvas = gui.initPlotFigures(rightFrame)

plots[1].plot(10, 5, 'ro', picker = 10)
def on_pick(event):
    artist = event.artist
    x, y = artist.get_xdata()[0], artist.get_ydata()[0]

    ind = event.ind
    popup_warning([x, y], ind)

    return 0

def popup_warning(pos, ind):
    win = tk.Toplevel()
    win.wm_title("Hold Up")

    l = tk.Label(win, text="Are you sure you want to delete point at {} and {} ?".format(pos[0], pos[1]), font=25)
    l.grid(row=0, column=0, padx = 20, pady=10)


    buttonframe = Frame(win)
    buttonframe.grid(row = 1, column = 0, pady=10)
    a = ttk.Button(buttonframe, text="Okay", command=lambda : deletepoint(win ,ind))
    b = ttk.Button(buttonframe, text="Cancel", command=win.destroy)
    a.grid(row=1, column=0)
    b.grid(row=1, column=1)

    win.mainloop()

def deletepoint(frame, ind):
    for i in range(4):
        del metadatahandler.tvsd[i][ind[0]]
    plots[1].clear()
    canvas.draw()
    window.update()
    frame.destory()


fig.canvas.callbacks.connect('pick_event', on_pick)

leftFrame, metadatahandler = create_left_frame(window, plots, canvas)


leftFrame.grid(row=0,column=0, padx=20, pady=50)
rightFrame.grid(row=0,column=1, padx=20, pady=50)



menubar = Menu(window)
window.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label="Experiment Profile Builder...", command=window.quit)
fileMenu.add_command(label="Load Experiment Profile", command=window.quit)
fileMenu.add_command(label="Exit", command=window.quit)


menubar.add_cascade(label="File", menu=fileMenu)

# Main loop to open GUI window
window.mainloop()

