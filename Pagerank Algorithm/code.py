import numpy as np
from scipy.sparse import csr_matrix

# function to read the graph from a .dat file
def read_graph(filename):
    with open(filename) as f:
        num_vertices = int(f.readline().strip())
        num_edges = int(f.readline().strip())
        edges = [tuple(map(int, line.strip().split())) for line in f]
    rows, cols = zip(*edges)
    adj_matrix = csr_matrix(([1] * num_edges, (rows, cols)), shape=(num_vertices, num_vertices))
    return adj_matrix

# function to compute the PageRank scores
def pagerank(adj_matrix, num_iterations=10, damping_factor=0.85):
    num_vertices = adj_matrix.shape[0]
    out_degree = adj_matrix.sum(axis=1).A.flatten()
    transition_matrix = adj_matrix.multiply(1 / out_degree[:, np.newaxis])
    r = np.ones(num_vertices) / num_vertices
    for i in range(num_iterations):
        r = (1 - damping_factor) / num_vertices + damping_factor * transition_matrix.T.dot(r)
        yield r

# read the graph from the input file
adj_matrix = read_graph('HW9/smallrmat.dat')


for i, scores in enumerate(pagerank(adj_matrix)):
    with open(f'result.iter{i+1}', 'w') as f:
        # f.write(f'Iteration {i+1}:\n')
        for score in scores:
            f.write(f'{score:.6g}\n')
