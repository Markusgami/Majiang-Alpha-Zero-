import math
import numpy as np
import zlib
import copy

class MCTS():
    """
    This class handles the MCTS tree.
    """

    def __init__(self, game, nnet):
        self.game = game
        self.nnet = nnet
        self.numMCTSSims = 800
        self.cpuct = 1
        self.Qsa = {}       # stores Q values for s,a (as defined in the paper)
        self.Nsa = {}       # stores #times edge s,a was visited
        self.Ns = {}        # stores #times board s was visited
        self.Ps = {}        # stores initial policy (returned by neural net)
        self.end = 0
        self.Es = {}        # stores game.getGameEnded ended for board s
        self.Vs = {}        # stores game.getValidMoves for board s

    def getActionProb(self, canonicalBoard,board,zimo, temp=1, ):
        """
        This function performs numMCTSSims simulations of MCTS starting from
        canonicalBoard.
        Returns:
            probs: a policy vector where the probability of the ith action is
                   proportional to Nsa[(s,a)]**(1./temp)
        """
        for i in range(self.numMCTSSims):
            print (i)
            self.search(canonicalBoard, board, zimo = zimo)
            

            
        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.game.getActionSize())]
        if temp==0:
            bestA = np.argmax(counts)
            probs = [0]*len(counts)
            probs[bestA]=1
            return probs

        counts = [x**(1./temp) for x in counts]
        probs = [x/float(sum(counts)) for x in counts]
        return probs


    def search(self,canonicalBoard, board,zimo):
        """
        This function performs one iteration of MCTS. It is recursively called
        till a leaf node is found. The action chosen at each node is one that
        has the maximum upper confidence bound as in the paper.
        Once a leaf node is found, the neural network is called to return an
        initial policy P and a value v for the state. This value is propogated
        up the search path. In case the leaf node is a terminal state, the
        outcome is propogated up the search path. The values of Ns, Nsa, Qsa are
        updated.
        NOTE: the return values are the negative of the value of the current
        state. This is done since v is in [-1,1] and if v is the value of a
        state for the current player, then its value is -v for the other player.
        Returns:
            v: the negative of the value of the current canonicalBoard
        """
        self.game.left_cards = copy.copy(board['left_cards'])
        self.game.card_out = copy.copy(board['card_out'])
        self.game.last_action = copy.copy(board['last_action'])
        self.game.players = copy.copy(board['players'])
        self.game.curPlayer = copy.copy(board['curPlayer'])
        self.game.lastPlayer = copy.copy(board['lastPlayer'])
        
        s = self.game.stringRepresentation(canonicalBoard)
        if s not in self.Es:
            self.Es[s] = self.game.getGameEnded(board,zimo = zimo)
                
        if self.Es[s]!=0:
            # terminal node
            print ('胡牌导致search end')
            self.end = 1
            return -self.Es[s]
            

        if s not in self.Ps:
            # leaf node

            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            valids = self.game.getValidMoves(canonicalBoard)
            self.Ps[s] = self.Ps[s]*valids      # masking invalid moves
            self.Ps[s] /= np.sum(self.Ps[s])    # renormalize

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s,a) in self.Qsa:
                    u = self.Qsa[(s,a)] + self.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:
                    u = self.cpuct*self.Ps[s][a]*math.sqrt(self.Ns[s])     # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        
        next_s, next_zimo = self.game.getNextState(board = board, action = a, zimo = zimo)
        next_s = self.game.getCanonicalForm(next_s)
        next_board = self.game.getCurInfo()
        
        v = self.search(next_s, next_board, zimo = next_zimo)

        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1

        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1

        self.Ns[s] += 1
        
        print ('whole search end')

        return -v