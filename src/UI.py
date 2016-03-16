import cv2

class Window:

  def __init__(self, name):
    self._name = name

  def show(self, img):
    cv2.imshow(self._name, img)