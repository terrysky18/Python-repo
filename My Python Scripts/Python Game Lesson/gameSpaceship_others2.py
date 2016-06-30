#******************************************************
# Name:         Darren Freeman
# Course:       An Introduction to Interactive Programming in Python
# Date:         November 15th, 2014
# Mini-Project: 8
# 
# Purpose: The purpose of this game is to recreate the classic game asteroids.
# In this game the user can fire the ship, rotate and move around using the up, left and right arrow buttons
# Firing the ship can be done using the space bar.  To start a new game once it has ended click the mouse inside
# the splash screen.  You can also select the game level which you start.  For every 12 asteroids the player 
# destroys the game will increase in difficulty by one level.
# Enjoy!

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800		# Canvas width
HEIGHT = 600	# Canvas height
score = 0		# holds the current game score
lives = 3		# number of lives for the current game
time = 0.5		# used for the canvas background animation

rock_spawn_limit = 12			# initial maximum limit of spawned rocks
rock_group = set([])			# hold the objects for the rock sprites
missle_group = set([])			# hold the objects for the missle sprites
explosion_group = set([])		# hold the objects for the rock explosion sprites
ship_explosion_group = set([])	# hold the object for the ship explosion sprite
started = False					# has game been started
total_rock_count = 0			# counts the total number of rocks destroyed
game_level = 0					# maintains the internal game level
player_level_mod = 0			# maintains the play modified game level


# image class that contains the image specific information
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False, grid = False):
        self.center = center				# x,y center position of image
        self.size = size					# x,y deminsions of image
        self.radius = radius				# radius of image cicle for impacts
        if lifespan:						
            self.lifespan = lifespan		# sets lifespan if it is define in object call
        else:
            self.lifespan = float('inf')	# if not define in object call set to infinity
        self.animated = animated			# is object animated
        self.is_grid = grid					# is object graphic an grid tile versus a single row tile

    def get_center(self):					# returns the image center
        return self.center

    def get_size(self):						# returns the image size
        return self.size

    def get_radius(self):					# returns the image radius
        return self.radius

    def get_lifespan(self):					# returns the image lifespan
        return self.lifespan

    def get_animated(self):					# returns the animation status
        return self.animated
    
    def get_is_grid(self):					# returns the grid status
        return self.is_grid

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
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
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# animated explosion to overlay on ship when ship hits an asteroid
# credit for this graphic is given to the following website where it was taken
# http://excubitorgame.com/2013/08/dev-blog-entry-5-smoke-and-fire/
ship_explosion_info = ImageInfo([64, 64], [128, 128],30,50,True,True)
ship_explosion_image = simplegui.load_image("https://dl.dropboxusercontent.com/s/ahorhujhsg16u5k/Explosion2.png?dl=1")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]					# returns the vector of an angle provided

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)	# returns the distance between two x,y positions


