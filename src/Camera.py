import numpy as np
from pylibfreenect2 import Freenect2, OpenCLPacketPipeline, FrameType, SyncMultiFrameListener, Registration, Frame
import cv2

class Camera:

  def __init__(self):
    pass

  def getFrame(self):
    return None

  def stop(self):
    pass

class KinectCamera(Camera):

  def __init__(self):
    self.pipeline = OpenCLPacketPipeline()
    fn = Freenect2()
    self.device = fn.openDefaultDevice(pipeline=self.pipeline)
    self.listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)
    self.device.setColorFrameListener(self.listener)
    self.device.setIrAndDepthFrameListener(self.listener)
    self.device.start()
    # self.registration = Registration(self.device.getIrCameraParams(), self.device.getColorCameraParams())
    self.undistorted = Frame(512, 424, 4)
    self.registered = Frame(512, 424, 4)

  def getFrame(self):
    frames = self.listener.waitForNewFrame()
    # self.registration.apply(frames['color'], frames['depth'], self.undistorted, self.registered)
    # frames['registered'] = self.registration
    return frames

  def stop(self):
    self.device.stop()
    self.device.close()

class WebCam(Camera):

  def __init__(self):
    self._capture = cv2.VideoCapture(0)

  def getFrame(self):
    ret, frame = self._capture.read()
    return {
      'color': frame
    }

  def stop(self):
    self._capture.release()

def getCamera():
  devices = Freenect2().enumerateDevices()
  if devices > 0:
    return KinectCamera()

  print 'Kinect not found - falling back to webcam'
  return WebCam()