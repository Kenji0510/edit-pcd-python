import os
import re
import json
import numpy as np
import open3d as o3d

def get_sorted_pcd_files(input_dir, pattern=r"^cluster_(\d{2})_(\d{2})\.pcd$"):
    """
    input_dir 内の PCD ファイルを「cluster_{xx}_{yy}.pcd」という形式で抽出し、
    (xx, yy) の数値順にソートしてファイル名リストを返す。
    """
    regex = re.compile(pattern)
    files = []

    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(".pcd"):
            continue
        m = regex.match(fname)
        if not m:
            # 「cluster_xx_yy.pcd」にマッチしないファイルは無視
            print(f"[warning] ファイル名が指定形式に合わないためスキップ: {fname}")
            continue

        xx = int(m.group(1))
        yy = int(m.group(2))
        files.append((xx, yy, fname))

    # (xx, yy) の昇順でソート
    files.sort(key=lambda x: (x[0], x[1]))
    return [fname for (_, _, fname) in files]

def compute_average_fpfh(pcd, 
                         normal_radius=0.05, 
                         normal_max_nn=30,
                         fpfh_radius=0.1,
                         fpfh_max_nn=100):
    """
    1. 法線推定 (radius=normal_radius, max_nn=normal_max_nn)
    2. FPFH を計算 (radius=fpfh_radius, max_nn=fpfh_max_nn)
    3. 各点の FPFH を平均して長さ 33 のベクトルを返す
    """
    # (1) 法線推定
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=normal_radius,
            max_nn=normal_max_nn
        )
    )
    # (2) FPFH 計算
    fpfh = o3d.pipelines.registration.compute_fpfh_feature(
        pcd,
        search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=fpfh_radius,
            max_nn=fpfh_max_nn
        )
    )
    # fpfh.data は (33, N) の配列
    fpfh_np = np.asarray(fpfh.data)  # shape = (33, num_points)

    # (3) 各行（次元）ごとに平均 → length=33 のベクトル
    avg_fpfh = np.mean(fpfh_np, axis=1)  # shape = (33,)
    return avg_fpfh.tolist()

def process_all_clusters(input_dir, output_dir,
                         normal_radius=0.05, normal_max_nn=30,
                         fpfh_radius=0.1, fpfh_max_nn=100):
    """
    1. input_dir 内の PCD を番号順にソートして取得
    2. 各ファイルを読み込み、FPFH の平均を計算
    3. ファイル名からラベル情報 (xx, yy) を抽出
    4. JSON に {"label": {"x": xx, "y": yy}, "fpfh": [...] } の形式で保存
    """
    os.makedirs(output_dir, exist_ok=True)
    pcd_files = get_sorted_pcd_files(input_dir)

    if len(pcd_files) == 0:
        print(f"[error] PCD ファイルが見つかりません: {input_dir}")
        return

    # 正規表現を再定義して、ファイル名から xx, yy を取り出せるようにしておく
    regex = re.compile(r"^cluster_(\d{2})_(\d{2})\.pcd$")

    for fname in pcd_files:
        # パス組み立て
        pcd_path = os.path.join(input_dir, fname)
        cluster_name = os.path.splitext(fname)[0]  # "cluster_xx_yy"

        # (1) 点群を読み込み
        try:
            pcd = o3d.io.read_point_cloud(pcd_path)
        except Exception as e:
            print(f"[error] 点群読み込み失敗: {pcd_path} → {e}")
            continue

        if pcd.is_empty():
            print(f"[info] 空の点群または読み込みできない: {pcd_path} （スキップ）")
            continue

        # (2) 平均 FPFH を計算
        avg_fpfh = compute_average_fpfh(
            pcd,
            normal_radius=normal_radius,
            normal_max_nn=normal_max_nn,
            fpfh_radius=fpfh_radius,
            fpfh_max_nn=fpfh_max_nn
        )

        # (3) ファイル名からラベル情報 (xx, yy) を抽出
        m = regex.match(fname)
        if not m:
            # 通常はここを通らないが、安全策として
            print(f"[warning] 正規表現にマッチしない: {fname} → ラベル (0,0) を仮設定")
            xx = yy = 0
        else:
            xx = int(m.group(1))
            yy = int(m.group(2))

        # (4) JSON の中身を構築
        data_to_save = {
            "label": {
                "x": xx,
                "y": yy
            },
            "fpfh": avg_fpfh
        }

        # 保存先のパス (cluster_xx_yy.json)
        out_fname = f"{cluster_name}.json"
        out_path = os.path.join(output_dir, out_fname)

        # (5) JSON ファイルとして保存
        try:
            with open(out_path, "w", encoding="utf-8") as fo:
                json.dump(data_to_save, fo, ensure_ascii=False, indent=2)
            print(f"[saved] {out_path}  （ラベル: x={xx}, y={yy}）")
        except Exception as e:
            print(f"[error] JSON 保存失敗: {out_path} → {e}")

if __name__ == "__main__":
    # ===========================
    # 環境に合わせて以下を書き換えてください
    # ===========================
    # (1) PCD ファイル群が入ったフォルダ
    input_dir = "../data/averaging_data/20250530-1643_choiced"

    # (2) JSON 出力先フォルダ
    output_dir = "../data/averaging_data/20250530-1643_choiced_fpfh"

    # (3) 法線推定・FPFH 計算パラメータ
    normal_radius = 0.05
    normal_max_nn = 30
    fpfh_radius = 0.1
    fpfh_max_nn = 100
    # ===========================

    process_all_clusters(
        input_dir, output_dir,
        normal_radius, normal_max_nn,
        fpfh_radius, fpfh_max_nn
    )