# Ship class
# The ship class contains all the functionality for the ship to function
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]				# initialize the ship position
        self.vel = [vel[0],vel[1]]				# initialize the ship velocity
        self.thrust = False						# initialize the thrust status to false
        self.angle = angle						# initialize the ship angle
        self.angle_vel = 0						# initialize the ship velocity
        self.image = image						# initialize the ship image
        self.image_center = info.get_center()	# initialize the ship image center position
        self.image_size = info.get_size()		# initialize the ship x,y dimension
        self.radius = info.get_radius()			# initialize the ship image radius
        
    def draw(self,canvas):  
        # draws the appropriate ship tile image if the ship is under thrust or not
        if self.thrust:
            # if currently thrusting draw this image
            canvas.draw_image(ship_image,[self.image_center[0]+90,self.image_center[1]],self.image_size,self.pos,self.image_size,self.angle)        
        else:
            # else draw this image
            canvas.draw_image(ship_image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)

    def update(self):
        # this method updates the positional and velocity information for the ship
        self.angle += self.angle_vel			# modify the ship angle if the velocity is positive of negative

        # Position Update
        self.pos[0] = self.pos[0]%WIDTH			# modifies the ships x position to wrap the screen if it exits the canvas width
        self.pos[1] = self.pos[1]%HEIGHT		# modifies the ships y position to wrap the screen if it exits the canvas height
        self.pos[0] += self.vel[0]*0.9			# calculates the ships new x position with the velocity multiplier
        self.pos[1] += self.vel[1]*0.9          # calculates the ships new y position with the velocity multiplier  
        
        # Friction Update
        self.vel[0] *= (1-.02)					# adds a friction multiplier to the x velocity to slow the ship down
        self.vel[1] *= (1-.02)					# adds a friction multiplier to the y velocity to slow the ship down
        
        # Thrust Vector Update
        forward = angle_to_vector(self.angle)	# calculates the vector for the ship to travel
        
        if self.thrust:
            self.vel[0] += forward[0]			# updates the value of the x velocity
            self.vel[1] += forward[1]			# updates the value of the y velocity
      
    def update_angle_vel(self,vel):
        self.angle_vel += vel					# updates the angle velocity 
        
    def update_thrust(self,thrust):
        self.thrust = thrust					# updates the thrust value when on or off thrust
        
    def shoot(self):
        forward = angle_to_vector(self.angle)	# returns the vector direction which the ship will shoot
        
        x = self.pos[0]+self.radius*forward[0]	# calculates the x position which the missle sprite will fire from
        y = self.pos[1]+self.radius*forward[1]  # calculates the y position which the missle sprite will fire from

        # returns a missle sprite that appears at the front tip of the ship
        return Sprite([x,y], [self.vel[0]+forward[0]*10,self.vel[1]+forward[1]*10], self.angle, self.angle_vel, missile_image, missile_info, missile_sound)

    def get_radius(self):
        return self.radius						# returns the ship radius area
    
    def get_position(self):						# returns the current ship position
        return self.pos
    
    def get_vel(self):							# returns the current ship velocity
        return self.vel
    
    def get_ang(self):							# returns the current ship angle
        return self.angle
    
    def get_ang_vel(self):						# returns the current ship anglar velocity
        return self.angle_vel
    
