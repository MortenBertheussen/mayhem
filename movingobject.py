#!/usr/bin/env python3
from gameconstants import *
from Vector2D import *
from spritesheet import *
import math

RESPAWN_TIMER = pygame.USEREVENT + 2

class Movingobject(pygame.sprite.Sprite):
	"""
	Superclass for all moving objects.
	"""
	def __init__(self):
		super().__init__()
		self.pos = Vector2D(0, 0)
		self.speed = Vector2D(0,-1)		#Initial direction pointing upwards
		self.angle = 0
		self.maxspeed = 5				#Default maxspeed if not redefined by child

	def screen_wrap(self):
		"""
		Makes the object wrap if it goes outside the screen border.
		"""
		if self.pos.x <= 0: 		self.pos.x = SCREEN_X - 1	#Left
		if self.pos.x >= SCREEN_X:	self.pos.x = 1				#Right
		if self.pos.y >= SCREEN_Y:	self.pos.y = 1				#Bottom
		if self.pos.y <= 0:			self.pos.y = SCREEN_Y - 1 	#Top

	def rotate_point(self, point, center, angle):
		"""
		Rotate a point with a set angle around a center point.
 		Usage: rotate_point( (Vector2D)oldpoint, (Vector2D)centerpoint, (int)angle)
 		Returns a vector for the new point.
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
		Usage: image = new_sprite( (x,y,w,h) )
		"""
		oldrect = self.rect
		self.image = self.spritesheet.get_image(rect)
		self.image = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.image.get_rect(center=oldrect.center)			#Realign the image to be at the center where the old image was

	def resize_sprite(self, w, h):
		self.image = pygame.transform.scale(self.image, (w, h))

	def rotate_left(self):
		"""
		Rotate the speed vector left 4 degrees
		"""
		rad = math.radians(-4)
		x = self.speed.x * math.cos(rad) - self.speed.y * math.sin(rad)
		y = self.speed.x * math.sin(rad) + self.speed.y * math.cos(rad)
		self.speed = Vector2D(x, y)
		self.calc_angle()

	def rotate_right(self):
		"""
		Rotate the speed vector right 4 degrees
		"""
		rad = math.radians(4)
		x = self.speed.x * math.cos(rad) - self.speed.y * math.sin(rad)
		y = self.speed.x * math.sin(rad) + self.speed.y * math.cos(rad)
		self.speed = Vector2D(x, y)
		self.calc_angle()

	def calc_angle(self):
		"""
		Calculates the angle for the speed vector if it has been modified slightly by gravity.
		If this is not done the image angle and the speed vector angle will be slightly off.
		"""
		baseline = Vector2D(0,-1) #Vector pointing upwards
		dot = (self.speed.x * baseline.x) + (self.speed.y * baseline.y)
		det = (self.speed.x * baseline.y) - (self.speed.y * baseline.x)
		angle = math.atan2(det, dot)
		self.angle = math.degrees(angle)

	def speed_limit(self):
		"""
		Universal speed limit for moving objects.
		"""
		if self.speed.magnitude() > self.maxspeed:
			self.speed = self.speed.normalized() * self.maxspeed