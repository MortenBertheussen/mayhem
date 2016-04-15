#!/usr/bin/env python3
from gameconstants import *
from config import *
from spritesheet import *
from Vector2D import *
import math

class Background(pygame.sprite.Sprite):
	"""
	Creates a background object.

	Background() -> object
	"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/bg.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (1400, 1000))
		self.rect = self.image.get_rect()
		self.paralax = 0
		self.moveleft = True

	def update(self):
		"""
		Updates the position of the background, slight paralaxing effect.

		update() -> none
		"""
		if self.moveleft:
			self.paralax -= 0.1
		else:
			self.paralax += 0.1
		if self.paralax < -50:
			self.moveleft = False
		if self.paralax > 0:
			self.moveleft = True
		self.rect.x = self.paralax
		self.rect.y = self.paralax

class Hud(pygame.sprite.Sprite):
	"""
	Creates a hud object.

	Hud() -> object
	"""
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("sprites/hud.png").convert_alpha()
		self.rect = self.image.get_rect()

class Platform(pygame.sprite.Sprite):
	"""
	Creates a platform object.

	Platform() -> object

	Parameters:
	-----------
	uid: int
		Player identifier.
	spritesheet: object
		Pointer to spritesheet object.
	"""
	def __init__(self, uid, spritesheet):
		super().__init__()
		self.uid = uid
		if uid is 1:	self.spriterect = BLUE_PLATFORM
		else:			self.spriterect = RED_PLATFORM
		self.spritesheet = spritesheet
		self.image = self.spritesheet.get_image((self.spriterect))
		self.rect = self.image.get_rect()
		if self.uid is 1:	self.rect.center = PLAYER1_SPAWN
		elif self.uid is 2: self.rect.center = PLAYER2_SPAWN

class Explotion(pygame.sprite.Sprite):
	"""
	Creates a explotion object.

	Explotion() -> object

	Parameters:
	-----------
	x: int
		x position.
	y: int
		y position.
	size: int
		Size of explotion.
	"""
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
		"""
		Loads image and scales it.

		handle_img(path) -> image (pygame.image object)

		Parameters:
		-----------
		path: string
			Path to image.
		"""
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image,(self.size,self.size))
		return image


	def update(self):
		"""
		Update method for sprite group.

		update() -> none
		"""
		self.index += 1
		self.timer += 1
		if self.timer % 1 == 0:
			if self.index is len(self.images):
				self.index = 11
				self.kill = True
			self.image = self.images[self.index]
