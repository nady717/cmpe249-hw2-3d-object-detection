# 📄 report.md — Homework 2: 3D Object Detection (CMPE 249)

## **1. Overview**
This report documents my implementation of Homework 2 using **MMDetection3D** on the SJSU HPC cluster.  
I ran **3D object detection with the PointPillars model** on:

- **KITTI 3D Dataset**
- **Weather-KITTI** (KITTI with weather-modified scans)

For both datasets, I successfully generated:

- **PNG frames** (BEV LiDAR visualizations)  
- **PLY point clouds** with predicted 3D detections  
- **JSON prediction metadata**  
- **Demo videos** created from the PNG frames  
- **3D Open3D screenshots**

All results were transferred from HPC → macOS for visualization and submission.

---

## **2. Environment Setup (HPC3 – g17)**

### Conda environment
```bash
conda create -n hw2_3d python=3.10 -y
conda activate hw2_3d
```

### Key packages installed
- PyTorch 2.9.1 + CUDA 12.6  
- Torchvision 0.24.1  
- MMCV 2.1.0  
- MMEngine  
- MMDetection3D (editable install)  
- NumPy, Matplotlib  
- Open3D (local visualization on Mac)

### Hardware
- GPU: **NVIDIA A40**  
- CUDA: **12.6**  
- HPC node: **g17.hpc.coe**  

GPU acceleration confirmed.

---

## **3. Dataset Setup**
Datasets were linked into the mmdetection3d project:

```bash
ln -s /data/cmpe249-fa25/kitti kitti
ln -s /data/cmpe249-fa25/weather_kitti weather_kitti
```

MMDetection3D successfully recognized dataset structure.

---

## **4. Model**
I used the official **PointPillars** model for KITTI 3D detection.

**Config file:**  
```
configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py
```

**Checkpoint:**  
```
hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth
```

---

## **5. Inference Pipeline**
I created and used a custom inference script:

```
run_kitti_pointpillars_infer.py
```

The script:

- Loads KITTI or Weather-KITTI  
- Runs the pretrained PointPillars detector  
- Saves for each frame:
  - `frames/XXXXX.png`
  - `pointclouds/XXXXX.ply`
  - `metadata/XXXXX.json`

---

## **6. Local Visualization (Open3D)**

Point clouds were visualized on macOS:

```python
import open3d as o3d
pcd = o3d.io.read_point_cloud("000000.ply")
o3d.visualization.draw_geometries([pcd])
```

Screenshots were taken and included in the results.

---

# **7. Attempts to Generate Camera-View Bounding Boxes (Important)**

The homework does **not** explicitly require RGB camera-view boxes, but I attempted it extensively.

### Tools tested:
- `visualize_results.py`
- `browse_dataset.py`
- Conversion JSON → PKL
- Installing/upgrading mmengine
- Multiple syntax variations

### **Major roadblocks**
#### **1. Version mismatch**
The HPC version of MMDetection3D uses **old config structure**:

- expects `cfg.data.test`
- expects old dataset wrappers  
- expects legacy `.pkl` result format  

My installed version uses **new config structure**, without `cfg.data.*`.

This caused:

```
AttributeError: 'ConfigDict' object has no attribute 'data'
```

#### **2. Tool requires .pkl predictions**
But MMDetection3D now produces lists of per-frame JSON files.

Even after converting to `.pkl`, the tool still rejected the format.

#### **3. PyPI connectivity issues**
HPC repeatedly failed with:

```
ConnectTimeoutError: pypi.org timed out
```

making upgrades unreliable.

#### **4. Missing visualizer**
Some expected newer tools were not available in the HPC build.

---

# ⭐ **Conclusion**
**Camera-view bounding box PNGs could NOT be generated due to:**

- mismatched MMDetection3D versions  
- incompatible config structure  
- outdated visualizer tools on HPC  
- strict `.pkl` format requirement  
- missing modules  

After hours of attempts and multiple errors, these images could not be produced.

### ✔ BUT: The homework does NOT require RGB box images.  
### ✔ BEV PNG + Open3D screenshots fully satisfy the requirement:  
**“Include screenshots of detected objects.”**

And all other outputs are complete.

---

## **8. Results Summary**

### **KITTI**
- Clear detections in BEV  
- Smooth inference  
- Video shows consistent detections  

### **Weather-KITTI**
- Harder due to environmental distortion  
- Still produced valid detection metadata  
- Demos and screenshots generated successfully  

---

## **9. Takeaways**

- Inference and result generation were fully successful  
- Visualization worked well using Open3D  
- HPC version differences caused camera-view failures  
- Still met all deliverable requirements  

---

## **10. Submitted Deliverables**
- `report.md`  
- `README.md`  
- Custom inference script  
- KITTI and Weather-KITTI:
  - PNG frames
  - PLY point clouds
  - JSON metadata
  - Demo videos
  - Open3D screenshots  
- GitHub repository  
- Full results tar.gz on Canvas  

---

# **End of Report**
