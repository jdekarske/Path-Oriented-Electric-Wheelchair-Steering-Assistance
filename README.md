# Path-Oriented-Electric-Wheelchair-Steering-Assistance
* See abstract for research background and see [TJOE](idkyet) for full research paper.

## Starting from scratch.
* See the bill of materials in appendix of paper for parts used in this project. 
* The "backup image" file can be flashed to an sd card using [this tutorial](http://computers.tutsplus.com/articles/how-to-flash-an-sd-card-for-raspberry-pi--mac-53600) or your favorite method.

## Adding to an existing system.
* Install the OpenCV library using [this tutorial](http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/).

## Using the scripts.
* Add run command `sudo python <script directory> &` to `etc/profile`, use ampersand to run script in background.
* Use `sudo raspi-config` and switch to "auto login command line" or errors will occur! 
* Use `live_sidewalk_recogize.py` for the intended application described by the research documents.
* Use `sidewalkrecognize.py` to analyze images and adjust range parameters.
* Use `videowatcher.py` to see frame by frame if omxplayer isn't working.
* Use `vsidewalkrecognize.py` to analyze videofiles.

# TODO (`live_sidewalk_recognize.py`):
* Find more graceful way to use `onbuttonpress()`.
* Add cliff detection. When the centroid falls below a certain vertical coordinate.
* Add shadow detection. See article: ["Shadow Detection and Removal from a Single Image Using LAB Color Space"](url=http://www.degruyter.com/view/j/cait.2013.13.issue-1/cait-2013-0009/cait-2013-0009.xml)
* Improve framerate/optimize.
