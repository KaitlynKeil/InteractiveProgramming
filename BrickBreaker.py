import pygame
from pygame.locals import QUIT, KEYDOWN, MOUSEMOTION
import time
from random import choice


class PygameBrickBreakerView(object):
    """ Visualizes a brick breaker game in a pygame window """
    def __init__(self, model, screen):
        """ Initialize the view with the specified model
            and screen. """
        self.model = model
        self.screen = screen


    def draw(self):
        """ Draw the game state to the screen """
        self.screen.fill(pygame.Color('black'))
        # draw the bricks to the screen
        for brick in self.model.bricks:
            r = pygame.Rect(brick.left, brick.top, brick.width, brick.height)
            pygame.draw.rect(self.screen, pygame.Color(brick.color), r)

        # draw the paddle to the screen
        r = pygame.Rect(self.model.paddle.left,
                        self.model.paddle.top,
                        self.model.paddle.width,
                        self.model.paddle.height)
        pygame.draw.rect(self.screen, pygame.Color('white'), r)
        pygame.display.update()


class Brick(object):
    """ Represents a brick in our brick breaker game """
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.color = choice(["red", "green", "orange", "blue", "purple"])


class Paddle(object):
    """ Represents the paddle in our brick breaker game """
    def __init__(self, left, top, width, height):
        """ Initialize the paddle with the specified geometry """
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class BrickAlt(object):
    pass

class BrickBreakerModel(object):
    """ Stores the game state for our brick breaker game """
    def __init__(self):
        self.bricks = []
        self.MARGIN = 5
        self.BRICK_WIDTH = 40
        self.BRICK_HEIGHT = 20

        new_brick = Brick(5, 5, 40, 20)
        self.bricks.append(new_brick)
        for left in range(self.MARGIN,
                          640 - self.BRICK_WIDTH - self.MARGIN,
                          self.BRICK_WIDTH + self.MARGIN):
            for top in range(self.MARGIN,
                             480/2,
                             self.BRICK_HEIGHT + self.MARGIN):
                brick = Brick(left, top, self.BRICK_WIDTH, self.BRICK_HEIGHT)
                self.bricks.append(brick)
        self.paddle = Paddle(640/2, 480 - 30, 50, 20)

class PyGameKeyboardController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Look for left and right keypresses to
            modify the x position of the paddle """
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT:
            self.model.paddle.left -= 10
        if event.key == pygame.K_RIGHT:
            self.model.paddle.left += 10


class PyGameMouseController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Look for mouse movements and respond appropriately """
        if event.type != MOUSEMOTION:
            return
        self.model.paddle.left = event.pos[0]

if __name__ == '__main__':
    pygame.init()
    size = (640, 480)
    screen = pygame.display.set_mode(size)

    model = BrickBreakerModel()
    view = PygameBrickBreakerView(model, screen)
    controller = PyGameKeyboardController(model)
    #controller = PyGameMouseController(model)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            controller.handle_event(event)
        view.draw()
        time.sleep(.001)
