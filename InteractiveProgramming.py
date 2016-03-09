"""
A simple GUI to generate circle plots based on mathematical constants

Authors: Coleman Ellis and Kaitlyn Keil

SoftDes Spring 2016
"""

from math import *
import pygame
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygbutton import PygButton
import time
from random import choice

def color_surface(surface, red, green, blue):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = red
    arr[:,:,1] = green
    arr[:,:,2] = blue

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
            pygame.draw.line(self.screen, pygame.Color(connection.color), connection.start_pos, connection.end_pos, connection.width)
        for button in self.model.buttons:
            button.draw(self.screen)
        for label in self.model.labels:
            self.screen.blit(label.im,label.pos)    

        pygame.display.update()

class ElementArc(object):
    """ An arc section that represents an element (integer or word) of the given 
        thing

        Rect = the bounds of the outer circle
        start_angle = the angle (in radians) at which the arc begins
        stop_angle = the angle (in radians) at which the arc ends
    """
#arc(Surface, color, Rect, start_angle, stop_angle, width=1)
    def __init__(self, start_angle, stop_angle, color, width):
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width
        self.color = color

class ConnectionArc(object):
    """ Connects two elements. Currently a straight line.
    """
    #line(Surface, color, start_pos, end_pos, width=1) -> Rect
    def __init__(self, start_pos, end_pos, color, width = 1):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width
        self.color = color

class ModelButton(PygButton):
    """ A PygButton that changes what number's plot is displayed

    rect = bounds of the button
    im = image of the button to display
    num = number to generate model from"""
    def __init__(self, rect, im, num):
        self.num = num

        #Initialize a PygButton using the rectangle and image provided
        super(ModelButton, self).__init__(rect,'',(0,0,0),(0,0,0),None,im,None,None)      

        #Make the buttons white
        self.surfaceNormal.convert_alpha()
        color_surface(self.surfaceNormal,255,255,255) 
        self.surfaceNormal = pygame.transform.scale(self.surfaceNormal,(50,50))

        self.surfaceHighlight = pygame.transform.scale(self.surfaceHighlight,(50,50))
        color_surface(self.surfaceHighlight,255,255,128)
        self.surfaceDown = self.surfaceHighlight

        self._rect = pygame.Rect(rect)

class Label(object):
    """ Makes a label object """
    def __init__(self, file_name, pos, color):
        self.file_name = file_name
        self.pos = pos
        self.color = color

        self.color = pygame.Color(self.color)
        self.r = self.color.r
        self.g = self.color.g
        self.b = self.color.b

        self.im = pygame.image.load(file_name)
        self.im = pygame.transform.scale(self.im, (20, 40))
        self.im.convert_alpha()
        color_surface(self.im,self.r,self.g,self.b)
    
class CirclePlotModel(object):
    """ Stores the state of the circle plot """
    def __init__(self, number, button_list, circle_radius = 400):
        self.elements = []
        self.connections = []
        self.buttons = button_list
        self.labels = []
        self.ELEMENT_MARGIN_MULTIPLIER = .05
        self.CIRCLE_MARGIN = 50
        self.RECTANGLE = pygame.Rect(self.CIRCLE_MARGIN, self.CIRCLE_MARGIN, circle_radius * 2, circle_radius * 2)
        self.RADIUS = circle_radius
        self.ELEMENT_WIDTH = 20
        self.CIRCLE_CENTER = self.CIRCLE_MARGIN + circle_radius
        inner_radius = circle_radius - self.ELEMENT_WIDTH

        connection_list, element_histogram = generate_connection_histogram(sanitize_float(number))

        # For now, we don't care what the elements actually are; we want to make sure it points
        # to the right place with all 10 integers.

        # element_list = sorted(element_histogram.keys())
        element_list = list('0123456789')

        colors = ['red','blue','green','orange','purple']

        wedge_angle = 2*pi / len(element_list)
        margin = wedge_angle * self.ELEMENT_MARGIN_MULTIPLIER
        starting_angle = pi/2 - wedge_angle/2 + margin
        d_theta = wedge_angle - margin

        #A dictionary of possible startpoints
        startpoint_dict = {}

        color_dict = {'0':'#29D5BD','1':'#AA8239','2':'#E43C4C','3':'#246B61','4':'#ECAE3E',
            '5':'#FB3044','6':'#279485','7':'#FFB531','8':'#A43741','9':'#1A413C'}

        for element in element_list:
            arc = ElementArc(starting_angle, starting_angle + d_theta, color_dict[element], self.ELEMENT_WIDTH)
            self.elements.append(arc)

            middle_of_arc = starting_angle + d_theta/2

            pos_point_x = (self.CIRCLE_CENTER - 10) + (circle_radius + 30)*cos(middle_of_arc)
            pos_point_y = (self.CIRCLE_CENTER - 20) - (circle_radius + 20)*sin(middle_of_arc)

            label = Label("images/{}.png".format(element),(pos_point_x, pos_point_y),color_dict[element])
            self.labels.append(label)

            #Because the number might not have all 10 digits
            if element in element_histogram:
                startpoint_d_theta = d_theta / (element_histogram[element]+1)
                startpoints = [margin - starting_angle - startpoint_d_theta*i for i in range(1,element_histogram[element]+1)]
                startpoint_dict[element] = startpoints

            starting_angle -= wedge_angle

        # Assumes integers
        for first, second in connection_list:
            first_angle = startpoint_dict[first].pop(0)
            first_point_x = self.CIRCLE_CENTER + inner_radius*cos(first_angle)
            first_point_y = self.CIRCLE_CENTER + inner_radius*sin(first_angle)

            second_angle = startpoint_dict[second][0]
            second_point_x = self.CIRCLE_CENTER + inner_radius*cos(second_angle)
            second_point_y = self.CIRCLE_CENTER + inner_radius*sin(second_angle)
            connection = ConnectionArc((first_point_x, first_point_y), (second_point_x, second_point_y),color_dict[first])
            self.connections.append(connection)

