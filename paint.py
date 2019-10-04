from PIL import Image, ImageDraw
from tkinter import Frame, Canvas


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
    self.imageRatio = 32 / self.parent.winfo_height()
    self.canvImage = Image.new("RGB", tuple(int(x * self.imageRatio) for x in self.getResolution()), (255, 255, 255))
    self.canvDraw = ImageDraw.Draw(self.canvImage)

  def clear(self, event):
    if self.canv.cget("state") == "disabled":
      return;
    self.canv.delete("all")
    self.canvDraw.rectangle((0, 0, self.canvImage.size[0], self.canvImage.size[1]), fill=(255, 255, 255, 255))

  def draw(self, event):
    if self.canv.cget("state") == "disabled":
      return;
    self.canv.create_oval(event.x - self.brush_size,
                          event.y - self.brush_size,
                          event.x + self.brush_size,
                          event.y + self.brush_size,
                          fill=self.brush_color, outline=self.brush_color)
    self.canvDraw.ellipse((event.x * self.imageRatio - 0.5,
                           event.y * self.imageRatio - 0.5,
                           event.x * self.imageRatio + 0.5,
                           event.y * self.imageRatio + 0.5),
                           fill=self.brush_color, outline=self.brush_color)

  def getResolution(self):
    return (self.parent.winfo_width(), self.parent.winfo_height())