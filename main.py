#!./env/bin/python
import numpy as np
import cv2
from pylibfreenect2 import Freenect2, SyncMultiFrameListener, FrameType, Registration, Frame, OpenCLPacketPipeline

pipeline = OpenCLPacketPipeline()

classifier = cv2.CascadeClassifier('./src/classifiers/symaX5C-1.xml')

fn = Freenect2()
device = fn.openDefaultDevice(pipeline=pipeline)
listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth )

device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)
device.start()

registration = Registration(device.getIrCameraParams(), device.getColorCameraParams())

undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)

color = None
roiPoints = []
inputMode = False
itter = 1

def handleTrackbar(value):
  global iter
  iter = value

def selectROI(event, x, y, flags, param):
  global color, roiPoints, inputMode

  if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPoints) < 4:
    roiPoints.append((x,y))
    cv2.circle(color, (x,y), 4, (0, 255, 0), 2)
    cv2.imshow('color', color)


def main():
  global color, roiPoints, inputMode, itter

  cv2.namedWindow('color')
  cv2.setMouseCallback('color', selectROI)
  cv2.createTrackbar('tb1', 'color', 1, 10, handleTrackbar)

  termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 80, 1)
  roiBox = None
  quit = False
  tracker = cv2.Tracker_create('TLD')
  tracker_init = False
  tracker_box = (263.0,462.0,98,51)

  fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=True)
  firstFrame = None

  while True:
    frames = listener.waitForNewFrame()
    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]

    kernel = np.ones((5,5),np.uint8)

    registration.apply(color, depth, undistorted, registered)
    color = cv2.resize(color.asarray(), (int(1920/2), int(1080/2)))
    hsv = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
    fgmask = fgbg.apply(hsv)

    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
      firstFrame = gray

    # frameDelta = cv2.absdiff(firstFrame, gray)
    # thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    # thresh = cv2.dilate(thresh, None, iterations=10)
    #
    # _, cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #
    # for c in cnts:
    #   if cv2.contourArea(c) < 500:
    #     continue
    #   (cx, cy, cw, ch) = cv2.boundingRect(c)
    #   cv2.rectangle(color, (cx, cy), (cx+cw, cy+ch), (0,0,255), 2)

    if roiBox is not None:
      backProj = cv2.calcBackProject([fgmask], [0], roiHist, [0, 180], 1)
      if not tracker_init:

        tracker.init(hsv, (roiBox[0], roiBox[1], roiBox[2] - roiBox[0], roiBox[3] - roiBox[1]))
        tracker_init = True
      (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
      (r2, tracker_box) = tracker.update(hsv)

      p1 = (int(tracker_box[0]), int(tracker_box[1]))
      p2 = (int(tracker_box[0] + tracker_box[2]), int(tracker_box[1] + tracker_box[3]))
      cv2.rectangle(hsv, p1, p2, (250,0,0), 2)
      cv2.rectangle(color, p1, p2, (250,0,0), 2)

      pts = np.int0(cv2.boxPoints(r))

      cv2.polylines(color, [pts], True, (0, 255, 0), 2)
      cv2.polylines(hsv, [pts], True, (0, 255, 0), 2)

    cv2.imshow('hsv', hsv)
    cv2.imshow('color', color)
    cv2.imshow('frame', fgmask)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("i") and len(roiPoints) < 4:
      inputMode = True
      while len(roiPoints) < 4:
        cv2.imshow("color", color)
        cv2.waitKey(0)
      roiPoints = np.array(roiPoints)
      s = roiPoints.sum(axis=1)
      tl = roiPoints[np.argmin(s)]
      br = roiPoints[np.argmax(s)]

      roi = hsv[tl[1]:br[1], tl[0]:br[0]]
      roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
      roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
      roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
      roiBox = (tl[0], tl[1], br[0], br[1])

    elif key == ord('q'):
      quit = True

    listener.release(frames)
    if quit:
      break

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    device.stop()
    device.close()
