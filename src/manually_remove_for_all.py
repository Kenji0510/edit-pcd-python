import open3d as o3d
import numpy as np
import glob
import os
import re

# removed_noise_path = "../data/original_data/combined_data/combined_0.pcd"

# removed_noise_pcd = o3d.io.read_point_cloud(removed_noise_path)
# print(removed_noise_pcd)
pcd_dir = "/home/kenji/workspace/cpp/align_pcd/data/alignment_data/by_mimotos_matrix/combined_data"

# ファイル名から数値を抽出する関数
def extract_number(filename):
    match = re.search(r'combined_(\d+)\.pcd', filename)
    return int(match.group(1)) if match else -1

# ディレクトリ内の全.pcdファイルを取得し、数値順にソート
pcd_files = glob.glob(os.path.join(pcd_dir, "combined_*.pcd"))
pcd_files_sorted = sorted(pcd_files, key=lambda x: extract_number(os.path.basename(x)))

# 点群を順に読み込み、すべて足し合わせる
total_pcd = None
for pcd_path in pcd_files_sorted:
    print(f"Reading: {pcd_path}")
    pcd = o3d.io.read_point_cloud(pcd_path)
    if total_pcd is None:
        total_pcd = pcd
    else:
        total_pcd += pcd

print(total_pcd)

# x, y軸方向の最小値・最大値を取得
points = np.asarray(total_pcd.points)
x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])

print(f"x: min={x_min}, max={x_max}")
print(f"y: min={y_min}, max={y_max}")

# 可視化用にコーナー点を作成
corner_points = np.array([
    [x_min, y_min, 0],
    [x_min, y_max, 0],
    [x_max, y_min, 0],
    [x_max, y_max, 0]
])
corner_pcd = o3d.geometry.PointCloud()
corner_pcd.points = o3d.utility.Vector3dVector(corner_points)
corner_pcd.paint_uniform_color([1, 0, 0])  # 赤色

# 部屋点群とremoved_noise_pcdとコーナー点を同時に表示
# removed_noise_pcd.paint_uniform_color([0, 1, 0])  # 緑色
# removed_noise_pcd.paint_uniform_color([0.7, 0.7, 0.7])     # 薄いグレー

o3d.visualization.draw_geometries([total_pcd, total_pcd, corner_pcd])

# <-- 壁を削除 -->
# 壁を削除するための条件を設定
x_margin_right = 1.0
x_margin_left = 1.1
y_margin_top = 0.4
y_margin_bottom = 0.6

# 壁を削除
mask = (points[:, 0] > x_min + x_margin_right) & (points[:, 0] < x_max - x_margin_left) & \
       (points[:, 1] > y_min + y_margin_bottom) & (points[:, 1] < y_max - y_margin_top)

filtered_pcd = total_pcd.select_by_index(np.where(mask)[0])
print(filtered_pcd)

# 可視化
# filtered_pcd.paint_uniform_color([0, 1, 0])  # 緑色
# filtered_pcd.paint_uniform_color([0.7, 0.7, 0.7])     # 薄いグレー
o3d.visualization.draw_geometries([filtered_pcd, corner_pcd])

# 保存
# o3d.io.write_point_cloud("../data/results/manually_edit/removed_wall_mimoto_room.pcd", filtered_pcd)
o3d.io.write_point_cloud("../data/results/manually_edit/combined_data/removed_wall_total.pcd", filtered_pcd, write_ascii=True)
