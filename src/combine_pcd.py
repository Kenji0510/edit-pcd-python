import open3d as o3d
import numpy as np
import glob
import os
import re

# ディレクトリパス
pcd_dir = "/home/kenji/workspace/cpp/align_pcd/data/none_person/livox_lidar_192_168_10_185/raw"

# ファイル名から数値を抽出してソート
def extract_number(filename):
    match = re.search(r'_(\d+)\.pcd', filename)
    return int(match.group(1)) if match else -1

pcd_files = glob.glob(os.path.join(pcd_dir, "*.pcd"))
pcd_files_sorted = sorted(pcd_files, key=lambda x: extract_number(os.path.basename(x)))

# 点群を順に読み込み、合成
total_pcd = None
for pcd_path in pcd_files_sorted:
    print(f"Reading: {pcd_path}")
    pcd = o3d.io.read_point_cloud(pcd_path)
    if total_pcd is None:
        total_pcd = pcd
    else:
        total_pcd += pcd

print(total_pcd)
# 必要なら保存
# o3d.io.write_point_cloud("combined_livox_lidar_192_168_10_185.pcd", total_pcd)

init_transform = np.array([
        [
            -0.999510759696,
            0.024226643579,
            0.019781767703,
            6.414355955818
        ],
        [
            -0.023740663936,
            -0.999419298753,
            0.024442861918,
            6.782590659609
        ],
        [
            0.020362450000,
            0.023961270000,
            0.999505490000,
            -1.085985510000
        ],
        [
            0.000000000000,
            0.000000000000,
            0.000000000000,
            1.000000000000
        ]
    ]
)

total_pcd.transform(init_transform)

room_back_avias = "/home/kenji/workspace/python3/pcd_operation/data/results/manually_edit/combined_data/removed_wall_total.pcd"
room_back_pcd = o3d.io.read_point_cloud(room_back_avias)

# o3d.visualization.draw_geometries([ room_back_pcd, total_pcd ], "Combined Point Cloud")
room_back_avias = room_back_pcd + total_pcd

save_path = "../data/results/combined_back_data/room_back_avias_mid360.pcd"
o3d.io.write_point_cloud(save_path, room_back_avias)