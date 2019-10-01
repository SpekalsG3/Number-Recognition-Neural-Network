from tkinter import *
from tkinter import filedialog
import network


class Paint(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.setUI()
        self.brush_size = 5
        self.brush_color = "black"

    def setUI(self):
        self.canv = Canvas(self.parent, bg="white")
        self.canv.pack(fill="both", expand=1)
        self.canv.bind("<Button-1>", lambda event: self.canv.delete("all"))
        self.canv.bind("<B1-Motion>", self.draw)

    def draw(self, event):
        self.canv.create_oval(event.x - self.brush_size,
                              event.y - self.brush_size,
                              event.x + self.brush_size,
                              event.y + self.brush_size,
                              fill=self.brush_color, outline=self.brush_color)


def SavePhoto(event):
    fn = filedialog.Open(root, filetypes=[("Image", "*.jpg")], defaultextension=[("Image", "*.jpg")]).show()


def Quit(event):
    global root
    root.destroy()


root = Tk()
root.title = "Digits prediction Neural Network"

root.columnconfigure(3, weight=0)
root.rowconfigure(1, weight=0)

saveBtn = Button(root, text="Save", height=2, width=6)
saveBtn.bind("<Button-1>", SavePhoto)
saveBtn.grid(row=0, column=0, padx=(10, 0), pady=10)

quitBtn = Button(root, text="Quit", height=2, width=6)
quitBtn.bind("<Button-1>", Quit)
quitBtn.grid(row=0, column=1, padx=(10, 0), pady=10)

paintFrame = Frame(root, width=200, height=200)
paintApp = Paint(paintFrame)
paintFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=0)

root.mainloop()

network.test()