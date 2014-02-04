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

  def louvain(self):
    from random import shuffle
    # Compute the  MapEquation for all communities
    self._LM = np.abs(self.LM())
    # For all communities
    community_id = list(self.keys())
    shuffle(community_id)
    for k in community_id:
      if k in self._communities:
        print('community',k)
        community = self._communities[k]
        # For all node in community
        config = {}
        for node in community:
          # For all node's neighbor not in the same community
          for neighbor in self._G.neighbors(node):
            if self._G.node[neighbor]['community_id'] != k :
              # try to move all the nodes inside one community into the neighbor's community
              # and Recompute the LM
              comTo = self._G.node[neighbor]['community_id']
              comFrom = self._G.node[node]['community_id']
              node_moved = self.moveToCommunity(comFrom, comTo)
              new_LM = np.abs(self.LM())
              if new_LM < self._LM:
                config[new_LM] = (comFrom,comTo)
              # move the node back into their original community
              self.moveNodeToCommunity(node_moved, comFrom)
          if len(config.keys()):
            min_val = min(config.keys())
            (comFrom, comTo) = config[min_val]
            self.moveToCommunity(comFrom, comTo)
            self._LM = np.abs(self.LM())

    #self._LM = self.LM()

    # Debug
    if self._DEBUG:
      print('')
      print("### Louvain ###")
      print("---------------------------")
      print("Community_id \t node_id")
      print("---------------------------")
      for k, v in self.iteritems():
        print("{}\t\t{}".format(k,v))
      print('---------------------------')
      print('LM :', self._LM)
      print("### End ###")
    return self._LM

  def moveToCommunity(self, communityFrom, communityTo):
    node_moved = []
    for node in self._G.nodes():
      if self._G.node[node]['community_id'] == communityFrom:
        self._G.node[node]['community_id'] = communityTo
        node_moved.append(node)
    return node_moved

  def moveNodeToCommunity(self, node_set, communityTo):
    for node in node_set:
      self._G.node[node]['community_id'] = communityTo

  def run_louvain(self):
    LM = float('inf')
    stop = True
    while stop:
      LM_new = self.louvain()
      if LM_new < LM:
        LM = LM_new
      else:
        stop = False
    return LM



