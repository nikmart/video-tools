# @Author: Nik Martelaro <nikmart>
# @Date:   2018-02-01T22:01:27-05:00
# @Email:  nmartelaro@gmail.com
# @Filename: createClips.py
# @Last modified by:   nikmart
# @Last modified time: 2018-02-01T22:33:55-05:00

# Purpose: Create video clips based on the time markers provides in a CSV file.
# Settings: clip time, participant name

import os, sys

# CONSTANTS
CUT_TIME = 0
TIME = 0

# FUNCTIOINS
def create_clip(cut_in, cut_out):
    print("Cutting from {} to {}".format(cut_in, cut_out))
    # run an ffmpeg thread to create MP4 clips
    mp4 = 'ffmpeg -i ' + videoFile + ' -ss ' + \
        cut_in + \
        ' -to ' + \
        cut_out + \
        ' -c copy clip' + str(clip_counter) + '.mp4'
    print(mp4)
    os.system(mp4)

# SCRIPT
# Check for the command line inputs
if len(sys.argv) < 5:
    print("No video file or cut file given\nUsage: \
    python clipCreator.py [videoFile] [cutFile] [seconds] [startTime]")
    quit()
else:
    videoFile = sys.argv[1]
    cutFile = sys.argv[2]
    cutSeconds = int(sys.argv[3])
    startTime = float(sys.argv[4])


print("Cutting {} into {} second clips using {}".format(videoFile, cutSeconds, cutFile))

# Find all the cut points and create the clips
linenum = 0
clip_counter = 0
with open(cutFile, 'r') as f:
    for line in f:
        line = line.strip().split(",")
        print(line)
        if linenum != 0:
            question_time = float(line[TIME]) - startTime
            cut_time = question_time - cutSeconds
            print(cut_time, question_time)
            create_clip(cut_time, question_time)
        linenum += 1
