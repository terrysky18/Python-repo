# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
PI = math.pi
WIDTH = 800
HEIGHT = 600
TEXT_SIZE = 18
score = 0
lives = 3
time = 0.5

# constants for ship behaviours
SHIP_TURN_RATE = PI/24
SHIP_ACCELERATION = 0.7		# linear acceleration
SHIP_DRAG = 0.012			# frictional drag in space?
SHIP_MISSILE_SPEED = 5		# missile speed relative to the ship, the ship is centre of the frame of reference

class ImageInfo:
	def __init__(self, centre, size, radius = 0, lifespan = None, animated = False):
		self.centre = centre
		self.size = size
		self.radius = radius
		if lifespan:
			self.lifespan = lifespan
		else:
			self.lifespan = float('inf')
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

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#				debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([10, 10], [20, 20], 4, 50)	# using shot3
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot3.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.ogg")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.ogg")
missile_sound.set_volume(0.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.ogg")
ship_thrust_sound.set_volume(0.7)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.ogg")

# helper functions to handle transformations
def angle_to_vector(ang):
	return [math.cos(ang), math.sin(ang)]

def dist(p, q):
	return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
	def __init__(self, pos, vel, angle, image, info):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.thrust = False
		self.angle = angle
		self.angle_vel = 0
		self.image = image
		self.image_centre = info.get_centre()
		self.image_size = info.get_size()
		self.radius = info.get_radius()

	def draw(self, canvas):
		if not self.thrust:
			# thrusters off
			ship_thrust_sound.pause()
			ship_thrust_sound.rewind()
			canvas.draw_image(self.image, self.image_centre, self.image_size, self.pos, self.image_size, self.angle)
		
		else:
			# ignite the thrusters for propulsion
			ship_thrust_sound.play()
			new_image_centre = [self.image_centre[0] + self.image_size[0], self.image_centre[1]]
			canvas.draw_image(self.image, new_image_centre, self.image_size, self.pos, self.image_size, self.angle)
		
	def manoeuvre(self, anti_clockwise, clockwise):
	# modify the angular velocity of the ship
	# one parameter contains a value, the other parameter must contain 0
		self.angle_vel = anti_clockwise + clockwise

	def ignition(self, propulsion):
	# modify the boolean thrust variable of the ship
	# propulsion is a boolean variable
		self.thrust = propulsion
	
	def shoot(self):
		global a_missile
		cannon_direction = angle_to_vector(self.angle)	# unit vector of the ship's current heading
		
		missile_pos = [0, 0]
		missile_pos[0] = self.pos[0] + self.radius * cannon_direction[0]
		missile_pos[1] = self.pos[1] + self.radius * cannon_direction[1]
		
		missile_vel = [0, 0]
		missile_vel[0] = (abs(self.vel[0]) + SHIP_MISSILE_SPEED) * cannon_direction[0]
		missile_vel[1] = (abs(self.vel[1]) + SHIP_MISSILE_SPEED) * cannon_direction[1]
		
		a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound)
	
	def update(self):
		self.angle += self.angle_vel
		
		# frictional drag on the ship
		self.vel[0] *= (1 - SHIP_DRAG)
		self.vel[1] *= (1 - SHIP_DRAG)
		
		if self.thrust:
			accel_vec = angle_to_vector(self.angle)		# acceleration vector
			self.vel[0] += SHIP_ACCELERATION * accel_vec[0]
			self.vel[1] += SHIP_ACCELERATION * accel_vec[1]
		
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		
		# check if the ship is within bound
		if (self.pos[0] < 0) or (self.pos[0] > WIDTH):
			self.pos[0] = self.pos[0] % WIDTH
		
		elif (self.pos[1] < 0) or (self.pos[1] > HEIGHT):
			self.pos[1] = self.pos[1] % HEIGHT


