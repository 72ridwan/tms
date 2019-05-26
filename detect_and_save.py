#!/usr/bin/env python3

import os
import signal
import subprocess

class Detector():

    def __init__(self, file_type, folder_path):
        self.file_type = file_type.replace('.', '')
        self.folder_path = folder_path
        self.files = []
        self.pid = os.getpid()
        self.flag = {'interrupted':True}
        self.__bash_commands = ['./darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', '']

        if not os.path.isdir(self.folder_path):
            raise FileNotFoundError('Folder path not found: "' + self.folder_path + '"')
        self.files = sorted([i for i in os.listdir(self.folder_path) if os.path.splitext(i)[1] == '.' + self.file_type])

        with open("main_pid", "w") as outfile:
            outfile.write(str(os.getpid()))

    def warn_interrupt(self, sig, frame):
        self.flag['interrupted'] = True

    def detect_single_frame(self, frame_id):
        signal.signal(signal.SIGUSR1, self.warn_interrupt)

        fname = self.files[frame_id]
        fname_name, fname_ext = os.path.splitext(fname)

        # Detect object locations with darknet.
        # The output detection will be returned as CSV
        # in hasil_prediksi.csv

        self.flag['interrupted'] = False
        self.__bash_commands[-1] = self.folder_path + '//' + fname
        process = subprocess.Popen(self.__bash_commands, stdout=subprocess.PIPE)

        # Wait for the neural net process to finish...

        while not self.flag['interrupted']:
            pass

        # Move the hasil_prediksi to the original image file location
        # and rename it to match the frame number.

        boundaries_old_path = 'hasil_prediksi.csv'
        boundaries_new_path = self.folder_path + '//' + fname_name + '.csv'
        os.rename(boundaries_old_path, boundaries_new_path)
        print("Processing {:} done!".format(fname))

    def get_start_point_id(self, start_point):
        i_start = 0
        for i, fname in enumerate(self.files):
            if fname == start_point:
                i_start = i
                break
        return i_start

    def get_end_point_id(self, end_point, start_index = 0):
        i_end = len(self.files) - 1
        for i in range(start_index, len(self.files)):
            fname = self.files[i]
            if fname == end_point:
                i_end = i
                break
        return i_end

    def detect_from_filename(self, start_point, end_point):
        i_start = self.get_start_point_id(start_point)
        i_end   = self.get_end_point_id(end_point, i_start)
        print(i_start, i_end)

        for i in range(i_start, i_end+1):
            self.detect_single_frame(i)

if __name__ == '__main__':
    # Example usage:
    # python3 detect_and_save.py -s "0000004.jpg" -e "0000005.jpg" -t "jpg" -p="../frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 1200_x264.mp4"

    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-s", "--start", dest="start", default="", action="store",
                        help="Start frame file name, sorted alphabetically")
    parser.add_argument("-e", "--end", dest="end", action="store",  default="",
                        help="End frame file name, sorted alphabetically")
    parser.add_argument("-t", "--file_type", action="store", dest="filetype", default="", required=True,
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
    detector = Detector(file_type=file_type, folder_path = args.folder_path)
    detector.detect_from_filename(start_point, end_point)