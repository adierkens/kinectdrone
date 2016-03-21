#!../env/bin/python
import argparse
import Camera
import Tracking
import cv2
import gc

def getArguments():
  parser = argparse.ArgumentParser(description='kinect-drone - a utility to track a quadcopter using a kinect')
  parser.add_argument('--verbose', '-v', action='store_true', help='View debug information')
  parser.add_argument('--videofile', '-f', help='Use a video file rather than a live-feed')
  args = parser.parse_args()
  return args

def main():
  args = getArguments()
  camera = None
  if args.videofile:
    camera = Camera.VideoCamera(args.videofile)
  else:
    camera = Camera.getCamera()
  drone = Tracking.Drone()

  cv2.namedWindow('frame')

  def run():
    while True:
      frames = camera.getFrames()
      if frames is None:
        return
      frame = cv2.resize(frames['color'], (0,0), fx=0.5, fy=0.5)
      cv2.imshow('frame', frame)

      key = cv2.waitKey(1)
      if key == ord('q'):
        break
      del frame
      gc.collect()


  try:
    run()
  except Exception as e:
    print e
  finally:
    camera.stop()

if __name__ == '__main__':
  main()