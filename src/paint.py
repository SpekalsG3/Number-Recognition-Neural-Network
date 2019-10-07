from PIL import Image, ImageDraw
from tkinter import Frame, Canvas


class Paint(Frame):
  def __init__(self, parent):
    self.parent = parent
    self.setUI()
    self.brush_size = 10
    self.brush_color = "black"

  def setUI(self):
    self.canv = Canvas(self.parent, bg="white")
    self.canv.pack(fill="both", expand=1)
    self.canv.bind("<Button-1>", self.clear)
    self.canv.bind("<B1-Motion>", self.draw)

  def setImage(self):
    self.canvImage = Image.new("RGB", (self.parent.winfo_width(), self.parent.winfo_height()), (255, 255, 255))
    self.canvDraw = ImageDraw.Draw(self.canvImage)

  def clear(self, event):
    if self.canv.cget("state") == "disabled":
      return;
    self.canv.delete("all")
    self.canvDraw.rectangle((0, 0, self.canvImage.size[0], self.canvImage.size[1]), fill=(255, 255, 255))

  def getImage(self):
    return self.canvImage.resize(self.getSmallSize())

  def getSmallSize(self):
    imageRatio = 32 / self.parent.winfo_height()
    return (round(self.parent.winfo_width() * imageRatio), round(self.parent.winfo_height() * imageRatio))

  def draw(self, event):
    if self.canv.cget("state") == "disabled":
      return;
    self.canv.create_oval(event.x - self.brush_size,
                          event.y - self.brush_size,
                          event.x + self.brush_size,
                          event.y + self.brush_size,
                          fill=self.brush_color, outline=self.brush_color)
    # self.canvImage.putpixel((round(event.x * self.imageRatio), round(event.y * self.imageRatio)), (0, 0, 0))
    self.canvDraw.ellipse((event.x - self.brush_size,
                           event.y - self.brush_size,
                           event.x + self.brush_size,
                           event.y + self.brush_size,),
                           fill=self.brush_color, outline=self.brush_color)