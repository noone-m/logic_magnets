import pygame
from pprint import pprint
from draw_helpers import draw_dots, draw_tokens, draw_targets
from math import floor
from utils import get_four_sides_cells, pull_down, pull_up, pull_left, pull_right, push_down, push_up, push_left, push_right
from tree import Tree,Node
from copy import deepcopy


class Board:
    def __init__(self):
        self.board = []
        self.targets = []
        self.tokens = {}
        self.height = 0
        self.width = 0
        # self.visited = False

    def init_board(self):
        self.height = int(input('Board height: '))
        self.width = int(input('Board width: '))
        self.board = [['E' for _ in range(self.width)] for _ in range(self.height)]
        
        print('Choose a value for each cell:')
        print('Red (pull) -> R')
        print('Black (normal) -> B')
        print('Purple (push) -> P')
        print('Empty (nothing) -> E')
        print('Does not exist (deleted) -> D')
        
        for i in range(self.height):
            for j in range(self.width):
                value = input(f'Choose a value for ({i},{j}): ').upper()
                while value not in {'R', 'B', 'P', 'E', 'D'}:
                    print("Invalid input. Please enter R, B, P, E, or D.")
                    value = input(f'Choose a value for ({i},{j}): ').upper()
                self.board[i][j] = value
                if value in {"R", "P", "B"}:
                    self.tokens[(i, j)] = value

    def set_targets(self):
        print("Enter target locations (e.g., 0,1) or 'q' to stop:")
        while True:
            target = input('Input target location: ')
            if target.lower() == 'q':
                break
            try:
                row, col = map(int, target.split(','))
                if 0 <= row < self.height and 0 <= col < self.width:
                    if self.board [row][col] == 'D':
                        print("you can't place target in a cell that does not exist")
                    else:
                        self.targets.append((row, col))
                else:
                    print("Location out of bounds.")
            except ValueError:
                print("Invalid format. Enter as row,col.")

    def display_board(self):
        pprint(self.board)


    def draw(self, screen):
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        rect = pygame.Rect(0,0,screen_width,screen_height)
        pygame.draw.rect(screen,(200,100,60),rect)
        space_bet_dots_in_row = floor(screen_width / (self.width + 1))
        space_bet_dots_in_col = floor(screen_height / (self.height + 1))
        i = space_bet_dots_in_row 
        j = space_bet_dots_in_col

        dot_radius = floor(0.2 * min(space_bet_dots_in_row,space_bet_dots_in_col))
        token_radius = floor(0.3 * min(space_bet_dots_in_row,space_bet_dots_in_col))
        target_radius = floor(0.35 * min(space_bet_dots_in_row,space_bet_dots_in_col))
        target_width = floor(0.2 * target_radius)

        for w in range(self.height):
            for z in range(self.width):
                value = self.board[w][z]
                
                # let's draw the dots where a Token can take place
                # in some board it is not alwayse n*n valid places for tokens
                draw_dots(value,screen,(i,j),dot_radius)
                draw_tokens(value,screen,(i,j),token_radius)
                if (w,z) in self.targets:
                    draw_targets(screen,(i,j),target_radius,target_width)
                i += space_bet_dots_in_row
            i = space_bet_dots_in_row
            j += space_bet_dots_in_col
    
    def apply_red_logic(self,row,col):
        """ 
        red token pulls other tokens towards it
        if two token are adjacent one of them is going to be pulled(the closer)
        """
        up_cells,down_cells,left_cells,right_cells = get_four_sides_cells(self,row,col)
        pull_down(self, up_cells)
        pull_up(self,down_cells)
        pull_left(self,right_cells)
        pull_right(self,left_cells)

    def apply_purple_logic(self,row,col):
        """ 
        purple token pulls other tokens towards it
        if two token are adjacent one of them is going to be pulled(the closer)
        """
        up_cells,down_cells,left_cells,right_cells = get_four_sides_cells(self,row,col)
        push_down(self, down_cells)
        push_up(self,up_cells)
        push_left(self,left_cells)
        push_right(self,right_cells)

    def apply_logic(self,token):
        """
        params:
            token(dict) : key is the token position and the value is (R,P)
        """
        row, col = next(iter(token.keys()))
        value = next(iter(token.values()))
        if value == 'R':
            self.apply_red_logic(row,col)
        if value == 'P':
            self.apply_purple_logic(row,col)
        print(f'tokens : {self.tokens}')

    def check_victory(self):
        # Check if all tokens are on their target positions
        return all(pos in self.targets for pos in self.tokens.keys())

    def get_tokens(self):
        red_tokens = []
        purple_tokens = []
        empty_places = []
        black_tokens = []
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 'R':
                    red_tokens.append((i,j))
                if self.board[i][j] == 'P':
                    purple_tokens.append((i,j))
                if self.board[i][j] == 'B':
                    black_tokens.append((i,j))
                if self.board[i][j] == 'E':
                    empty_places.append((i,j))

        return red_tokens,purple_tokens,black_tokens,empty_places

    def get_possible_boards(self):
        """
        we can move red and purple tokens to get a new board
        """
        possible_boards = []
        red_tokens, purple_tokens,_, empty_places = self.get_tokens()
        print(f'self tokens {self.tokens}')
        for token in red_tokens:
            for empty_place in empty_places:
                board = deepcopy(self)
                board.board[token[0]][token[1]] = 'E'
                board.board[empty_place[0]][empty_place[1]] = 'R'
                board.tokens.pop((token[0],token[1]))
                board.tokens[(empty_place[0],empty_place[1])] = 'R'
                board.apply_red_logic(empty_place[0],empty_place[1])
                possible_boards.append(board)
        for token in purple_tokens:
            for empty_place in empty_places:
                board = deepcopy(self)
                board.board[token[0]][token[1]] = 'E'
                board.board[empty_place[0]][empty_place[1]] = 'P'
                board.tokens.pop((token[0],token[1]))
                board.tokens[(empty_place[0],empty_place[1])] = 'P'
                board.apply_purple_logic(empty_place[0],empty_place[1])
                possible_boards.append(board)
            
        
        return possible_boards
    
    def __str__(self):
        return f'board is {self.board}'
    
    def __repr__(self):
        return f'board is {self.board}'
    
