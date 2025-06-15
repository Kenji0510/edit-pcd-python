import json
import matplotlib.pyplot as plt
import numpy as np

file_num = "67_00"

# ファイルからデータを読み込む
file_name = f"/home/kenji/workspace/cpp/create-features-pcl/data/output/output_features_vfh-grsd_{file_num}.json"
with open(file_name, "r") as f:
    data = json.load(f)

FPFH_lower = data.get("FPFH", {}).get("LOWER", [])
FPFH_upper = data.get("FPFH", {}).get("UPPER", [])
GRSD_all = data.get("GRSD", {}).get("ALL", [])
GRSD_lower = data.get("GRSD", {}).get("LOWER", [])
GRSD_upper = data.get("GRSD", {}).get("UPPER", [])

# FPFHの異常値を0に置換
# FPFH = [v if abs(v) < 1e10 else 0.0 for v in FPFH]

# plt.figure(figsize=(14, 5))

# # 両方まとめた図
# plt.figure(figsize=(14, 5))
# plt.subplot(1, 2, 1)
# plt.bar(np.arange(len(GRSD)), GRSD)
# plt.title("GRSD Histogram")
# plt.xlabel("Bin")
# plt.ylabel("Count")
# plt.subplot(1, 2, 2)
# plt.bar(np.arange(len(FPFH)), FPFH)
# plt.title("FPFH Histogram")
# plt.xlabel("Bin")
# plt.ylabel("Value")
# plt.tight_layout()
# plt.savefig("../data/results/figure_analysis/FPFH_grsd_hist.png")
# plt.close()

plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(FPFH_lower)), FPFH_lower, label="LOWER", alpha=0.7)
plt.bar(np.arange(len(FPFH_upper)), FPFH_upper, label="UPPER", alpha=0.7)
plt.title("FPFH Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/fpfh_hist.png")
plt.close()

# GRSDヒストグラム
save_path = f"../data/results/figure_analysis/grsd_hist_{file_num}.png"
plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(GRSD_all)), GRSD_all, label="ALL", alpha=0.7)
plt.bar(np.arange(len(GRSD_lower)), GRSD_lower, label="LOWER", alpha=0.7)
plt.bar(np.arange(len(GRSD_upper)), GRSD_upper, label="UPPER", alpha=0.7)
plt.title("GRSD Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.savefig(save_path)
plt.close()

# --- 正規化ヒストグラム ---
def normalize(arr):
    s = np.sum(arr)
    return arr / s if s != 0 else arr

def minmax_normalize(arr):
    arr = np.array(arr, dtype=np.float64)
    min_v = np.min(arr)
    max_v = np.max(arr)
    if max_v - min_v == 0:
        return arr  # すべて同じ値の場合はそのまま返す
    return (arr - min_v) / (max_v - min_v)

FPFH_lower_norm = normalize(FPFH_lower)
FPFH_upper_norm = normalize(FPFH_upper)
# GRSD_lower_norm = normalize(GRSD_lower)
# GRSD_upper_norm = normalize(GRSD_upper)

GRSD_all_norm = normalize(GRSD_all)
GRSD_lower_norm = minmax_normalize(GRSD_lower)
GRSD_upper_norm = minmax_normalize(GRSD_upper)

plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(FPFH_lower_norm)), FPFH_lower_norm, label="LOWER (norm)", alpha=0.7)
plt.bar(np.arange(len(FPFH_upper_norm)), FPFH_upper_norm, label="UPPER (norm)", alpha=0.7)
plt.title("FPFH Histogram (Normalized)")
plt.xlabel("Bin")
plt.ylabel("Normalized Value")
plt.legend()
plt.tight_layout()
plt.savefig("fpfh_hist_normalized.png")
plt.close()

save_path = f"../data/results/figure_analysis/grsd_hist_normalized_{file_num}.png"
plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(GRSD_all_norm)), GRSD_all_norm, label="ALL (norm)", alpha=0.7)
plt.bar(np.arange(len(GRSD_lower_norm)), GRSD_lower_norm, label="LOWER (norm)", alpha=0.7)
plt.bar(np.arange(len(GRSD_upper_norm)), GRSD_upper_norm, label="UPPER (norm)", alpha=0.7)
plt.title("GRSD Histogram (Normalized)")
plt.xlabel("Bin")
plt.ylabel("Normalized Value")
plt.legend()
plt.tight_layout()
plt.savefig(save_path)
plt.close()