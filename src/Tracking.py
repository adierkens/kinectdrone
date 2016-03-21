from Filter import BackgroundRemovalFilter
import cv2

class Drone:

  def __init__(self):
    self._backgroundSubtractor = BackgroundRemovalFilter()

  def getPosition(self, frames):
    cv2.imshow('frame', frames['color'])
