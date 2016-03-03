import cv2
import numpy as np

class Filter:

  def __init__(self):
    pass

  def apply(self, frame):
    return frame


class BackgroundRemovalFilter(Filter):

  def __init__(self):
    self.backgroundSubtractor = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=True)

  def apply(self, frame):
    return self.backgroundSubtractor.apply(frame)


class CamShiftFilter(Filter):

  def __init__(self, roiPoints):
    self._roiPoints = np.array(roiPoints)
    self._s = roiPoints.sum(axis=1)
    self._tl = roiPoints[np.argmin(self._s)]
    self._br = roiPoints[np.argmax(self._s)]
    self._termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1)
    self._initalized = False

  def _initialize(self, frame):
    roi = frame[self._tl[1]:self._br[1], self._tl[0]:self._br[0]]
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    self._roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
    self._roiHist = cv2.normalize(self._roiHist, self._roiHist, 0, 255, cv2.NORM_MINMAX)
    self._roiBox = (self._tl[0], self._tl[1], self._br[0], self._br[1])
    self._initalized = True

  def apply(self, frame):
    if not self._initalized:
        self._initalized(frame)
    backProject = cv2.calcBackProject([frame], [0], self._roiHist, [0, 180], 1)
    r, self._roiBox = cv2.CamShift(backProject, self._roiBox, self._termination)
    pts = np.int0(cv2.boxPoints(r))
    return [pts]