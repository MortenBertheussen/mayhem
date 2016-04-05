#!/usr/bin/env python3
from gameconstants import *
from spritesheet import *
from Vector2D import *
import math

class Background(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/bg.png").convert_alpha()
		self.rect = self.image.get_rect()

class Hud(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/hud.png").convert_alpha()
		self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
	"""platform station"""
	def __init__(self, uid):
		super().__init__()
		self.uid = uid
		if uid is 1:
			self.spriterect = BLUE_PLATFORM
		else:
			self.spriterect = RED_PLATFORM
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((self.spriterect))
		self.rect = self.image.get_rect()
		if self.uid is 1:
			self.rect.centerx = 150
			self.rect.centery = SCREEN_Y - 150
		elif self.uid is 2:
			self.rect.centerx = SCREEN_X - 150
			self.rect.centery = 150

class Explotion(pygame.sprite.Sprite):
	def __init__(self, x, y, size):
		super().__init__()
		self.size = size
		self.images = []
		self.images.append(self.handle_img("sprites/explotions/exp1.png"))
		self.images.append(self.handle_img("sprites/explotions/exp2.png"))
		self.images.append(self.handle_img("sprites/explotions/exp3.png"))
		self.images.append(self.handle_img("sprites/explotions/exp4.png"))
		self.images.append(self.handle_img("sprites/explotions/exp5.png"))
		self.images.append(self.handle_img("sprites/explotions/exp6.png"))
		self.images.append(self.handle_img("sprites/explotions/exp7.png"))
		self.images.append(self.handle_img("sprites/explotions/exp8.png"))
		self.images.append(self.handle_img("sprites/explotions/exp9.png"))
		self.images.append(self.handle_img("sprites/explotions/exp10.png"))
		self.images.append(self.handle_img("sprites/explotions/exp11.png"))
		self.images.append(self.handle_img("sprites/explotions/exp12.png"))
		
		self.index = 0
		
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = y
		self.kill = False
		self.timer = 0

	def handle_img(self, path):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image,(self.size,self.size))
		return image

	def update(self):
		self.index += 1
		self.timer += 1
		if self.timer % 1 == 0:
			if self.index is len(self.images):
				self.index = 11
				self.kill = True
			self.image = self.images[self.index]
