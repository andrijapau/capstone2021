import tkinter as tk
import guiHelperFunctions as gui
from meta_data_handler import meta_data_handler


def create_left_frame(container):

    frame = tk.Frame(container)

    # grid layout for the input frame
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)
    frame.columnconfigure(1, weight=1)
    # Find what
    tk.Label(frame, text='Total counts:').grid(column=0, row=0, sticky=tk.W)
    keyword = tk.Entry(frame, width=25)
    keyword.focus()
    keyword.grid(column=1, row=0, sticky=tk.W)

    folderPath = gui.selectSaveDirectory(frame, 1)

    tk.Label(frame, text='Fibre Name:').grid(column=0, row=2, sticky=tk.W)
    fibname = tk.Entry(frame, width=25)
    fibname.grid(column=1, row=2, sticky=tk.W)

    tk.Label(frame, text='Distance Away from Ref SiPM:').grid(column=0, row=3, sticky=tk.W)
    distway = tk.Entry(frame, width=25)
    distway.grid(column=1, row=3, sticky=tk.W)

    tk.Label(frame, text='Fibre Length:').grid(column=0, row=4, sticky=tk.W)
    fiblen = tk.Entry(frame, width=25)
    fiblen.grid(column=1, row=4, sticky=tk.W)
    metadata = meta_data_handler(frame)
    tk.Button(frame, text='Run', width = "6", command = metadata.grab_meta_data).grid(column=2, row=5, sticky=tk.E)

    for widget in frame.winfo_children():
        widget.grid(padx=0, pady=5)

    return frame, metadata

