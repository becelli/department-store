class Controller:
    def __init__(self):
        pass

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
