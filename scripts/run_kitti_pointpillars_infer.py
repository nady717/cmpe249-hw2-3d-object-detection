import os
import os.path as osp
import json

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import open3d as o3d

from mmdet3d.apis import init_model, inference_detector


def main():
    # 1) Config & checkpoint (the ones we already downloaded)
    config_file = 'configs/pointpillars/pointpillars_hv_secfpn_8xb6-160e_kitti-3d-3class.py'
    checkpoint_file = 'checkpoints/hv_pointpillars_secfpn_6x8_160e_kitti-3d-3class_20220301_150306-37dc2420.pth'

    # 2) Output dirs
    out_root = osp.expanduser('~/hw2_3d_results/weather_kitti_pointpillars')
    frame_dir = osp.join(out_root, 'frames')
    pc_dir = osp.join(out_root, 'pointclouds')
    meta_dir = osp.join(out_root, 'metadata')
    for d in (frame_dir, pc_dir, meta_dir):
        os.makedirs(d, exist_ok=True)

    # 3) Build model on GPU 0
    print('Loading model...')
    model = init_model(config_file, checkpoint_file, device='cuda:0')
    print('Model loaded.')

    # 4) KITTI point cloud directory (via your data symlink)
    pcd_dir = 'data/kitti/training/velodyne'
    all_files = sorted(
        [osp.join(pcd_dir, f) for f in os.listdir(pcd_dir) if f.endswith('.bin')]
    )

    if not all_files:
        raise RuntimeError(f'No .bin files found under {pcd_dir}')

    max_samples = 20  # you can increase later if you want

    for i, pcd_path in enumerate(all_files[:max_samples]):
        base = osp.splitext(osp.basename(pcd_path))[0]
        print(f'[{i+1}/{max_samples}] Processing {base} ...')

        # 5) Run inference
        result = inference_detector(model, pcd_path)

        # 6) Load raw KITTI point cloud: (N,4) = x,y,z,intensity
        points = np.fromfile(pcd_path, dtype=np.float32).reshape(-1, 4)
        xyz = points[:, :3]

        # 7) Save PLY point cloud
        ply_path = osp.join(pc_dir, base + '.ply')
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d.io.write_point_cloud(ply_path, pcd)
        # Some versions of mmdet3d return (result,) as a tuple or list
        if isinstance(result, (list, tuple)):
            result = result[0]

        # 8) Save detection metadata to JSON
        det3d = result.pred_instances_3d
        meta = {
            'file': pcd_path,
            'boxes_3d': det3d.bboxes_3d.tensor.cpu().numpy().tolist(),
            'scores_3d': det3d.scores_3d.cpu().numpy().tolist(),
            'labels_3d': det3d.labels_3d.cpu().numpy().tolist(),
        }
        json_path = osp.join(meta_dir, base + '.json')
        with open(json_path, 'w') as f:
            json.dump(meta, f)

        # 9) Save a simple BEV PNG (x vs y)
        png_path = osp.join(frame_dir, base + '.png')
        plt.figure(figsize=(6, 6))
        plt.scatter(
            xyz[:, 0],
            xyz[:, 1],
            s=0.2,
            c=xyz[:, 2],
            cmap='viridis',
        )
        plt.title(
            f'KITTI frame {base}\n#points={len(xyz)}, #dets={len(det3d.scores_3d)}'
        )
        plt.xlabel('X (m)')
        plt.ylabel('Y (m)')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(png_path, dpi=150)
        plt.close()

    print('✅ Done. Outputs in:', out_root)


if __name__ == '__main__':
    main()
