import open3d as o3d
import numpy as np

avia01_path = "../data/avia/avia_65.pcd"
avia02_path = "../data/avia/avia_66.pcd"
mid360_path = "../data/mid360/cr_20.pcd"

avia01_pcd = o3d.io.read_point_cloud(avia01_path)
avia02_pcd = o3d.io.read_point_cloud(avia02_path)
mid360_pcd = o3d.io.read_point_cloud(mid360_path)

total_pcd = mid360_pcd + avia01_pcd + avia02_pcd

print(total_pcd)

# 点群のZ座標範囲を取得
points = np.asarray(total_pcd.points)
z_min = np.min(points[:, 2])
z_max = np.max(points[:, 2])

floor_limit = z_min + 0.7
ceiling_limit = z_max - 0.3

mask = (points[:, 2] > floor_limit) & (points[:, 2] < ceiling_limit)
filtered_pcd = total_pcd.select_by_index(np.where(mask)[0])

print(filtered_pcd)
o3d.visualization.draw_geometries([filtered_pcd])

o3d.io.write_point_cloud("../data/removed_noise/filtered_avia6566_cr20pcd.pcd", filtered_pcd)