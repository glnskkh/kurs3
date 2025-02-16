from framework import *

import igraph as ig
import matplotlib.pyplot as plt
from itertools import pairwise


def draw(partitions: list[Partition]):
    fig, axs = plt.subplots(1, len(partitions))
    fig.set_size_inches(len(partitions), 1)

    for i, partition in enumerate(partitions):
        g = ig.Graph()
    
        g.add_vertices(range(2 * partition.size))
        g.add_edges(
            (edge for cls in range(2 * partition.size) for edge in pairwise(i for i, el in enumerate(partition.repr) if el == cls)),
            attributes={"curved": 0.2},
        )
    
        ig.plot(
            g,
            layout=ig.Layout((i % partition.size, i // partition.size) for i in range(2 * partition.size)),
            vertex_size=10,
            target=axs[i]
        )
