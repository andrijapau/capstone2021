import tkinter as tk


class inputfield(tk.Frame):
    def __init__(self, name=None,master=None, xpos=0, ypos=0, sep = 150, width=10, placeholder = 0):
        super().__init__(master)
        self.placeholder = str(placeholder)
        self.xpos = xpos
        self.ypos = ypos
        self.sep = sep
        self.width = width
        if name == None:
            print("please enter valid label name")
        else:
            self.create_widgets(name)


    def create_widgets(self, name):
        self.label = tk.Label(self.master,text=name)
        self.entry = tk.Entry(self.master,width=self.width)
        self.entry.insert(0, self.placeholder)
        self.label.place(x=self.xpos,y=self.ypos)
        self.entry.place(x=self.xpos+self.sep,y=self.ypos)

    def get_entry(self):
        return self.entry.get()
