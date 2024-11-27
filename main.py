import pygame
import sys
from board import Board
from utils import handle_left_click,find_solution_bfs,find_solution_dfs,find_solution_ucs, find_solution_hill_climbing
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
ucs_button_rect = pygame.Rect(0, 0, 180, 40)
hc_button_rect = pygame.Rect(0, 0, 180, 40)
path = find_solution_hill_climbing(board)
print(path)



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
                    elif ucs_button_rect.collidepoint(event.pos):
                        try:
                            path,cost = find_solution_ucs(board)
                            draw_solution_path(path, screen)
                        except Exception:
                            pass
                        print('ucs')
                        menu_open = False
                    elif hc_button_rect.collidepoint(event.pos):
                        try:
                            path,cost = find_solution_hill_climbing(board)
                            print(f'cost is {cost}')
                            draw_solution_path(path, screen)
                        except Exception:
                            pass
                        print('hc')
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
                ucs_button_rect.topleft = (menu_position[0] + 10, menu_position[1] + 90)
                hc_button_rect.topleft = (menu_position[0] + 10, menu_position[1] + 130)
                print("menu opened at:", menu_position)  

    board.draw(screen)
    if menu_open:
        draw_menu(screen, menu_position, bfs_button_rect, dfs_button_rect,ucs_button_rect,hc_button_rect)

    pygame.display.flip()


    if board.check_victory():
        show_victory_message(screen)
        running = False

pygame.quit()
sys.exit()

