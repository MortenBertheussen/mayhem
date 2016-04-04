#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Environment(pygame.sprite.Sprite):
	"""The environment/background"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/bg_and_hud.png").convert_alpha()
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
			self.rect.y = 314
		elif self.uid is 2:
			self.rect.x = 1060
			self.rect.y = 200

class Explotion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.images = []
		self.images.append(self.handle_img("sprites/explotion1.png"))
		self.images.append(self.handle_img("sprites/explotion2.png"))
		self.images.append(self.handle_img("sprites/explotion3.png"))
		
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.timer = 0

	def handle_img(self, path):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image,(50,50))
		return image

	def update(self):
		self.timer += 1
		self.index += 1
		if self.index >= len(self.images):
			self.index = 0
		self.image = self.images[self.index]

#class Hud(pygame.sprite.Sprite):
#	def __init__(self):
#		super().__init__()
#		self.image = pygame.image.load("sprites/hud.png").convert_alpha()
#		self.rect = self.image.get_rect()