import random
import pygame
import math
from connect4 import connect4
import sys
from copy import deepcopy
import time
import numpy as np
import heapq

class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict["move"] = -1

class humanConsole(connect4Player):
	'''
	Human player where input is collected from the console
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		move_dict['move'] = int(input('Select next move: '))
		while True:
			if int(move_dict['move']) >= 0 and int(move_dict['move']) <= 6 and env.topPosition[int(move_dict['move'])] >= 0:
				break
			move_dict['move'] = int(input('Index invalid. Select next move: '))

class humanGUI(connect4Player):
	'''
	Human player where input is collected from the GUI
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move_dict['move'] = col
					done = True

class randomAI(connect4Player):
	'''
	connect4Player that elects a random playable column as its move
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move_dict['move'] = random.choice(indices)

class stupidAI(connect4Player):
	'''
	connect4Player that will play the same strategy every time
	Tries to fill specific columns in a specific order 
	'''
	def play(self, env: connect4, move_dict: dict) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move_dict['move'] = 3
		elif 2 in indices:
			move_dict['move'] = 2
		elif 1 in indices:
			move_dict['move'] = 1
		elif 5 in indices:
			move_dict['move'] = 5
		elif 6 in indices:
			move_dict['move'] = 6
		else:
			move_dict['move'] = 0

class minimaxAI(connect4Player):
	'''
	This is where you will design a connect4Player that 
	implements the minimiax algorithm WITHOUT alpha-beta pruning
	'''

	def play(self, env: connect4, move_dict: dict) -> None:
		start_time = time.time()
		max_depth = 4
		best_move = self.minimax(env, max_depth, True, start_time)[1]
		move_dict['move'] = best_move


	def minimax(self, env: connect4, depth: int, maximizing_player: bool, start_time: float):
		if time.time() - start_time > 2.9:
			return self.evaluate_board(env.board, self.position), None
		
		if depth == 0 or env.gameOver(-1, self.position):
			return self.evaluate_board(env.board, self.position), None
		
		possible_moves = [col for col in range(env.shape[1]) if env.topPosition[col] >= 0]
		possible_moves.sort(key=lambda x: abs(x - 3))

		if maximizing_player:
			max_eval = -float('inf')
			best_move = None
			for move in possible_moves:
				new_env = deepcopy(env)
				new_env.board[new_env.topPosition[move]][move] = self.position
				new_env.topPosition[move] -= 1

				eval = self.minimax(new_env, depth - 1, False. start_time)[0]

				if eval > max_eval:
					max_eval = eval
					best_move = move
			return max_eval, best_move
		else:
			min_eval = float('inf')
			best_move = None
			for move in possible_moves:
				new_env = deepcopy(env)
				new_env.board[new_env.topPosition[move]][move] = 3 - self.position
				new_env.topPosition[move] -= 1

				eval = self.minimax(new_env, depth - 1, True. start_time)[0]

				if eval < min_eval:
					min_eval = eval
					best_move = move
			return min_eval, best_move
	
	def evaluate_board(self, board, player):
		opponent = 3 - player
		score = 0

		score_two = 1
		score_three = 10
		score_four = 1000
		center_weight = 2

		for row in range(board.shape[0]):
			for col in range(board.shape[1] - 3):
				window = list(board[row, col:col+4])
				score = self.evaluate_window(window, player, opponent, score_two, score_three, score_four)
		
		center_cols = [2, 3, 4]
		for col in center_cols:
			for row in range(board.shape[0]):
				if board[row][col] == player:
					score += center_weight
		
		return score
	
	def evaluate_window(self, window, player, opponent, score_two, score_three, score_four):
		score = 0

		player_count = window.count(player)
		opponent_count = window.count(opponent)

		if player_count == 4:
			score += score_four
		elif player_count == 3 and opponent_count == 0:
			score += score_three
		elif player_count == 2 and opponent_count == 0:
			score += score_two


		if opponent_count == 4:
			score -= score_four
		elif opponent_count == 3 and player_count == 0:
			score -= score_three
		elif opponent_count == 2 and player_count == 0:
			score -= score_two

		return score

	

class alphaBetaAI(connect4Player):
	'''
	This is where you will design a connect4Player that 
	implements the minimiax algorithm WITH alpha-beta pruning
	'''

	def __init__(self, position, seed=0, CVDMode=False):
		super().__init__(position, seed, CVDMode)
		self.weights = np.array([
			[1,  2,  3,  4,  3, 2, 1],
            [2,  4,  6,  8,  6, 4, 2],
            [3,  6,  9, 12,  9, 6, 3],
            [3,  6,  9, 12,  9, 6, 3],
            [2,  4,  6,  8,  6, 4, 2],
            [1,  2,  3,  4,  3, 2, 1]
		])

	def play(self, env: connect4, move_dict: dict) -> None:
		best_move = self.alpha_beta_search(env, depth=4)
		move_dict['move'] = best_move

	def alpha_beta_search(self, env, depth):
		_, best_move = self.alpha_beta(env, depth, -math.inf, math.inf, True)
		return best_move
		
	def alpha_beta(self, env: connect4, depth: int, alpha: float, beta: float, maximizing_player: bool):
		
		if env.gameOver:
			return -math.inf
		
		if depth == 0:
			return self.evaluate_board(env.board), None
		
		possible_moves = self.order_moves(env, maximizing_player)
		best_move = possible_moves[0] if possible_moves else None

		if maximizing_player:
			max_eval = -math.inf
			for move in possible_moves:
				if env.topPosition[move] < 0:
					continue

				# Simulate the move
				new_env = self.simulate_move(env, move, self.position)

				# Recursively call alpha_beta for the opponent
				eval, _ = self.alpha_beta(new_env, depth - 1, alpha, beta, False)


				# Update the best move
				if eval > max_eval:
					max_eval = eval
					best_move = move
				# Update alpha
				alpha = max(alpha, eval)

				# Prune the branch if beta <= alpha
				if beta <= alpha:
						break
			return max_eval, best_move
		else:
			min_eval = math.inf
			best_move = None
			for move in possible_moves:
				# Simulate the move
				new_env = self.simulate_move(env, move, 3-self.position)

				# Recursively call alpha_beta for the player
				eval, _ = self.alpha_beta(new_env, depth - 1, alpha, beta, True)

				# Update the best move
				if eval < min_eval:
					min_eval = eval
					best_move = move
				# Update beta
				beta = min(beta, eval)

				# Prune the branch if beta <= alpha
				if beta <= alpha:
						break
			return min_eval, best_move

	def evaluate_board(self, board):
			# Positional score
			positional_score = np.sum(board * self.positional_weights)
			
			# Threat analysis
			threat_score = 0
			# Horizontal
			for r in range(6):
				for c in range(4):
					window = list(board[r, c:c+4])
					threat_score += self.evaluate_window(window)
			# Vertical
			for c in range(7):
				for r in range(3):
					window = [board[r+i][c] for i in range(4)]
					threat_score += self.evaluate_window(window)
			# Diagonals
			for r in range(3):
				for c in range(4):
					window = [board[r+i][c+i] for i in range(4)]
					threat_score += self.evaluate_window(window)
					window = [board[r+i][c+3-i] for i in range(4)]
					threat_score += self.evaluate_window(window)
			
			return threat_score * 1000 + positional_score

	def order_moves(self, env, maximizing=True):
		possible_moves = [col for col in range(7) if env.topPosition[col] >= 0]
		move_scores = []

		for move in possible_moves:
			temp_env = self.simulate_move(env, move, 
				self.position if maximizing else 3 - self.position)
				
				# Immediate win check
			if self.is_winning_move(temp_env, move):
				score = self.win_score if maximizing else self.lose_score
			# Immediate loss check
			elif self.is_losing_move(temp_env, move):
				score = self.lose_score if maximizing else self.win_score
			else:
				score = self.evaluate_board(temp_env.board)
				
			move_scores.append((score, move))
		
		reverse_sort = maximizing
		move_scores.sort(reverse=reverse_sort, key=lambda x: x[0])
		return [move for _, move in move_scores]


	def simulate_move(self, env, move, player):
		new_env = deepcopy(env)
		row = new_env.topPosition[move]
		new_env.board[row][move] = player
		new_env.topPosition[move] -= 1
		return new_env
	
	def is_winning_move(self, env, move):
		temp_env = deepcopy(env)
		temp_env.gameOver(move, self.position)
		return temp_env.is_winner

	def is_losing_move(self, env, move):
		temp_env = deepcopy(env)
		temp_env.gameOver(move, 3 - self.position)
		return temp_env.is_winner
	
	def evaluate_window(self, window):
			opponent = 3 - self.position
			player_count = window.count(self.position)
			opponent_count = window.count(opponent)

			# Immediate win/loss
			if player_count == 4: return math.inf
			if opponent_count == 4: return -math.inf

			# Player threats
			if opponent_count == 0:
				if player_count == 3: return 10000
				if player_count == 2: return 100

			# Opponent threats
			if player_count == 0:
				if opponent_count == 3: return -10000
				if opponent_count == 2: return -1000
			
			return 0

	

# Defining Constants
SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




