import tkinter as tk
from tkinter import ttk
import guiHelperFunctions as gui
from meta_data_handler import meta_data_handler


def create_left_frame(container):

    frame = tk.Frame(container)

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(2, weight=1)
    # Find what
    tk.Label(frame, text='Total counts:').grid(column=0, row=0, sticky=tk.W)
    keyword = tk.Entry(frame, width=25)
    keyword.focus()
    keyword.insert(0, '0')
    keyword.grid(column=1, row=0, sticky=tk.W)

    folderPath = gui.selectSaveDirectory(frame, 1, "Home Directory")

    tk.Label(frame, text='Fibre Name:').grid(column=0, row=2, sticky=tk.W)
    fibname = tk.Entry(frame, width=25)
    fibname.grid(column=1, row=2, sticky=tk.W)

    tk.Label(frame, text='Fibre Length:').grid(column=0, row=3, sticky=tk.W)
    fiblen = tk.Entry(frame, width=25)
    fiblen.grid(column=1, row=3, sticky=tk.W)

    tk.Label(frame, text='Distance Away from Ref SiPM:').grid(column=0, row=4, sticky=tk.W)
    distway = tk.Entry(frame, width=25)
    distway.grid(column=1, row=4, sticky=tk.W)


    metadata = meta_data_handler(frame)
    tk.Button(frame, text='Lock in Parameter', command = metadata.lockin).grid(column=1, row=5)
    tk.Button(frame, text='Run Next', command=metadata.runNext).grid(column=2, row=5)
    tk.Button(frame, text='Stop', command=metadata.stopscan).grid(column=3, row=5)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=6, columnspan=4, sticky = tk.EW)

    tk.Label(frame, text='Plotting Functions:').grid(column=0, row=7, sticky=tk.W)

    readpath = gui.selectSaveDirectory(frame, 8, "Read Plot Directory")
    plotpath = gui.selectSaveDirectory(frame, 9, "Save Plot Directory")


    buttonframe = tk.Frame(frame)
    buttonframe.grid(column=1, row=10, rowspan=2, columnspan=2)
    tk.Button(buttonframe, text='Read CSV Data', width=15).grid(column=0, row=0,
                                                                                              sticky=tk.W, padx=5,
                                                                                              pady=5)
    tk.Button(buttonframe, text='Plot Timing Graph', width=15).grid(column=1, row=0, sticky=tk.W, padx=5,pady=5)
    tk.Button(buttonframe, text='Plot Flat Color Plot', width=15).grid(column=0, row=1, sticky=tk.E, padx=5,pady=5)
    tk.Button(buttonframe, text='Plot Full 3D Plot', width=15).grid(column=1, row=1, sticky=tk.W, padx=5,pady=5)

    separator = ttk.Separator(frame, orient='horizontal')
    separator.grid(row=12, columnspan=4, sticky = tk.EW)

    tk.Label(frame, text='View specific raw data:').grid(column=0, row=13, sticky=tk.W)
    plotpath = gui.selectSaveDirectory(frame, 14, "Read Directory")
    tk.Button(frame, text='View Plot').grid(column=2, row=15, padx=5,pady=5)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame, metadata

