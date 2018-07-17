# @Author: Nik Martelaro <nikmart>
# @Date:   2018-02-01T22:01:27-05:00
# @Email:  nmartelaro@gmail.com
# @Filename: createClips.py
# @Last modified by:   nikmart
# @Last modified time: 2018-07-17T13:53:55-05:00

# Purpose: Create video clips based on the time markers provides in a CSV file.
# Settings: clip time, participant name

import argparse
import glob
import os, sys
import pandas as pd
import numpy as np

# CONSTANTS
CUT_TIME = 0
TIME = 0

# FUNCTIOINS
def create_clip(video, participant, cut_in, duration, timestamp, out_dir):
    print("Cutting from {} to {}".format(cut_in, cut_in + duration))
    # run an ffmpeg thread to create MP4 clips
    mp4 = 'ffmpeg -ss ' + str(cut_in) + \
        ' -i ' + video + \
        ' -t ' + str(duration) + \
        ' -movflags faststart -vcodec copy -acodec copy {}/{}_{}.mov'.format(out_dir, participant, timestamp)
    print(mp4)
    os.system(mp4)

def getQueries(df_file):
    df = pd.read_csv(df_file)
    queries = df.query('response==1')
    times = pd.DatetimeIndex(queries.timestamp)
    times = times.astype(np.int64) / 10**9
    return times


# SCRIPT
# Check for the command line inputs
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True,
    help="path to the clean data directory of Is Now a Good Time participants")
ap.add_argument("-b", "--before", type=float, required=True,
    help="number of seconds to cut before a query")
ap.add_argument("-a", "--after", type=float, required=True,
    help="number of seconds to cut after a query")
ap.add_argument("-o", "--output", required=True,
    help="name of output directory for clips")
args = vars(ap.parse_args())
directory = args["directory"]
before = args["before"]
after = args["after"]
output = args["output"]

# Change into the main data directory
os.chdir(directory)
print(os.getcwd())

# Run through each participant directory
participants = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(os.path.abspath(directory), d))] #[3]

for participant in participants:
    # Get the video file, start time, and query time filenames
    try:
        video = glob.glob("{}/*.mov".format(participant,participant))[0]
        queries = getQueries(glob.glob("{}/*.csv".format(participant))[0])
        start = glob.glob("{}/*_videoStart.txt".format(participant))[0]
        print(video, queries, start)
    except:
        print("{} directory error, skipping".format(participant))
        pass

    print("Cutting {} {} seconds before and {} seconds after using {}".format(video, before, after, queries))

    try:
        output_dir = "{}/CLIPS/{}".format(participant,output)
        os.mkdir(output_dir)
    except FileExistsError:
        print("{}/CLIPS/{} exists, moving forward".format(participant,output))
        pass


    # Get the start time from the second line of the file
    with open(start, 'r') as f:
        for line in f:
            x = line
        startTime = float(x.split(': ')[-1])
        print("startime = {}".format(startTime))

    # Find all the cut points and create the clips
    linenum = 0
    for timestamp in queries:
        question_time = timestamp - startTime
        cut_time = question_time - before
        create_clip(video, participant, cut_time, before + after, timestamp, output_dir) # clipped before and after the question is asked
        linenum += 1

# REFERENCES
# [1] Getting filenames using glob: https://stackoverflow.com/questions/3964681/find-all-files-in-a-directory-with-extension-txt-in-python
# [2] Changing working directory: https://stackoverflow.com/questions/17359698/how-to-get-the-current-working-directory-using-python-3/17361545
# [3] https://code.i-harness.com/en/q/227eb - listiong only the top level directories
