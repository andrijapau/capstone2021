from tkinter import *
import guiHelperFunctions as gui
import numpy as np
from left_frame import *
import dataAcquisitionHelperFunctions as dataAcq
from tkinter import filedialog
import matplotlib.pyplot as plt


### TEST DATA ###
xData = np.linspace(0,10,1000)
yData = np.random.rand(1000,1)
#################

# Create application window
window, w, h = gui.createWindow()
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
rightFrame = Frame(window)
rightFrame.rowconfigure(0, weight = 8)
plots = [None] * 2
fig, plots[0], plots[1], canvas = gui.initPlotFigures(rightFrame, 0)


def on_pick(event):
    artist = event.artist
    ind = event.ind
    x, y = artist.get_xdata()[ind[0]], artist.get_ydata()[ind[0]]
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

    metadatahandler.plots[1].clear()
    metadatahandler.plots[1].set_title("Timing vs. Length")
    metadatahandler.plots[1].set_xlabel("Length (cm)")
    metadatahandler.plots[1].set_ylabel("Time (s)")

    metadatahandler.plots[1].plot(metadatahandler.tvsd[0], metadatahandler.tvsd[1], 'ro', picker=10)
    metadatahandler.plots[1].errorbar(metadatahandler.tvsd[0], metadatahandler.tvsd[1], yerr=metadatahandler.tvsd[3], xerr=metadatahandler.tvsd[2], fmt='r+')

    metadatahandler.canvas.draw()
    metadatahandler.frame.update()
    frame.destroy()

def file_save():
    f = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=(("PDF", "*.pdf"),("JPEG", "*.jpg"),("PNG", "*.png"),("All Files", "*.*") ))
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    extent = plots[1].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    extent = extent.expanded(1.4, 1.8)
    extent.y1 = extent.y1 * 0.9
    print(extent)
    fig.savefig(f, bbox_inches=extent)

def saveparameter(frame, counts, path, fiblength, disuncer, disaway, fib):
    f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text File", "*.txt"),("All Files", "*.*")))
    fibname = None
    for i in range(3):
        if fib[i].get() == True:
            fibname = 'Fiber' + str(i + 1)
    np.savetxt(f, [counts, path, fiblength, disuncer, disaway, fibname],fmt = '%s')
    frame.destroy()

def loadparam(leftframe, metadata):
    f = filedialog.askopenfilename()
    data = np.loadtxt(f, dtype = 'U')
    fibselected = int(data[5][-1]) - 1
    fcounter = 0
    counter = 0
    for widget in leftframe.winfo_children():
        if counter < 5:
            if widget.winfo_class() == 'Entry':
                widget.delete(0, 'end')
                widget.insert(0, data[counter])
                counter = counter + 1

        if widget.winfo_class() == 'Frame':
            for w in widget.winfo_children():
                if w.winfo_class() == 'Checkbutton' and fcounter == fibselected:
                    w.select()
                    break
                fcounter = fcounter + 1
    leftframe.update()
    return 0

def constructprofile():
    win = tk.Toplevel()
    win.wm_title("Construct Experiment Profile")

    win.columnconfigure(0, weight=1)
    win.columnconfigure(1, weight=2)
    win.columnconfigure(2, weight=1)

    tk.Label(win, text='Total counts:').grid(column=0, row=0, sticky=tk.W)
    keyword = tk.Entry(win, width=25)
    keyword.focus()
    keyword.insert(0, '0')
    keyword.grid(column=1, row=0, sticky=tk.W)

    folderPath = gui.selectSaveDirectory(win, 1, "Home Directory")

    tk.Label(win, text='Fibre Name:').grid(column=0, row=2, sticky=tk.W)
    fibframe = tk.Frame(win)
    fibframe.grid(column=1, row = 2, columnspan=1)
    selfib1 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 1", variable=selfib1).grid(column = 1, row =1)
    selfib2 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 2", variable=selfib2).grid(column=2, row =1)
    selfib3 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 3", variable=selfib3).grid(column=3, row =1)

    tk.Label(win, text='Fibre Length:').grid(column=0, row=3, sticky=tk.W)
    fiblen = tk.Entry(win, width=25)
    fiblen.grid(column=1, row=3, sticky=tk.W)

    tk.Label(win, text='Distance Uncertainty:').grid(column=0, row=4, sticky=tk.W)
    distuncer = tk.Entry(win, width=25)
    distuncer.grid(column=1, row=4, sticky=tk.W)

    tk.Label(win, text='Distance Away from Ref SiPM:').grid(column=0, row=5, sticky=tk.W)
    distaway = tk.Entry(win, width=25)
    distaway.grid(column=1, row=5, sticky=tk.W)

    tk.Button(win, text='Create Experiment Profile', command = lambda: saveparameter(win, keyword.get(), folderPath.get(), fiblen.get(), distuncer.get(), distaway.get(), [selfib1, selfib2, selfib3])).grid(column=2, row=6)

    for widget in win.winfo_children():
        widget.grid(padx=5, pady=5)

    win.mainloop()


fig.canvas.callbacks.connect('pick_event', on_pick)

Button(rightFrame, text='Save Plot', command = file_save).grid(column=0, row=1, pady=10)

leftFrame, metadatahandler = create_left_frame(window, plots, canvas)

leftFrame.grid(row=0,column=0, padx=20, pady=50)
rightFrame.grid(row=0,column=1, padx=20, pady=50)



menubar = Menu(window)
window.config(menu=menubar)

fileMenu = Menu(menubar)
fileMenu.add_command(label="Experiment Profile Builder...", command=constructprofile)
fileMenu.add_command(label="Load Experiment Profile", command= lambda : loadparam(leftFrame, metadatahandler))
fileMenu.add_command(label="Exit", command=window.quit)


menubar.add_cascade(label="File", menu=fileMenu)

# Main loop to open GUI window
window.mainloop()

