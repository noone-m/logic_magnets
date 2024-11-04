import pygame


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
    # let's wait 2 seconds
    pygame.time.wait(2000)  
