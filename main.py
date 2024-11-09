import pygame
import sys
from board import Board
from utils import handle_left_click,find_solution_bfs,find_solution_dfs
from draw_helpers import show_victory_message, draw_menu, draw_solution_path

# Initialize the board and pygame
board = Board()
board.init_board()
board.set_targets()
board.display_board()
selected_token = {'value': None}
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
menu_open = False
menu_position = (0, 0)
bfs_button_rect = pygame.Rect(0, 0, 180, 40)
dfs_button_rect = pygame.Rect(0, 0, 180, 40)


while running:
    # let me clear the screen with white background
    screen.fill((255, 255, 255)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                # Handle left click: close menu if it's open and not clicking a button
                if menu_open:
                    if bfs_button_rect.collidepoint(event.pos):
                        path = find_solution_bfs(board)
                        draw_solution_path(path, screen)
                        print('bfs')
                        menu_open = False
                    elif dfs_button_rect.collidepoint(event.pos):
                        path = find_solution_dfs(board)
                        draw_solution_path(path, screen)
                        print('dfs')
                        menu_open = False
                    else:
                        # Close the menu if clicked outside of buttons
                        menu_open = False
                else:
                    handle_left_click(board, event.pos, selected_token)
            elif event.button == pygame.BUTTON_RIGHT:
                # Open menu on right-click and set menu position
                menu_open = True
                menu_position = event.pos
                bfs_button_rect.topleft = (menu_position[0] + 10, menu_position[1] + 10)
                dfs_button_rect.topleft = (menu_position[0] + 10, menu_position[1] + 50)
                print("menu opened at:", menu_position)  

    board.draw(screen)
    if menu_open:
        draw_menu(screen, menu_position, bfs_button_rect, dfs_button_rect)

    pygame.display.flip()


    if board.check_victory():
        show_victory_message(screen)
        running = False

pygame.quit()
sys.exit()
