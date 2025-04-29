import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

o3d.visualization.webrtc_server.enable_webrtc()

total_pcd_path = "../data/removed_noise/total_pcd/filtered_avia6566_cr20pcd.pcd"
room_path = "../data/removed_noise/room_pcd/filtered_mimoto_room.pcd"

total_pcd = o3d.io.read_point_cloud(total_pcd_path)
room_pcd = o3d.io.read_point_cloud(room_path)
print(total_pcd)
print(room_pcd)

total_pcd.paint_uniform_color([0, 1, 0]) 

# <-- Downsampled -->
# room_pcd = room_pcd.voxel_down_sample(voxel_size=0.05)

# <-- Subtraction background -->
room_tree = o3d.geometry.KDTreeFlann(room_pcd)
diff_indices = []
threshold = 0.05

for i, point in enumerate(np.asarray(total_pcd.points)):
    [_, idx, dists] = room_tree.search_knn_vector_3d(point, 1)
    if dists[0] > threshold*2:
        diff_indices.append(i)

background_diff_pcd = total_pcd.select_by_index(diff_indices)
background_diff_pcd.paint_uniform_color([1, 0, 0]) 

o3d.visualization.draw_geometries([total_pcd, background_diff_pcd], "diff room_pcd between total_pcd")

o3d.io.write_point_cloud("../data/results/background_diff/background_diff.pcd", background_diff_pcd)

# labels = np.array(total_pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True))
# print(f"ラベル数: {labels.max()+1} クラスタ (ノイズは -1)")  

# max_label = labels.max()
# print(f"検出されたクラスタ数: {max_label+1}")

# # 3. 点群に色付け (全体表示用)
# colors = plt.get_cmap("tab20")(labels / (max_label if max_label>0 else 1))
# total_pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

# geometries = [total_pcd]
# # 4. 各クラスタのバウンディングボックスを追加
# for i in range(max_label + 1):
#     indices = np.where(labels == i)[0].tolist()
#     cluster = total_pcd.select_by_index(indices)  # :contentReference[oaicite:15]{index=15}
#     aabb = cluster.get_axis_aligned_bounding_box()  # :contentReference[oaicite:16]{index=16}
#     aabb.color = (1, 0, 0)  # 赤でカラー設定
#     geometries.append(aabb)

# # 5. 可視化
# o3d.visualization.draw_geometries(geometries)
# o3d.visualization.draw(geometries)

# for i in range(max_label + 1):
#     indices = np.where(labels == i)[0].tolist()
#     cluster = pcd.select_by_index(indices)
#     # cluster はクラスタ i の点群

# aabb = cluster.get_axis_aligned_bounding_box()
# aabb.color = (1, 0, 0)  # 赤でカラー設定
# o3d.visualization.draw_geometries([cluster, aabb])
# o3d.visualization.draw([cluster, aabb])
