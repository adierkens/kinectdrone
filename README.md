#kinectdrone
> A library for tracking a quadcopter using a kinect

# Installation

## OSX

Make sure you have [libfreenect2](https://github.com/OpenKinect/libfreenect2) installed

And OpenCV installed
```
brew tap homebrew/science
brew install opencv3 --with-contrib --with-cuda --with-ffmpeg --with-tbb --with-qt5
```

Check if the python bindings work
```
 % python
 Python 2.7.10 (default, Sep 23 2015, 04:34:21)
 [GCC 4.2.1 Compatible Apple LLVM 7.0.0 (clang-700.0.72)] on darwin
 Type "help", "copyright", "credits" or "license" for more information.
 >>> import cv2
 >>>
```

Now run the install script
```
./install.sh
```

## Linux
TODO: Add steps for Linux installation

## Windows
TODO: Add steps for Windows installation

# Running


# Cascade Images

A helper python script for running classifiers on movies, and generating pictures to use in creating a cascade classifier.

```
 % ./cascadeImages.py -h
usage: cascadeImages.py [-h] [--output OUTPUT] [--negative] [--stream STREAM]
                        [--cascade CASCADE]
                        videofile

Filters a video for positive images for use with Cascade Classifiers

positional arguments:
  videofile             The video to process

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        The folder to store all of the positive images
  --negative, -n        Generate photos that don't contain the image
  --stream STREAM, -s STREAM
                        Stream the location data of the quad to a network
                        address. Supports http:// POST and ws://
  --cascade CASCADE, -c CASCADE
                        A cascade filter to use on the video stream
```


### Using the generated classifier for a quadcopter

```
./cascadeImages.py ../../videos/quad_ballroom.mov -c ../../classifiers/quadcopter-cascade-1500.xml
```

### Using the tld tracker

```
./cascadeImages.py ../../videos/quad_ballroom.mov
```

Once the video is started, press `i` on your keyboard. This will pause the video on that frame
Using your mouse, click the 4 corners of the area you wish to track. A green dot will be placed when you click.
<img width="962" alt="screen shot 2016-03-23 at 10 30 48 pm" src="https://cloud.githubusercontent.com/assets/13004162/14006794/41939f34-f147-11e5-89eb-9be4f3da4007.png">

After selecting the 4 points for the bounding box, press the space bar. 
The video will resume and a blue box will form around the object you're tracking.

<img width="961" alt="screen shot 2016-03-23 at 10 31 08 pm" src="https://cloud.githubusercontent.com/assets/13004162/14006795/449a08bc-f147-11e5-901a-a8a6f3868c8c.png">

Press `q` to quit

# TODO
 - Finish modularizing the code
 - Work on best way to get quad location in Frame
   - CamShiftFilter
   - KNNBackgroundSubtractor
   - CascadeClassifier
 - Define API for sending quad location to client apps
 - Switch to use setup.py



