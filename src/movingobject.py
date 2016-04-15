#!/usr/bin/env python3
from gameconstants import *
from config import *
from Vector2D import *
from spritesheet import *
import math

RESPAWN_TIMER = pygame.USEREVENT + 2

class Movingobject(pygame.sprite.Sprite):
	"""
	Superclass for all objects that move on the screen.
	NB! Do not create objects out of this class, only inherit.
	"""
	def __init__(self, uid, spritesheet, spawn, speed = Vector2D(0,-1)):
		super().__init__()
		self.uid = uid
		self.spritesheet = spritesheet
		self.spawn = spawn
		self.pos = Vector2D(spawn[0], spawn[1])
		self.speed = speed										#Initial direction pointing upwards 0 deg
		self.angle = 0											#Default angle
		self.maxspeed = 5										#Default maxspeed if not redefined by child

	def screen_wrap(self):
		"""
		Makes the object wrap if it goes outsidsae the screen border.

		screen_wrap() -> none
		"""
		if self.pos.x <= 0: 		self.pos.x = SCREEN_X - 1	#Left
		if self.pos.x >= SCREEN_X:	self.pos.x = 1				#Right
		if self.pos.y >= SCREEN_Y:	self.pos.y = 1				#Bottom
		if self.pos.y <= 0:			self.pos.y = SCREEN_Y - 1 	#Top

	def rotate_point(self, point, center, angle):
		"""
		Rotate a point with a set angle around a center point.

		rotate_point(point, center, angle) -> Vector2D object

		Parameters
		----------
		point : Vector2D
		center : Vector2D
			Center point to rotate the point around.
		angle : int
			Ammount to rotate.
		"""
		ang = math.radians(-angle)
		x1 = point.x - center.x
		y1 = point.y - center.y
		x2 = x1 * math.cos(ang) - y1 * math.sin(ang)
		y2 = x1 * math.sin(ang) + y1 * math.cos(ang)
		pointx = x2 + center.x
		pointy = y2 + center.y

		return Vector2D(pointx,pointy)

	def new_sprite(self, rect):
		"""
		Fetches a new sprite from the spritesheet and rotates it to the angle stored by the object.
		
		new_sprite(rect) -> none

		Parameters
		----------
		rect : (x,y,w,h)
			Position on spritesheet to get image.
		"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)			#Realign the image to be at the center where the old image was

	def resize_sprite(self, w, h):
		"""
		Resize its image.

		resize_sprite(w,h) -> none
		"""
		self.image = pygame.transform.scale(self.image, (w, h))

	def calc_angle(self):
		"""
		Calculates the angle for the speed vector if it has been modified slightly by gravity.

		calc_angle() -> none
		"""
		baseline = Vector2D(0,-1) #Vector pointing upwards
		dot = (self.speed.x * baseline.x) + (self.speed.y * baseline.y)
		det = (self.speed.x * baseline.y) - (self.speed.y * baseline.x)
		angle = math.atan2(det, dot)
		self.angle = math.degrees(angle)

	def speed_limit(self):
		"""
		Universal speed limit for moving objects.

		speed_limit() -> none
		"""
		if self.speed.magnitude() > self.maxspeed:
			self.speed = self.speed.normalized() * self.maxspeed