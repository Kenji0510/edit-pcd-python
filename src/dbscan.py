import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import json  # 追加
import glob
import os

# PCDファイル群をナンバリング順に取得
pcd_dir = "/home/kenji/workspace/python3/mimotos_avias/data/removed_data"
pcd_files = sorted(
    glob.glob(os.path.join(pcd_dir, "background_diff_*.pcd")),
    key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1])
)

# pcd_path = "../data/results/background_diff/combined_data/background_diff.pcd"

loop_index = 0

for pcd_path in pcd_files:
    pcd = o3d.io.read_point_cloud(pcd_path)
    print(f"Processing: {pcd_path}")
    print(pcd)

    eps = 0.12
    min_points = 20

    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points = min_points, print_progress=True))
    print(f"ラベル数: {labels.max()+1} クラスタ (ノイズは -1)")  

    max_label = labels.max()
    print(f"検出されたクラスタ数: {max_label+1}")

    # 3. 点群に色付け (全体表示用)
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label>0 else 1))
    pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

    geometries = [pcd]
    cluster_info = {}  # 追加

    # 4. 各クラスタのバウンディングボックスを追加
    for i in range(max_label + 1):
        indices = np.where(labels == i)[0].tolist()
        cluster = pcd.select_by_index(indices)  # :contentReference[oaicite:15]{index=15}
        aabb = cluster.get_axis_aligned_bounding_box()  # :contentReference[oaicite:16]{index=16}
        aabb.color = (1, 0, 0)  # 赤でカラー設定
        geometries.append(aabb)

        # --- クラスタ情報を取得 ---
        points = np.asarray(cluster.points)
        x_min, x_max = float(np.min(points[:, 0])), float(np.max(points[:, 0]))
        y_min, y_max = float(np.min(points[:, 1])), float(np.max(points[:, 1]))
        z_min, z_max = float(np.min(points[:, 2])), float(np.max(points[:, 2]))
        num_points = int(points.shape[0])
        width = x_max - x_min
        depth = y_max - y_min
        height = z_max - z_min

        cluster_info[f"cluster_{i}"] = {
            "num_points": num_points,
            "x_min": x_min, "x_max": x_max,
            "y_min": y_min, "y_max": y_max,
            "z_min": z_min, "z_max": z_max,
            "width": width,
            "depth": depth,
            "height": height
        }

    # 5. 可視化
    # o3d.visualization.draw_geometries(geometries)
    #o3d.visualization.draw(geometries)

    # 各クラスタごとに色付きで保存
    for j in range(max_label + 1):
        indices = np.where(labels == j)[0].tolist()
        cluster = pcd.select_by_index(indices)
        # クラスタごとに色を付与
        color = plt.get_cmap("tab20")(j / (max_label if max_label > 0 else 1))[:3]
        cluster.paint_uniform_color(color)
        o3d.io.write_point_cloud(f"../data/results/dbscan/each_cluster/20250530-1643/cluster_{loop_index:02d}_{j:02d}.pcd", cluster)



    # 全体（色付き）の点群も保存
    o3d.io.write_point_cloud(f"../data/results/dbscan/overall/20250530-1643/colored_clusters_{loop_index:02d}.pcd", pcd)

    # --- クラスタ情報をJSONで保存 ---
    with open(f"../data/results/dbscan/overall/20250530-1643/cluster_info{loop_index:02d}.json", "w") as f:
        json.dump(cluster_info, f, indent=2, ensure_ascii=False)

    loop_index += 1



    # for i in range(max_label + 1):
    #     indices = np.where(labels == i)[0].tolist()
    #     cluster = pcd.select_by_index(indices)
    #     # cluster はクラスタ i の点群

    # aabb = cluster.get_axis_aligned_bounding_box()
    # aabb.color = (1, 0, 0)  # 赤でカラー設定
    # o3d.visualization.draw_geometries([cluster, aabb])
    #o3d.visualization.draw([cluster, aabb])
