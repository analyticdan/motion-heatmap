# motion-heatmap
This program takes in a video (or webcam footage) and produces a video with a trailing rainbow of colors behind wherever the program detects motion.

This program requires `OpenCV 3` (including some non-core modules) and `numpy`. To install both of these on Unix-like system, run:
```
pip install python-numpy opencv-contrib-python
```
or use the appropriate command for your favorite Python package manager.

Then, to use this program, `cd` into the repo and run the command:
```
python motion-heatmap.py [commands]
```
where `[commands]` may be any number of the following commands, separated by spaces:

* `-i [filename]`

  where `[filename]` is the name of some video file. This flag sets the input video file. If this flag is not used, the program will default to the webcam.

* `-o`

  This flag tells the program to write the output video to disk.  If the `-f` or `-of` flags are not used, the program will default to writing the program to `out.mp`.

* `-f [filename]`

  where `[filename]` is the name of the desired output file. If the `-o` or `-of` flag is not used, the program will not write any output to disk.

* `-of [filename]`

  where `[filename]` is the name of the desired output file.

* `-d`

  This flag tells the program to display the output as it processes the input video.

* `-r [rate]`

  where `[rate]` is some floating point number greater than 1, representing the inverse decay rate for the program. If this flag is not set, the program will default to an inverse decay rate of 1.01.

Note 1: The program can only output `mp4` files in its current state.

Note 2 : If multiple flags with the same functionality are used, the last instance of the flag will be used. For example:
```
python motion-heatmap.py -r 1.3 -o -f "file1.mp4" -of "file2.mp4" -r 1.5
```
will run the program with an inverse decay rate of 1.5 and not 1.3 and write the output of the program to `file2.mp4` and not `file1.mp4`.

Here is a video showcasing example outputs:

[![Video of example outputs.](https://img.youtube.com/vi/a2vCkVucpEc/hqdefault.jpg)](https://youtu.be/a2vCkVucpEc)

This project's implementation was built on top of Roberto Sannazzaro's example from his [Medium post](https://towardsdatascience.com/build-a-motion-heatmap-videousing-opencv-with-python-fd806e8a2340). He, in turn, was inspired by a project from Intel which is publicly available on [GitHub](https://github.com/intel-iot-devkit/python-cv-samples/tree/master/examples/motion-heatmap).

