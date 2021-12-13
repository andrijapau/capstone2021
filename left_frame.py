import tkinter as tk
from tkinter import ttk
import guiHelperFunctions as gui
from meta_data_handler import meta_data_handler


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
    var1 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 1", variable=var1).grid(column = 1, row =1)
    var2 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 2", variable=var2).grid(column=2, row =1)
    var3 = tk.BooleanVar()
    tk.Checkbutton(fibframe, text="Fibre 3", variable=var3).grid(column=3, row =1)

    tk.Label(frame, text='Fibre Length:').grid(column=0, row=3, sticky=tk.W)
    fiblen = tk.Entry(frame, width=25)
    fiblen.grid(column=1, row=3, sticky=tk.W)

    tk.Label(frame, text='Distance Uncertainty:').grid(column=0, row=4, sticky=tk.W)
    distway = tk.Entry(frame, width=25)
    distway.grid(column=1, row=4, sticky=tk.W)

    tk.Label(frame, text='Distance Away from Ref SiPM:').grid(column=0, row=5, sticky=tk.W)
    distuncer = tk.Entry(frame, width=25)
    distuncer.grid(column=1, row=5, sticky=tk.W)

    metadata = meta_data_handler(frame, plots, canvas, [var1, var2, var3])
    tk.Button(frame, text='Lock in Parameter', command = metadata.lockin).grid(column=1, row=6)
    tk.Button(frame, text='Run Next', command=metadata.runNext).grid(column=2, row=6)
    tk.Button(frame, text='Stop', command=metadata.stopscan).grid(column=3, row=6)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=7, columnspan=4, sticky = tk.EW)

    tk.Label(frame, text='Plotting Functions:').grid(column=0, row=8, sticky=tk.W)

    readpath = gui.selectSaveDirectory(frame, 9, "Read Plot Directory")
    plotpath = gui.selectSaveDirectory(frame, 10, "Save Plot Directory")


    buttonframe = tk.Frame(frame)
    buttonframe.grid(column=1, row=11, rowspan=2, columnspan=2)
    tk.Button(buttonframe, text='Read CSV Data', width=15).grid(column=0, row=0,sticky=tk.W, padx=5,pady=5)
    tk.Button(buttonframe, text='Plot Timing Graph', width=15).grid(column=1, row=0, sticky=tk.W, padx=5,pady=5)
    tk.Button(buttonframe, text='Plot Flat Color Plot', width=15).grid(column=0, row=1, sticky=tk.E, padx=5,pady=5)
    tk.Button(buttonframe, text='Plot Full 3D Plot', width=15).grid(column=1, row=1, sticky=tk.W, padx=5,pady=5)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=13, columnspan=4, sticky = tk.EW)

    tk.Label(frame, text='View specific raw data:').grid(column=0, row=14, sticky=tk.W)
    plotpath = gui.selectSaveDirectory(frame, 15, "Read Directory")
    tk.Button(frame, text='View Plot').grid(column=2, row=16, padx=5,pady=5)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame, metadata

