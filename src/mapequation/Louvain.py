# -*- encoding: utf-8 -*-
from __future__ import print_function
# -------------------------------------------------------------------------------
# Copyright (c) 2014 Vincent Gauthier Telecom SudParis.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# -------------------------------------------------------------------------------

__author__ = """\n""".join(['Vincent Gauthier <vgauthier@luxbulb.org>'])

try:
  from ..Communities import Communities
except ValueError:
  import sys, os
  sys.path.append(os.path.join('..'))
  from mapequation.Communities import Communities

import networkx as nx
import numpy as np

class Louvain(Communities):

  def __init__(self, *args, **kwargs):
    super(Louvain, self).__init__(*args, **kwargs)

  def louvain_phase_1(self):
    # Compute the initial MapEquation for all communities
    for n in self._G.nodes():
      config = dict()
      ME = self.LM()
      config[self._G.node[n]['community_id']] = np.abs(ME)
      for neighbor in self._G.neighbors(n):
        if self._G.node[neighbor]['community_id'] != self._G.node[n]['community_id'] :
          community_id = self._G.node[n]['community_id']
          self._G.node[n]['community_id'] = self._G.node[neighbor]['community_id']
          ME_new = self.LM()
          config[self._G.node[n]['community_id']] = np.abs(ME_new)
      ## End For

      # Search the local minimum
      min_val = None
      for k,v in config.iteritems():
        if min_val == None:
          min_val = v
          min_community = k
        if v < min_val:
          min_val = v
          min_community = k
      self._G.node[n]['community_id'] = min_community
    ## End For


    #
    # DEBUG
    #
    if self._DEBUG:
      print('')
      print("### Begining of Phase 1 ###")
      print("---------------------------")
      print("Community_id \t node_id")
      print("---------------------------")
      for k, v in self.iteritems():
        print("{}\t\t{}".format(k,v))
      print("### End of Phase 1 ###")

    return self

  def louvain_phase_2(self):
    '''
    To Check
    '''
    G = nx.DiGraph()
    weight = self._weight_attribut
    for u,v in self._G.edges():
      u_community_id = self._G.node[u]['community_id']
      v_community_id = self._G.node[v]['community_id']

      # if the nodes belong to different communities
      if u_community_id != v_community_id:
        G = self.egdes_fusion(G, u_community_id, u, v_community_id, v)
      # if node u,v belong to the same community
      else:
        G.add_node(u_community_id)
        G = self.add_node_in_community(G, u_community_id, u)
        G = self.add_node_in_community(G, u_community_id, v)
    self._G = G
    self.init_communities()
    #
    # DEBUG
    #
    if self._DEBUG:
      print("### Begining of Phase 2 ###")
      print("---------------------------")
      print("Community id, node id, nodes_in_community")
      print("---------------------------")
      for k, v in self.iteritems():
        print('{}\t{}\t'.format(k,v), end='')
        for n in v:
          print(self._G.node[n]['nodes_in_community'], end='')
        print('')
      print("### End of Phase 2 ###")
      print('')

    return self

  def egdes_fusion(self, G, u_community_id, u, v_community_id, v):
    weight = self._weight_attribut
    # if edge between the two communities already exist
    if G.has_edge(u_community_id,v_community_id):
      G[u_community_id][v_community_id][weight] += self._G[u][v][weight]
      G = self.add_node_in_community(G, u_community_id, u)
      G = self.add_node_in_community(G, v_community_id, v)
    else:
      G.add_edge(u_community_id, v_community_id)
      self.add_node_in_community(G,v_community_id, v)
      self.add_node_in_community(G,u_community_id, u)
      G[u_community_id][v_community_id][weight] = self._G[u][v][weight]
    return G

  def get_node_in_community(self, community):
    nodes = self._communities[community]
    node_in = []
    for n in nodes:
      for nn in self._G.node[n]['nodes_in_community']:
        node_in.append(nn)
    return node_in

  def add_node_in_community(self, G, community_id, u):
    # Initialize awith a empty list
    if 'nodes_in_community' not in G.node[community_id]:
      G.node[community_id]['nodes_in_community'] = []

    nn = self._G.node[u]['nodes_in_community']

    if nn[0] not in G.node[community_id]['nodes_in_community']:
      s1 = set(self._G.node[u]['nodes_in_community'])
      s2 = set(G.node[community_id]['nodes_in_community'])
      G.node[community_id]['nodes_in_community'] = list( s1 | s2)
    return G

  def run_louvain(self):
    self.louvain_phase_1()
    self.louvain_phase_2()
    self.normalize_edges_weight()
    try:
      self.compute_pagerank(alpha=self._alpha)
    except nx.NetworkXError as e:
      return -1
    return 0



