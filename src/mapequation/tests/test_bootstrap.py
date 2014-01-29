from Bootstrap import Bootstrap
import networkx as nx
import numpy as np

if __name__ == '__main__':
  # Number of node in the network
  n = 100
  # Probablity for a edges
  p = 0.01
  # Generate a Graph
  G = nx.gnp_random_graph(n, p, directed=True)
  # Generate the edges weights
  lam = 10
  for s,d,edata in G.edges(data=True):
    G[s][d]['weight'] = np.random.poisson(lam, 1).item(0)
  # Generate the Bootstrap
  B = Bootstrap(G)
  for H in B:
    print G.edges(data=True)

