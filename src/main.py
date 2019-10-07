import tkinter.filedialog as filedialog
import csv
from PIL import Image, ImageDraw
from tkinter import END, Tk, Frame, Button, BooleanVar, StringVar, Label, Checkbutton, Entry
from paint import Paint
from network import NeuralNetwork


def SavePhoto(event):
  fn = filedialog.asksaveasfilename(filetypes=[("Image", "*.jpg")], defaultextension=[("Image", "*.jpg")])
  if fn is None:
    return
  paintApp.getImage().save(fn)


def iterateImage(imageObj, state):
  row = 0
  column = 0
  resized_data = []
  while row != imageSize[1]-1 or column != imageSize[0]-1:
    (r, g, b) = imageObj.getpixel((column, row))
    pixel = (r + g + b) / 3
    resized_data.append(state(pixel))
    if column == imageSize[0]-1:
      column = -1
      row += 1
    column += 1
  (r, g, b) = imageObj.getpixel((imageSize[0]-1, imageSize[1]-1))
  pixel = (r + g + b) / 3
  resized_data.append(state(pixel))
  return resized_data 


def resizeData(data):
  img = Image.new("RGB", (28, 28), (255, 255, 255))
  row = 0
  column = 0
  for pix in data:
    img.putpixel((column, row), (int(pix), int(pix), int(pix)))
    if column == 27:
      column = -1
      row += 1
    column += 1

  img = img.resize(imageSize)
  return iterateImage(img, lambda pixel: 1 if pixel > 225 else 0)

def openTrainingData(event):
  fn = filedialog.askopenfilename(filetypes=[("Excel", "*.csv"), ("Image", "*.jpg")])
  if fn is None:
    return

  data = iter(csv.reader(open(fn)))
  next(data)
  column = 0
  i = 1

  for element in data:
    element = iter(element)
    trainNumber = int(next(element))
    print("{} iteration. Next number {}.".format(i, trainNumber))

    network.feedForward(resizeData(element))
    network.backProp([int(x == trainNumber) for x in range(10)])

    i += 1
  print("Training done.")


def predictData(data):
  predict_right = 0
  predict_wrong = 0
  column = 0
  for element in data:
    element = iter(element)
    trainNumber = int(next(element))

    network.feedForward(resizeData(element))
    
    result = network.getResults()
    predicted = result.index(max(result))
    if predicted == trainNumber:
      predict_right += 1
    else:
      predict_wrong += 1

    print("{} times right and {} times wrong".format(predict_right, predict_wrong))
  print("Predicts done. {}% accuracy".format(round(100*(predict_right / (predict_right + predict_wrong)))))


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


def readAndPredict(event):
  paintApp.canv.configure(state="disable")

  training_inputs = []
  imageObj = paintApp.getImage()

  network.feedForward(iterateImage(imageObj, lambda pixel: 1 if pixel < 25 else 0))

  if trainFlag.get():
    network.backProp([int(x == int(targetMsg.get())) for x in range(10)])

  result = network.getResults()
  print(result)
  predictionEntry.configure(text=result.index(max(result)))

  paintApp.canv.configure(state="normal")


def displayInputs(inputs, path):
  img = Image.new("RGB", imageSize, (255, 255, 255))
  row = 0
  column = 0
  for pix in inputs:
    pix = round(pix * 255)
    img.putpixel((row, column), (pix, pix, pix))
    if row == imageSize[0]-1:
      row = -1
      column += 1
    row += 1
  img.save(path)


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


openDataBtn = Button(root, text="Open Data", height=2, width=8)
openDataBtn.bind("<Button-1>", openTrainingData)
openDataBtn.grid(row=0, column=1, padx=(10, 0), pady=(10, 0))


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

imageSize = paintApp.getSmallSize()
paintApp.canv.bind("<ButtonRelease-1>", readAndPredict)

root.protocol("WM_DELETE_WINDOW", quitAndSave)
root.mainloop()