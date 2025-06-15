import os
import json
import shutil

def copy_selected_pcds(json_dir, pcd_source_dir, pcd_dest_dir):
    """
    1. json_dir 以下の各 JSON ファイルを読み込み、
       その中のキーを (例: "cluster_00_03") 抽出する。
    2. キー + ".pcd" をファイル名として pcd_source_dir から探し、
       見つかったら pcd_dest_dir にコピーする。
    3. コピー先のフォルダがなければ自動作成する。
    """
    os.makedirs(pcd_dest_dir, exist_ok=True)

    # json_dir にある全 .json ファイルを走査
    for fname in os.listdir(json_dir):
        if not fname.lower().endswith(".json"):
            continue

        json_path = os.path.join(json_dir, fname)
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[error] JSON の読み込みに失敗しました: {json_path} → {e}")
            continue

        # JSON のキーは "cluster_??_??" の形式を仮定
        for key_name in data.keys():
            pcd_name = key_name + ".pcd"           # 例: "cluster_00_03.pcd"
            src_path = os.path.join(pcd_source_dir, pcd_name)
            dst_path = os.path.join(pcd_dest_dir, pcd_name)

            if not os.path.isfile(src_path):
                print(f"[warning] 元の PCD が見つかりません: {src_path}（スキップ）")
                continue

            try:
                shutil.copy2(src_path, dst_path)
                print(f"[copied] {src_path} → {dst_path}")
            except Exception as e:
                print(f"[error] コピー失敗: {src_path} → {dst_path} → {e}")

if __name__ == "__main__":
    # ==========================================
    # 環境に合わせてここを書き換えてください
    # ==========================================
    # (1) JSON ファイル群が格納されているフォルダ
    json_dir = "../data/averaging_data/20250530-1643_json"

    # (2) ボクセル化済み PCD が置いてあるフォルダ
    pcd_source_dir = "../data/averaging_data/20250530-1643-voxelized_pcd"

    # (3) コピー先フォルダ（存在しなければ自動生成される）
    pcd_dest_dir = "../data/averaging_data/20250530-1643_choiced"
    # ==========================================

    copy_selected_pcds(json_dir, pcd_source_dir, pcd_dest_dir)
