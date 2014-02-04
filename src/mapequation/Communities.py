# -*- encoding: utf-8 -*-

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

import networkx as nx
from functools import partial

class Communities(object):

  #
  # Class Variables
  #
  _G = {}
  _communities = {}
  _nodes = 0
  _alpha = 0
  _DEBUG = False
  #
  # Constructor
  #
  def __init__(self, G, alpha=0.85, weight='weight', debug=False):
    if not isinstance(G, nx.classes.graph.Graph):
      raise AttributeError('The Graph is not an instance of networkx Graph')
    if isinstance(G, nx.classes.multidigraph.MultiDiGraph):
      raise AttributeError('The MultiDiGraph instance is not supported')
    self._DEBUG = debug
    self._G = G.copy()
    self._nodes = len(self._G)
    self._alpha = alpha
    weight_tot = 0.0
    # Test if each edge of the graph has an attribut 'weight'
    self._weight_attribut = weight
    for u,v,edata in self._G.edges(data=True):
      if self._weight_attribut not in edata:
        raise AttributeError('The Graph has a missing weight attribut on edges')


    # Compute the pageRank for the Graph
    self.init_nodes_in_community()
    self.init_communities()
    self.normalize_edges_weight()
    self.compute_pagerank(alpha=alpha)

  def __str__(self):
    self.gen_communities_dict()
    return "Networkx Graph with {} communities found".format(len(self._communities))

  def __unicode__(self):
    self.gen_communities_dict()
    return u"Networkx Graph with {} communities found".format(len(self._communities))

  def __iter__(self):
    '''
    return an Iterator for communites dictionary
    '''
    self.gen_communities_dict()
    return iter(self._communities)

  @property
  def graph(self):
    '''
    Get the graph
    '''
    return self._G

  def iteritems(self):
    self.gen_communities_dict()
    return self._communities.iteritems()

  def init_communities(self):
    '''
    Initialize the communities structure with one single node in each community
    '''
    community_id = 0
    for n in self._G.nodes():
      self._G.node[n]['community_id'] = community_id
      community_id += 1

  def init_nodes_in_community(self):
    for n in self._G.nodes():
      self._G.node[n]['nodes_in_community'] = [n]

  def gen_communities_dict(self):
    '''
    Extract the communities structure from the Graph attributes (self._G)
    '''
    communities = dict()
    for n in self._G.nodes():
      if self._G.node[n]['community_id'] in communities:
        communities[self._G.node[n]['community_id']].append(n)
      else:
        communities[self._G.node[n]['community_id']] = [n]
    self._communities = communities

  def normalize_edges_weight(self):
    '''
    Normalize the
    '''
    weight = self._weight_attribut
    for n in self._G.nodes():
      weight_tot = 0.0
      for neighbor in self._G.neighbors(n):
        weight_tot += self._G[n][neighbor][weight]
      for neighbor in self._G.neighbors(n):
        self._G[n][neighbor][weight] = self._G[n][neighbor][weight]/weight_tot

  def run(self, action):
    p = partial(action)
    return [p(k,v) for k,v in self.iteritems()]

  def compute_pagerank(self, alpha=0.85):
    '''
    Compute  Return the PageRank of the nodes in the graph and store the result in each node of the graph

    Parameters:
    -----------
    alpha : float, optional
      Damping parameter for PageRank, default=0.85
    '''
    # Return the pageRank into a dict
    pangeRank = nx.pagerank(self._G, alpha=alpha)
    # Update the the pageRank of each node in the graph G
    for n in self._G.nodes():
      self._G.node[n]['pageRank'] = float(pangeRank[n])


  def LM(self):
    '''
    MapEquation algorithm
    '''

    # Import
    from numpy import log2

    # Init variables
    q_sum = 0.0

    resultats = self.run(self.exit_probability)
    cId, p_exit, p_i = zip(*resultats)
    q_sum = sum(p_exit)


    #
    # eq. (2,3)
    # SI Appendix of [1]
    #
    # [1] Martin Rosvall and Carl T. Bergstrom,
    # Maps of random walks on complex networks reveal community structure,
    # PNAS 2008 105 (4) 1118-1123.
    H = 0.0
    if q_sum == float('inf'):
        left_eq_1  = float('inf')
    else:
      for q in p_exit:
        H += (q/q_sum) * log2(q/q_sum)
      left_eq_1 = q_sum * H
      print 'left', left_eq_1
    #
    # eq. (4, 5a, 5b)
    # SI Appendix of [1]
    #
    # [1] Martin Rosvall and Carl T. Bergstrom,
    # Maps of random walks on complex networks reveal community structure,
    # PNAS 2008 105 (4) 1118-1123.
    right_eq_1 = 0.0
    if left_eq_1 != float('inf'):
      for r in resultats:
        sum_q_p_i = 0.0
        cId, q, p_i = r
        # eq(4)
        sum_q_p_i = q+sum(p_i)
        # eq(5a)
        Hp_a = (q/sum_q_p_i) * log2(q/sum_q_p_i)
        # eq(5b) HERE IS THE ERROR
        Hp_b = sum([(p/sum_q_p_i) * log2(p/sum_q_p_i) for p in p_i])
        print 'Hp_a', Hp_a, 'Hp_b', Hp_b, 'sum_q_p_i', sum_q_p_i
        right_eq_1 += sum_q_p_i * (Hp_a + Hp_b)

    Lm = left_eq_1 + right_eq_1
    print 'right_eq_1', right_eq_1
    return Lm

  def exit_probability(self, community_id, nodes_in_community):
    '''
    eq (7) Appendix S1 of [1]

    [1] Martin Rosvall and Carl T. Bergstrom,
    Maps of random walks on complex networks reveal community structure,
    PNAS 2008 105 (4) 1118-1123.

    Parameters:
    -----------
    community_id : interger
      community identifier

    nodes_in_community: list
      list of node id inside a given community id

    Returns:
    --------
    (p_exit, p_ergodic_stay, p_i): tulpe (float, float, list)
      p_exit: Probability of extiting the community
      p_ergodic_stay: Probability of staying the community
    '''
    p_exit = 0.0
    p_ergodic_stay = 0.0
    weight = self._weight_attribut
    nb_node_in_community = len(nodes_in_community)
    if nb_node_in_community == len(self._G.nodes()):
      p_exit = float('inf')
    p_i = []
    # Compute the exit probability of each node in the community
    for n in nodes_in_community:
      p_ergodic_stay += self._G.node[n]['pageRank']
      p_i.append(self._G.node[n]['pageRank'])
      # For each link outside the community n
      for neighbor in self._G.neighbors(n):
        if neighbor not in nodes_in_community:
          p_exit += self._G.node[n]['pageRank'] * self._G[n][neighbor][weight]
      # Compute the P_exit as funtion of the pageRank of each node in the community
      p_exit *= self._alpha
      p_exit += ((1-self._alpha) *
        ((self._nodes - nb_node_in_community)/(self._nodes - 1)) *
        p_ergodic_stay)

    return (community_id, p_exit, p_i)

