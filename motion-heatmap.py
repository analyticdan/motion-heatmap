import numpy as np
import cv2
import sys

def decay(accumulator):
    return accumulator / decay_const

def rejuvenate(fgmask, accumulator):
    fgmask = np.where(fgmask > 0, 1, 0)
    fgmask = np.stack((fgmask,) * 3, axis=-1)
    return np.maximum(accumulator, fgmask * rejuvenate_const)

decay_rate = 1.01 # Generally values between 1.01 and 2.0 seem reasonable.
display = False
output = False

input_file = 0 # Default to zero, which asks the OS to use the webcam.
output_file = 'out.mp4'

i = 1
while i < len(sys.argv):
    if sys.argv[i] == '-d':
        display = True
    elif sys.argv[i] == '-o':
        output = True
    elif sys.argv[i] == '-f':
        i += 1
        if i < len(sys.argv):
            output_file = sys.argv[i]
        else:
            print('Error: To use the "-f" flag, the program must be provided '
                  'the name of an output file as the next argument.')
            exit(-1)
    elif sys.argv[i] == '-of':
        output = True
        i += 1
        if i < len(sys.argv):
            output_file = sys.argv[i]
        else:
            print('Error: To use the "-of" flag, the program must be provided '
                  'the name of an output file as the next argument.')
            exit(-1)
    elif sys.argv[i] == '-i':
        i += 1
        if i < len(sys.argv):
            input_file = sys.argv[i]
        else:
            print('Error: To use the "-i" flag, the program must be provided '
                  'the name of an input file as the next argument.')
            exit(-1)
    elif sys.argv[i] == '-r':
        i += 1
        if i < len(sys.argv):
            try:
                decay_rate = float(sys.argv[i])
            except ValueError:
                print('Error: To use the "-r" flag, the program must be provided '
                      'a number as a decay rate.')
                exit(-1)
            if decay_rate <= 0:
                print('Error: To use the "-r" flag, the program must be provided '
                      'a positive number as a decay rate.')
                exit(-1)
        else:
            print('Error: To use the "-r" flag, the program must be provided '
                  'the decay rate as the next argument.')
            exit(-1)
    else:
        print('Unrecognized program parameter: {0}'.format(sys.argv[i]))
        exit(-1)
    i += 1

video = cv2.VideoCapture(input_file)
frame_shape = (int(video.get(4)), int(video.get(3)), 3)
decay_const = np.full(frame_shape, [decay_rate, 1, 1])
rejuvenate_const = np.full(frame_shape, [179, 225, 225])
accumulator = np.full(frame_shape, [0, 225, 225])

bg_subtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

frames = []

while video.isOpened():
    try:
        ok, frame = video.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        fgmask = bg_subtractor.apply(gray)
        accumulator = decay(accumulator)
        accumulator = rejuvenate(fgmask, accumulator)
        frame = cv2.cvtColor(accumulator.astype(np.uint8), cv2.COLOR_HSV2BGR)
        if display:
            cv2.imshow('Video', frame)
            cv2.waitKey(1)
        frames.append(frame)
    except KeyboardInterrupt:
        break

if output:
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(video.get(5))
    out_shape = (int(video.get(3)), int(video.get(4)))
    out = cv2.VideoWriter(output_file, fourcc, fps, out_shape)
    for frame in frames:
        out.write(frame)
    out.release()

video.release()
cv2.destroyAllWindows()
        
