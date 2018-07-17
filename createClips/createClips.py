# @Author: Nik Martelaro <nikmart>
# @Date:   2018-02-01T22:01:27-05:00
# @Email:  nmartelaro@gmail.com
# @Filename: createClips.py
# @Last modified by:   nikmart
# @Last modified time: 2018-02-01T22:33:55-05:00

# Purpose: Create video clips based on the time markers provides in a CSV file.
# Settings: clip time, participant name

import glob
import os, sys

# CONSTANTS
CUT_TIME = 0
TIME = 0

# FUNCTIOINS
def create_clip(cut_in, cut_out, timestamp, out_dir):
    print("Cutting from {} to {}".format(cut_in, cut_out))
    # run an ffmpeg thread to create MP4 clips
    mp4 = 'ffmpeg -i ' + videoFile + ' -ss ' + \
        str(cut_in) + \
        ' -to ' + \
        str(cut_out) + \
        ' -c copy {}{}_{}.mov'.format(out_dir, participantNumber, timestamp)
    print(mp4)
    os.system(mp4)

# SCRIPT
# Check for the command line inputs
if len(sys.argv) < 3:
    print("No participant directory given\nUsage: \
    python clipCreator.py [participantDirectory] [seconds]")
    quit()
else:
    participantDirectory = sys.argv[1]
    cutSeconds = float(sys.argv[2])
    os.chdir(participantDirectory) # [2]
    print("Moving into {}".format(os.getcwd()))


# Get the files we need [1]
videoFile = glob.glob("*.mov")[0]
cutFile = glob.glob("*.csv")[0]
startFile = glob.glob("*.txt")[0]
participantNumber = participantDirectory.split('/')[-1] #last element of list is the participantNumber
print(participantNumber)
print("Cutting {} into {} second clips using {}".format(videoFile, cutSeconds, cutFile))
os.mkdir('{}_no-response'.format(participantNumber))
os.mkdir('{}_response'.format(participantNumber))

# Get the start time from the second line of the file
with open(startFile, 'r') as f:
    for line in f:
        x = line
    startTime = float(x.split(': ')[-1])
    print("startime = {}".format(startTime))

# Find all the cut points and create the clips
linenum = 0
with open(cutFile, 'r') as f:
    for line in f:
        line = line.strip().split(",")
        #print(line)
        if linenum != 0:
            timestamp = float(line[TIME])
            question_time = timestamp - startTime
            cut_time = question_time - cutSeconds
            #print(cut_time, question_time)
            create_clip(cut_time, question_time, timestamp, '{}_no-response/'.format(participantNumber)) # clipped up to question
            create_clip(cut_time, question_time + 5, timestamp, '{}_response/'.format(participantNumber)) # clipped 5 seconds after the questions is asked
        linenum += 1

# REFERENCES
# [1] Getting filenames using glob: https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
# Changing working directory: https://stackoverflow.com/questions/17359698/how-to-get-the-current-working-directory-using-python-3/17361545
