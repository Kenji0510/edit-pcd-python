import json
import matplotlib.pyplot as plt
import numpy as np

# ファイルからデータを読み込む
with open("/home/kenji/workspace/cpp/create-features-pcl/data/output/output_features_vfh-grsd_67_00.json", "r") as f:
    data = json.load(f)

VFH_lower = data.get("VFH", {}).get("LOWER", [])
VFH_upper = data.get("VFH", {}).get("UPPER", [])
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
plt.bar(np.arange(len(VFH_lower)), VFH_lower, label="LOWER", alpha=0.7)
plt.bar(np.arange(len(VFH_upper)), VFH_upper, label="UPPER", alpha=0.7)
plt.title("VFH Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/vfh_hist.png")
plt.close()

# GRSDヒストグラム
plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(GRSD_lower)), GRSD_lower, label="LOWER", alpha=0.7)
plt.bar(np.arange(len(GRSD_upper)), GRSD_upper, label="UPPER", alpha=0.7)
plt.title("GRSD Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.legend()
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/grsd_hist.png")
plt.close()