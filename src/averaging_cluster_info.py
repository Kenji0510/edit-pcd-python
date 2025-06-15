import os
import re
import json
import open3d as o3d

def get_pcd_files_grouped_by_y(input_dir, pattern=r"^cluster_(\d{2})_(\d{2})\.pcd$"):
    """
    input_dir 内の PCD ファイルを走査し、"cluster_{y}_{z}.pcd" という形式を正規表現でマッチさせる。
    グループ化キーとして、y（最初の2桁）を使って辞書 { y_str: [ファイル名, ...], ... } を返す。
    """
    regex = re.compile(pattern)
    groups = {}

    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(".pcd"):
            continue
        m = regex.match(fname)
        if not m:
            # 名前形式が "cluster_{y}_{z}.pcd" でない場合はスキップ
            print(f"[warning] スキップ (ファイル名形式不正): {fname}")
            continue

        y_str = m.group(1)  # 先頭2桁 (例: "00", "10", …)
        groups.setdefault(y_str, []).append(fname)

    # 各グループ内のファイル名をソートしておく
    for y_str, flist in groups.items():
        flist.sort()

    return groups

def compute_bbox_metrics(pcd):
    """
    Open3D の PointCloud オブジェクト pcd に対し、
    AxisAlignedBoundingBox を使って以下を計算して辞書として返す：
      - num_points: 点数
      - width: x_max - x_min
      - depth: y_max - y_min
      - height: z_max - z_min
    """
    num_points = len(pcd.points)
    aabb = pcd.get_axis_aligned_bounding_box()
    min_b = aabb.get_min_bound()  # [x_min, y_min, z_min]
    max_b = aabb.get_max_bound()  # [x_max, y_max, z_max]

    width  = float(max_b[0] - min_b[0])
    depth  = float(max_b[1] - min_b[1])
    height = float(max_b[2] - min_b[2])

    return {
        "num_points": num_points,
        "width":      width,
        "depth":      depth,
        "height":     height
    }

def process_and_save_top3(input_dir, output_dir, min_height=0.7, top_k=3):
    """
    1. input_dir 内の PCD ファイルを "y" 番号ごとにグループ化
    2. 各ファイルを読み込み、BBox と点数を計算
    3. 同じ y グループの中で、
       - height >= min_height のものだけを抽出
       - num_points の降順でソートして上位 top_k 件を選択
    4. 選ばれた上位 top_k 件だけを、グループごとに JSON に保存

    :param input_dir: PCD ファイル群が入ったフォルダ
    :param output_dir: 結果 JSON を保存するフォルダ
    :param min_height: 抽出条件となる最小 height（例: 0.7）
    :param top_k: 各グループから選ぶクラスタ数（例: 3）
    """
    os.makedirs(output_dir, exist_ok=True)

    # step1: ファイルを y 番号ごとにグループ化
    groups = get_pcd_files_grouped_by_y(input_dir)

    # step2: 各グループを処理
    for y_str, flist in groups.items():
        # すべてのクラスタ (ファイル) のメトリクスを一時リストに保持
        metrics_list = []  # 例: [ ( "cluster_00_00", {num_points:…, width:…, …} ), … ]

        print(f"--- グループ cluster_{y_str}_* を処理中（height >= {min_height} → 上位 {top_k}） ---")
        for fname in flist:
            in_path = os.path.join(input_dir, fname)

            # 点群読み込み
            try:
                pcd = o3d.io.read_point_cloud(in_path)
            except Exception as e:
                print(f"[error] 読み込み失敗: {in_path}  → {e}")
                continue

            if pcd.is_empty():
                print(f"[info] 空の点群または読み込みエラー: {in_path} （スキップ）")
                continue

            # BBox メトリクス計算
            m = compute_bbox_metrics(pcd)
            key_name = os.path.splitext(fname)[0]  # "cluster_00_00" のように拡張子を外す

            # 一旦すべて追加（後で絞り込み）
            metrics_list.append((key_name, m))

            print(f"  ・{key_name}: num={m['num_points']}, w={m['width']:.4f}, d={m['depth']:.4f}, h={m['height']:.4f}")

        # step3: height >= min_height のものだけをフィルタ
        filtered = [
            (name, data)
            for name, data in metrics_list
            if data["height"] >= min_height
        ]

        # num_points の降順ソート
        filtered.sort(key=lambda x: x[1]["num_points"], reverse=True)

        # 上位 top_k 件を取得
        topk = filtered[:top_k]

        # JSON に出力する辞書を構築
        summary_dict = { name: data for (name, data) in topk }

        # step4: グループごとの JSON 保存
        out_fname = f"cluster_{y_str}_top{top_k}.json"
        out_path = os.path.join(output_dir, out_fname)
        try:
            with open(out_path, "w", encoding="utf-8") as fo:
                json.dump(summary_dict, fo, ensure_ascii=False, indent=2)
            print(f"[saved] {out_path}  （エントリ数: {len(summary_dict)}）\n")
        except Exception as e:
            print(f"[error] JSON 保存失敗: {out_path}  → {e}\n")

if __name__ == "__main__":
    # --- ここを環境に合わせて変更してください ---
    # PCD ファイルが入ったフォルダ
    input_dir = "../data/averaging_data/20250530-1643-voxelized_pcd"
    # 結果 JSON をまとめて置きたいフォルダ
    output_dir = "../data/averaging_data/20250530-1643_json"
    # 抽出条件：height >= 0.7
    min_height = 0.7
    # 各 y グループから上位 3 件を選択
    top_k = 3

    process_and_save_top3(input_dir, output_dir, min_height, top_k)
