import argparse
import Camera
import Tracking
import Beacon

def getArguments():
  parser = argparse.ArgumentParser(description='kinect-drone - a utility to track a quadcopter using a kinect')
  parser.add_argument('--verbose', '-v', action='store_true', help='View debug information')
  parser.add_argument('--videofile', '-f', help='Use a video file rather than a live-feed')
  args = parser.parse_args()
  return args

def main():
  args = getArguments()
  camera = None
  if args['videofile'] is not None:
    camera = Camera.VideoCamera(args['videofile'])
  else:
    camera = Camera.getCamera()
  drone = Tracking.Drone()

  def run():
    while True:
      frames = camera.getFrames()
      position = drone.getPosition(frames)
      Beacon.beacon({
        "event": "quad-position",
        "data": {
          "x": position[0],
          "y": position[1],
          "z": position[2]
        }
      })
      print 'New position: X:%s Y:%s Z:%s' % position

  try:
    run()
  except:
    pass
  finally:
    camera.stop()

if __name__ == '__main__':
  main()