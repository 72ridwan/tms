import os
FOLDER_PATH = './frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 1200_x264.mp4'
darknet_comand = "test_my_knowledge_of_c"
# TODO: Replace this with "darknet"
# once these steps has been achieved:
# For all files:
# 1. Detect object locations with darknet
# 2. The output detection will be returned as CSV
#    in hasil_prediksi.csv
# 3. Move the hasil_prediksi to the original image file location
#    and rename it to match the frame number.
# 
# Note: it will be nice if we can resume it.
# So expect this python to work with 

bashCommandFormat = "./test_my_knowledge_of_c detect cfg/yolov3.cfg yolov3.weights {:}"

with open("darknet/pid", "w") as outfile:
    outfile.write(os.getpid())

for fname in os.listdir(FOLDER_PATH):
    print(fname)
    