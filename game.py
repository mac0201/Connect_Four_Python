from termcolor import colored

class Connect_Four:
    def __init__(self, width: int, height: int, players: list):
        self.width = width
        self.height = height
        self.empty_box = '| |'
        self.board = [[self.empty_box for col in range(width)]
                      for row in range(height)]
        self.players = players
        self.current_player = self.players[0]
        self.filled_columns = [False for i in range(width)] # Keep track of filled columns
        print(colored(f"Created {self.width}x{self.height} board.", "blue"))
        self.taken_box = '|X|'
        self.p1_token = '\x1b[32m☉\x1b[0m'
        self.p2_token = '\x1b[33m☉\x1b[0m'

    SPACE = "        "
    ERROR_FULL = ''

    def __repr__(self) -> str:
        return f'   Game of Connect Four.\n   Size: {self.width}x{self.height}\n   Players: {self.players[0]} [GREEN]  and  {self.players[1]} [YELLOW]'

    def print_error(self, error):
        print()
        print(self.SPACE, colored(error, 'red'))

    def get_player_tokens(self):
        p1 = colored('\u2609', 'green')
        p2 = colored('\u2609', 'yellow')
        return [p1, p2]

    def display_players(self):
        return f"{colored(self.players[0], 'green')} vs {colored(self.players[1], 'yellow')}"

    def padding(self):
        """ Creates padding between the printed boards in each game loop """
        for i in range(5):
            print()

    def update_current_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]


    def print_board(self):
        """ Prints the game board with column number tags """
        print(f"{self.SPACE}  {self.display_players()}\n")
        tags = ''
        for row in self.board:
            print(self.SPACE, ''.join(row))
        for tag in range(self.width):
            tags += f" {str(tag+1)} "
        print(self.SPACE, tags)


    def check_available(self, column):
        """
            Checks if there are any available cells in specified column. Empty cell index is added to list which gets returned after loop finished.
            If no available cells, set field in class filled_columns array at given column index to True, which keeps track of full columns.

            Returns list of available indices in the column  
        """
        available = []  # available indices to place the disc
        for i in range(self.height):
            if self.board[i][column] == self.empty_box:
                available.append(i)
        if len(available) == 0:
            self.filled_columns[column] = True
            return False
        return available


    def drop(self, column):
        """
            Drops current player's disc in the specified column, given there are available cells. Return if none.
            If cells available, disc is added to last available cell; for example, if cells 0-4 are available, disc is placed in cell 4
            Taken boxes are initially marked with 'X', but are replaced with coloured player tokens.
        """
        available = self.check_available(column)
        if not available:
            self.ERROR_FULL = f'No spaces left in column {column + 1}.'
            self.update_current_player()
            return
        token = self.p1_token if self.current_player == self.players[0] else self.p2_token
        # self.update_current_player()
        row = max(available)
        self.board[row][column] = self.taken_box.replace('X', token)
        self.check_available(column)

    def check_win_horizontal(self):
        """ 
            Checks for winning combination horizontally. 
            Returns an array containing winning coordinates and the direction, otherwise returns False
         """
        win_coords = []
        for row in range(self.height-1, -1, -1):
            for col in range(self.width-3):
                check = self.board[row][col:(col+4)]
                win = True if (all(i == f'|{self.p1_token}|' for i in check) or all(i == f'|{self.p2_token}|' for i in check)) else False 
                if win: #return True
                    win_coords.append([row, col, col+3])
                    return win_coords, 'horizontal'
        return False

    def check_win_vertical(self):
        """ 
            Checks for winning combination vertically. 
            Returns an array containing winning coordinates and the direction, otherwise returns False
         """
        win_coords=[]
        for col in range(self.width):
            check = []
            for row in self.board:
                check.append(row[col])
            for i in range(len(check)-3):
                if (all(j == f'|{self.p1_token}|' for j in check[i:i+4]) or all(j == f'|{self.p2_token}|' for j in check[i:i+4])):
                    win_coords.append([col, i, i+3])
                    return win_coords, 'vertical'
        return False


    def check_win_diagonal_right(self):
        """ 
            Checks for winning combination diagonally, right /. 
            Returns an array containing winning coordinates and the direction, otherwise returns False
         """
        win_coords = []
        for row in range(self.height-1, 2, -1):
            for col in range(0, self.width-3):
                check = []
                for i in range(4):
                    check.append(self.board[row-i][col+i])
                if all(i == f'|{self.p1_token}|' for i in check) or all(i == f'|{self.p2_token}|' for i in check):
                    win_coords = []
                    for i in range(4):
                        win_coords.append([row-i, col+i])
                    return win_coords, 'diagonal_right'
        return False
               
               
    def check_win_diagonal_left(self):
        win_coords = []
        for row in range(self.height-1, 2, -1):
            for col in range(self.width-1, 2, -1):
                check = []
                for i in range(4):
                    check.append(self.board[row-i][col-i])
                if all(i == f'|{self.p1_token}|' for i in check) or all(i == f'|{self.p2_token}|' for i in check):
                    win_coords = []
                    for i in range(4):
                        win_coords.append([row-i, col-i])
                    return win_coords, 'diagonal_left'
        return False


    def check_win(self):
        """ 
            Uses defined win-checking functions. Each function returns either False (if no win) or iterable containing winning coordinates, and the direction. 
            If return is the iterable, pass into change_colour function to change colours.

            Returns True if win, else switches current player and returns False
         """
        h = self.check_win_horizontal()
        v = self.check_win_vertical()
        d_r = self.check_win_diagonal_right()
        d_l = self.check_win_diagonal_left()
        if v:
            self.change_color(v[0], v[1])
            return True
        if h:
            self.change_color(h[0], h[1])
            return True
        if d_r:
            for i in range(0, 4):
                self.change_color(d_r[0][i], d_r[1])
            return True
        if d_l:
            for i in range(4):
                self.change_color(d_l[0][i], d_l[1])
            return True
        
        self.update_current_player()
        return False
        

    def change_color(self, coords, direction):
        """ Change the colour of winning player's discs at passed coordinates, in the direction specified """
        if direction == 'diagonal_right' or direction == 'diagonal_left':
            self.board[coords[0]][coords[1]] = '|\x1b[31m☉\x1b[0m|'
        else:
            c = coords[0][0]    # Row or Column index
            start = coords[0][1] # index of starting row/col
            end = coords[0][2] # index of ending row/col
            for i in range(start, end + 1):
                if direction == 'horizontal':
                    self.board[c][i] = '|\x1b[31m☉\x1b[0m|'    
                if direction == 'vertical':
                    self.board[i][c] = '|\x1b[31m☉\x1b[0m|'



    def test(self):
        t = self.get_player_tokens()
        #! Horizontal
        # self.board[1][1] = f'|{t[0]}|'
        # self.board[1][2] = f'|{t[0]}|'
        # self.board[1][3] = f'|{t[0]}|'
        # self.board[1][4] = f'|{t[0]}|'

        #! Vertical
        # self.board[1][1] = f'|{t[0]}|'
        # self.board[2][1] = f'|{t[0]}|'
        # self.board[3][1] = f'|{t[0]}|'
        # self.board[4][1] = f'|{t[0]}|'

        #! Diagonal Right   
        # self.board[3][0] = f'|{t[0]}|'
        # self.board[2][1] = f'|{t[0]}|'
        # self.board[1][2] = f'|{t[0]}|'
        # self.board[0][3] = f'|{t[0]}|'

        #! Diagonal Left

        # self.board[3][0] = f'|{t[0]}|'
        # self.board[4][1] = f'|{t[0]}|'
        # self.board[5][2] = f'|{t[0]}|'
        # self.board[6][3] = f'|{t[0]}|'


        # self.board[0][0] = f'|{t[0]}|'
        # self.board[1][1] = f'|{t[0]}|'
        # self.board[2][2] = f'|{t[0]}|'
        # self.board[3][3] = f'|{t[0]}|' 


        # self.board[0][1] = f'|{t[0]}|'
        # self.board[1][2] = f'|{t[0]}|'
        # self.board[2][3] = f'|{t[0]}|'
        # self.board[3][4] = f'|{t[0]}|'    

        self.print_board()

        if self.check_win():
            print('WON')
        
        self.print_board()


    def play(self):

        if self.width < 4 or self.height < 4:
            self.print_error('Board must be at least 4x4')
            return
        if not len(self.players) == 2:
            self.print_error('Number of players must be equal to 2.')
            return 

        self.padding()
        print('\n********** CONNECT FOUR **********')
        self.print_board()

        while True:
            valid_input = False
            print(f'\nTurn: {self.current_player}')
            # Validate if input is integer
            while not (valid_input):
                inp = input(f'\nSpecify column to place disc (1-{self.width}):  ')
   
                if inp == 'exit': return
                try:
                    inp = int(inp) # convert to integer
                    if inp in range(1, self.width+1):
                        valid_input = True
                    else:
                        self.print_error('Number out of range.')
                except:
                    self.print_error('Wrong input format.')
    
            # Input valid, continue...
            self.drop(inp - 1)

            if self.check_win():
                self.padding()
                self.print_board()
                print(f'\n{self.SPACE} {self.current_player} has won!')
                return True

            self.padding()
            self.print_board()

            if all(self.filled_columns):
                self.print_error('GAME OVER - DRAW')
                # print(f'{self.SPACE} GAME OVER - DRAW')
                return False

            if self.ERROR_FULL:
                self.print_error(self.ERROR_FULL)
                self.ERROR_FULL = ''


class Player:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}'

p1 = Player('Maciej')
p2 = Player('Julia')

game = Connect_Four(5, 7, [p1, p2])

game.play()
