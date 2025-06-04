import open3d as o3d
import numpy as np
import glob
import os
import re

# 背景点群パス
room_path = "../data/results/combined_back_data/room_back_avias_mid360.pcd"
room_pcd = o3d.io.read_point_cloud(room_path)

# 対象ディレクトリ
pcd_dir = "/home/kenji/workspace/cpp/align_pcd/data/alignment_data/by_mimotos_matrix/combined_data"
save_dir = "../data/results/background_diff/processed_data"
os.makedirs(save_dir, exist_ok=True)

# ファイル名から番号を抽出してソート
def extract_number(filename):
    match = re.search(r'combined_(\d+)\.pcd', filename)
    return int(match.group(1)) if match else -1

pcd_files = glob.glob(os.path.join(pcd_dir, "combined_*.pcd"))
pcd_files_sorted = sorted(pcd_files, key=lambda x: extract_number(os.path.basename(x)))

voxel_size = 0.025  # 必要に応じて調整
threshold = 0.020  # 必要に応じて調整

for pcd_path in pcd_files_sorted:
    print(f"Processing: {pcd_path}")
    total_pcd = o3d.io.read_point_cloud(pcd_path)
    total_pcd = total_pcd.voxel_down_sample(voxel_size)

    room_tree = o3d.geometry.KDTreeFlann(room_pcd)
    diff_indices = []
    for i, point in enumerate(np.asarray(total_pcd.points)):
        [_, idx, dists] = room_tree.search_knn_vector_3d(point, 1)
        if dists[0] > threshold*2:
            diff_indices.append(i)

    background_diff_pcd = total_pcd.select_by_index(diff_indices)
    save_path = os.path.join(save_dir, f"background_diff_{extract_number(os.path.basename(pcd_path))}.pcd")
    o3d.io.write_point_cloud(save_path, background_diff_pcd)
    print(f"Saved: {save_path}")