# Sprite class
class Sprite:
	def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
		self.pos = [pos[0],pos[1]]
		self.vel = [vel[0],vel[1]]
		self.angle = ang
		self.angle_vel = ang_vel
		self.image = image
		self.image_centre = info.get_centre()
		self.image_size = info.get_size()
		self.radius = info.get_radius()
		self.lifespan = info.get_lifespan()
		self.animated = info.get_animated()
		self.age = 0
		if sound:
			sound.rewind()
			sound.play()

	def draw(self, canvas):
		canvas.draw_image(self.image, self.image_centre, self.image_size, self.pos, self.image_size, self.angle)

	def update(self):
		self.angle += self.angle_vel
		
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]
		
		# check if the rock is within bound
		if (self.pos[0] < 0) or (self.pos[0] > WIDTH):
			self.pos[0] = self.pos[0] % WIDTH
		
		elif (self.pos[1] < 0) or (self.pos[1] > HEIGHT):
			self.pos[1] = self.pos[1] % HEIGHT


def draw(canvas):
	global time, score, lives

	# animiate background
	time += 1
	wtime = (time / 4) % WIDTH
	centre = debris_info.get_centre()
	size = debris_info.get_size()
	canvas.draw_image(nebula_image, nebula_info.get_centre(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
	canvas.draw_image(debris_image, centre, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
	canvas.draw_image(debris_image, centre, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
	canvas.draw_text('Lives', [20, 38], TEXT_SIZE, 'white')
	canvas.draw_text(str(lives), [32, 60] , TEXT_SIZE - 2, 'white')
	canvas.draw_text('Score', [WIDTH - 80, 38], TEXT_SIZE, 'white')
	canvas.draw_text(str(score), [WIDTH - 55, 60], TEXT_SIZE - 2, 'white')

	# draw ship and sprites
	my_ship.draw(canvas)
	a_rock.draw(canvas)
	a_missile.draw(canvas)

	# update ship and sprites
	my_ship.update()
	a_rock.update()
	a_missile.update()

# timer handler that spawns a rock    
def rock_spawner():
	global a_rock
	
	posX = random.randrange(10, WIDTH - 10)		# horizontal position
	posY = random.randrange(10, HEIGHT - 10)	# vertical position
	
	velX = random.randrange(-2, 3)				# horizontal velocity
	velY = random.randrange(-2, 3)				# vertical velocity
	
	# make sure velocity of the sprite is non-zero
	while (velX == 0) or (velY == 0):
		velX = random.randrange(-2, 3)
		velY = random.randrange(-2, 3)
	
	angle = random.randrange(-6, 7)				# initial angle
	direction = random.choice([1, 2, 3, 4, 5, 6])	# even number in clockwise direction
	if direction % 2 == 0:
		angular_vel = random.random() / PI
	else:
		angular_vel = -1 * (random.random() / PI)
	
	# reintroduce a new sprite
	a_rock = Sprite([posX, posY], [velX, velY], angle, angular_vel, asteroid_image, asteroid_info)


# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([WIDTH / 2, HEIGHT / 2], [SHIP_MISSILE_SPEED, 0], 0, 0, missile_image, missile_info)	

# actions the keys are mapped to
inputs = {'left':[-1*SHIP_TURN_RATE, 0], 'right':[0, SHIP_TURN_RATE]}

# key handlers
def keydown(key):
# separate actions for forward thrust and manoeuvre
# so the ship can propel forward and steer simultaneously
	if key == simplegui.KEY_MAP['up']:
		my_ship.ignition(True)
	elif key == simplegui.KEY_MAP['space']:
		my_ship.shoot()
	else:
		for i in inputs:		# cycle through key map
			if key == simplegui.KEY_MAP[i]:
				my_ship.manoeuvre(inputs[i][0], inputs[i][1])


def keyup(key):
	if key == simplegui.KEY_MAP['up']:
		my_ship.ignition(False)
	else:
		my_ship.manoeuvre(0, 0)


# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1500.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
