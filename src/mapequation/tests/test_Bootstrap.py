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

try:
  from ..Bootstrap import Bootstrap
except ValueError:
  import sys, os
  sys.path.append(os.path.join('..', '..'))
  from mapequation.Bootstrap import Bootstrap

import networkx as nx
import numpy as np
import unittest

class test_Bootstrap(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(test_Bootstrap, self).__init__(*args, **kwargs)
    self.G = nx.DiGraph()
    self.G.add_nodes_from([0,1,2,3])
    self.G.add_edge(0,1, weight=1)
    self.G.add_edge(1,0, weight=1)
    self.G.add_edge(1,2, weight=10)
    self.G.add_edge(2,3, weight=10)
    self.G.add_edge(3,1, weight=10)
    self.G.add_edge(3,2, weight=10)
    self.weight = [10, 8, 5, 8, 0, 1]

  def test_init(self):
    B = Bootstrap(self.G)

  def test_init_n(self):
    B = Bootstrap(self.G, n=100)
    cpt = 0
    for b in B:
      cpt += 1
    self.assertEqual(cpt,100)

  def test_init_weight(self):
    self.assertRaises(AttributeError,Bootstrap, self.G, weight='xxxxx')

  def test_generate(self):
    B = Bootstrap(self.G, n=1, seed=1)
    g = B.next()
    for u,v, edata in g.edges(data=True):
      self.assertEqual(edata['weight'], self.weight.pop())

def main():
  unittest.main()

if __name__ == '__main__':
    main()