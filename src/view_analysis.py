import json
import matplotlib.pyplot as plt

# Load statistics
with open('../data/results/cluster_analysis/cluster_stats.json', 'r') as f:
    stats = json.load(f)

# Prepare data
# person_stats = stats['person']
person_stats = stats['non_person']
params = [p for p in person_stats.keys() if p != 'num_points']
means = [person_stats[p]['mean'] for p in params]
mins = [person_stats[p]['min'] for p in params]
maxs = [person_stats[p]['max'] for p in params]

# Plot grouped bar chart
x = list(range(len(params)))
width = 0.25

plt.figure()
plt.bar([i - width for i in x], means, width, label='mean')
plt.bar(x, mins, width, label='min')
plt.bar([i + width for i in x], maxs, width, label='max')
plt.xticks(x, params, rotation=45, ha='right')
plt.xlabel('パラメータ')
plt.ylabel('値')
plt.title('「人」クラスタの各パラメータ Mean / Min / Max')
plt.legend()
plt.tight_layout()
plt.show()

# plt.savefig('../data/results/figure_analysis/person_cluster_stats.png')
plt.savefig('../data/results/figure_analysis/non_person_cluster_stats.png')