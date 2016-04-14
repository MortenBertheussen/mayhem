#!/usr/bin/env python3
from gameconstants import *
from config import *
from spritesheet import *
from Vector2D import *
import math

class StaticObject(pygame.sprite.Sprite):
	def __init__(self, spawn, spriterect, spritesheet):
		super().__init__()
		self.pos = Vector2D(spawn[0], spawn[1])
		self.spritesheet = spritesheet
		self.original_image = self.spritesheet.get_image((spriterect))
		self.image = self.original_image
		self.rect = self.image.get_rect()
		self.angle = 0

	def resize_image(self, w, h):
		self.image = pygame.transform.scale(self.original_image, (w, h))
		self.rect = self.image.get_rect()

	def rotate_image(self):
		oldrect = self.rect
		self.image = self.original_image
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)
