#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import math
import random

class Astroid(Movingobject):
	"""This is the astroid class"""
	def __init__(self, pos, rect):
		super().__init__()
		self.pos = Vector2D(pos[0], pos[1])
		self.spritesheet = Spritesheet("sprites/spritesheet.png")
		self.image = self.spritesheet.get_image((rect))
		self.image_pos = rect
		self.rect = self.image.get_rect()
		self.angle = 0
		self.gravity = 10
		self.life = 3
		self.speed = Vector2D(random.uniform(0,5), random.uniform(0,5))
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		self.maxspeed = 5
		if rect is ASTROID_1: self.mass = 25
		if rect is ASTROID_2: self.mass = 20
		if rect is ASTROID_3: self.mass = 5
		
	def update(self):
		"""Runs what is needed for the class"""
		self.angle += 0.5
		self.new_sprite(self.image_pos)
		self.move()
		self.speed_limit()
		self.screen_wrap()

	def move(self):
		"""Controls the movement of the astroid"""
		self.pos += self.speed
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y

	def new_sprite(self, rect):
		"""Fetches a new sprite from the spritesheet and keep its rotation"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)

	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.speed.magnitude() > self.maxspeed:
			self.speed = self.speed.normalized() * self.maxspeed