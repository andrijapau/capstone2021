from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askdirectory
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import os

def createWindow():
    window = Tk()
    window.title("MATHUSLA Timing Measurement GUI")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    #window.geometry("{0}x{1}+0+0".format(w, h))
    return window, w, h

def openDirectory(folderPath, cwd):
    folderSelected = askdirectory(initialdir="{}".format(cwd), title="Please select a folder...")
    folderPath.set(folderSelected)

def selectSaveDirectory(window, placerow, name):
    # Set-up
    cwd = os.getcwd()
    folderPath = StringVar()
    folderPath.set(cwd)
    browseLabel = Label(window, text=name)
    browseEntry = Entry(window, textvariable=folderPath, width = 25)
    browseButton = Button(window,text="Browse",width="6",command=lambda: openDirectory(folderPath, cwd))
    
    # Locations
    browseEntry.grid(row=placerow, column=1, sticky=W, pady=10)
    browseLabel.grid(row=placerow, column=0, sticky=W, pady=5)
    browseButton.grid(row=placerow, column=2)

    return folderPath.get()

def initPlotFigures(window):
    #Initialize the two plots that are run in the rightFrame
    #This function will create a figure with 2 subplots stacked vertically
    fig, ax = plt.subplots(2)

    a = ax[0]
    a.set_title("Most recent collection")
    a.set_xlabel("Time (ns)")
    a.set_ylabel("Counts")

    b = ax[1]
    b.set_title("Timing vs. Length")
    b.set_xlabel("Length (cm)")
    b.set_ylabel("Time (s)")

    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(expand=True)
    canvas.draw()

    return a, b, canvas

def plotData(plot, x, y):
    plot.plot(x,y)

def plotHistogram(plot, x):
    plot.hist(x, bins=int(np.sqrt(len(x))))