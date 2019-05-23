#!/usr/bin/env python3

# Example usage:
# python3 detect_and_save.py -s "0000004.jpg" -e "0000005.jpg" -t "jpg" -p="../frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 1200_x264.mp4"

from argparse import ArgumentParser
import errno
import os
import signal
import subprocess
import sys
import time

parser = ArgumentParser()
parser.add_argument("-s", "--start", dest="start", default="", action="store",
                    help="Start frame file name, sorted alphabetically")
parser.add_argument("-e", "--end", dest="end", action="store",  default="",
                    help="End frame file name, sorted alphabetically")
parser.add_argument("-t", "--filetype", action="store", dest="filetype", default="", required=True,
                    help="File type of the image sequences. Required. Write the extension directly." +\
                        "Example: -t=jpg")
parser.add_argument("-p", "--folder_path", action="store", dest="folder_path", default="", required=True,
                    help="Folder path of the images. Required.")
                    
args = parser.parse_args()
start_point = args.start.strip()
end_point = args.end.strip()
file_type = args.filetype.strip().replace('.', '').lower()

is_start_point_defined = start_point != ''
is_end_point_defined = end_point != ''

os.chdir("darknet")

global flag
flag = {'interrupted':True}

def warn_interrupt(sig, frame):
    flag['interrupted'] = True

FOLDER_PATH = args.folder_path
darknet_command = "./darknet"

if not os.path.isdir(FOLDER_PATH):
    raise FileNotFoundError('Folder path not found: "' + FOLDER_PATH + '"')

bashCommands = [darknet_command, 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', '']

with open("main_pid", "w") as outfile:
    outfile.write(str(os.getpid()))
    print("PID of this Python process:", os.getpid())

signal.signal(signal.SIGUSR1, warn_interrupt)

files = os.listdir(FOLDER_PATH)

i_start = 0
i_end = len(files)-1

if is_start_point_defined:
    for i, fname in enumerate(files):
        if fname == start_point:
            i_start = i
            break
            
if is_end_point_defined:
    for i in range(i_start, len(files)):
        fname = files[i]
        if fname == end_point:
            i_end = i
            break
            
for i in range(i_start, i_end+1):
    fname = files[i]
    fname_name, fname_ext = os.path.splitext(fname)
    
    if fname_ext.replace('.', '').lower() != file_type:
        continue
    
    # Detect object locations with darknet.
    # The output detection will be returned as CSV
    # in hasil_prediksi.csv
    
    flag['interrupted'] = False
    bashCommands[-1] = FOLDER_PATH + '//' + fname
    process = subprocess.Popen(bashCommands, stdout=subprocess.PIPE)
    
    # Wait for the neural net process to finish...
    
    while not flag['interrupted']:
        time.sleep(0.1)
    print("Processing {:} done!".format(fname))
    
    # Move the hasil_prediksi to the original image file location
    # and rename it to match the frame number.
    
    boundaries_old_path = 'hasil_prediksi.csv'
    boundaries_new_path = FOLDER_PATH + '//' + fname_name + '.csv'
    os.rename(boundaries_old_path, boundaries_new_path)