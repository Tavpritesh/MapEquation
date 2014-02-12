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
  from ..pagerank import pagerank_unrecorded
except ValueError:
  import sys, os
  sys.path.append(os.path.join('..', '..'))
  from mapequation.pagerank import pagerank_unrecorded

import unittest
import networkx as nx

class test_pagerank(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(test_pagerank, self).__init__(*args, **kwargs)
    # Graph
    self.D = nx.DiGraph()
    self.D.add_nodes_from([1,2,3,4,5])
    self.D.add_edge(1,2, weight=9.0)
    self.D.add_edge(2,3, weight=10.0)
    self.D.add_edge(3,1, weight=10.0)
    self.D.add_edge(3,2, weight=10.0)
    self.D.add_edge(1,4, weight=1.0)
    self.D.add_edge(4,5, weight=1.0)
    self.D.add_edge(5,2, weight=1.0)
    self.D.add_edge(5,4, weight=1.0)
    # Build the personalization Vector
    self._personalization = dict.fromkeys(self.D, 0)
    sumW = sum([edata['weight'] for u,v,edata in self.D.edges(data=True)])
    # Personalization Vector
    for n in self.D.nodes():
      self._personalization[n] = float(self.D.out_degree(n,weight='weight'))/sumW
    # Result
    self.result_pr = {1: 0.18715871661599273,
      2: 0.38048280772432452,
      3: 0.35829410749590934,
      4: 0.038149187065269964,
      5: 0.035915181098503418
    }

  def test_pagerank_algo(self):
    W = nx.stochastic_graph(self.D, weight='weight')
    prs = pagerank_unrecorded(W, personalization=self._personalization, weight='weight')
    for key,val in prs.iteritems():
      self.assertEqual(val , self.result_pr[key])

