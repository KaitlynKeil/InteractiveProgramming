"""
A simple GUI to generate circle plots based on mathematical constants

Authors: Coleman Ellis and Kaitlyn Keil

SoftDes Spring 2016
"""

from math import *
import pygame
from pygame.locals import QUIT
import time
from random import choice

class CirclePlotView(object):
    """ Visualizes the circle plot in a pygame window """
    def __init__(self, model, screen):
        self.model = model
        self.screen = screen

    def draw(self):
        self.screen.fill(pygame.Color('black'))
        for element in self.model.elements:
            pygame.draw.arc(self.screen, pygame.Color(element.color), model.RECTANGLE, element.start_angle, element.stop_angle, element.width)
        for connection in self.model.connections:
            pygame.draw.line(self.screen, pygame.Color("white"), connection.start_pos, connection.end_pos, connection.width)
        pygame.display.update()

class ElementArc(object):
    """ An arc section that represents an element (integer or word) of the given 
        thing

        Rect = the bounds of the outer circle
        start_angle = the angle (in radians) at which the arc begins
        stop_angle = the angle (in radians) at which the arc ends
    """
#arc(Surface, color, Rect, start_angle, stop_angle, width=1)
    def __init__(self, start_angle, stop_angle, width):
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width
        self.color = choice(["red", "green", "orange", "blue", "purple"])

class ConnectionArc(object):
    """ Connects two elements. Currently a straight line.
    """
    #line(Surface, color, start_pos, end_pos, width=1) -> Rect
    def __init__(self, start_pos, end_pos, width = 1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
    
class CirclePlotModel(object):
    """ Stores the state of the circle plot """
    def __init__(self, element_list, connection_dict, circle_radius = 300):
        self.elements = []
        self.connections = []
        self.ELEMENT_MARGIN_MULTIPLIER = .05
        self.RECTANGLE = pygame.Rect(50, 50, circle_radius * 2, circle_radius * 2)
        self.RADIUS = circle_radius
        self.ELEMENT_WIDTH = 20
        inner_radius = circle_radius - self.ELEMENT_WIDTH

        wedge_angle = 2*pi / len(element_list)
        margin = wedge_angle * self.ELEMENT_MARGIN_MULTIPLIER
        starting_angle = 0
        d_theta = wedge_angle - margin
        centerpoint_dict = {}

        for element in element_list:
            arc = ElementArc(starting_angle, starting_angle + d_theta, self.ELEMENT_WIDTH)
            angle_center = starting_angle + d_theta / 2
            centerpoint_dict[element] = angle_center
            starting_angle += wedge_angle
            self.elements.append(arc)

        # Assumes integers
        for first, second in connection_dict:
            first_point_x = 350 + inner_radius*cos(centerpoint_dict[first])
            first_point_y = 350 + inner_radius*sin(centerpoint_dict[first])
            second_point_x = 350 + inner_radius*cos(centerpoint_dict[second])
            second_point_y = 350 + inner_radius*sin(centerpoint_dict[second])
            connection = ConnectionArc((first_point_x, first_point_y), (second_point_x, second_point_y))
            self.connections.append(connection)

def generate_connection_histogram(input_list):
    """Given a list of strings, generate a histogram of each adjacent
    pair of strings in the list, stored as a dictionary.

    >>> dict, list = generate_connection_histogram(['the','dog','and','the','dog'])
    >>> print dict[('the', 'dog')]
    2
    >>> print dict[('dog', 'and')]
    1
    """
    output_dict = {}
    word_list = []

    for i in range(len(input_list)-1):
        first = input_list[i]
        second = input_list[i+1]
        pair = (first, second)

        if first not in word_list:
            word_list.append(first)

        output_dict[pair] = output_dict.get(pair, 0) + 1

    return output_dict, word_list

def sanitize_float(flt):
    """Given a floating point number, returns a list of the digits of the
    number as strings

    >>> print sanitize_float(3.1415)
    ['3', '1', '4', '1', '5']
    """

    flt_string = str(flt)
    flt_list = list(flt_string)
    flt_list.remove('.')
    return flt_list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    connection_dict, element_list = generate_connection_histogram(sanitize_float(pi))
    # For now, we don't care what the elements actually are; we want to make sure it points
    #  to the right place with all 10 integers.
    element_list = list('0123456789')
    element_list.sort()
    print element_list
    pygame.init()
    size = (700, 700)
    screen = pygame.display.set_mode(size)

    model = CirclePlotModel(element_list, connection_dict)
    view = CirclePlotView(model, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        view.draw()
        time.sleep(.001)