#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from Movingobjects import *
import math
import random

class Astroid(Movingobject):
	def __init__(self, pos, rect):
		super().__init__()
		self.pos = Vector2D(pos[0], pos[1])
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.angle = 0
		self.gravity = 10
		self.speed = Vector2D(random.uniform(0,5), random.uniform(0,5))
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		self.maxspeed = 3
	def update(self):
		self.angle += 0.5
		self.new_sprite(self.image_pos)
		self.move()
		self.speed_limit()
		self.screen_wrap()

	def move(self):
		self.pos += self.speed
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

	def new_sprite(self, rect):
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)

	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.speed.magnitude() > self.maxspeed:
			self.speed = self.speed.normalized() * self.maxspeed