"""
A simple GUI to generate circle plots based on mathematical constants

Authors: Coleman Ellis and Kaitlyn Keil

SoftDes Spring 2016
"""

from math import pi

def generate_connection_histogram(input_list):
    """Given a list of strings, generate a histogram of each adjacent
    pair of strings in the list, stored as a dictionary.

    >>> dict = generate_connection_histogram(['the','dog','and','the','dog'])
    >>> print dict[('the', 'dog')]
    2
    >>> print dict[('dog', 'and')]
    1
    """
    output_dict = {}

    for i in range(len(input_list)-1):
        first = input_list[i]
        second = input_list[i+1]
        pair = (first, second)

        output_dict[pair] = output_dict.get(pair, 0) + 1

    return output_dict

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
    print generate_connection_histogram(sanitize_float(pi))