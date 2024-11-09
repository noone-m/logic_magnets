"""
this file is for drawing methods
"""

import pygame
import sys

def draw_dots(value,screen,center,radius):
    """
    this function draw the dots(where it is valid to place a token)

    if the value is D then we don't draq a dot 
    otherwise we draw one

    params:
        board(list): the values in each position
        screen : the screen that we are drawing on
    """
    if value != 'D':
        pygame.draw.circle(screen,(150,100,50),center,radius)


def draw_tokens(value,screen,center,radius):
    """
    draw tokens Red and Purple and Black
    """

    if value == 'B':
        pygame.draw.circle(screen,(50, 50, 50),center,radius)
    elif value == 'R':
        pygame.draw.circle(screen,(255, 0, 0),center,radius)
    elif value == 'P':
        pygame.draw.circle(screen,(128, 0, 128),center,radius)


def draw_targets(screen,center,radius,width):
    """
    draw targets in white

    params:
        screen : the screen
        center : center of the circle
        radius : the radius
        width : the with of the circle
    """ 
    pygame.draw.circle(screen,(255, 255, 255),center,radius,width=width)

def show_victory_message(screen):
    font = pygame.font.Font(None, 74) 
    text = font.render("You Won!", True, (255, 255, 255))  
    text_rect = text.get_rect(center=(400, 300))  
    screen.fill((0, 0, 0)) 
    screen.blit(text, text_rect)  
    pygame.display.flip()  

    # Pause to allow the player to read the message
    # let's wait 2 good seconds
    pygame.time.wait(2000)  


def draw_text(screen, text, x, y, font_size=24, color=(0, 0, 0)):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def draw_menu(screen, pos, bfs_button_rect, dfs_button_rect):
    """
    draw a menu with options to solve the game
    """
    # menu background
    menu_width, menu_height = 200, 100
    button_height = 40
    bg_color = (200, 200, 200)
    hover_color = (180, 180, 180)
    text_color = (0, 0, 0)

    # draw menu background....
    menu_rect = pygame.Rect(pos[0], pos[1], menu_width, menu_height)
    pygame.draw.rect(screen, bg_color, menu_rect, border_radius=8)
    pygame.draw.rect(screen, (100, 100, 100), menu_rect, width=2, border_radius=8)

    # draw BFS button with hover effect
    if bfs_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, bfs_button_rect, border_radius=5)
    else:
        pygame.draw.rect(screen, bg_color, bfs_button_rect, border_radius=5)
    draw_text(screen, "Solve with BFS", bfs_button_rect.x + 10, bfs_button_rect.y + 8, color=text_color)

    # Draw DFS button with hover effect
    if dfs_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, dfs_button_rect, border_radius=5)
    else:
        pygame.draw.rect(screen, bg_color, dfs_button_rect, border_radius=5)
    draw_text(screen, "Solve with DFS", dfs_button_rect.x + 10, dfs_button_rect.y + 8, color=text_color)

def draw_solution_path(path, screen):
    """implement visualization for the path of boards returned by BFS or DFS"""
    
    for board_state in path:
        board_state.value.draw(screen)
        pygame.display.flip()
        pygame.time.delay(4000)  # Delay for each step of visualization
    show_victory_message(screen)
    pygame.quit()
    sys.exit()