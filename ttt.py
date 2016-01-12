#-----------------------------Tic Tac Toe-----------------------------------------
#If the two players are smart enough, there is no way that any one can win.
#The only way that conducts to the winning is player one is on the offensive, and 
#	he put the chess piece in the center, while the other one put the piece at the
#	mid-point of each side.

#Author: LuCima


class tictactoe:
	def __init__(self):
		self.pos = [[0, 0, 0], [0, 0, 0],[0, 0, 0]]
		self.step = 0 #Game step
		self.seq  = 1 #1 means offensive pos, while 2 means defensive pos, user
		self.ai_seq = 2
		self.seq_dict = {}
		self.graph = []
		self.check = [[0 for x in range(3)] for y in range(8)]
		self.new_game = 0

# Method of Get
	def get_seqdict(self):
		return self.seq_dict

	def get_pos(self):
		return self.pos
	
	def get_step(self):
		return self.step

	def get_check(self):
		return self.check

# Method of Set
	def set_seq(self, seq):
		'''Set sequence of players'''
		self.seq	= seq
		self.ai_seq = 3 - seq
		self.seq_dict = {str(self.seq):"Human", str(self.ai_seq):"Computer"}
	
# Private method 
	def __transform(self, var):
		'''Transform from number to symbol'''
		if var == 1:
			return "X"
		elif var == 2:
			return "O"
		else:
			return " "

	def __set_pos(self, x, y, num = 2):
		'''Put a piece in the chessboard'''
		self.pos[x][y] = num

	def __check_convert(self, line, ind):
		'''Convert coodinates from check to grid'''
		x, y = 0, 0
		if line <= 2:
			x = line
			y = ind
		elif line <= 5:
			x = ind
			y = line - 3
		elif line == 6:
			x = y = ind
		elif line == 7:
			x = ind
			y = 2 - ind
		return (x, y)

	def __get_lines(self):
		'''Get all lines'''
		self.check = []
		row		= [self.pos[x] for x in range(3)]
		temp = [[self.pos[x][y] for x in range(3)] for y in range(3)]
		column  = [temp[i] for i in range(3)]
		dia		= [self.pos[i][i] for i in range(3)]
		cdia	= [self.pos[i][2 - i] for i in range(3)]
		self.check = row + column
		self.check.append(dia)
		self.check.append(cdia)

# AI
	def ai(self):
		'''AI'''
		print("AI's turn:")
		x, y = 1, 1
		ind = 0
		pos = 0
		line = []
		defense = {}
		prior = [[0, 0, 0] for x in range(3)]
		for ind, line in enumerate(self.check):			
			if line.count(0) == 0:
				continue
			elif line.count(0) == 1:
				x, y = self.__check_convert(ind, line.index(0))		
				if line.count(self.ai_seq) == 2:
					#Win
					prior[x][y] += 11
				elif line.count(self.seq) == 2:
					#Block
					prior[x][y] += 6
				else:
					prior[x][y] += 1	
			elif line.count(0) == 2:
				pos_list = [] 
				for l_ind, val in enumerate(line):
					if val == 0:
						pos_list.append(self.__check_convert(ind, l_ind))
					else:
						continue
						
				if self.ai_seq in line:
					add_val = 3
				else:
					add_val = 2
				for i in pos_list:
					prior[i[0]][i[1]] += add_val
					
			elif line.count(0) == 3:
				pos_list = [self.__check_convert(ind, x) for x in range(3)]
				for i in pos_list:
					prior[i[0]][i[1]] += 4

		max_val = 0
		for ind, val in enumerate(prior):
			for ind_y, j in enumerate(val):
				if max_val < j:
					x = ind
					y = ind_y
					max_val = j
				else:
					continue
		self.__set_pos(x, y, self.ai_seq)
		self.__get_lines()

# Other functions
	def print_pos(self):
		'''Print the chessboard'''
		self.graph = [list(map(self.__transform, self.pos[y])) for y in range(3)]
		for i in range(3):
			out = '|'.join(self.graph[i])
			print(out)

	def get_input(self):
		'''Get input from human player'''
		while True:
			try:
				x, y = input("Please input the pos of the sign (1~3, 1~3): ").split(",")
				x, y = int(x), int(y)
			except ValueError:
				print("Please input digitals!")
				continue
			else:
				if x < 0 or x > 3 or y < 0 or y > 3:
					print("Error scope!")
					continue
				elif self.pos[x - 1][y - 1] != 0: 
					print("Error place!")	
					continue
				break
		self.__set_pos(x - 1, y - 1, self.seq)
		self.__get_lines()
	
	def nstep(self):
		'''Add number of step'''
		self.step += 1
		return self.step
	
	def check_win(self):
		'''Check if which player wins'''
		for i in self.check:
			if i[0] == i[1] and i[1] == i[2]:
				return i[0]
			else:
				continue
		return 0

	def c_game(self):
		'''Whether create a new game'''
		n = input("Another game?: Y/N ")
		if n == "Y" or n == "y":	
			self.new_game = 1
		else:
			self.new_game = 0
		return self.new_game	

#Game starts
new = 1

while True:
	if new == 1:
		t = tictactoe()
		seq = int(input("Please choose the sequence, 1 for offensive, 2 for defensive: "))
		t.set_seq(seq)
		t.print_pos()
		new = -1
	elif new == 0:
		break
	else:
		pass

	if seq == 1:
		t.get_input()
		seq = 2
	else:
		t.ai()
		seq = 1	

	t.print_pos()
	t.nstep()

	if t.get_step() >= 5:
		win = t.check_win()
		if win == 0:
			if t.get_step() == 9:
				print("Draw")
				new = t.c_game()
			else:
				continue
		else:
			sd = t.get_seqdict()
			print('{0} wins the game'.format(sd[str(win)]))
			new = t.c_game()

print("Bye Bye")

