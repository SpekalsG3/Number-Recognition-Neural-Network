import tkinter.filedialog as filedialog
from tkinter import *
from PIL import Image, ImageDraw

# import network


class Paint(Frame):
  def __init__(self, parent):
    self.parent = parent
    self.setUI()
    self.brush_size = 5
    self.brush_color = "black"

  def setUI(self):
    self.canv = Canvas(self.parent, bg="white")
    self.canv.pack(fill="both", expand=1)
    self.canv.bind("<Button-1>", self.clear)
    self.canv.bind("<B1-Motion>", self.draw)

  def setImage(self):
    self.canvImage = Image.new("RGB", (self.parent.winfo_width(), self.parent.winfo_height()), (255, 255, 255))
    self.canvDraw = ImageDraw.Draw(self.canvImage)

  def clear(self, *args):
    self.canv.delete("all")
    self.canvDraw.rectangle((0, 0, self.parent.winfo_width(), self.parent.winfo_height()), fill=(255, 255, 255, 255))

  def draw(self, event):
    self.canv.create_oval(event.x - self.brush_size,
                          event.y - self.brush_size,
                          event.x + self.brush_size,
                          event.y + self.brush_size,
                          fill=self.brush_color, outline=self.brush_color)
    self.canvDraw.ellipse((event.x - self.brush_size,
                           event.y - self.brush_size,
                           event.x + self.brush_size,
                           event.y + self.brush_size),
                           fill=self.brush_color, outline=self.brush_color)


def SavePhoto(event):
  fn = filedialog.asksaveasfilename(filetypes=[("Image", "*.jpg")], defaultextension=[("Image", "*.jpg")])
  if fn is None:
    return
  paintApp.canvImage.save(fn)


def Quit(event):
  global root
  root.destroy()


def trainTrack():
  if trainFlag.get():
    predictionFrame.configure(bg="#666")
    targetInput.configure(state=NORMAL)
  else:
    predictionFrame.configure(bg=defaultbg)
    targetInput.configure(state="disabled")


def targetChange(event):
  print (event)
  if event.keycode >= 48 and event.keycode <= 57:
    targetInput.delete(0, END)
  else:
    return "break"


root = Tk()
root.resizable(False, False)
defaultbg = root.cget('bg')
root.title = "Digits prediction Neural Network"


root.columnconfigure(3, weight=0)
root.rowconfigure(2, weight=0)


saveBtn = Button(root, text="Save", height=2, width=6)
saveBtn.bind("<Button-1>", SavePhoto)
saveBtn.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))


quitBtn = Button(root, text="Quit", height=2, width=6)
quitBtn.bind("<Button-1>", Quit)
quitBtn.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))


trainFlag = BooleanVar(value=1)
trainBox = Checkbutton(root, text="Training", variable=trainFlag, onvalue=1, offvalue=0, command=trainTrack)
trainBox.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))


targetMsg = StringVar(root, value=0)
targetInput = Entry(textvariable=targetMsg, width=3, font=("TimesNewRoman", 15), justify="center")
targetInput.grid(row=0, column=3, padx=(10,0), pady=(10, 0))

targetInput.bind("<Key>", targetChange)


paintFrame = Frame(root, width=200, height=200)
paintApp = Paint(paintFrame)
paintFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=(10, 0))


predictionFrame = Frame(root, bg="#666")
predictionFrame.grid(row=2, column=0, sticky="we", columnspan=4, pady=10)

predictionFrame.columnconfigure(3, weight=0)
predictionFrame.rowconfigure(0, weight=0)

predictionLabel = Label(predictionFrame, text="Prediction: ", font=("TimesNewRoman", 10))
predictionLabel.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=10)

predictionEntry = Label(predictionFrame, text=0, state="disabled", width=3, font=("TimesNewRoman", 15), bg="#fff")
predictionEntry.grid(row=0, column=2, columnspan=2, padx=10, pady=10)


root.update_idletasks()
paintApp.setImage()
root.mainloop()