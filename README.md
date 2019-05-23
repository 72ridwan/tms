# Traffic Management System (TMS): A Data Science Analysis Project

TMS is a traffic management system that maps all the vehicles to the map.
The code is downloaded from the repository of [PJreddie's YOLOv3 Darknet](https://github.com/pjreddie/darknet).

## How to Use

### Preparing the project

1. Clone this repository

   ```
   git clone https://gitlab.cs.ui.ac.id/rachmat.ridwan/tms
   cd tms
   ```
   
1. Download the YOLOv3 pre-trained weights data to `darknet` folder.

1. Download the CCTV data and the maps from this drive.

1. Run `make` to compile the C source code

### Detecting the vehicles

Due to the time constraint of this project, we will be focusing only to detect
the vehicles in CCTV of Simpang 5 Patung Kuda Selatan at 12:00.
The video is located in cctv/SIMPANG 4 PATUNG KUDA.

1. Go to the root folder.

1. Run the `Pre-processing.ipynb` Jupyter notebook. In the code, you can see that

1. In the Linux environment, run `detect_and_save.py` to begin detection.
   You can pass the argument to resume the detection from certain frame name
   shall the process was terminated in the middle.
   ```
   python3 detect_and_save.py --start "0000006.jpg" --filetype "jpg" \
     --folder_path="../frame/cctv_SIMPANG 4 PATUNG KUDA_patungkuda selatan 120 0_x264.mp4"
   ```
   
### Other configurations

- ##### Operating on GPU
  Currently, this setup is made for CPU purposes and has not been tested on GPU using CUDNN.
  We have not implemented it due to environment complexity, especially on Windows.

- ##### 100% CPU Utilization
  The default setting is setup for normal CPU utilization. To utilize maximum CPU,
  go to `Makefile` and change the line `OPENMP=0` to `OPENMP=1`.

## Developers

- Agas Yanpratama (1606918396)
- Fardhan Dhiadribratha Sudjono (1606918332)
- Luqman Iffan Windrawan (1606876090)
- Muhammad Yudistira Hanifmuti (1606829560)
- Rachmat Ridwan (1606886974)

## Special Thanks

We would like to thank our lecturers, Mr. Ari Wibisono and Mr. Ivan Fanany, especially
Mr. Ari who had been giving us advices, the datasets, and the resources for this project.