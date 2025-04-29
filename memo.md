# aa
- In case of cr_50.pcd
```python3
pcd = o3d.io.read_point_cloud("/home/kenji/workspace/cpp/ndt-matching/data/matching_results/cr/cr_50.pcd")

pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True)
```
- Results
```bash
(pcd_operation) kenji@kenji-24:~/workspace/python3/pcd_operation/src$ python3 main.py 
[Open3D INFO] WebRTC GUI backend enabled.
PointCloud with 10329 points.
Precompute neighbors.[========================================] 100%
ラベル数: 26 クラスタ (ノイズは -1)==>             ] 65%
検出されたクラスタ数: 26
```

- In case of cr_10.pcd
```python3
pcd_path = "/home/kenji/workspace/cpp/ndt-matching/data/matching_results/cr/cr_10.pcd"
pcd = o3d.io.read_point_cloud(pcd_path)

pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True)
```
- Results
```bash
(pcd_operation) kenji@kenji-24:~/workspace/python3/pcd_operation/src$ python3 main.py 
[Open3D INFO] WebRTC GUI backend enabled.
PointCloud with 9918 points.
Precompute neighbors.[========================================] 100%
ラベル数: 8 クラスタ (ノイズは -1)=======>         ] 75%
検出されたクラスタ数: 8
```

- In case of cr_75.pcd
```python3
pcd_path = "/home/kenji/workspace/cpp/ndt-matching/data/matching_results/cr/cr_75.pcd"
pcd = o3d.io.read_point_cloud(pcd_path)

pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True)
```
- Results
```bash
(pcd_operation) kenji@kenji-24:~/workspace/python3/pcd_operation/src$ python3 main.py 
[Open3D INFO] WebRTC GUI backend enabled.
PointCloud with 9133 points.
Precompute neighbors.[========================================] 100%
ラベル数: 12 クラスタ (ノイズは -1)>               ] 60%
検出されたクラスタ数: 12

```

- In case of cr_100.pcd
```python3
pcd_path = "/home/kenji/workspace/cpp/ndt-matching/data/matching_results/cr/cr_100.pcd"
pcd = o3d.io.read_point_cloud(pcd_path)

pcd.cluster_dbscan(eps=0.2, min_points = 20, print_progress=True)
```
- Results
```bash
(pcd_operation) kenji@kenji-24:~/workspace/python3/pcd_operation/src$ python3 main.py 
[Open3D INFO] WebRTC GUI backend enabled.
PointCloud with 8461 points.
Precompute neighbors.[========================================] 100%
ラベル数: 8 クラスタ (ノイズは -1)=====>           ] 70%
検出されたクラスタ数: 8

```

