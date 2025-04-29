import open3d as o3d
import numpy as np

removed_noise_path = "../data/removed_noise/room_pcd/filtered_mimoto_room02.pcd"

removed_noise_pcd = o3d.io.read_point_cloud(removed_noise_path)
print(removed_noise_pcd)

# x, y軸方向の最小値・最大値を取得
points = np.asarray(removed_noise_pcd.points)
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
removed_noise_pcd.paint_uniform_color([0, 1, 0])  # 緑色
removed_noise_pcd.paint_uniform_color([0.7, 0.7, 0.7])     # 薄いグレー

o3d.visualization.draw_geometries([removed_noise_pcd, removed_noise_pcd, corner_pcd])

# <-- 壁を削除 -->
# 壁を削除するための条件を設定
x_margin_right = 0.5
x_margin_left = 1.1
y_margin_top = 0.4
y_margin_bottom = 0.4

# 壁を削除
mask = (points[:, 0] > x_min + x_margin_right) & (points[:, 0] < x_max - x_margin_left) & \
       (points[:, 1] > y_min + y_margin_bottom) & (points[:, 1] < y_max - y_margin_top)

filtered_pcd = removed_noise_pcd.select_by_index(np.where(mask)[0])
print(filtered_pcd)

# 可視化
filtered_pcd.paint_uniform_color([0, 1, 0])  # 緑色
filtered_pcd.paint_uniform_color([0.7, 0.7, 0.7])     # 薄いグレー
o3d.visualization.draw_geometries([filtered_pcd, corner_pcd])

# 保存
o3d.io.write_point_cloud("../data/results/manually_edit/removed_wall_mimoto_room.pcd", filtered_pcd)
