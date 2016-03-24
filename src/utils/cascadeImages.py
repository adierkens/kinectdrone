#!../../env/bin/python
import os
import re
import cv2
import argparse
import numpy as np
import requests
import datetime

WINDOW_NAME = 'Cascade Filter'
frame = None
roiPoints = []
inputMode = False
roiBox = None
tracker = cv2.Tracker_create('TLD')
trackerInit = False
pastPoints = []

def getNextImageNumber(directory):
  files = os.listdir(directory)
  nextNumber = -1
  for f in files:
    match = re.search('positive(\d+)\.png', f)
    if match:
      nextNumber = max(nextNumber, int(match.group(1)))
  return nextNumber + 1

def getArguments():
  parser = argparse.ArgumentParser( description='Filters a video for positive images for use with Cascade Classifiers')
  parser.add_argument('videofile', help='The video to process')
  parser.add_argument('--output', '-o', help='The folder to store all of the positive images')
  parser.add_argument('--negative', '-n', help='Generate photos that don\'t contain the image', action='store_true')
  parser.add_argument('--stream', '-s', help='Stream the location data of the quad to a network address. Supports http:// POST and ws://')
  parser.add_argument('--cascade', '-c', help='A cascade filter to use on the video stream')
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

def stream(location, point):
  payload = {
    'x': point[0],
    'y': point[1],
    'z': 0,
    'timestamp': datetime.datetime.now()
  }

  def sendPostRequest():
    r = requests.post(location, json=payload)

  def sendWebSocket():
    pass

  try:
    thread.start_new_thread(sendRequest)
  except:
    print "Error: Unable to start thread"

def main():
  global frame, roiPoints, inputMode, roiBox, roiHist, trackerInit, pastPoints

  args = getArguments()
  imageNumber = 0
  if args.output:
    if not os.path.exists(args.output):
      os.makedirs(args.output)
    else:
      imageNumber = getNextImageNumber(args.output) 
  
  capture = cv2.VideoCapture(args.videofile)
  cv2.namedWindow(WINDOW_NAME)
  cv2.setMouseCallback(WINDOW_NAME, handleWindowClick)

  cascade = None
  quads = None

  if args.cascade:
    cascade = cv2.CascadeClassifier(args.cascade)

  while capture.isOpened():
    ret, origFrame = capture.read()
    if not ret:
      break
    frame = cv2.resize(origFrame, (0,0), fx=0.5, fy=0.5)
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    grayFrame = cv2.cvtColor(origFrame, cv2.COLOR_BGR2GRAY)

    if cascade:
      quads = cascade.detectMultiScale(grayFrame)

    if args.output and args.negative:
      cv2.imwrite("./%s/negative%d.png" % (args.output, imageNumber), origFrame)
      imageNumber += 1

    if roiBox is not None:
      if not trackerInit:
        tracker.init(hsvFrame, (roiBox[0], roiBox[1], roiBox[2] - roiBox[0], roiBox[3] - roiBox[1]))
        trackerInit = True

      (r2, trackerBox) = tracker.update(hsvFrame)
      p1 = (int(trackerBox[0]), int(trackerBox[1]))
      p2 = (int(trackerBox[0] + trackerBox[2]), int(trackerBox[1] + trackerBox[3]))

    
      currentPosition = ( (p1[0] + p2[0])/2, (p1[1] + p2[1])/2  )
      
      if currentPosition[0] > 0 and currentPosition[1] > 0:
        pastPoints.append(currentPosition)
        roi = origFrame[p1[1]*2:p2[1]*2, p1[0]*2:p2[0]*2]

        height, width, channels = roi.shape
        if height > 0 and width > 0:
          cv2.imshow('roi', roi)
          if args.output:
            cv2.imwrite("./%s/positive%d.png" % (args.output, imageNumber) , roi)
          imageNumber += 1
          if args.stream:
            stream(args.stream, currentPosition)

      cv2.rectangle(frame, p1, p2, (250, 0, 0), 2)
      cv2.rectangle(hsvFrame, p1, p2, (250, 0, 0), 2)
      drawPoints(hsvFrame, pastPoints)
    
    if quads is not None:
      for (x,y,w,h) in quads:
        cv2.rectangle(frame, (x/2,y/2), ((x+w)/2, (y+h)/2), (255, 0, 0), 2)
    
    cv2.imshow(WINDOW_NAME, frame)

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
