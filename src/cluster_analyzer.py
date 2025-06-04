#!/usr/bin/env python3
import json
import statistics
from typing import Dict, List, Any

# 設定：元データと出力先
INPUT_FILE = '../data/results/dbscan/each_cluster/combined_data/cluster_info.json'
OUTPUT_FILE = '../data/results/cluster_analysis/cluster_stats.json'

# クラスタ番号のリスト
PERSON_CLUSTERS = [0, 1, 7, 10, 18, 21, 24]
NON_PERSON_CLUSTERS = [2, 4, 6, 13, 25]

def load_clusters(path: str) -> Dict[str, Dict[str, Any]]:
    """ JSON ファイルを読み込んで辞書で返す """
    with open(path, 'r') as f:
        return json.load(f)

def extract_values(clusters: Dict[str, Dict], ids: List[int], key_prefix='cluster_') -> Dict[str, List[float]]:
    """ 与えられたクラスタ番号リスト ids から、各パラメータの値リストを抽出 """
    # 例： 'cluster_0' のようなキー名を生成
    selected = {f'{key}': clusters[f'{key}'] for key in clusters if int(key.split('_')[1]) in ids}
    # パラメータ名を取得（最初のクラスタから）
    params = list(next(iter(selected.values())).keys())
    # 各パラメータごとに値を集める
    values: Dict[str, List[float]] = {p: [] for p in params}
    for cl in selected.values():
        for p, v in cl.items():
            values[p].append(v)
    return values

def compute_stats(values: List[float]) -> Dict[str, float]:
    """ 数値リストから統計量を計算して返す """
    return {
        'mean':    statistics.mean(values),
        'median':  statistics.median(values),
        'variance': statistics.pvariance(values),  # 母分散
        'min':     min(values),
        'max':     max(values),
    }

def build_stats(clusters: Dict[str, Dict], ids: List[int]) -> Dict[str, Dict[str, Dict[str, float]]]:
    """ person / non-person 用の統計情報をまとめて返す """
    vals = extract_values(clusters, ids)
    stats = {param: compute_stats(vals_list) for param, vals_list in vals.items()}
    return stats

def main():
    # 1. 元 JSON の読み込み
    clusters = load_clusters(INPUT_FILE)

    # 2. 人クラスタ／人以外クラスタごとの統計を計算
    person_stats = build_stats(clusters, PERSON_CLUSTERS)
    non_person_stats = build_stats(clusters, NON_PERSON_CLUSTERS)

    # 3. 結果をまとめて保存
    result = {
        'person': person_stats,
        'non_person': non_person_stats,
    }
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, indent=2)
    print(f'統計結果を {OUTPUT_FILE} に書き出しました。')

if __name__ == '__main__':
    main()
