# Path-Oriented-Electric-Wheelchair-Steering-Assistance
* See abstract for research backgroud and see <a href "url=idkyet">TJOE</a> for full research paper.
## Starting from scratch.
* See the bill of materials in appendix of paper for parts used in this project. 
* The "backup image" file can be flashed to an sd card using <a href "url="http://computers.tutsplus.com/articles/how-to-flash-an-sd-card-for-raspberry-pi--mac-53600"> this tutorial</a> or your favorite method.
## Adding to an existing system.
* Install the OpenCV library using <a href "url=http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/">this tutorial.</a>
## Using the scripts.
* Add run command "sudo python <script directory> &" to etc/profile, use ampersand to run script in background.
* Use "sudo raspi-config" to switch to auto login command line or errors will occur! 
* Use live_sidewalk_recogize.py for the inteded application described by the research documents.
* Use sidewalkrecognize.py to analyze images and adjust range parameters.
* Use videowather.py to see frame by frame if omxplayer isn't working.
* Use vsidewalkrecognize.py to analyze videofiles.
# TODO (livesidewalkrecognize.py):
* Find more graceful way to use Onbuttonpress().
* Add shadow detection. See article: <a href"url=http://www.degruyter.com/view/j/cait.2013.13.issue-1/cait-2013-0009/cait-2013-0009.xml">"Shadow Detection and Removal from a Single Image Using LAB Color Space".</a>
* Improve framerate/optimize.