# -*- encoding: utf-8 -*-

# -------------------------------------------------------------------------------
# Copyright (c) 2013 Vincent Gauthier Telecom SudParis.
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

import Communities

class Louvain(Community):
  def louvain_phase_1(self):
    import numpy as np
    # Compute the initial MapEquation
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
    print "### Begining of Phase 1 ###"
    print "---------------------------"
    print "Community id, node id"
    print "---------------------------"
    for k, v in self.iteritems():
      print k,v
    print "### End of Phase 1 ###"


  def louvain_phase_2(self):
    '''
    To be cleaned
    '''
    G = nx.DiGraph()
    weight = self._weight_attribut
    for u,v in self._G.edges():
      u_community_id = self._G.node[u]['community_id']
      v_community_id = self._G.node[v]['community_id']

      # if the nodes belong to different communities
      if u_community_id != v_community_id:
        # if edge between the two communities already exist
        if G.has_edge(u_community_id,v_community_id):
          G[u_community_id][v_community_id][weight] += self._G[u][v][weight]
          if u not in G.node[u_community_id]['nodes_in_community']:
            G.node[u_community_id]['nodes_in_community'].append(u)
            G.node[u_community_id]['nodes_in_community'] = list(set(self._G.node[u]['nodes_in_community']) | set(G.node[u_community_id]['nodes_in_community']))
          if v not in  G.node[v_community_id]['nodes_in_community']:
            G.node[v_community_id]['nodes_in_community'].append(v)
            s1 = set(self._G.node[v]['nodes_in_community'])
            s2 = set(G.node[v_community_id]['nodes_in_community'])
            G.node[v_community_id]['nodes_in_community'] = list(s1 | s2)
        else:
          # Test if node exit
          if G.has_node(v_community_id):
            if v not in G.node[v_community_id]['nodes_in_community']:
              G.node[v_community_id]['nodes_in_community'].append(v)
              s1 = set(self._G.node[v]['nodes_in_community'])
              s2 = set(G.node[v_community_id]['nodes_in_community'])
              G.node[v_community_id]['nodes_in_community'] = list( s1 | s2 )
          else:
            G.add_node(v_community_id)
            G.node[v_community_id]['nodes_in_community'] = [v]
            s1 = set(self._G.node[v]['nodes_in_community'])
            s2 = set(G.node[v_community_id]['nodes_in_community'])
            G.node[v_community_id]['nodes_in_community'] = list( s2 | s1)
          # Test if node exit
          if G.has_node(u_community_id):
            if u not in G.node[u_community_id]['nodes_in_community']:
              G.node[u_community_id]['nodes_in_community'].append(u)
              s1 = set(self._G.node[u]['nodes_in_community'])
              s2 = set(G.node[u_community_id]['nodes_in_community'])
              G.node[u_community_id]['nodes_in_community'] = list( s1 | s2)
          else:
            G.add_node(u_community_id)
            G.node[u_community_id]['nodes_in_community'] = [u]
            s1 = set(self._G.node[u]['nodes_in_community'])
            s2 = set( G.node[u_community_id]['nodes_in_community'])
            G.node[u_community_id]['nodes_in_community'] = list( s1 | s2)

          G.add_edge(u_community_id, v_community_id)
          G[u_community_id][v_community_id][weight] = self._G[u][v][weight]

      # if node belong to the same community
      else:
        G.add_node(u_community_id)
        G.node[u_community_id]['nodes_in_community'] = [u,v]
        s1 = set(self._G.node[u]['nodes_in_community'])
        s2 = set(G.node[u_community_id]['nodes_in_community'])
        s3 = set(self._G.node[v]['nodes_in_community'])
        G.node[u_community_id]['nodes_in_community'] = list(s1 | s2 | s3)

    self._G = G
    self.init_communities()
    #
    # DEBUG
    #
    print "### Begining of Phase 2 ###"
    print "---------------------------"
    print "Community id, node id, nodes_in_community"
    print "---------------------------"
    for k, v in self.iteritems():
      print k,v
    for n in self._G.nodes():
      print self._G.node[n]['nodes_in_community']
    print "### End of Phase 2 ###"
