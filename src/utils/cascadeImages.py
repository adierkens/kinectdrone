#!../../env/bin/python
import os
import cv2
import argparse
import numpy as np

WINDOW_NAME = 'Cascade Filter'
frame = None
roiPoints = []
inputMode = False
roiBox = None
tracker = cv2.Tracker_create('TLD')
trackerInit = False
pastPoints = []

def getArguments():
  parser = argparse.ArgumentParser( description='Filters a video for positive images for use with Cascade Classifiers')
  parser.add_argument('videofile', help='The video to process')
  parser.add_argument('outputFolder', help='The folder to store all of the positive images')
  args = parser.parse_args()
  return args

def handleWindowClick(event, x, y, flags, param):
  global frame, roiPoints, inputMode
  if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPoints) < 4:
    roiPoints.append((x,y))
    cv2.circle(frame, (x,y), 4, (0, 255, 0), 2)
    cv2.imshow(WINDOW_NAME, frame)

def drawPoints(img, points):
  for pnt in points:
    cv2.circle(img, pnt, 2, (0, 255, 0), 1)

def crop(img, x, y, w, h):
  return img[y:h, x:w]

def main():
  global frame, roiPoints, inputMode, roiBox, roiHist, trackerInit, pastPoints

  imageNumber = 0
  args = getArguments()

  if not os.path.exists(args.outputFolder):
    os.makedirs(args.outputFolder)

  if os.listdir(args.outputFolder) != []:
    print "Output folder is non-empty"
    return

  capture = cv2.VideoCapture(args.videofile)
  cv2.namedWindow(WINDOW_NAME)
  cv2.setMouseCallback(WINDOW_NAME, handleWindowClick)

  while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
      break
    frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    if roiBox is not None:
      if not trackerInit:
        tracker.init(hsvFrame, (roiBox[0], roiBox[1], roiBox[2] - roiBox[0], roiBox[3] - roiBox[1]))
        trackerInit = True

      (r2, trackerBox) = tracker.update(hsvFrame)
      p1 = (int(trackerBox[0]), int(trackerBox[1]))
      p2 = (int(trackerBox[0] + trackerBox[2]), int(trackerBox[1] + trackerBox[3]))

      currentPosition = ( (p1[0] + p2[0])/2, (p1[1] + p2[1])/2  )
      pastPoints.append(currentPosition)

      roi = frame[p1[1]:p2[1], p1[0]:p2[0]]

      height, width, channels = roi.shape
      print "Height: %d Width: %d" % (height, width)
      if height > 0 and width > 0:
        cv2.imshow('roi', roi)
        cv2.imwrite("./%s/positive%d.png" % (args.outputFolder, imageNumber) , roi)
        imageNumber += 1

      cv2.rectangle(frame, p1, p2, (250, 0, 0), 2)
      cv2.rectangle(hsvFrame, p1, p2, (250, 0, 0), 2)
      drawPoints(hsvFrame, pastPoints)

    cv2.imshow(WINDOW_NAME, hsvFrame)

    key = cv2.waitKey(1)
    if key == ord('q'):
      break
    elif key == ord('i'):
      inputMode = True
      while len(roiPoints) < 4:
        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(0)
      roiPoints = np.array(roiPoints)
      s = roiPoints.sum(axis=1)
      tl = roiPoints[np.argmin(s)]
      br = roiPoints[np.argmax(s)]
      roiBox = (tl[0], tl[1], br[0], br[1])

if __name__ == '__main__':
  main()
