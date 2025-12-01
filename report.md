REPORT 
Homework 2: 3D Object Detection (CMPE 249)
1. Overview

This report documents my implementation of Homework 2 using MMDetection3D on the SJSU HPC cluster.
I ran 3D object detection with the PointPillars model on:

KITTI 3D Dataset

Weather-KITTI (KITTI with weather-modified scans)

For both datasets, I successfully generated:

PNG frames (BEV LiDAR visualizations)

PLY point clouds with predicted points

JSON prediction metadata

Demo videos created from the PNG frames

3D Open3D screenshots

All results were transferred from HPC → my Mac for visualization and submission.

2. Environment Setup (HPC3 – g17)

A dedicated conda environment was created:

conda create -n hw2_3d python=3.10 -y
conda activate hw2_3d


Installed key packages:

PyTorch 2.9.1 + CUDA 12.6

Torchvision 0.24.1

MMCV 2.1.0

MMEngine

MMDetection3D (editable install)

NumPy, Matplotlib, Open3D (local)

Hardware:

NVIDIA A40 (CUDA 12.6)

HPC node: g17.hpc.coe

Verified GPU acceleration worked

3. Dataset Setup

In ~/mmdetection3d/data/ I linked the course datasets:

ln -s /data/cmpe249-fa25/kitti kitti
ln -s /data/cmpe249-fa25/weather_kitti weather_kitti


The structure was correctly recognized by the MMDetection3D pipeline.

4. Model

I used the PointPillars pretrained model for 3-class KITTI detection:

Config:

configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py


Checkpoint:

hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth

5. Inference Pipeline

I wrote and used a custom inference script:

run_kitti_pointpillars_infer.py


This script:

Loads KITTI or Weather-KITTI

Runs the pretrained PointPillars detector

Saves for each frame:

frames/XXXXX.png (BEV point cloud visualizations)

pointclouds/XXXXX.ply

metadata/XXXXX.json

Example results directory
hw2_3d_results/
   kitti_pointpillars/
       frames/
       pointclouds/
       metadata/
   weather_kitti_pointpillars/
       frames/
       pointclouds/
       metadata/


Inference finished successfully for ALL 20 frames on both datasets.

6. Local Visualization

After transferring results to macOS using scp, I used Open3D to view PLY point clouds:

import open3d as o3d
pcd = o3d.io.read_point_cloud("000000.ply")
o3d.visualization.draw_geometries([pcd])


I rotated and zoomed the 3D clouds and captured screenshots.
These are included in the results.

7. Attempts to Generate Camera-View Bounding Boxes (Important)

The homework optionally allows the use of camera-view images showing bounding boxes.
I attempted to generate these using several official MMDetection3D tools:

Tools tested

tools/visualizations/browse_dataset.py

tools/misc/visualize_results.py

Old-style vs. new-style MMDetection3D configs

JSON → PKL conversion

mmengine installation issues

Obstacles Encountered
1. Version Mismatch Between Config + Visualizer

My config uses the new MMDetection3D format

My HPC-installed visualize_results.py uses the old format, expecting:

cfg.data.test

.pkl files

different structure for predictions

This produced errors like:

AttributeError: 'ConfigDict' object has no attribute 'data'
ValueError: The results file must be a pkl file

2. Visualization Tool Required .pkl Predictions

But my inference script saves per-frame JSON files.
Converting them manually still triggered format mismatches.

3. mmengine Installation Issues

HPC repeatedly showed PyPI timeout warnings:

ConnectTimeoutError: connection to pypi.org timed out


Even after successful installation, the visualizer still failed due to incompatible config interfaces.

4. browse_dataset.py Missing

Some newer visualizers were missing entirely from the HPC build of MMDetection3D.

⭐ IMPORTANT NOTE (Justification)

Despite multiple attempts, camera-view bounding box images could not be generated due to:

HPC package version constraints

Incompatibility between config architecture and visualizer tool

Inconsistent MMDetection3D versions required for the visualizer

However:

✔ The homework DOES NOT require camera images with boxes.
✔ BEV LiDAR PNGs are valid visualizations of detected objects.
✔ The demo video from BEV frames shows detections over time.
✔ Open3D screenshots visualize the 3D structure.

And MOST importantly:

✔ ALL required deliverables were successfully produced:

PNG frames

PLY files

JSON metadata

Screenshots of detected objects (BEV + 3D)

Demo videos

The instructor’s guideline only requires “screenshots of detected objects”, not necessarily RGB camera images.

8. Results Summary
KITTI

Good detection performance

Stable point cloud visuals

Clear bounding box counts in BEV images

Video shows consistent tracking across frames

Weather-KITTI

Weather distortion lowers point density

Some detections reduced

Point cloud structure still clear

Video illustrates performance drop in severe weather

9. Takeaways

MMDetection3D inference and result saving were fully successful.

Open3D visualization worked perfectly on macOS.

Accessing newer MMDetection3D visualizers on HPC was infeasible due to version conflicts.

Despite visualizer issues, BEV + 3D results fully satisfy homework criteria.

10. Submitted Deliverables

report.md

README.md

Custom inference script

Results for both datasets:

PNG frames

PLY point clouds

JSON metadata

Demo videos

Open3D screenshots

GitHub repository with reproducibility instructions

Full gzipped results folder for Canvas submission

End of Report
