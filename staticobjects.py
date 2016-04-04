#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Environment(pygame.sprite.Sprite):
	"""The environment/background"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/bg.png").convert_alpha()
		self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
	"""platform station"""
	def __init__(self, uid):
		super().__init__()
		self.uid = uid
		self.image = pygame.image.load("sprites/platform.png").convert_alpha()
		self.rect = self.image.get_rect()
		if self.uid is 1:
			self.rect.x = 285
			self.rect.y = 400
		elif self.uid is 2:
			self.rect.x = 1060
			self.rect.y = 257