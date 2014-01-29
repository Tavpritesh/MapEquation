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

import numpy as np

class Bootstrap:
  def __init__(self, Graph, n=10, weight='weight'):
    self._Graph = Graph
    self._n = n
    self._weight_attribut = weight
    self._current = 0
    # Test if each edge of the graph has an attribut 'weight'
    for u,v,edata in self._Graph.edges(data=True):
      if self._weight_attribut not in self._Graph[u][v]:
        raise AttributeError('The Graph has a missing weight attribut on his edges {} {}'.format(u,v))

  def __iter__(self):
    return self

  def next(self):
    if self._current > self._n:
      raise StopIteration
    else:
      self._current += 1
      return self.generate()

  def generate(self):
    '''
    Generate a random boostrap of the Graph (G)
    '''

    H = self._Graph.copy()
    for u,v,edata in H.edges(data=True):
      lam = int(edata[self._weight_attribut])
      H[u][v]['weight'] = np.random.poisson(lam, 1).item(0  )

    return H