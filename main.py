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

def main():
  while True:
    frames = listener.waitForNewFrame()
    color = frames["color"]
    ir = frames["ir"]
    depth = frames["depth"]
    color = color.asarray()

    cv2.imshow('color', cv2.resize(color, (int(1920/2), int(1080/2))))
    listener.release(frames)
    key = cv2.waitKey(delay=1)

    if key == ord('q'):
      break

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    print 'Interrupted'
    device.stop()
    device.close()
