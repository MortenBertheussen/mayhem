import pygame
 
class Spritesheet:
	"""
	Creates a spritesheet object.

	Spritesheet(path) -> object

	Parameters
	----------
	path : string
		Path to spriteshee
	"""
	def __init__(self, path):
		self.sheet = pygame.image.load(path).convert_alpha()

	def get_image(self, spriterect):
		"""
		Get image from the spritesheet.

		get_image(rectangle) -> image (pygame.Surface object)

		Parameters
		----------
		spriterect : (x,y,w,h)
			Position on spritesheet.
		"""
		rect = pygame.Rect(spriterect)
		image = pygame.Surface(rect.size, pygame.SRCALPHA)
		image.fill((0,0,0,0))
		image.blit(self.sheet, (0, 0), spriterect)
		
		return image


