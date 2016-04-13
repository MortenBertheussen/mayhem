#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
from movingobject import *
import random

class PowerUp(Movingobject):
	def __init__(self,powertype,pos,rect,spritesheet):
		super().__init__()
		self.type = powertype
		self.pos =  Vector2D(pos[0],pos[1])
		self.spritesheet = spritesheet
		self.image = self.spritesheet.get_image((rect))
		self.resize_sprite(20,20)
		self.rect = self.image.get_rect()
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y
		
	def update(self):
		self.rect.centerx = self.pos.x
		self.rect.centery = self.pos.y