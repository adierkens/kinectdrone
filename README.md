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
```
./main.py
```

# TODO
 - Finish modularizing the code
 - Work on best way to get quad location in Frame
   - CamShiftFilter
   - KNNBackgroundSubtractor
   - CascadeClassifier
 - Define API for sending quad location to client apps
 - Switch to use setup.py



