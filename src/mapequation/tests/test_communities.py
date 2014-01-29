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

try:
  from ..Communities import Communities
except ValueError:
  import sys, os
  sys.path.append(os.path.join('..', '..'))
  from mapequation import Communities

import networkx as nx
import numpy as np
import unittest

class test_Communities(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(test_Communities, self).__init__(*args, **kwargs)
    self.G = nx.DiGraph()
    self.G.add_nodes_from([0,1,2,3])
    self.G.add_edge(0,1, weight=1)
    self.G.add_edge(1,0, weight=1)
    self.G.add_edge(1,2, weight=10)
    self.G.add_edge(2,3, weight=10)
    self.G.add_edge(3,1, weight=10)
    self.G.add_edge(3,2, weight=10)

  def testCommunities_init(self):
    "Test Communities Constructor"
    Communities(self.G)

  def test_Communities_ValueError(self):
    "Test Raises AttributeError when the graph weight are not sets properly"
    self.assertRaises(AttributeError, Communities, self.G, weight='xxxx')

  def test_communities_initial_states(self):
    C = Communities(self.G)
    for k, v in C.iteritems():
      self.assertEqual([k], v)

  def test_nodes_in_community(self):
    "test if the node in community field in each node is empty"
    C = Communities(self.G)
    G = C.graph
    for n in G.nodes():
      self.assertEqual(G.node[n]['nodes_in_community'] , [])

  def test_pageRank(self):
    pr = nx.pagerank(self.G, alpha=0.85)
    C = Communities(self.G, alpha=0.85)
    G = C.graph
    for n in G.nodes():
      self.assertEqual(G.node[n]['pageRank'] , pr[n])



def main():
  unittest.main()

if __name__ == '__main__':
    main()