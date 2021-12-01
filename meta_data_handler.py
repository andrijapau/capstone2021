
class meta_data_handler():
    def __init__(self, frame):
        self.frame = frame
        self.metadata = [None] * 5
        #counts, directory name, fiber name, Distance Away, fiber length

    def grab_meta_data(self):
        counter = 0
        for widget in self.frame.winfo_children():
            if widget.winfo_class() == 'Entry':
                self.metadata[counter] = widget.get()
                counter = counter + 1

