# cmpe249-hw2-3d-object-detection
CMPE 249 – Homework 2: 3D Object Detection (mmdetection3d)



This repository contains my implementation for Homework 2 using
**MMDetection3D**.\
I used the **PointPillars** model and ran inference on **two datasets**:

-   **KITTI 3D**
-   **Weather-KITTI** (KITTI with weather variations)

All required artifacts are included:\
PNG frames, PLY point clouds (with predictions), JSON metadata, demo
videos, and screenshots.

------------------------------------------------------------------------

##  Repository Structure

    .
    ├── report.md
    ├── README.md
    ├── scripts/
    │   └── run_kitti_pointpillars_infer.py     # Custom inference script
    ├── results/
    │   ├── kitti_pointpillars/
    │   │   ├── frames/                         # sample frames (not full dataset)
    │   │   ├── pointclouds/                    # sample PLY files
    │   │   ├── metadata/                       # sample JSON files
    │   │   ├── kitti_pointpillars_demo.mp4     # demo video
    │   │   ├── kitti_detection_1.png           # screenshot (2D detection)
    │   │   ├── kitti_detection_2.png           # screenshot (optional)
    │   │   └── kitti_open3d_screenshot.png     # screenshot (3D point cloud)
    │   │
    │   └── weather_kitti_pointpillars/
    │       ├── frames/
    │       ├── pointclouds/
    │       ├── metadata/
    │       ├── weather_kitti_pointpillars_demo.mp4
    │       ├── weather_kitti_detection_1.png
    │       ├── weather_kitti_detection_2.png
    │       └── weather_open3d_screenshot.png

------------------------------------------------------------------------

## Environment Setup (HPC)

Create conda environment:

``` bash
conda create -n hw2_3d python=3.10 -y
conda activate hw2_3d
```

Install PyTorch (CUDA 12.6):

``` bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
```

Install MMCV and MMDetection3D:

``` bash
cd ~
git clone https://github.com/open-mmlab/mmdetection3d.git
cd mmdetection3d
pip install -v -e .
```

Verify:

``` bash
python -c "import torch; print('CUDA:', torch.cuda.is_available())"
python -c "import mmcv; print(mmcv.__version__)"
```

------------------------------------------------------------------------

##  Dataset Setup

Inside `mmdetection3d/data`:

``` bash
cd ~/mmdetection3d
mkdir -p data
cd data

ln -s /data/cmpe249-fa25/kitti kitti
ln -s /data/cmpe249-fa25/weather_kitti weather_kitti
```

------------------------------------------------------------------------

##  Model Used

Model: **PointPillars**\
Config:

    configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py

Checkpoint:

    hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth

------------------------------------------------------------------------

##  Running Inference on HPC

Script:

    scripts/run_kitti_pointpillars_infer.py

Example (KITTI):

``` bash
python scripts/run_kitti_pointpillars_infer.py   --config configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py   --checkpoint checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth   --out_dir ~/hw2_3d_results/kitti_pointpillars   --num_samples 20
```

Weather-KITTI:

``` bash
python scripts/run_kitti_pointpillars_infer.py   --config configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py   --checkpoint checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth   --out_dir ~/hw2_3d_results/weather_kitti_pointpillars   --num_samples 20
```

------------------------------------------------------------------------

##  Creating Demo Videos (Local)

KITTI video:

``` bash
cd ~/Downloads/hw2_3d_results/kitti_pointpillars
ffmpeg -framerate 10 -i frames/%06d.png   -c:v libx264 -pix_fmt yuv420p   kitti_pointpillars_demo.mp4
```

Weather-KITTI video:

``` bash
cd ~/Downloads/hw2_3d_results/weather_kitti_pointpillars
ffmpeg -framerate 10 -i frames/%06d.png   -c:v libx264 -pix_fmt yuv420p   weather_kitti_pointpillars_demo.mp4
```

------------------------------------------------------------------------

##  Open3D Visualization

Viewer script:

``` python
import open3d as o3d
import sys

if len(sys.argv) < 2:
    print("Usage: python view_ply.py <file.ply>")
    exit()

pcd = o3d.io.read_point_cloud(sys.argv[1])
o3d.visualization.draw_geometries([pcd])
```

Run:

``` bash
python view_ply.py 000000.ply
```

------------------------------------------------------------------------

##  Summary of Results

-   Strong performance on **KITTI**\
-   Slight degradation in **Weather-KITTI** (visibility + weather
    noise)\
-   Both datasets produce valid 3D/2D detections\
-   Demo videos show stable predictions\
-   Screenshots illustrate detections clearly

------------------------------------------------------------------------

## Reproducibility Steps

1.  Set up conda environment\
2.  Install MMDetection3D\
3.  Link datasets\
4.  Download checkpoint\
5.  Run inference\
6.  Transfer results\
7.  Create videos\
8.  View PLY files\
9.  Review and compare outputs

------------------------------------------------------------------------

##  Homework Deliverables Included

-   `report.md`\
-   `README.md`\
-   Scripts\
-   Demo videos\
-   Screenshots\
-   Sample frames + sample PLY/JSON




