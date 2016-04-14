#!/usr/bin/env python
""" Pre-code for INF-1400

22 January 2012 Revision 2 (Martin Ernstsen):
Reraise exception after showing error message.

11 February 2011 Revision 1 (Martin Ernstsen):
Fixed bug in intersect_circle. Updated docstrings to Python standard.
Improved __mul__. Added some exception handling. Put example code in separate
function.

"""

import pygame
import math


class Vector2D(object):
    """ Implements a two dimensional vector. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return 'Vector(X: {x}, Y: {y})'.format(x = self.x, y = self.y)

    def __nonzero__(self):
        """ Makes Vector2D(0,0) evaluate to False, all other vectors evaluate to True """
        return not (self.x, self.y) == (0,0)
            
    def __add__(self, b):
        """ Addition. Returns a new vector. """
        return Vector2D(self.x + b.x, self.y + b.y)

    def __sub__(self, b):
        """ Subtraction. Returns a new vector. """
        return Vector2D(self.x - b.x, self.y - b.y)

    def __mul__(self, b):
        """ Multiplication by a scalar """
        try:
            #Check if mulitplying with a vector
            if isinstance(b, Vector2D):
                return Vector2D(self.x * b.x, self.y * b.y)
            else:
                b = float(b)
                return Vector2D(self.x * b, self.y * b)
        except ValueError:
            print("Oops! Right value must be a float")
            raise

    def __rmul__(self, b):
        try:
            b = float(b)
            return Vector2D(self.x * b, self.y * b)
        except ValueError:
            print("Scalar must be a float!")
            raise

    def __truediv__(self, b):
        return Vector2D(self.x/b, self.y/b)

    def magnitude(self):
        """ Returns the magnitude of the vector. """
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def normalized(self):
        """ Returns a new vector with the same direction but magnitude 1. """
        try:
            m = self.magnitude()
            return Vector2D(self.x / m, self.y / m)
        except ZeroDivisionError:
            print("Oops! Cannot normalize a zero-vector")
            raise

    def copy(self):
        """ Returns a copy of the vector. """
        return Vector2D(self.x, self.y)
