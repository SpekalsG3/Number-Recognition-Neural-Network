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
    self.canvImage = Image.new("RGB", self.getResolution(), (255, 255, 255))
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

  def getResolution(self):
    return (self.parent.winfo_width(), self.parent.winfo_height())