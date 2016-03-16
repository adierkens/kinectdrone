from Filter import BackgroundRemovalFilter
import cv2

class Drone:

  def __init__(self):
    self._backgroundSubtractor = BackgroundRemovalFilter()

  def getPosition(self, frames):
    return 0,0,0