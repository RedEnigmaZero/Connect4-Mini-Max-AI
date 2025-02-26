import unittest
import math
import numpy as np
from copy import deepcopy
from players import alphaBetaAI
from connect4 import connect4
from montecarlo import monteCarloAI
class TestAlphaBetaAI(unittest.TestCase):
    def setUp(self):
        self.player1 = alphaBetaAI(1, 0, False)
        self.player2 = monteCarloAI(2, 0, False)
        self.env= connect4(
                      self.player1, self.player2, 
                      board_shape=(6,7), 
                      visualize=False, 
                      limit_players=(0, 1), 
                      time_limit='1.0,1.0', 
                      verbose=False, 
                      CVDMode=False, 
                      print_time_logs=False)
        
        positional_weights = [
           [1, 2, 3, 4, 3, 2, 1],
			[2, 7, 8, 8, 8, 7, 2],
			[6, 7, 14, 15, 14, 7, 6],
			[6, 5, 11, 15, 11, 5, 6],
			[3, 4, 11, 15, 11, 4, 3],
			[2, 4, 10, 4, 10, 4, 2]
        ]

        self.player1.positional_weights = positional_weights
        
                
        

   
    def test_term(self):

        self.player1.firstMove = False
        move_dict ={'move': -1}
        
        board = np.array([
				[0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 1, 1, 0],
                [0, 0, 0, 1, 1, 2, 1],
                [0, 0, 0, 1, 2, 2, 1],
                [2, 0, 2, 1, 2, 2, 1]
			]).astype('int32')
        
        self.env.board = board
        self.env.player1.lastMove = 2
        self.env.topPosition = np.array([4,5,4,1,1,1,2])

        
        a = self.player1.play(self.env, move_dict)

        print(move_dict)
        
        
        board2 = np.array([
				[0,  0,  0,  0,  0, 0, 0],
				[0,  0,  0,  0,  0, 0, 0],
				[0,  0,  0,  0,  0, 0, 2],
				[0,  0,  0,  0,  0, 0, 2],
				[0,  0,  0,  1,  0, 0, 2],
				[0,  0,  1,  1,  1, 0, 2]
			]).astype('int32')
        
        self.env.board = board2
        self.env.player1.lastMove = 6
        self.env.topPosition = np.array([5,5,4,3,4,5,1])
        b = self.player1.play(self.env, move_dict)
        print("done")


    """"
    def test_evaluate_function(self):

        board = np.array([
				[0,  0,  0,  0,  0, 0, 0],
				[0,  0,  0,  0,  0, 0, 0],
				[0,  0,  0,  0,  0, 0, 1],
				[0,  0,  0,  0,  0, 0, 1],
				[0,  0,  0,  2,  0, 0, 1],
				[0,  0,  2,  2,  2, 0, 1]
			]).astype('int32')

        self.env.board = board
        self.env.topPosition = np.array([5,5,4,3,4,5,1])


        # Calculate expected score based on positional_weights
        expected_score = (
            # Player 1 scores (positions with weight 1)
            1*(1 + 2 + 3 + 3) +  # Column 6 weights: row 2(3), 3(3), 4(3), 5(1)
            # Player 2 scores (positions with weight -)
            -1*(3 + 4 + 3 + 8)   # Player 2 positions: (5,2)=3, (5,3)=4, (5,4)=3, (4,3)=8
        )
        
        print(self.env.gameOver(6, 1))
        actual_score = self.player1.evaluateFunction(self.env, board)
        print(actual_score)
        self.assertEqual(actual_score, expected_score)


        board2 = np.array([
				[0,  0,  0,  0,  0, 0, 0],
				[0,  0,  0,  2,  0, 0, 0],
				[0,  0,  0,  2,  0, 0, 0],
				[0,  0,  0,  2,  0, 0, 0],
				[0,  0,  0,  2,  1, 0, 0],
				[0,  0,  0,  1,  1, 1, 0]
			]).astype('int32')
        
        self.env.board = board2
        self.env.topPosition = np.array([5,5,5,0,3,4,5])


        # Calculate expected score based on positional_weights
        expected_score2 = (
            # Player 1 scores (positions with weight 1)
            1*(4 + 3 + 2 + 6) +  # Column 6 weights: row 2(3), 3(3), 4(3), 5(1)
            # Player 2 scores (positions with weight -)
            -1*(8 + 12 + 12 + 8)   # Player 2 positions: (5,2)=3, (5,3)=4, (5,4)=3, (4,3)=8
        )

        print(self.env.gameOver(3, 2))
        actual_score2 = self.player1.evaluateFunction(self.env, board2)
        print(actual_score2)
        self.assertEqual(actual_score2, expected_score2)
        
"""
        

    

if __name__ == '__main__':
    unittest.main()