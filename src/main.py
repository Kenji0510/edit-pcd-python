import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

o3d.visualization.webrtc_server.enable_webrtc()

pcd_path = "/home/kenji/workspace/cpp/ndt-matching/data/matching_results/cr/cr_100.pcd"
pcd = o3d.io.read_point_cloud(pcd_path)
print(pcd)

labels = np.array(pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True))
print(f"ラベル数: {labels.max()+1} クラスタ (ノイズは -1)")  

max_label = labels.max()
print(f"検出されたクラスタ数: {max_label+1}")

# 3. 点群に色付け (全体表示用)
colors = plt.get_cmap("tab20")(labels / (max_label if max_label>0 else 1))
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

geometries = [pcd]
# 4. 各クラスタのバウンディングボックスを追加
for i in range(max_label + 1):
    indices = np.where(labels == i)[0].tolist()
    cluster = pcd.select_by_index(indices)  # :contentReference[oaicite:15]{index=15}
    aabb = cluster.get_axis_aligned_bounding_box()  # :contentReference[oaicite:16]{index=16}
    aabb.color = (1, 0, 0)  # 赤でカラー設定
    geometries.append(aabb)

# 5. 可視化
o3d.visualization.draw_geometries(geometries)
# o3d.visualization.draw(geometries)

# for i in range(max_label + 1):
#     indices = np.where(labels == i)[0].tolist()
#     cluster = pcd.select_by_index(indices)
#     # cluster はクラスタ i の点群

# aabb = cluster.get_axis_aligned_bounding_box()
# aabb.color = (1, 0, 0)  # 赤でカラー設定
# o3d.visualization.draw_geometries([cluster, aabb])
# o3d.visualization.draw([cluster, aabb])
