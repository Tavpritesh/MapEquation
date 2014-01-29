from Communities import Communities
import networkx as nx
import numpy as np

if __name__ == '__main__':
  # Number of node in the network
  n = 10
  # Probablity for a edges
  p = 0.3
  lam = 15.0
  G = nx.DiGraph()
  G.add_node(1)
  G.add_node(2)
  G.add_node(3)
  G.add_node(4)

  G.add_edge(1,2, weight=1)
  G.add_edge(2,1, weight=1)

  G.add_edge(2,3, weight=10)
  G.add_edge(3,4, weight=10)
  G.add_edge(4,2, weight=10)
  G.add_edge(4,3, weight=10)
  #print G.neighbors(1)
  pr1=nx.pagerank(G,alpha=0.85)
  print 'pageRank :', pr1
  # for n in G.nodes():
  #   weight_tot = 0.0
  #   for neighbor in G.neighbors(n):
  #     weight_tot += G[n][neighbor]['weight']
  #   for neighbor in G.neighbors(n):
  #     G[n][neighbor]['weight'] = G[n][neighbor]['weight']/weight_tot

  # pr2=nx.pagerank(G,alpha=0.85)
  #print pr1, pr2

  C = Communities(G)
  C.louvain_phase_1()
  C.louvain_phase_2()
  #C.louvain_phase_2()