# Sprite class
# this object maintains the functionality for the graphic images animated and non-animated so they can
# be placed in the correct position and drawn on the canvas
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]					# initializes the sprite position
        self.vel = [vel[0],vel[1]]					# initializes the sprite velocity
        self.angle = ang							# initializes the sprite angle
        self.angle_vel = ang_vel					# initializes the sprite angular velocity
        self.image = image							# set the image object of the spire class
        self.image_center = info.get_center()		# sets the sprite center to that of the image object
        self.image_size = info.get_size()			# sets the sprite size to that of the image object
        self.radius = info.get_radius()				# sets the sprite radius to that of the image object
        self.lifespan = info.get_lifespan()			# sets the sprite lifespan to that of the image object
        self.animated = info.get_animated()			# sets the sprite animation value to that of the image object
        self.is_grid = info.get_is_grid()			# sets the sprite grid value to that of the image object
        self.age = 0								# initializes the sprite age to zero
        if sound:									# if sprite has sound it will rewind the sounds the play it
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):							# wraps the sprite graphic x position if it is outside of the canvas
        if self.pos[0] >= WIDTH:
            self.pos[0] = 0.0001
        if self.pos[0] <= 0:
            self.pos[0] = WIDTH
             
        if self.pos[1] >= HEIGHT:					# wraps the sprite graphic y position if it is outside of the canvas
            self.pos[1] = 0.0001
        if self.pos[1] <= 0:
            self.pos[1] = HEIGHT 
        
        # checks to see if the sprite is animated
        if self.animated:
            if self.is_grid:	# checks to see if the sprite image animation is in grid format 
                image_center_x = self.image_center[0]+((self.age-1)%7*self.image_size[0])	# calculates which x image position to draw
                image_center_y = self.image_center[1]+((self.age-1)//7*self.image_size[1])	# calculates which y image position to draw
                # the below line determines the appropriate image tile to draw and position
                canvas.draw_image(self.image,[image_center_x,image_center_y],self.image_size,self.pos,self.image_size,self.angle) 
            else:
                # if sprite is not a grid but a single row of tiled images perform the below
                image_center_x = (self.image_center[0])+((self.age-1)*self.image_size[0])   # calculates which x image position to draw
                image_center_y = self.image_center[1]										# sets the y center to that of the image center since it is one row
                # the below line determines the appropriate image tile to draw and position
                canvas.draw_image(self.image,[image_center_x,image_center_y],self.image_size,self.pos,self.image_size,self.angle)
        else:
            # Since the graphic is not an animation draw the single graphic 
            canvas.draw_image(self.image,self.image_center,self.image_size,self.pos,self.image_size,self.angle)
        
    def update(self):
        self.age += 1						# increase the image age by 1
        if self.age < self.lifespan:		# update image position if lifespan has not expired
            self.pos[0] += self.vel[0]		# modify the sprite x position
            self.pos[1] += self.vel[1] 		# modify the sprite y position
            self.angle += self.angle_vel	# modify the sprite angle based on the velocity angle
            return True						# returns true of the image is still alive
        else:
            return False					# returns false if the image needs to be discarded

    def collision(self,other_object):		
        # determins if the image has collided with another object in a different position
        if dist(self.pos,other_object.get_position()) <= self.radius + other_object.get_radius():
            return True		# returns true of the two objects are within a specific distance
        else:
            return False	# returns false if the images are outside a specific distance
        
    def get_radius(self):		# returns the image object radius
        return self.radius
    
    def get_position(self):		# returns the image object x,y position
        return self.pos
    
    def get_vel(self):			# returns the image object velocity
        return self.vel
    
    def get_ang(self):			# returns the image object angle
        return self.angle
    
    def get_ang_vel(self):		# returns the image object angle velocity
        return self.angle_vel
    
# this procedure handles the main processing of the gain.  
# draws and moves the the background images 
def draw(canvas):
    # declares the global variables which needs to be modified by the draw procedure 
    global time,a_rock,lives,score,started,rock_group,missle_group,started,total_rock_count,game_level,explosion_group,ship_explosion_group
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw score and lives
    canvas.draw_text("Lives:", [50, 50], 22, "White", "sans-serif")								# lives text
    canvas.draw_text("Score:", [680, 50], 22, "White", "sans-serif")							# score text
    canvas.draw_text("Level:", [365, 50], 22, "White", "sans-serif")							# level text
    canvas.draw_text(str(lives), [50, 80], 22, "White", "sans-serif")							# prints the number of lives remaining
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")							# prints the current score
    canvas.draw_text(str(game_level+player_level_mod), [365, 80], 22, "White", "sans-serif")	# prints the current game level
    
    # draw ship and sprites
    my_ship.draw(canvas)						# draws the ship image on the canvas
    process_sprite_group(canvas,missle_group)	# draws the missle images on the canvas

    
    # update ship and sprites
    my_ship.update()							# updates the ship object based on the current inputs
    
    # if no lives remain or the game is not started reset the game
    if lives == 0 or not started:				
        started = False						# set started to false
        game_level = 0						# set the internal game level to zero
        total_rock_count = 0				# set the total rock count to zero
        rock_group = set([])				# clear all the rock group sprites
        explosion_group = set([])			# clear all the explosion group sprites
        ship_explosion_group = set([])		# clears the ship explosion sprite
        soundtrack.rewind()					# resets the background soundtrack
        # displays the splash image as the game has ended
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    else:
        process_sprite_group(canvas,rock_group)				# process and draw the rock group sprites
        process_sprite_group(canvas,explosion_group)		# process and draw any rock group explosions
        process_sprite_group(canvas,ship_explosion_group)	# process and draw any ship explosion sprites

        # if a rock has collided with the ship
        if group_collide(rock_group,my_ship):
            # create a explosion sprite and add it to the rock explosion group
            ship_explosion_group.add(Sprite(my_ship.get_position(),my_ship.get_vel(),my_ship.get_ang(),my_ship.get_ang_vel(),ship_explosion_image,ship_explosion_info))
            lives -= 1			# decrease lives by 1
        collision_count = group_group_collide(missle_group,rock_group)  # checks to see which missles have collided with which rocks
        total_rock_count += collision_count								# incriments the total rock count use to increase the game level
        game_level = total_rock_count//rock_spawn_limit					# increase the game level for every 12 rocks that have been destroyed
        score += 10*collision_count										# increase the game score by the number of rocks destroyed
    
            
# timer handler that spawns a rock    
def rock_spawner(): 
    global rock_group
    # the below calculates the spawn location, velocity, angle and rotational velocity of the new rock group
    spawn_pos = [WIDTH*random.randrange(1,101)/100.0, HEIGHT*random.randrange(1,101)/100.0]
    spawn_vel = [random.randrange(-2.0,3.0)*(1+0.05*(game_level+player_level_mod)),random.randrange(-2.0,3.0)*(1+0.05*(game_level+player_level_mod))]
    spawn_ang = random.randrange(0.0,360.0)
    spaw_ang_vel = random.randrange(-3.0,3.0)/60.0
    
    # create the rock sprite
    sprite = Sprite(spawn_pos,spawn_vel,spawn_ang,spaw_ang_vel, asteroid_image, asteroid_info)
    
    # if the rock sprite is too close to the ship ignore this round of the sprite creation
    if len(rock_group) < rock_spawn_limit+game_level and dist(my_ship.get_position(),spawn_pos) > (my_ship.get_radius()+sprite.get_radius()+30):
        rock_group.add(sprite)		# add the rock sprite to the rock sprite group

def process_sprite_group(canvas,sprite_set):
    # this method loops through the specified sprite group, tries to update the sprite or destroyes it if has expired
    for sprite in set(sprite_set):
        if sprite.update():				# update the sprite
            sprite.draw(canvas)			# draw the sprite if it has been updated
        else:
            sprite_set.discard(sprite)	# if it wasn't updated destroy it
  
def group_collide(group,other_object):
    # this method loops through the rock group and another object to determine collisions 
    global lives,explosion_group		# global variables to be updated 
    collision_num = 0					# initialized this variable to count the collisions
    for sprite in set(group):			# loop through all the sprites in the group
        if sprite.collision(other_object):		# did the sprite collide with another object
            # add a explosion sprite to the explosion group
            explosion_group.add(Sprite(sprite.get_position(),sprite.get_vel(),sprite.get_ang(),sprite.get_ang_vel(),explosion_image,explosion_info))               
            explosion_sound.play()  # play the explosion sound
            group.discard(sprite)	# destroy the rock sprite
            collision_num += 1		# increase the collision count by one
    if collision_num > 0:			
        return True					# returns true if there were collisions
    else:
        return False				# returns false if there were no collisions
    
def group_group_collide(missle_group,rock_group):
    # this method loops through the missle group and rock group to call the collibe function to determine collisions
    missle_collision_count = 0
    for missle in set(missle_group):			# for every missle check to see if it hits a rock in the rock group
        if group_collide(rock_group,missle):	# did missle collide with a rock?
            missle_group.discard(missle)		# if it collided with a rock destroy it
            missle_collision_count += 1			# increase the number of missle collisions
    return missle_collision_count				# return the missle collision count
    
def keydown(key):
    # this method executes the correct function based on the keyboard input
    global missle_group
    if key == simplegui.KEY_MAP["left"]:
        my_ship.update_angle_vel(-5.0 / 60)		# update the position angular velocity
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.update_angle_vel(5.0 / 60)		# update the negative angular velocity
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(True)				# sets the ship object to be thrusting
        ship_thrust_sound.play()				# play the thrusting ship sound
    elif key == simplegui.KEY_MAP["space"]:
        missle_group.add(my_ship.shoot())		# adds a missle sprite to the missle sprite group as the ship has fired

# Key up event handler for 
# checks to see which key was released for which paddle and sets the velocity to zero
def keyup(key):
    # cancels the key up event for thrust and left and right
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.angle_vel = 0				# sets the angular velocity to zero
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.update_thrust(False)		# turns off the ship thrust
        ship_thrust_sound.rewind()       	# resets the ship thrust sound
 
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started,lives,score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:   # if clicked this starts a new game
        started = True 			# when clicked it puts the game in play
        lives = 3				# reset the number of lives
        score = 0				# resets the game score
        soundtrack.play()		# starts the game sound track
        
def increase_level():			# this method increase the game level for every click of the increase level button
    global player_level_mod
    if player_level_mod < 30:	# upper level increase limit is 30
        player_level_mod += 1	# increase level if not at the limit
        
def decrease_level():			# this method decreases the game level for every click of the decrease level button 
    global player_level_mod
    if player_level_mod > 0:    # lower limit is zero, if level is not zero decrease one
        player_level_mod -= 1	# decrease level by one
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
#a_rock = Sprite([WIDTH*random.randrange(1,101)/100.0, HEIGHT*random.randrange(1,101)/100.0], [random.randrange(-2.0,3.0),random.randrange(-2.0,3.0)],random.randrange(0.0,360.0),random.randrange(-3.0,3.0)/60.0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 1, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_keyup_handler(keyup)
frame.add_label("Select Game Level")
frame.add_button("Increase",increase_level,100)
frame.add_button("Decrease",decrease_level,100)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
