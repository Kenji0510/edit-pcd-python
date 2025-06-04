import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# 対象ディレクトリ
pcd_dir = "../data/results/dbscan/each_cluster/combined_data"
save_dir = "../data/results/fpfh/combined_data"
os.makedirs(save_dir, exist_ok=True)

# ディレクトリ内の全.pcdファイルを取得
pcd_files = glob.glob(os.path.join(pcd_dir, "*.pcd"))

for pcd_path in pcd_files:
    print(f"Processing: {pcd_path}")
    # 点群の読み込み
    pcd = o3d.io.read_point_cloud(pcd_path)
    print(pcd)

    # 法線推定
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.05, max_nn=30))

    # FPFH特徴量の計算
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=100)
    )

    print("FPFH feature shape:", fpfh.data.shape)  # (33, 点数)

    mean_hist = np.mean(fpfh.data, axis=1)  # shape=(33,)
    std_hist = np.std(fpfh.data, axis=1)

    plt.figure(figsize=(10, 4))
    plt.bar(np.arange(33), mean_hist, yerr=std_hist, capsize=2)
    plt.xlabel("Bin index")
    plt.ylabel("Average FPFH value")
    plt.title(f"FPFH Histogram: {os.path.basename(pcd_path)}")
    save_path = os.path.join(save_dir, f"fpfh_hist_{os.path.splitext(os.path.basename(pcd_path))[0]}.png")
    plt.savefig(save_path)
    plt.close()
    print(f"Saved: {save_path}")