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

def pagerank(G, weight='weight', max_iter=100000, tol=1e-14, alpha=0.85):
  # Init
  W=nx.stochastic_graph(G, weight=weight)
  personalization = dict.fromkeys(W, 0)
  p = dict.fromkeys(W, 0)
  sumW = sum([edata['weight'] for u,v,edata in G.edges(data=True)])

  # Personalization Vector
  for n in G.nodes():
    personalization[n] = float(G.out_degree(n,weight='weight'))/sumW

  # Classical PageRank Algorithm with personalization vector
  pr = nx.pagerank(W,
                   max_iter=max_iter,
                   tol=tol,
                   alpha=alpha,
                   personalization=personalization)

  # Final step: compute the unrecorded Teleportation
  for u in W.nodes():
    for v in nx.neighbors(W,u):
      p[v] += W[u][v]['weight']*pr[u]

  # normalize vector results
  s=1.0/sum(p.values())
  for k,v in p.iteritems():
    p[k]*=s
  return p