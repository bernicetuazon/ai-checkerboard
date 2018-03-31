'''
File name: checkers.py
Author: Bernice Tuazon
Date created: Feb. 28, 2018
Date last modified: Mar. 13, 2018
Class: SDSU, Artificial Intelligence CS550
Prof.: M. Roch

'''
import imp      #tonto
import sys      #tonto

import time     
import datetime

import checkerboard
# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.5 and 3.6 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
#import tonto

# human - human player, prompts for input    
import human
import boardlibrary # might be useful for debugging -import tonto
import ai

#importing tonto
major = sys.version_info[0]
minor = sys.version_info[1]
modpath = "__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
tonto = imp.load_compiled("tonto", modpath)

def elapsed(earlier, later):
    """elapsed - Convert elapsed time.time objects to duration string
    """
    return time.strftime('%H:%M:%S', time.gmtime(later - earlier))
           

def Game(red=human.Strategy, black=ai.Strategy, 
         maxplies=5, init=None, verbose=False, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 
    """

    red_player = red('r', checkerboard.CheckerBoard, maxplies)  #human player
    black_player = black('b', checkerboard.CheckerBoard, maxplies)  #computer player
    
    board = checkerboard.CheckerBoard()     #instance of checkerboard used to play games
    
    game_start= time.time()                 #start timer for start of game
    while not board.is_terminal()[0]:       #continue taking turns until a player has won
        if verbose:
            print(board)
        move_start = time.time()            #start timer to show how long red takes to make a move
        [red_board, red_action] = red_player.play(board)        #allow red player, a human, to make a move
        current = time.time()               #end timer to show how long red takes to make a move
        if verbose:
            print("Red player moved {}".format(red_action))
            print("Move time: {} Game time: {}".format(
                elapsed(move_start, current), elapsed(game_start, current)))
        
        #use board returned after red_player has made a move
        move_start = time.time()            #start timer to show how long black takes to make a move
        [black_board, black_action] = black_player.play(red_board)      #allow black player, the computer, to make a move
        current= time.time()                #mark time for how long black player took to make a turn
        if verbose:
            print("Black player moved {}".format(black_action))
            print("Move time: {} Game time: {}".format(
                elapsed(move_start, current), elapsed(game_start, current)))
        board = black_board                 #copy board for red player to play with at next turn of loop 
    
    #while loop ends when a player has won
    print("Congratulations to player %c!", board.is_terminal()[1])

if __name__ == "__main__":
    Game()  
        
     
    
