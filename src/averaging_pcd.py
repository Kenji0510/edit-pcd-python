import os
import re
import open3d as o3d

def get_sorted_pcd_files(input_dir, pattern=r"cluster_(\d+)_(\d+)\.pcd"):
    """
    input_dir 内の .pcd ファイルを正規表現でマッチさせ、
    抽出した数字部分でソートしてファイルパスのリストを返す。

    例: "cluster_00_00.pcd", "cluster_10_05.pcd" などの形式を想定し、
    (\d+)_(\d+) の組み合わせでソートする。
    """
    regex = re.compile(pattern)
    files = []
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith(".pcd"):
            continue
        m = regex.match(fname)
        if m:
            # m.group(1), m.group(2) はそれぞれ番号部分
            idx1 = int(m.group(1))
            idx2 = int(m.group(2))
            files.append((idx1, idx2, fname))
        else:
            # 正規表現にマッチしないファイルは末尾に回す（あるいは無視する）
            # ここではマッチしないものも名前順で処理したい場合は、idx1=inf として扱う
            files.append((float("inf"), float("inf"), fname))

    # 番号部分で昇順ソート (idx1 → idx2 → ファイル名)
    files.sort(key=lambda x: (x[0], x[1], x[2]))
    # ソート後、ファイル名のみを返す
    return [fname for (_, _, fname) in files]

def voxelize_and_save(input_dir, output_dir, voxel_size=0.05):
    """
    - input_dir 内の全 .pcd ファイルを順に読み込み
    - voxel_size を使って voxel_down_sample（ボクセル化）を実行
    - 結果を output_dir に同じファイル名で書き出す

    :param input_dir: 元の PCD ファイル群が入っているフォルダ
    :param output_dir: ボクセル化後ファイルを出力したいフォルダ
    :param voxel_size: voxel の一辺の長さ（メートル単位など）。点群の単位に合わせて調整してください。
    """
    os.makedirs(output_dir, exist_ok=True)
    sorted_files = get_sorted_pcd_files(input_dir)

    for fname in sorted_files:
        in_path = os.path.join(input_dir, fname)
        out_path = os.path.join(output_dir, fname)

        # ファイルが本当に存在するかチェック
        if not os.path.isfile(in_path):
            print(f"[warning] ファイルが見つかりません: {in_path}（スキップ）")
            continue

        # 1. 点群を読み込む
        pcd = o3d.io.read_point_cloud(in_path)
        if pcd.is_empty():
            print(f"[info] 空の点群、または読み込み失敗: {in_path}（スキップ）")
            continue

        # 2. Voxel Downsampling（ボクセル化）
        voxel_pcd = pcd.voxel_down_sample(voxel_size=voxel_size)

        # 3. 結果を同じファイル名で保存
        #    - デフォルトでは ASCII 圧縮なしで書き出す
        #    - 必要に応じて write_point_cloud のオプションを追加してください
        success = o3d.io.write_point_cloud(out_path, voxel_pcd, write_ascii=True, compressed=False)
        if not success:
            print(f"[error] ボクセル化結果の保存に失敗: {out_path}")
        else:
            print(f"[saved] {out_path}  （元: {in_path}、ボクセルサイズ={voxel_size}）")

if __name__ == "__main__":
    # --- ユーザが変更すべき部分 ---
    # PCD ファイルがあるフォルダを指定してください
    input_dir = "../data/results/dbscan/each_cluster/20250530-1643"
    # ボクセル化後の PCD 保存先フォルダ（存在しなければ自動作成されます）
    output_dir = "../data/averaging_data/20250530-1643-voxelized"
    # ボクセル化の一辺の長さ (例: 0.05m)。点群の密度や単位に合わせて調整してください
    voxel_size = 0.05

    voxelize_and_save(input_dir, output_dir, voxel_size)
