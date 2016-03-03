from Filter import BackgroundRemovalFilter, CamShiftFilter
import Camera
import cv2

class Drone:

  def __init__(self, camera):
    self._camera = camera

  def start(self):
    while True:
      frame = self._camera.getFrame()
      cv2.imshow('color', frame['color'])

  def stop(self):
    self._camera.stop()

def main():
  camera = Camera.getCamera()
  drone = Drone(camera)

  try:
    drone.start()
  except KeyboardInterrupt:
    pass
  finally:
    drone.stop()


if __name__ == '__main__':
  main()
