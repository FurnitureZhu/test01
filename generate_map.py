import numpy as np
from scipy.spatial import Delaunay
import random

def generate_graph(num_nodes):
    #2d平面  生成每个点坐标，1000*1000
    points = np.random.rand(num_nodes, 2) * 1000
    print(points)
    points[0] = [0, 0]
    # 使用Delaunay，构建三角形
    tri = Delaunay(points)
    edges = {}
    # 遍历三角形，将边加入
    for simplex in tri.simplices:
        for i in range(3):
            u = simplex[i]
            v = simplex[(i+1)%3]
            if u not in edges:
                edges[u] = {}
            if v not in edges:
                edges[v] = {}
            distance = int(np.linalg.norm(points[u] - points[v]))
            edges[u][v] = distance
            edges[v][u] = distance
    return edges

def write_input_file(filename, alpha, num_nodes, H, s, edges):
    with open(filename, 'w') as f:
        f.write(f"{alpha:.5f}\n")
        f.write(f"{num_nodes} {len(H)}\n")
        f.write(" ".join(map(str, H)) + "\n")
        f.write(f"{s}\n")
        for u in range(num_nodes):
            neighbors = edges.get(u, {})
            f.write(f"{u} {len(neighbors)}\n")
            for v, w in neighbors.items():
                f.write(f"{v} {w}\n")

random.seed(42)
np.random.seed(42)

configs = [
    {"filename": "inputs/20_03.in", "alpha": 0.3, "num_nodes": 20, "num_friends": 10, "s": 1},
    {"filename": "inputs/20_10.in", "alpha": 1.0, "num_nodes": 20, "num_friends": 10, "s": 1},
    {"filename": "inputs/40_03.in", "alpha": 0.3, "num_nodes": 40, "num_friends": 20, "s": 1},
    {"filename": "inputs/40_10.in", "alpha": 1.0, "num_nodes": 40, "num_friends": 20, "s": 1},
]

for config in configs:
    # Extract parameters
    filename = config["filename"]
    alpha = config["alpha"]
    num_nodes = config["num_nodes"]
    num_friends = config["num_friends"]
    s = config["s"]

    # Generate graph
    edges = generate_graph(num_nodes)

    # Select home nodes (nodes 2 to 2+num_friends-1 to avoid 0 and 1)
    H = list(range(2, 2 + num_friends))

    # Write to file
    write_input_file(filename, alpha, num_nodes, H, s, edges)
    print(f"Generated {filename}")


#可能存在的改进
#  1.默认家在（0，0），其他所有点都在第一象限。
#  2.使用了Delaunay方法，将点集生成边集。
# 3.似乎无需优化生成逻辑。bonus主要和solver的性能有关。此程序用于给所有同学提供测试集。
