import random
import pygame
import math
from connect4 import connect4
import sys
from copy import deepcopy
import time
import numpy as np

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
		self.first_move = True  # Hardcode first move to center
		self.killer_moves = {} 
		self.weights = np.array([
			[1,  1,  3,  5,  3, 1, 1],
			[2,  4,  6,  8,  6, 4, 2],
			[3,  6,  12, 15, 12, 6, 3],
			[3,  6,  12, 15, 12, 6, 3],
			[2,  4,  6,  8,  6, 4, 2],
			[0,  1,  2,  3,  2, 1, 0],
		])

	def play(self, env: connect4, move_dict: dict) -> None:
		start_time = time.time()

		if self.first_move and env.topPosition[3] >= 0:
			move_dict['move'] = 3
			self.first_move = False
			return
			
		best_move = 3
		max_depth = 5
		time_per_depth = 0.4

		while time.time() - start_time < 2.5:
			time_remaining = 2.5 - (time.time() - start_time)
			max_possible_depth = max_depth + int(time_remaining // time_per_depth)
			for depth in range(max_depth, max_possible_depth + 1):
				result = self.alpha_beta(env, max_depth, -float('inf'), float('inf'), True, start_time)
				if result[1] is not None:
					best_move = result[1]
					self.killer_moves[max_depth] = best_move
		
			max_depth = max_possible_depth + 1
		move_dict['move'] = best_move
	
	def alpha_beta(self, env: connect4, depth: int, alpha: float, beta: float, maximizing_player: bool, start_time: float):
		#if time.time() - start_time > 2.9:
			#return self.evaluate_board(env.board), None
		
		if np.all(env.topPosition < 0) or depth == 0:
			return self.evaluate_board(env.board), None
		
		possible_moves = self.order_moves(env, depth)

		if maximizing_player:
			max_eval = -float('inf')
			best_move = possible_moves[0]
			for move in possible_moves:
				if env.topPosition[move] < 0:
					continue

				# Simulate the move
				new_env = self.simulate_move(env, move, self.position)

				# Check if move is winner
				new_env.gameOver(move, self.position)
				if new_env.is_winner:
					return math.inf, move
				else:
					# Recursively call alpha_beta for the opponent
					eval = self.alpha_beta(new_env, depth - 1, alpha, beta, False, start_time)[0]

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
			min_eval = float('inf')
			best_move = None
			for move in possible_moves:
				# Simulate the move
				new_env = self.simulate_move(env, move, 3-self.position)

				new_env.gameOver(move, 3-self.position)
				if new_env.is_winner:
					eval = -math.inf
				else:
					# Recursively call alpha_beta for the player
					eval = self.alpha_beta(new_env, depth - 1, alpha, beta, True, start_time)[0]

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
			score = 0
			# Threat-based scoring (10x higher priority)
			threat_score += self.evaluate_threats(board) 
			score += threat_score * 100000
			
			# Positional scoring (secondary)
			positional_score = 0
			for r in range(6):
				for c in range(7):
					if board[r][c] == self.position:
						positional_score += self.weights[r][c]
					elif board[r][c] == (3 - self.position):
						positional_score -= self.weights[r][c]
			score += positional_score * 0.1  # Reduce weight impact
			
			return score

	def evaluate_threats(self, board):
		threat_score = 0  # Initialize here

		# Check horizontal windows
		for r in range(6):
			for c in range(4):
				window = list(board[r, c:c+4])
				threat_score += self.evaluate_window(window)
		
		# Check vertical windows
		for c in range(7):
			for r in range(3):
				window = [board[r+i][c] for i in range(4)]
				threat_score += self.evaluate_window(window)
		
		# Check diagonal windows
		for r in range(3):
			for c in range(4):
				window = [board[r+i][c+i] for i in range(4)]
				threat_score += self.evaluate_window(window)
				window = [board[r+i][c+3-i] for i in range(4)]
				threat_score += self.evaluate_window(window)
		
		return threat_score

	def order_moves(self, env, depth=0):
		possible_moves = [col for col in range(7) if env.topPosition[col] >= 0]

		
		# Prioritize moves that block opponent's 3-in-a-row
		threat_scores = []
		for col in possible_moves:
			threat_score = 0
			# Simulate opponent dropping in this column
			temp_env = self.simulate_move(env, col, 3 - self.position)
			threat_score = self.evaluate_threats(temp_env.board)
			threat_scores.append(threat_score)
		
		# Order by most dangerous opponent threats first
		ordered = sorted(zip(possible_moves, threat_scores), key=lambda x: x[1])
		return [move for move, score in ordered]

	def simulate_move(self, env, move, player):
		new_env = deepcopy(env)
		row = new_env.topPosition[move]
		new_env.board[row][move] = player
		new_env.topPosition[move] -= 1
		return new_env
	
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