class PyGameMouseController(object):
    def __init__(self, model):
        self.model = model

    def handle_event(self, event):
        """ Look for mouse movements and respond appropriately """

def generate_connection_histogram(input_list):
    """Given a list of strings, generate two things:
    A list of each pair of adjacent elements as tuples
    A histogram of the number of occurences of each element, stored in a dictionary.

    >>> pair_list, list = generate_connection_histogram(['the','dog','and','the','dog'])
    >>> print pair_list[0]
    ('the', 'dog')
    >>> print pair_list[1]
    ('dog', 'and')
    """
    output_list = []
    element_histogram = {}

    for i in range(len(input_list)-1):
        first = input_list[i]
        second = input_list[i+1]
        pair = (first, second)
        output_list.append(pair)

    for element in input_list:
        element_histogram[element] = element_histogram.get(element,0)+1

    return output_list, element_histogram

def sanitize_float(flt):
    """Given a floating point number, returns a list of the digits of the
    number as strings

    >>> print sanitize_float(3.1415)
    ['3', '1', '4', '1', '5']
    """

    flt_string = str(flt)
    flt_list = list(flt_string)
    if '.' in flt_list:
        flt_list.remove('.')
    return flt_list

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    pi_value = pi
    medium_pi = "3.1415926535897932384626433832795028841971693993751058209749445923078164"
    long_pi = "3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273724587006606315588174881520920962829254091715364367892590360011330530548820466521384146951941511609433057270365759591953092186117381932611793105118548074462379962749567351885752724891227938183011949129833673362440656643086021394946395224737190"
    one_seventh = "0.142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857142857"
    three_sevenths = "0.428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571428571"
    five_sevenths = "0.714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285714285"
    e_value = "2.71828182845904523536028747135266249775724709369995957496696762772407663035354759457138217852516642742746639193200305992181741359662904357290033429526059563073813232862794349076323382988075319525101901157383418793070215408914993488416750924476146066808226480016847741185374234544243710753907774499206955170276183860626133138458300075204493382656029760673711320070932870912744374704723069697720931014169283681902551510865746377211125238978442505695369677078544996996794686445490598793163688923009879312"
    one_eleventh = "0.09090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909"
    one_43 = "0.023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093023255813953488372093"
    one_67 = "0.014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597014925373134328358208955223880597"
    phi = "1.61803398874989484820458683436563811772030917980576286213544862270526046281890244970720720418939113748475408807538689175212663386222353693179318006076672635443338908659593958290563832266131992829026788067520876689250171169620703222104321626954862629631361443814975870122034080588795445474924618569536486444924104432077134494704956584678850987433944221254487706647809158846074998871240076521705751797883416625624940758906970400028121042762177111777805315317141011704666599146697987317613560067087480710131795236894275219484353056783002287856997829"
    potential_plots = [
        (pi_value,"images/small_pi_button.png"), 
        (medium_pi,"images/medium_pi_button.png"),
        (long_pi,"images/large_pi.png"), 
        (one_seventh,"images/1_7_button.png"),
        (three_sevenths,"images/3_7_button.png"), 
        (five_sevenths,"images/5_7_button.png"),
        (e_value,"images/e_button.png"), 
        (one_eleventh,"images/1_11_button.png"),
        (one_43,"images/1_11_2_button.png"), 
        (one_67,"images/1_11_3_button.png"),
        (phi,"images/phi_button.png"), 
        (0,"images/small_pi_button.png")
    ]

    pygame.init()
    size = (900, 1000)
    screen = pygame.display.set_mode(size)

    buttons = []

    y_center = 1000 - 75
    x_center = 12
    for potential_plot in potential_plots:
        top_left = (x_center, y_center)
        width_height = (50,50)

        num = potential_plot[0]
        im_path = potential_plot[1]

        new_button = ModelButton(pygame.Rect(top_left,width_height),im_path,num)

        buttons.append(new_button)
        x_center += 75

    

    model = CirclePlotModel(0, buttons)
    view = CirclePlotView(model, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == MOUSEBUTTONUP or event.type == MOUSEBUTTONDOWN or event.type == MOUSEMOTION:
                for button in buttons:
                    events = button.handleEvent(event)
                    if 'click' in events:
                        model = CirclePlotModel(button.num,buttons)
                        view = CirclePlotView(model,screen)

        view.draw()
        time.sleep(.001)