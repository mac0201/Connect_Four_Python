# width = 5
# height = 7
# grid = [[' ' for col in range(width)] for row in range(height)]
from os import error
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
        self.taken_box = '|X|'#'|\u2609|' # Unicode symbol
        self.filled_columns = [False for i in range(width)] # Keep track of filled columns
        print(colored(f"Created {self.width}x{self.height} board.", "blue"))
        self.p1_token = '\x1b[32m☉\x1b[0m'
        self.p2_token = '\x1b[33m☉\x1b[0m'

    SPACE = "        "
    ERROR = ''

    def print_error(self, error):
        print()
        print(colored(error, 'red'))

    def print_board(self):
        # SPACE = "        "
        print(f"{self.SPACE}  {self.display_players()}\n")
        tags = ''
        for row in self.board:
            print(self.SPACE, ''.join(row))

        for tag in range(self.width):
            tags += f" {str(tag+1)} "
        print(self.SPACE, tags)

    def get_player_tokens(self):
        p1 = colored('\u2609', 'green')
        p2 = colored('\u2609', 'yellow')
        return [p1, p2]

    ##! Needed?
    def get_current_player(self):
        return self.current_player

    def update_current_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def check_available(self, column):
        available = []  # available indices to place the disc
        for i in range(self.height):
            if self.board[i][column] == self.empty_box:
                available.append(i)
        if len(available) == 0:
            self.filled_columns[column] = True
            return False
        return available

    def drop(self, column):
        available = self.check_available(column)
        if not available:
            self.ERROR = f'No spaces left in column {column + 1}.'
            return

        token = self.p1_token if self.current_player == self.players[0] else self.p2_token

        row = max(available)
        # print(f'drop in row {row}')
        self.board[row][column] = self.taken_box.replace('X', token)#self.taken_box.replace('\u2609', colored('\u2609', color))
        self.check_available(column)

    def check_win_horizontal(self):
        board = self.board
        win_coords = []
        for row in range(self.height-1, -1, -1):
            for col in range(self.width-3):
                
                check = board[row][col:(col+4)]
                # s.append((row, col))
                win = True if (all(i == f'|{self.p1_token}|' for i in check) or all(i == f'|{self.p2_token}|' for i in check)) else False #

                x = all(i == f'|{self.p1_token}|' for i in check)
                # print(x)


                # for i in check:
                #     if all(i == f'|{self.p1_token}|'):
                #         print("WWWWWWWIIIIIIIIN")
                
                if win: #return True
                    win_coords.append(([row, col], [row, col+3]))
                    print('You have won horizontally!')
                    print(win_coords)
                    return True, win_coords

                    # return True
            # win_coords = []
        return False

    def check_win_vertical(self):
        for col in range(self.width):
            check = []
            for row in self.board:
                check.append(row[col])
            for i in range(len(check)-3):
                win = True if (all(j == f'|{self.p1_token}|' for j in check[i:i+4]) or all(j == f'|{self.p2_token}|' for j in check[i:i+4])) else False                                  #! CHANGE HERE
                if win:
                    print('You have won vertically')
                    return True
        return False



    def display_players(self):
        p1 = self.players[0]
        p2 = self.players[1]
        return f"{colored(p1, 'green')} vs {colored(p2, 'yellow')}"

    def padding(self):
        for i in range(5):
            print()

    def test(self):
        
        self.board[0][3] = '|X|'
        self.board[1][3] = '|X|'
        self.board[2][3] = '|X|'
        self.board[3][3] = '|X|'
        self.print_board()
        self.chceck_win_horizontal()







    def play(self):

        if not len(self.players) == 2:
            self.print_error('Too many players. Max 2!')
            return 

        self.padding()

        print('\n********** CONNECT FOUR **********')
        # print(f"{self.SPACE}  {self.display_players()}\n")

        # game_over = False
        self.print_board()

        while True:
            valid_input = False

            print(f'\nTurn: {self.current_player}')
            # Validate if input is integer
            while not (valid_input):
                inp = input(f'\nSpecify column to place disc (1-{self.width}):  ')
                try:
                    inp = int(inp) # convert to integer
                    if inp in range(1, self.width+1):
                        valid_input = True
                    else:
                        self.print_error('Number out of range.')
                except:
                    self.print_error('Wrong input format.')
            

            

            self.drop(inp - 1)
            self.update_current_player()
            self.padding()
            self.print_board()

            # check for win
            if self.check_win_horizontal() or self.check_win_vertical():
                coords = self.check_win_horizontal()
                # print(coords)
                print("Have you won?")
                print(coords[1])
                return True


            if self.ERROR:
                self.print_error(self.ERROR)


            # make win check work with unicode symbol, instead of X and O

            # win check not working above row 1 (fixed)

            # when win, get the indices of discs and change their colour

            # return False




class Player:
    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'{self.name}'

p1 = Player('Maciej')
p2 = Player('Jack')


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
# game.play()


# def get_free_space(col):
#     available_indices = []
#     for i in range(height):
#         if grid[i][col] == ' ':
#             available_indices.append(i)
#             # print(f'Index {i} is available.')
#         print(grid[i][col].replace(' ', 'x'))
#     print(f'Available indices in column are: {available_indices}')
#     print(f'The disc should be placed in {max(available_indices)}')

#     # for row in grid[row][col]:
#     #     print(row.replace(' ', 'x'))


# get_free_space(0)


# def place_disc(current_player, column):
#     pass
#     # drop current player's disc in specified column


# def switch_player(current_player):
#     # p1 = 0,  p2 = 1
#     print(
#         f'player switched to {"player 1" if current_player == 1 else "player 2"}')
#     return 1 if current_player == 0 else 0


# # drop disc

# # refresh
