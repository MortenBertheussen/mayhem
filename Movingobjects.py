#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
import math

class Movingobject(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.gravity = Vector2D(0,2)
		self.maxspeed = 5
		self.pos = Vector2D(SCREEN_X/2 - 22, SCREEN_Y/2 - 22)
		self.direction = Vector2D(0,-1)

	def rotate(self):
		"""The math behind finding the new direction with an angle"""
		x = self.direction.x * math.cos(math.radians(-self.angle)) - self.direction.y * math.sin(math.radians(-self.angle))
		y = self.direction.x * math.sin(math.radians(-self.angle)) + self.direction.y * math.cos(math.radians(-self.angle))
		new_speed = Vector2D(x, y)

		return new_speed

class Rocket(Movingobject): 
	"""The class for rocket, broombroom"""
	def __init__(self, uid):
		super().__init__()
		self.uid = uid
		self.image = pygame.image.load("sprites/ship.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.engineOn = False
		self.turnLeft = False
		self.turnRight = False
		self.refuel = False
		self.fuel = 1000
		self.maxfuel = 1000
		self.score = 0
		self.angle = 0
		self.shots = []
		if self.uid == 1:
			self.spawn = Vector2D(300,350)
			self.pos = self.spawn
		elif self.uid == 2:
			self.spawn = Vector2D(1075, 210)
			self.pos = self.spawn


	def logic(self, screen):
		"""Logic method of rocket"""
		self.speed_limit()
		self.move()
		self.screen_wrap()
		self.fule()
		#pygame.draw.rect(screen,RED,(self.pos.x,self.pos.y,45,45))

	def move(self):
		"""move method of rocket"""
		if self.turnLeft:
			self.angle += 4
		if self.turnRight:
			self.angle -= 4
		
		new_speed = self.rotate()

		if self.engineOn and self.fuel>0:
			self.image = pygame.image.load("sprites/ship_engine_on.png").convert_alpha()
			self.image = pygame.transform.scale(self.image,(30,30))
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.rect = self.image.get_rect()
			self.direction *= 1.5
			if self.refuel is False:
				self.pos += new_speed + self.gravity
			self.rect.center = (self.pos.x + 22, self.pos.y + 22)
			self.refuel = False
			self.fuel -=1
			self.gravity.y = 2
			
			#set fuel not to go under 0
			if self.fuel <= 0:
				self.fuel = 0
		else:
			self.image = pygame.image.load("sprites/ship.png").convert_alpha()
			self.image = pygame.transform.scale(self.image,(30,30))
			self.image = pygame.transform.rotate(self.image, self.angle)
			self.rect = self.image.get_rect()
			if self.direction.magnitude() > 0.5 and self.refuel is False:
				self.direction /= 1.04
				self.pos += new_speed + self.gravity
			else:
				self.pos += self.gravity
			self.rect.center = (self.pos.x + 22, self.pos.y + 22)


	def speed_limit(self):
		"""Speed_limit method of rocket"""
		if self.direction.magnitude() > self.maxspeed:
			self.direction = self.direction.normalized() * self.maxspeed

	def shoot(self):
		"""Shoot method of rocket"""
		return Bullet(self.rect, self.rotate(), self.uid)
		#self.shots.append(Bullet(self.pos, self.rotate()))

	def screen_wrap(self):
		"""Screen_wrap method of rocket"""
		##Venstre Vegg
		if self.pos.x <= 0:
			self.pos.x = SCREEN_X - 1
		##Høyre Vegg
		if self.pos.x >= SCREEN_X:
			self.pos.x = 1
		##Nedre Vegg
		if self.pos.y >= SCREEN_Y:
			self.pos.y = 1
		##Øvre Vegg
		if self.pos.y <= 0:
			self.pos.y = SCREEN_Y

			
	def fule(self):
		if self.fuel > self.maxfuel:
			self.fuel = self.maxfuel
		if self.refuel and self.fuel < self.maxfuel:
			self.fuel += 1

class Bullet(Movingobject):
	"""The bullet class"""
	def __init__(self, rect, direc, uid):
		super().__init__()
		self.uid = uid
		self.dir = direc
		self.image = pygame.image.load("sprites/bullet.png").convert_alpha()
		self.rect = self.image.get_rect()
		self.pos.x = rect.center[0] - self.rect.width/2
		self.pos.y = rect.center[1]

	def move(self):
		self.pos += self.dir.normalized() * 15
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

	def logic(self):
		self.move()
		#pygame.draw.circle(screen, RED, (int(self.pos.x),int(self.pos.y)), self.radius)