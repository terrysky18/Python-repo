# Partial example code for spaceship

import simpleguitk as simplegui

class ImageInfo:
	def __init__(self, centre, size, radius = 0, lifespan = None, animated = False):
		self.centre = centre
		self.size = size
		self.radius = radius
		if lifespan:		# check lifespan is passed
			self.lifespan = lifespan
		else:
			self.lifespan = float('inf')	# infinite lifespan

		self.animated = animated
	
	def get_centre(self):
		return self.centre

	def get_size(self):
		return self.size

	def get_radius(self):
		return self.radius

	def get_lifespan(self):
		return self.lifespan

	def get_animated(self):
		return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# sound assets purchased from sounddogs.com, please do not redistribute
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")

# ship class
class Ship:
	def __init__(self, pos, vel, angle, image, info):
		self.pos = [pos[0], pos[1]]
		self.vel = [vel[0], vel[1]]
		self.thrust = False
		self.angle = angle
		self.angle_vel = 0
		self.image = image
		self.image_centre = info.get_centre()
		self.image_size = info.get_size()
		self.radius = info.get_radius()
	
	def draw(self, canvas):
		canvas.draw_circle(self.pos, self.radius, 1, "white", "white")
	
	def update(self):
		pass

