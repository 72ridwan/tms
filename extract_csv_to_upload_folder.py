#!/usr/bin/env python3

import os
import sys
import shutil
import time

if not os.path.exists('detections'):
    os.makedirs('detections')

cctv_views = os.listdir('frame')

for subdir in cctv_views:
    if not os.path.isdir('frame/' + subdir):
        continue
    
    frame_csv_path = 'detections/' + subdir
    frame_path = 'frame/' + subdir
    if not os.path.exists(frame_csv_path):
        os.makedirs(frame_csv_path)
    
    csv_files = sorted([i for i in os.listdir(frame_path) if os.path.splitext(i)[1] == '.csv'])
    
    csv_file_length = str(len(csv_files))
    csv_file_char_len = len(csv_file_length)
    
    for i, file in enumerate(csv_files):
        shutil.copyfile(frame_path + '/' + file, frame_csv_path + '/' + file)
        modtime = os.path.getmtime(frame_path + '/' + file)
        os.utime(frame_csv_path + '/' + file, (modtime, modtime))
        if i % 30 == 0:
            if i >= 30:
                print("\rCopying {:} ... ({:}/{:})".format(subdir, str(i).zfill(csv_file_char_len), csv_file_length), end='')
    print("\rCopying {:} ... ({:}/{:})".format(subdir, csv_file_length, csv_file_length))
    print('Completed!')