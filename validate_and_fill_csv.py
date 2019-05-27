#!/usr/bin/env python3

def validate_csv(region_name, limit, time):
    # Check if view folder exists
    _, region_views = zip(*[i for i in cctv_views_data if i[CCTV_REGION_NAME_INDEX] == region_name])

    view_paths = {}
    missing_folders = []
    print("Checking the folder paths...   ", end = "")

    for view_name in region_views:
        view_folder_path = './frame/cctv_{:}_{:} {:}_x264.mp4/'.format(region_name, view_name, time)
        if not os.path.isdir(view_folder_path):
            missing_folders.append(view_name)
        else:
            view_paths[view_name] = view_folder_path

    if len(missing_folders) > 0:
        print()
        raise FileNotFoundError("CCTV folder is missing for time {:}: {:}".format(time, ', '.join(missing_folders)))
    else:
        print("all folders are found!")

    print("Checking the CSV's...   ")

    view_max_csv = []
    view_csv_file_indices = []

    def digitize_name_and_discard_non_csv(file):
        filename, fileext = os.path.splitext(file)
        if fileext == '.csv':
            fileid = int(filename)
            return fileid
        else:
            return None

    # Get list of CSVs and ignore non-CSV files

    for view_name in region_views:
        csv_files = [digitize_name_and_discard_non_csv(file) for file in os.listdir(view_paths[view_name])]
        csv_files = [file for file in csv_files if file is not None]
        csv_files = sorted(csv_files)
        view_csv_file_indices.append(csv_files)
        view_max_csv.append(csv_files[-1])

    max_csv = max(view_max_csv)
    if (limit['end'] == -1):
        limit['end'] = max_csv

    view_missing_csv = []

    for view_index, view_name in enumerate(region_views):
        missing_csv = []
        file_indices = view_csv_file_indices[view_index]
        file_indices_length = len(file_indices)

        # Initialize the iteration index

        i_iteration = 0
        while i_iteration < file_indices_length:
            i_iteration += 1
            if file_indices[i_iteration - 1] >= limit['start']:
                break
        i_iteration -= 1

        # Keep record of everytime the ideal indices (j)
        # is not in the file indices.

        for j in range(limit['start'], limit['end'] + 1):
            if i_iteration >= file_indices_length:
                pass
            elif file_indices[i_iteration] == j:
                i_iteration += 1
                continue
            missing_csv.append(j)
        view_missing_csv.append(missing_csv)

        if len(missing_csv) > 0:
            print("Missing frame ids for {:}: {:}".format(view_name, ', '.join([str(i) for i in missing_csv])))

    return view_missing_csv

def run_darknet_on_missing_csv(region_name, limit, missing_csv, time):
    _, region_views = zip(*[i for i in cctv_views_data if i[CCTV_REGION_NAME_INDEX] == region_name])

    view_paths = []
    for view_name in region_views:
        view_folder_path = '../frame/cctv_{:}_{:} {:}_x264.mp4/'.format(region_name, view_name, time)
        view_paths.append(view_folder_path)

    os.chdir("darknet")
    detectors = [Detector(file_type='jpg', folder_path=view_path) for view_path in view_paths]
    view_index_iterators = [0 for i in range(len(missing_csv))]

    current_index = min([j for sub in missing_csv for j in sub])
    while current_index <= limit['end']:
        for view_index, view_missing_csv in enumerate(missing_csv):
            # Do not advance if there is no missing files anymore
            # for this view
            idx = view_index_iterators[view_index]
            if idx >= len(missing_csv[view_index]):
                continue

            # Do not run detectors if it's not a missing value.
            if current_index < missing_csv[view_index][idx]:
                continue
            else:
                view_index_iterators[view_index] += 1

            print("Processing view: {:} at frame: {:}".format(region_views[view_index], current_index)) 
            detectors[view_index].detect_single_frame(current_index)
        current_index += 1

if __name__ == '__main__':

    from argparse import ArgumentParser
    import os
    import sys
    import subprocess
    from detect_and_save import Detector

    example_usage =\
    """Example usage:
        ./validate_and_fill_csv.py\
            -r "SIMPANG 4 CUNGKING"
            -t "0700"
            -e "510"
            -i
       This will check in the SIMPANG 4 CUNGKING frame folder at
       time 07:00 from frame 0 to 510, whether there are any
       missing CSV detection files.
    """

    parser = ArgumentParser(description="Check the frame folder whether there are any missing CSV" +\
        "detection files. If any, the program can be made to invoke YOLOv3 object detection using Darknet.",
        epilog = example_usage)
    parser.add_argument("-r", "--region_name", dest="region_name", default="", required=True, action="store",
                        help="The region name that we want to analyze whether the CSV of all its views are complete")
    parser.add_argument("-s", "--start_limit", dest="start_limit", default="", action="store",
                        help="The start limit frame to check")
    parser.add_argument("-e", "--end_limit", dest="end_limit", default="", action="store",
                        help="The end limit frame to check")
    parser.add_argument("-t", "--time", dest="time", default="", action="store", required=True,
                        help="The time of the CCTV video. Write it in hhmm instead of hh:mm (without colon)")
    parser.add_argument("-l", "--filename_length", dest="filename_length", default="7", action="store",
                        help="File name length. For example: 0000000.csv -> file name length = 7. By default, " +\
                        "the length is set to 7.")
    parser.add_argument("-n", "--noinput", dest="noinput", default=False, action="store_true",
                        help="Choose whether the program should run without input."+\
                        "If there's any missing CSV, the program will automatically run Darknet.")

    args = parser.parse_args()
    region_name = args.region_name.strip()
    time = args.time.strip()
    file_name_length = int(args.filename_length.strip())

    try:
        start_limit = int(args.start_limit.strip())
    except ValueError:
        start_limit = 0

    try:
        end_limit = int(args.end_limit.strip())
    except ValueError:
        end_limit = -1

    limit = {'start': start_limit, 'end': end_limit}

    cctv_views_data = []
    CCTV_REGION_NAME_INDEX = 0
    CCTV_VIEW_NAME_INDEX = 1

    with open('cctv_views.csv', 'r') as infile:
        string = infile.read()
        string = string.splitlines()
        cctv_views_data = [i.split(',') for i in string[1:]] # We do not need the header

    _, region_views = zip(*[i for i in cctv_views_data if i[CCTV_REGION_NAME_INDEX] == region_name])

    missing_csvs = validate_csv(region_name, limit, time)

    if max([len(i) for i in missing_csvs]) == 0:
        print("All CSV frame have been checked. No missing CSV found.")
        sys.exit(0)

    run_darknet_response = ''

    if args.noinput:
        run_darknet_response = 'Y'

    while(run_darknet_response != 'Y' and run_darknet_response != 'n'):
        run_darknet_response = input("Do you want to run darknet on missing CSV frames [Y/n]? ")

    if run_darknet_response == 'n':
        sys.exit(0)

    run_darknet_on_missing_csv(region_name, limit, missing_csvs, time)