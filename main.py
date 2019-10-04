import tkinter.filedialog as filedialog
from tkinter import END, Tk, Frame, Button, BooleanVar, StringVar, Label, Checkbutton, Entry
from paint import Paint
from network import NeuralNetwork


def SavePhoto(event):
  fn = filedialog.asksaveasfilename(filetypes=[("Image", "*.jpg")], defaultextension=[("Image", "*.jpg")])
  if fn is None:
    return
  paintApp.canvImage.save(fn)


def trainTrack():
  if trainFlag.get():
    targetInput.configure(state="normal")
  else:
    targetInput.configure(state="disabled")


def targetChange(event):
  if event.keycode >= 48 and event.keycode <= 57:
    targetInput.delete(0, END)
  else:
    return "break"


def readAndTrain(event):
  paintApp.canv.configure(state="disable")
  paintApp.canv.configure(bg="#e0e0e0")

  training_inputs = []
  for i in range(imageSize[0]):
    for j in range(imageSize[1]):
      if (255, 255, 255) == paintApp.canvImage.getpixel((i, j)):
        training_inputs.append(1)
      else:
        training_inputs.append(0)
  network.feedForward(training_inputs)

  if trainFlag.get():
    network.backProp([int(x == targetMsg.get()) for x in range(10)])

  result = network.getResults()
  predictionEntry.configure(text=result.index(max(result)))

  paintApp.canv.configure(state="normal")
  paintApp.canv.configure(bg="white")


def quitAndSave():
  network.saveModel("model.json")
  root.destroy()


root = Tk()
root.resizable(False, False)
defaultbg = root.cget('bg')
root.title = "Digits prediction Neural Network"


root.columnconfigure(3, weight=0)
root.rowconfigure(2, weight=0)


saveBtn = Button(root, text="Save", height=2, width=6)
saveBtn.bind("<Button-1>", SavePhoto)
saveBtn.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))


trainFlag = BooleanVar(value=0)
trainBox = Checkbutton(root, text="Training", variable=trainFlag, onvalue=1, offvalue=0, command=trainTrack)
trainBox.grid(row=0, column=2, padx=(10, 0), pady=(10, 0))


targetMsg = StringVar(root, value=0)
targetInput = Entry(textvariable=targetMsg, width=3, font=("TimesNewRoman", 15), justify="center")
targetInput.grid(row=0, column=3, padx=(10,0), pady=(10, 0))

targetInput.bind("<Key>", targetChange)


paintFrame = Frame(root, width=200, height=200, bd=1)
paintApp = Paint(paintFrame)
paintFrame.grid(row=1, column=0, columnspan=4, padx=10, pady=(10, 0))


predictionFrame = Frame(root)
predictionFrame.grid(row=2, column=0, sticky="we", columnspan=4, pady=10)

predictionFrame.columnconfigure(3, weight=0)
predictionFrame.rowconfigure(0, weight=0)

predictionLabel = Label(predictionFrame, text="Prediction: ", font=("TimesNewRoman", 10))
predictionLabel.grid(row=0, column=0, columnspan=2, padx=(10, 0), pady=10)

predictionEntry = Label(predictionFrame, text=0, state="disabled", width=3, font=("TimesNewRoman", 15), bg="#fff")
predictionEntry.grid(row=0, column=2, columnspan=2, padx=10, pady=10)


root.update_idletasks()
paintApp.setImage()


network = NeuralNetwork()
network.loadModel("model.json")

imageSize = paintApp.canvImage.size
paintApp.canv.bind("<ButtonRelease-1>", readAndTrain)

root.protocol("WM_DELETE_WINDOW", quitAndSave)
root.mainloop()