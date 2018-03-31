'''
File name: ai.py
Author: Bernice Tuazon
Date created: Feb. 28, 2018
Date last modified: Mar. 13, 2018
Class: SDSU, Artificial Intelligence CS550
Prof.: M. Roch

'''
import checkerboard
import abstractstrategy
from math import inf

class Strategy(abstractstrategy.Strategy):
    
    def utility(self, board):
        "Return the utility of the specified board"
    
        util = 0        #value returned, utility of board
        
        #get indices for maxplayer and minplayer for CheckerBoard functions
        max_idx = board.playeridx(self.maxplayer)       
        min_idx = board.playeridx(self.minplayer)
            
        util += board.get_pawnsN()[max_idx] + 2*board.get_kingsN()[max_idx]     #add to util in favor of maxplayer
        util -= board.get_pawnsN()[min_idx] + 2*board.get_kingsN()[min_idx]     #subtract from util not in favor of minplayer
        return util
    
    def play(self, board):
        """"play - Make a move
        Given a board, return (newboard, action) where newboard is
        the result of having applied action to board and action is
        determined via a game tree search (e.g. minimax with alpha-beta
        pruning).
        """     
        print(board)    #show player the current board
        search = AlphaBetaSearch(Strategy, self.maxplayer, self.minplayer, self.maxplies)   #create instance of AlphaBetaSearch
        best_move = search.alphabeta(board)     #find best move using alpha beta search
        newboard = board.move(best_move)        #return a new board based on results of alpha beta search
        return (newboard, best_move)
        
    def evaluation(self, state):
        """Returns an estimate of the expected utility of 
        the game from a given position"""
        evaluator = 0
        max_idx = state.playeridx(self.maxplayer)   #get index for maxplayer for CheckerBoard functions       
        evaluator += state.get_pawnsN()[max_idx] + 2*state.get_kingsN()[max_idx]     #add to evaluator in favor of maxplayer
        if self.verbose:
            print("Evaluation for state is: %d" %evaluator)
        return evaluator


class AlphaBetaSearch:
    """AlphaBetaSearch
    Conduct alpha beta searches from a given state.
    """
     
    #Strategy: red_player = red('r', checkerboard.CheckerBoard, maxplies)
    #AlphaBetaSearch(strategy, 'r', 'b', 3)
    def __init__(self, strategy, maxplayer, minplayer, maxplies = 3,
                  verbose=False):
        """AlphaBetaSearch - Initialize a class capable of alphabeta search
        strategy - implementation of AbstractStrategy class
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the utility function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.strategy = strategy
        self.maxplayer = maxplayer      #red player
        self.minplayer = minplayer      #black player
        self.maxplies = maxplies
        self.verbose = verbose          #default to false
        self.depth = 0
             
    def alphabeta(self, state):
        """alphabeta(state) - Run an alphabeta search from the current
        state. Returns best action.
        """
        #based on pseudocode by Russel and Norvig
        best_val = 0 
        for a in state.get_actions(self.maxplayer):    #get possible actions from current state:
            possible_board = state.move(a)
            val = self.minvalue(possible_board, -inf, inf)  #calculate the minvalue for the MIN player
            if val > best_val:      #use MIN's lowest utility to get best move
                best_val = val
                best_action = a
        return best_action

##################################################################################
    
    #HELPER FUNCTIONS
    def cutoff_test(self, state):
        "cutoff_test(state) - Check if search tree has reached a certain depth"
        #stop search once a certain depth is reached in the tree
        cutoff = self.depth >= self.maxplies or state.is_terminal()[0]
        if self.verbose:
            print("Is there a cut off?")
            print("Depth: %d, Maxplies: %d" %(self.depth, self.maxplies))
            print("Is it terminal?")
            print(state.is_terminal()[0])
            print(cutoff)
        return cutoff
    
    #take the max utility value from moves we can make to maximize utility function
    def maxvalue(self, state, alpha, beta):
        "maxvalue(state, alpha, beta) - Increase utility of MAX player"
        self.depth += 1
        if self.cutoff_test(state):
            if self.verbose:
                print("Cutoff test returns true in maxvalue. Now using evaluation function.\n") 
            return Strategy.evaluation(self, state)
        
        self.v = -inf       #initialize value to -infinity if game is not in winning state
            
        #get possible actions available from current checkerboard state in the view of player who is maximizing utility function
        for a in state.get_actions(self.maxplayer):  #possible actions are children of current state
            child_board = state.move(a)
            #use recursion to go down tree and find MAX's value
            self.v = max(self.v, self.minvalue(child_board, alpha, beta))
            if self.v >= beta: return self.v
            alpha = max(alpha, self.v)  #try to increase alpha (raise MAX's utility)
        return self.v
    
    #take the min utility value from moves the opponent can make to minimize their utility function
    def minvalue(self, state, alpha, beta):
        "minvalue(state, alpha, beta) - Decrease utility of MIN player"
        self.depth += 1
        if self.cutoff_test(state): 
            if self.verbose:
                print("Cutoff test returns true in minvalue. Now using evaluation function.\n") 
            return Strategy.evaluation(self, state)
        self.v = inf
        for a in state.get_actions(self.minplayer): #possible actions are children of current state
            child_board = state.move(a)
            #use recursion to go down tree and find MIN's value
            self.v = min(self.v, self.maxvalue(child_board, alpha, beta))   
            if self.v <= alpha: return self.v
            beta = min(beta, self.v)    #try to lower beta (lower MIN's utility)
        return self.v            