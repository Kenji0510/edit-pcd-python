import open3d as o3d
import numpy as np

# ファイルパス
source_path_01 = "/home/kenji/workspace/cpp/align_pcd/data/none_person/livox_lidar_192_168_10_185/raw/livox_lidar_192_168_10_185_15.pcd"
source_path_02 = "/home/kenji/workspace/cpp/align_pcd/data/none_person/livox_lidar_192_168_10_185/raw/livox_lidar_192_168_10_185_18.pcd"
source_path_03 = "/home/kenji/workspace/cpp/align_pcd/data/none_person/livox_lidar_192_168_10_185/raw/livox_lidar_192_168_10_185_21.pcd"
target_path = "/home/kenji/workspace/python3/pcd_operation/data/room/lab-room.pcd"

# 点群読み込み
source = o3d.io.read_point_cloud(source_path_01)
source_02 = o3d.io.read_point_cloud(source_path_02)
source_03 = o3d.io.read_point_cloud(source_path_03)
target = o3d.io.read_point_cloud(target_path)

source = source + source_02 + source_03  # 複数のソース点群を結合

# 事前回転・並進行列（4x4）
# init_transform = np.array([
#     [-0.9311131,   0.36458713,  0.01022883,  4.53183632],
#     [-0.36416174, -0.93086094,  0.02973454,  6.88796509],
#     [ 0.02036245,  0.02396127,  0.99950549, -1.08598551],
#     [ 0.0,         0.0,         0.0,         1.0]
# ])

# # --- ここで初期回転・並進を適用 ---
# source.transform(init_transform)

# # θ = 4.4° をラジアンに変換（実際の測定値に応じて微調整してください）
# theta = np.deg2rad(20.0)

# # Z 軸まわりに −θ 回転（画像上で CCW 傾きを CW に戻す）
# R_z = np.array([
#     [ np.cos(theta),  np.sin(theta), 0.0],
#     [-np.sin(theta),  np.cos(theta), 0.0],
#     [          0.0,           0.0, 1.0]
# ])

# R_z_homo = np.eye(4)
# R_z_homo[:3, :3] = R_z

# # 確認のため表示
# print(R_z_homo)

# source.transform(R_z_homo)

# translation = np.array([0.05, 1.7, 0.0])
# # source.translate(translation)

init_transform = np.array([[-0.99951076,  0.02422664,  0.01978177,  6.66435596],
 [-0.02374066, -0.99941930,  0.02444286,  6.62259066],
 [ 0.02036245,  0.02396127,  0.99950549, -1.08598551],
 [ 0.        ,  0.        ,  0.        ,  1.        ]])

source.transform(init_transform)

# 初期位置合わせの可視化
o3d.visualization.draw_geometries([
    target.paint_uniform_color([0.7, 0.7, 0.7]),
    source.paint_uniform_color([1, 0, 0])
], window_name="Initial Alignment")

# ボクセルダウンサンプリングで密度を統一
voxel_size = 0.3
source_down = source.voxel_down_sample(voxel_size)
target_down = target.voxel_down_sample(voxel_size)

# 法線推定
source_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=50))
target_down.estimate_normals(o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=50))

# FPFH特徴量計算
source_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    source_down, o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=50))
target_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
    target_down, o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=50))

# RANSACによる粗い位置合わせ
result_ransac = o3d.pipelines.registration.registration_ransac_based_on_feature_matching(
    source_down, target_down, source_fpfh, target_fpfh, mutual_filter=True,
    max_correspondence_distance=voxel_size * 2.0,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False),
    ransac_n=4,
    checkers=[
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnEdgeLength(0.9),
        o3d.pipelines.registration.CorrespondenceCheckerBasedOnDistance(voxel_size * 2.0)
    ],
    criteria=o3d.pipelines.registration.RANSACConvergenceCriteria(50000000, 500)
)
print("RANSAC transformation:\n", result_ransac.transformation)

# RANSAC後の可視化
source_ransac = source_down.transform(result_ransac.transformation.copy())
o3d.visualization.draw_geometries([
    target_down.paint_uniform_color([0.7, 0.7, 0.7]),
    source_ransac.paint_uniform_color([0, 0, 1])
], window_name="RANSAC Alignment")

# ICPによる精密位置合わせ
result_icp = o3d.pipelines.registration.registration_icp(
    source, target, voxel_size, result_ransac.transformation,
    o3d.pipelines.registration.TransformationEstimationPointToPlane()
)
print("ICP transformation:\n", result_icp.transformation)

# ICP後の可視化（既存のコードでOK）
source_icp = source.transform(result_icp.transformation.copy())
o3d.visualization.draw_geometries([
    target.paint_uniform_color([0.7, 0.7, 0.7]),
    source.paint_uniform_color([1, 0, 0])
], window_name="ICP Alignment")

# 位置合わせ結果の可視化
# source.transform(result_icp.transformation)
# o3d.visualization.draw_geometries([target.paint_uniform_color([0.7,0.7,0.7]), source.paint_uniform_color([1,0,0])])

# 必要なら保存
# o3d.io.write_point_cloud("aligned_source.pcd", source)