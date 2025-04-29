import open3d as o3d
import numpy as np

mimoto_room_path = "../data/room/mimoto_room.pcd"

mimoto_room_pcd = o3d.io.read_point_cloud(mimoto_room_path)

print(mimoto_room_pcd)

cl, ind = mimoto_room_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=0.1)

denoised_pcd = mimoto_room_pcd.select_by_index(ind)
print(denoised_pcd)

o3d.visualization.draw_geometries([denoised_pcd])

points = np.asarray(denoised_pcd.points)
x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])

print(f"x: min={x_min}, max={x_max}")
print(f"y: min={y_min}, max={y_max}")

# x軸方向で13.0以上の点群を除去
mask = points[:, 0] < 13.0
filtered_pcd = denoised_pcd.select_by_index(np.where(mask)[0])

o3d.visualization.draw_geometries([filtered_pcd])

o3d.io.write_point_cloud("../data/removed_noise/room_pcd/filtered_mimoto_room02.pcd", filtered_pcd)