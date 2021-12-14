import tkinter as tk
from tkinter import ttk
import guiHelperFunctions as gui
from meta_data_handler import meta_data_handler
from tkinter import filedialog
import csv
from scipy import stats
import matplotlib as plt
import numpy as np

def askopen(frame, filename):
    f = filedialog.askopenfilename()
    if not f.endswith(("TvsD.csv")):
        return
    filename.set(f)
    frame.update()

def changetvsd(metadata, filename):
    file = filename.get()
    metadata.tvsd = [[]] * 4
    with open(file, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for lines in csv_reader:
            for i in range(4):
                metadata.tvsd[i] = metadata.tvsd[i] + [float(lines[i])]
    for artist in metadata.plots[0].collections:
        artist.remove()
    for artist in metadata.plots[1].collections:
        artist.remove()
    metadata.plots[1].plot(metadata.tvsd[0], metadata.tvsd[1], 'ro', picker=10)
    metadata.plots[1].errorbar(metadata.tvsd[0], metadata.tvsd[1], yerr=metadata.tvsd[3], xerr=metadata.tvsd[2], fmt='r+')
    metadata.canvas.draw()
    metadata.frame.update()

def linearfit(metadata, slopes, inter, derr,pi):
    slope, intercept, r, p, se = stats.linregress(metadata.tvsd[0], metadata.tvsd[1])

    x_vals = np.array(metadata.plots[1].get_xlim())
    y_vals = intercept + slope * x_vals
    metadata.plots[1].plot(x_vals, y_vals, '--')
    metadata.canvas.draw()
    slopes.set(slope)
    inter.set(intercept)
    derr.set(se)
    pi.set(p)
    metadata.frame.update()


def create_left_frame(container, plots, canvas):

    frame = tk.Frame(container)

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)

    tk.Label(frame, text='Total counts:').grid(column=0, row=0, sticky=tk.W)
    keyword = tk.Entry(frame, width=25)
    keyword.focus()
    keyword.insert(0, '0')
    keyword.grid(column=1, row=0, sticky=tk.W)

    folderPath = gui.selectSaveDirectory(frame, 1, "Home Directory")

    tk.Label(frame, text='Fibre Name:').grid(column=0, row=2, sticky=tk.W)
    fibframe = tk.Frame(frame)
    fibframe.grid(column=1, row = 2, columnspan=1)
    selfib1 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 1", variable=selfib1).grid(column = 1, row =1)
    selfib2 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 2", variable=selfib2).grid(column=2, row =1)
    selfib3 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 3", variable=selfib3).grid(column=3, row =1)

    tk.Label(frame, text='Fibre Length:').grid(column=0, row=3, sticky=tk.W)
    fiblen = tk.Entry(frame, width=25)
    fiblen.grid(column=1, row=3, sticky=tk.W)

    tk.Label(frame, text='Distance Uncertainty:').grid(column=0, row=4, sticky=tk.W)
    distway = tk.Entry(frame, width=25)
    distway.grid(column=1, row=4, sticky=tk.W)

    tk.Label(frame, text='Distance Away from Ref SiPM:').grid(column=0, row=5, sticky=tk.W)
    distuncer = tk.Entry(frame, width=25)
    distuncer.grid(column=1, row=5, sticky=tk.W)


    bottombuttonframe = tk.Frame(frame)
    bottombuttonframe.grid(row = 6, columnspan = 4)
    save = tk.BooleanVar()
    tk.Checkbutton(bottombuttonframe, text="Save All Raw Data", variable=save).grid(column = 0, row =0)

    saveall = tk.BooleanVar()
    tk.Checkbutton(bottombuttonframe, text="Save T vs D Data", variable=saveall).grid(column=1, row =0)

    metadata = meta_data_handler(frame, plots, canvas, [selfib1, selfib2, selfib3], save, saveall)

    tk.Button(bottombuttonframe, text='Lock in Parameter', command = metadata.lockin).grid(column=2, row=0)
    tk.Button(bottombuttonframe, text='Run Next', command=metadata.runNext, state = 'disabled').grid(column=3, row=0)
    tk.Button(bottombuttonframe, text='Stop', command=metadata.stopscan, state = 'disabled').grid(column=4, row=0)


    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=7, columnspan=4, sticky = tk.EW)

    tk.Label(frame, text='Plotting Functions:').grid(column=0, row=8, sticky=tk.W)

    readpath = tk.StringVar(value="No file selected")
    tk.Label(frame, text='Read T vs D Data:').grid(column=0, row=9, sticky=tk.W)
    tk.Label(frame, textvariable=readpath, width = 25).grid(column=1, row=9, sticky=tk.W)
    tk.Button(frame, text='Browse', command=lambda : askopen(frame, readpath)).grid(column=2, row=9, sticky=tk.W)

    slope = tk.StringVar(value="Not yet fitted")
    intercept = tk.StringVar(value="Not yet fitted")
    derr = tk.StringVar(value="Not yet fitted")
    p = tk.StringVar(value="Not yet fitted")

    buttonframe = tk.Frame(frame)
    buttonframe.grid(column=1, row=10, columnspan=2)
    tk.Button(buttonframe, text='Plot Timing Graph', width=15, command = lambda : changetvsd(metadata,readpath)).grid(column=0, row=0,sticky=tk.W, padx=5,pady=5)
    tk.Button(buttonframe, text='Linear Fit', command = lambda : linearfit(metadata, slope, intercept, derr, p)).grid(column=1, row=0, sticky=tk.W, padx=5,pady=5)

    tk.Label(frame, text = "The fitted slope is:").grid(column=0, row=11, sticky=tk.W)
    tk.Label(frame, textvariable=slope, width = 25).grid(column=1, row=11, sticky=tk.W)

    tk.Label(frame, text="The fitted Intercept is:").grid(column=0, row=12, sticky=tk.W)
    tk.Label(frame, textvariable=intercept, width=25).grid(column=1, row=12, sticky=tk.W)

    tk.Label(frame, text="The standard deviation on slope is:").grid(column=0, row=13, sticky=tk.W)
    tk.Label(frame, textvariable=derr, width=25).grid(column=1, row=13, sticky=tk.W)

    tk.Label(frame, text="With p value of:").grid(column=0, row=14, sticky=tk.W)
    tk.Label(frame, textvariable=p, width=25).grid(column=1, row=14, sticky=tk.W)
    # tk.Button(buttonframe, text='Plot Flat Color Plot', width=15).grid(column=0, row=1, sticky=tk.E, padx=5,pady=5)
    # tk.Button(buttonframe, text='Plot Full 3D Plot', width=15).grid(column=1, row=1, sticky=tk.W, padx=5,pady=5)

    # separator = ttk.Separator(frame, orient='horizontal')
    # separator.grid(row=13, columnspan=4, sticky = tk.EW)
    #
    # tk.Label(frame, text='View specific raw data:').grid(column=0, row=14, sticky=tk.W)
    # plotpath = gui.selectSaveDirectory(frame, 15, "Read Directory")
    # tk.Button(frame, text='View Plot').grid(column=2, row=16, padx=5,pady=5)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame, metadata

