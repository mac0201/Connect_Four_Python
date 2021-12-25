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
                win = True if (all(j == f'|{self.p1_token}|' for j in check[i:i+4]) or all(j == f'|{self.p2_token}|' for j in check[i:i+4])) else False  
                if win:
                    win_coords.append([col, i, i+3])
                    return win_coords, 'vertical'
        return False


    def check_win_diagonal_right(self):
        win_coords = []
        for row in range(self.height-1, 2, -1):
            # print(self.board[row])
            check = []
            print(row)
            b = self.board
            for col in range(0, self.width-3):

                print('current col: ', col)
                # print(self.board[row][col])

                # check.append([b[row][col],  b[row-1][col+1], b[row-2][col+2], b[row-3][col+3]]) # WORKS
                # check = []
                check = []
                for i in range(4):
                    print(b[row-i][col+i])
                    check.append(b[row-i][col+i])
                if all(i == f'|{self.p1_token}|' for i in check):
                    print('**************************************** WIN')
                    coord = []
                    for i in range(4):
                        coord.append([row-i, col+i])
                    print('coords = ')
                    print(coord)
                    return coord, 'diagonal_right'

                    
                #     check.append(b[row-i][col+i])
                # # check.append(c)

                # # print('current check:')
                # # print(check)
                # win = True if (all(i == f'|{self.p1_token}|' for i in check)) else False
                # if win:
                #     #! Update here
                #     print('WON!!!!')
                #     # print([row-i, col+i] for i in range(0, 4))
                #     for i in range(0,4):
                #         print(row-i, col+i)
                #     win_coords.append([[row-i, col+i] for i in range(0, 4)])
                    # return win_coords[0], 'diagonal_right'



                    # for i in range(0, 4):
                    #     # win_coords.append([row-i, col+i])
                    #     win_coords.append([row])
                    # return win_coords
                # print(self.board[row:(row+3)][col:(col+3)])
                # print()
                # check = self.board[row:(row-3)][col:(col+3)]
                # # print(check)

                # print(win)
                # if win:
                #     win_coords.append([row, row+3])
            # return False
            # print(check)
            print()
                # print(win_coords)

    def check_win(self):
        """ 
            Uses defined win-checking functions. Each function returns either False (if no win) or iterable containing winning coordinates, and the direction. 
            If return is the iterable, pass into change_colour function to change colours.

            Returns True if win, else switches current player and returns False
         """
        h = self.check_win_horizontal()
        v = self.check_win_vertical()
        d_r = self.check_win_diagonal_right()
        # if v:
        #     self.change_color(v[0], v[1])
        #     return True
        # if h:
        #     self.change_color(h[0], h[1])
        #     return True
        if d_r:
            print("DR WINNNN")
            coords_list = d_r[0]
            for i in range(0, 4):
                self.change_color_diag(coords_list[i], 'diagonal_right')
                # print(coords_list[i])
            self.print_board()
            return True
            # print(d_r[0])
        self.update_current_player()
        return False


    def change_color_diag(self, coords, direction):
        # print('passed:')
        # print(coords)
        # print(f'{coords[0]}, {coords[1]}')
        c1 = coords[0]
        c2 = coords[1]
        # print(c1, c2)
        # pass
        self.board[c1][c2] = '|\x1b[31m☉\x1b[0m|'
        # for i in range(c1, c2+1):
        #     self.board[c1][c2] = '|\x1b[31m☉\x1b[0m|'
             

    def change_color(self, coords, direction):
        """ Change the colour of winning player's discs at passed coordinates, in the direction specified """
        c = coords[0][0]    # Row or Column index
        start = coords[0][1] # index of starting row/col
        end = coords[0][2] # index of ending row/col
        for i in range(start, end + 1):
            if direction == 'vertical':
                self.board[i][c] = '|\x1b[31m☉\x1b[0m|'
            if direction == 'horizontal':
               self.board[c][i] = '|\x1b[31m☉\x1b[0m|'     
            if direction == 'diagonal_right':
                pass
            if direction == 'diagonal_left':
                pass
        
        self.print_board()


    def test(self):
        t = self.get_player_tokens()
        token = f'|{t[0]}|'
        token2 = f'|{t[1]}|'
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
        self.board[3][0] = f'|{t[0]}|'
        self.board[2][1] = f'|{t[0]}|'
        self.board[1][2] = f'|{t[0]}|'
        self.board[0][3] = f'|{t[0]}|'

        # self.board[6][0] = f'|{t[0]}|'
        # self.board[5][1] = f'|{t[0]}|'
        # self.board[4][2] = f'|{t[0]}|'
        # self.board[3][3] = f'|{t[0]}|'

        # self.board[5][0] = f'|5|'
        # self.board[4][1] = f'|6|'
        # self.board[3][2] = f'|7|'
        # self.board[2][3] = f'|8|'
        
        
        # self.board[6][1] = f'|{t[0]}|'
        # self.board[5][2] = f'|{t[0]}|'
        # self.board[4][3] = f'|{t[0]}|'
        # self.board[3][4] = f'|{t[0]}|'


        #! Diagonal Left
        # self.board[0][0] = token
        # self.board[1][1] = token
        # self.board[2][2] = token
        # self.board[3][3] = token

        x = self.check_win_diagonal_right()
        print(x)

        self.print_board()
        if self.check_win():
            print('WON')






    def play(self):
        if not len(self.players) == 2:
            self.print_error('Too many players. Max 2!')
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
                print(f'{self.SPACE} {self.current_player} has won!')
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

#! TEST DATA
# game.drop(1)
# game.drop(1)
# game.drop(1)
# game.drop(1)
# game.update_current_player()
# game.drop(2)
# game.drop(3)
# game.drop(4)


# game.play()
game.test()
