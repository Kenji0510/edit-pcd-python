import os
import re
import json

def get_sorted_json_files(directory, prefix="cluster_info", suffix=".json"):
    """
    ディレクトリ内で prefix + 数字 + suffix という名前のファイルを探し，
    数字部分をキーにして昇順ソートしたリストを返す。
    例: cluster_info00.json, cluster_info01.json, … のような命名規則を想定
    """
    pattern = re.compile(rf"^{re.escape(prefix)}(\d+){re.escape(suffix)}$")
    files = []
    for fname in os.listdir(directory):
        m = pattern.match(fname)
        if m:
            idx = int(m.group(1))
            files.append((idx, fname))
    files.sort(key=lambda x: x[0])
    return [fname for (_, fname) in files]

def select_top3_clusters(data_dict, min_height=0.7):
    """
    JSON 内部の {"cluster_0": {…}, "cluster_1": {…}, …} という構造を想定し，
    height ≥ min_height のものを抽出し，num_points の降順でソートして上位３つを返す。
    """
    # data_dict: たとえば {"cluster_0": {"num_points": ..., "height": ..., そのほか…}, …}
    # items() で (cluster_name, cluster_data) のリストを取得
    candidates = [
        (name, info)
        for name, info in data_dict.items()
        if info.get("height", 0) >= min_height
    ]
    # num_points の降順でソート
    candidates.sort(key=lambda x: x[1].get("num_points", 0), reverse=True)
    # 上位３つだけ返す
    top3 = candidates[:3]
    # top3 は [ (cluster_name, info), … ] のタプル３要素
    return {name: info for name, info in top3}

def process_directory(input_dir, output_dir):
    """
    input_dir にある cluster_infoXX.json を順に読み込み，
    select_top3_clusters() によって抽出した結果を output_dir に別ファイルとして保存する。
    """
    os.makedirs(output_dir, exist_ok=True)
    json_files = get_sorted_json_files(input_dir)

    for fname in json_files:
        in_path = os.path.join(input_dir, fname)
        with open(in_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # height >= 0.7 のクラスタを num_points 降順で並べ，上位3件を抽出
        selected = select_top3_clusters(data, min_height=0.7)

        # 処理例：ここで selected の中身に対して何らかの追加処理（可視化や別フォーマット出力など）を挿入してもよい
        # 例: for cluster_name, info in selected.items(): print(cluster_name, info)

        # 結果を別ファイルに保存
        # 例: 入力が cluster_info00.json なら、出力を selected_cluster_info00.json とする
        out_fname = f"selected_{fname}"
        out_path = os.path.join(output_dir, out_fname)
        with open(out_path, "w", encoding="utf-8") as fo:
            json.dump(selected, fo, ensure_ascii=False, indent=2)

        print(f"[saved] {out_path}  （抽出数: {len(selected)} 件）")


if __name__ == "__main__":
    # --- 使い方例 ---
    # input_dir: cluster_infoXX.json が格納されているフォルダ
    # output_dir: 抽出結果を出力するフォルダ
    input_dir = "../data/averaging_data/20250530-1635-onlyPerson_voxelized_pcd"
    output_dir = "../data/averaging_data/20250530-1635-onlyPerson_json"

    process_directory(input_dir, output_dir)
