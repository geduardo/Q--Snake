# Módulos
import pygame
import qsharp
from Qrng import GenerateRandomNumber
from pygame.locals import*
import numpy as np

def qrng(max):
    """ Generates a random number using the Q# quantum random bit generator

    :param max: Maximum random number allowed
    :type max: int
    :return: The random number
    :rtype: int
    """    
    output = max + 1 # Variable to store the output
    while output > max:
        bit_string = [] # We initialise a list to store the bits thatesc
        # will define our random integer
        for i in range(0, max.bit_length()): # We need to call the quantum
            # operation as many times as bits are needed to define the
            # maximum of our range. For example, if max=7 we need 3 bits
            # to generate all the numbers from 0 to 7. 
            bit_string.append(GenerateRandomNumber.simulate()) 
            # Here we call the quantum operation and store the random bit
            # in the list
        output = int("".join(str(x) for x in bit_string), 2) 
    return output

# Constants

x_grid_size = 10 # Horizontal length of the map 
y_grid_size = 10 # Vertical length of the map 

# Visualization parameters 

WIDTH = 500
HEIGHT = 500
tile_size = min(HEIGHT/y_grid_size, WIDTH/x_grid_size)
margin = 0.9 # from 0 (whole tile is margin) to 1 (no margin at all)

#Colors

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 150, 0)
BLUE = (0, 0, 255)
BLACK= (0, 0, 0)


# Classes 
class Game:
    def __init__(self):
        """ Defines a matrix to store the information
        """        
        self.map=np.zeros((x_grid_size, y_grid_size))
        self.game_over = False

class Player:
    def __init__(self):
        """Class that represents the snake, i.e, the player.
        """        
        self.snake = [(2,3)] #Initial position
        self.x, self.y = 2, 3 
        self.step = 1
        self.dx, self.dy = 1, 0
        self.speed = 5
        self.points = 0
        self.K= True
    def change_velocity(self, keys):
        """ Function to change velocity as result of keyboard interaction with 
        a marker parameter to avoid several inputs before the movement occurred.

        :param keys: Keyboard input
        :type keys: List of bools?
        """        
        if self.dx == 0 and keys[K_RIGHT] and self.K == True:
            self.dx = 1
            self.dy = 0
            self.K = False
        if self.dx == 0 and keys[K_LEFT] and self.K == True:
            self.dx = -1
            self.dy = 0
            self.K = False
        if self.dy == 0 and keys[K_UP] and self.K == True:
            self.dx = 0
            self.dy = -1
            self.K = False
        if self.dy == 0 and keys[K_DOWN] and self.K == True:
            self.dx = 0
            self.dy = 1 
            self.K = False
    def moving1(self):
        """ Function to add the new tile to the snake each turn in the direction
        of movement.
        """        
        self.x=(self.x+self.dx)%x_grid_size
        self.y=(self.y+self.dy)%y_grid_size
        self.snake.append((self.x, self.y))
    def moving2(self):
        """ Function to pop the tail each step it doesn't eat an apple 
        """
        self.snake.pop(0)

class Apple:
    """Class representing the apples
    """    
    def __init__(self):
           """We use the Q# function to generate the apple position
           """        
           self.x = qrng(x_grid_size-1)
           self.y = qrng(y_grid_size-1)
    def new_apple(self):
        self.x = qrng(x_grid_size-1)
        self.y = qrng(y_grid_size-1)
# Functions
def text(texto, posx, posy, color=(255, 255, 255)):
    """To print text in the screen with Pygame
    """    
    fuente = pygame.font.Font('images/DroidSans.ttf', 25)
    salida = pygame.font.Font.render(fuente, texto, 1, color)
    salida_rect = salida.get_rect()
    salida_rect.centerx = posx
    salida_rect.centery = posy
    return salida, salida_rect
#  -----------------------------------------------------------------------------
def main():
    """Logic of the snake game
    """    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My PySnake")
    game = Game()
    player = Player()
    apple = Apple()
    screen.fill(BLACK)
    clock = pygame.time.Clock()
    while True:
        keys = pygame.key.get_pressed()
        time = clock.tick(player.speed)
        for events in pygame.event.get():
            if events.type == QUIT:
                sys.exit(0)
        #--------------------- Logic of the game -------------------------------
        player.change_velocity(keys)
        player.moving1()
        player.K = True
        if len(player.snake)!=len(set(player.snake)):
            game.game_over = True
        if not (game.game_over):
            if (player.x, player.y) == (apple.x, apple.y):
                while (apple.x, apple.y) in player.snake:
                    apple.new_apple()
                player.speed = player.speed + 0.2
                player.points = player.points + 1
            else:
                player.moving2()
        #--------------------- Drawing the map in the display-------------------
            screen.fill(BLACK)
            game.map = np.zeros((x_grid_size, y_grid_size))
            for (i,j) in player.snake:
                if (i,j) == player.snake[-1]:
                    game.map[i,j] = 3
                else:
                    game.map[i,j] = 1
            game.map[apple.x, apple.y] = 2
            for i in range(0, x_grid_size):
                for j in range(0, y_grid_size):
                    if int(game.map[i,j])==1:
                        pygame.draw.rect(screen,GREEN_DARK,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
                    if int(game.map[i,j])==2:
                        pygame.draw.rect(screen,RED,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
                    if int(game.map[i,j])==3:
                        pygame.draw.rect(screen,GREEN,(i*tile_size,j*tile_size,
                        tile_size*margin,tile_size*margin))
            p_jug, p_jug_rect = text(str(player.points), WIDTH/5, 50)
            screen.blit(p_jug, p_jug_rect)
        if game.game_over:
            screen.fill(BLACK)
            points, points_rect = text('Points: ' + str(player.points), WIDTH/2, HEIGHT/2.2-40)
            game_over, game_over_rect = text('GAME OVER', WIDTH/2, HEIGHT/2.2)
            cont, cont_rect = text('Press C to play again', WIDTH/2, HEIGHT/2.2+40)
            if keys[K_c]:
                game = Game()
                player = Player()
                apple = Apple()
            screen.blit(points, points_rect)
            screen.blit(game_over, game_over_rect)
            screen.blit(cont, cont_rect)
        pygame.display.flip()
         #--------------------- Drawing the map in the display-------------------

main()