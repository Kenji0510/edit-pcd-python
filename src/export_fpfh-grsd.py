import json
import matplotlib.pyplot as plt
import numpy as np

# ファイルからデータを読み込む
with open("/home/kenji/workspace/cpp/create-features-pcl/data/output/output_features_123_00.json", "r") as f:
    data = json.load(f)

GRSD = data.get("GRSD", [])
FPFH = data.get("FPFH", [])

# FPFHの異常値を0に置換
FPFH = [v if abs(v) < 1e10 else 0.0 for v in FPFH]

plt.figure(figsize=(14, 5))

# 両方まとめた図
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.bar(np.arange(len(GRSD)), GRSD)
plt.title("GRSD Histogram")
plt.xlabel("Bin")
plt.ylabel("Count")
plt.subplot(1, 2, 2)
plt.bar(np.arange(len(FPFH)), FPFH)
plt.title("FPFH Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/FPFH_grsd_hist.png")
plt.close()

# GRSDのみ
plt.figure(figsize=(7, 5))
plt.bar(np.arange(len(GRSD)), GRSD)
plt.title("GRSD Histogram")
plt.xlabel("Bin")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/grsd_hist.png")
plt.close()

# FPFHのみ
plt.figure(figsize=(7, 5))
plt.bar(np.arange(len(FPFH)), FPFH)
plt.title("FPFH Histogram")
plt.xlabel("Bin")
plt.ylabel("Value")
plt.tight_layout()
plt.savefig("../data/results/figure_analysis/FPFH_hist.png")
plt.close()