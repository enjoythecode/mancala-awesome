# implemented from mcts.ai

# transferring from Amazons

from math import *
import random

MAX_ITERATIONS = 30000


class GameNode:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """
    def __init__(self, move=None, parent=None, state=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentnode = parent  # "None" for the root node
        self.childnodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_possible_moves()  # future child nodes
        self.playerJustMoved = state.playerJustMoved  # the only part of the state that the node needs later
        
    def select_child_ucb(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childnodes, key=lambda c: c.wins/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def add_child(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = GameNode(move=m, parent=self, state=s)
        self.untriedMoves.remove(m)
        self.childnodes.append(n)
        return n
    
    def update(self, result):
        """ update this node - one additional visit and result additional wins. result must be from the viewpoint of
        playerJustmoved.
        """
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + \
               str(self.untriedMoves) + "]"


class MancalaPlayer():
    def __init__(self, friend):
        self.friend = friend

    def next_move(self, root_state):
        #global node
        """ Conduct a UCT search for iter_max iterations starting from root_state.
            Return the best move from the root_state.
            Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

        root_node = GameNode(state=root_state)

        for i in range(MAX_ITERATIONS):
            node = root_node
            state = root_state.clone()

            # Select
            while node.untriedMoves == [] and node.childnodes != []:  # node is fully expanded and non-terminal
                node = node.select_child_ucb()
                state.make_move(node.move)

            # Expand
            if node.untriedMoves:  # if we can expand (i.e. state/node is non-terminal)
                m = random.choice(node.untriedMoves) 
                state.make_move(m)
                node = node.add_child(m, state)  # add child and descend tree

            # Roll-out - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
            possible_moves = state.get_possible_moves()
            while possible_moves:  # while state is non-terminal
                state.make_move(random.choice(possible_moves))
                possible_moves = state.get_possible_moves()

            # Back-propagate
            while node is not None:  # back-propagate from the expanded node and work back to the root node
                node.update(state.check_game_end())  # state is terminal. update node with result from POV of playerJustMoved
                node = node.parentnode

        return sorted(root_node.childnodes, key=lambda c: c.visits)[-1].move  # return the move that was most visited
