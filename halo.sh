CURR_DIR="./frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 1200_x264.mp4";
cd "./frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 1200_x264.mp4";
hasil=`find . -maxdepth 1 -mindepth 1 -printf '%f\n'`

# echo $$ >> './darknet/main_pid'
# "./darknet detect cfg/yolov3.cfg yolov3.weights data/dog.jpg"