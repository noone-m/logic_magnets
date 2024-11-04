import pygame
import sys
from board import Board
from utils import handle_click
from draw_helpers import show_victory_message

board = Board()
board.init_board()
board.set_targets()
board.display_board()

selected_token = {'value': None}

pygame.init()
screen = pygame.display.set_mode((800,600))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('down')
            handle_click(board,event.pos,selected_token)
    board.draw(screen)
    pygame.display.flip()
    victory = board.check_victory()
    if victory:
        show_victory_message(screen)
        running = False
pygame.quit()
sys.exit()