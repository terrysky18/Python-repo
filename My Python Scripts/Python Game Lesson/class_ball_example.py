"""
ball physics code for generic 2D domain
the functions inside() and normal() encode the shape of the environment
"""

import simpleguitk as simplegui
import random
import math

# canvas size
WIDTH = 600
HEIGHT = 400

# ball traits
ball_radius = 20
ball_colour = "white"

# match helper function
def dot(vec1, vec2):
# dot product of two 2D vectors, both vectors have 2 components
	return vec1[0] * vec2[0] + vec1[1] * vec2[1]
# end of dot()

class RectangularDomain:
# class of a rectangular domain
	def __init__(self, width, height):	# initialiser
		self.width = width
		self.height = height
		self.border = 2
	# end of __init__()
	
	def inside(self, centre, radius):
	# return boolean value if bounding circle is inside the domain
		in_width = ((radius + self.border) < centre[0] <
				(self.width - self.border - radius))
		in_height = ((radius + self.border) < centre[1] <
				(self.height - self.border - radius))
		# determine both horizontal and vertical components are within
		return in_width and in_height
	# end of inside()
	
	def normal(self, centre):
	# return a unit vector normal to the domain boundary nearest centre
		left_dist = centre[0]			# distance from left
		right_dist = self.width - centre[0]	# distance from right

		top_dist = centre[1]			# distance from top
		bottom_dist = self.height - centre[1]	# distance from bottom

		if left_dist < min(right_dist, top_dist, bottom_dist):
			return (1, 0)		# point to right
		elif right_dist < min(left_dist, top_dist, bottom_dist):
			return (-1, 0)		# point to left
		elif top_dist < min(bottom_dist, left_dist, right_dist):
			return (0, 1)		# point to bottom
		else:
			return (0, -1)		# point to top
	# end of normal()

	def random_pos(self, radius):
	# return a random location within border
		x = random.randrange(radius, self.width - radius - self.border)
		y = random.randrange(radius, self.height - radius - self.border)
		return [x, y]

	def draw(self, canvas):
	# draw boundary of domain
		polygonPoints = ([5, 5], [self.width, 5],
				[self.width, self.height], [5, self.height])
		canvas.draw_polygon(polygonPoints, self.border*2, "red")
	# end of draw()

class CircularDomain:
# class of a  circular domain
	def __init__(self, centre, radius):
		self.centre = centre
		self.radius = radius
		self.border = 2
	# end of __init__()

	def inside(self, centre, radius):
	# return boolean value if bounding circle is inside the domain
		dx = centre[0] - self.centre[0]
		dy = centre[1] - self.centre[1]
		# distance between bounding circle centre and domain centre
		dr = math.sqrt(dx**2 + dy**2)
		return dr < (self.radius - radius - self.border)
	# end of inside()

	def normal(self, centre):
	# return a unit vector normal to the domain boundary nearest centre
		dx = centre[0] - self.centre[0]
		dy = centre[1] - self.centre[1]
		dr = math.sqrt(dx**2 + dy**2)
		# the radius of a circle is always normal the boundary
		return [dx / dr, dy / dr]
	# end of normal()

	def random_pos(self, radius):
	# return a random location
		r = random.random() * (self.radius - radius - self.border)
		theta = random.random() * 2 * math.pi
		x = r * math.cos(theta) + self.centre[0]
		y = r * math.sin(theta) + self.centre[1]
		return [x, y]
	# end of random_pos()

	def draw(self, canvas):
	# draw domain boundary
		canvas.draw_circle(self.centre, self.radius, self.border*2, "red")
	# end of draw()

class Ball:
# class of a bouncing ball
	def __init__(self, radius, colour, domain):
		self.radius = radius
		self.colour = colour
		self.domain = domain

		self.pos = self.domain.random_pos(self.radius)
		self.vel = [random.random() + 0.1, random.random() + 0.1]
	# end of __init__()

	def reflect(self):
	# bounce function
		norm = self.domain.normal(self.pos)	# normal unit vector
		norm_length = dot(self.vel, norm)	# vector magnitude
		self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
		self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]
	# end of reflect()

	def update(self):
	# update the ball position
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]

		# when the ball hits a boundary
		if not self.domain.inside(self.pos, self.radius):
			self.reflect()		# bounce off
	# end of update()

	def draw(self, canvas):
	# draw the bouncing ball
		canvas.draw_circle(self.pos, self.radius, 1,
				self.colour, self.colour)
	# end of draw()

# generic update code for ball physics
def draw(canvas):
	ball.update()
	field.draw(canvas)
	ball.draw(canvas)

field = RectangularDomain(WIDTH, HEIGHT)
# field = CircularDomain([WIDTH / 2, HEIGHT / 2], 180)
ball = Ball(ball_radius, ball_colour, field)

frame = simplegui.create_frame("Ball physics", WIDTH + 10, HEIGHT + 10)
frame.set_draw_handler(draw)

frame.start()

