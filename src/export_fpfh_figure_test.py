import json
import matplotlib.pyplot as plt

# =========================
# ここを環境に合わせて変更してください
# =========================
# 読み込みたい JSON ファイルのパス（例: cluster_27_00.json）
json_path = "../data/averaging_data/20250530-1635-onlyPerson_choiced_fpfh/cluster_27_00.json"
# 出力する PNG ファイルのパス
output_png_path = "../data/averaging_data/20250530-1635-onlyPerson_choiced_fpfh-figures/cluster_27_00_fpfh.png"
# =========================

# JSON を読み込む
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# "fpfh" キーから 33 次元のリストを取得
fpfh = data.get("fpfh", [])
if len(fpfh) != 33:
    raise ValueError("FPFH ベクトルが 33 次元ではありません。")

# X 軸用に 1～33 の整数リストを用意
indices = list(range(1, 34))

# 棒グラフを作成
plt.figure(figsize=(10, 5))
plt.bar(indices, fpfh, color="orange")
plt.xticks(indices)
plt.xlabel("FPFH Dimension")
plt.ylabel("Average Feature Value")
# ラベル情報があればタイトルに表示
label = data.get("label", {})
plt.title(f"Cluster Label: x={label.get('x')}, y={label.get('y')}")

# PNG として保存
plt.savefig(output_png_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"Saved bar chart to: {output_png_path}")
