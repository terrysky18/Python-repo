# implementation of Spaceship - program template for RiceRocks
#   JKM - PART II 

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
MIN_ROCK_DISTANCE = 10
score = 0
lives = 3
time = 0
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

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
# center, size, radius = 0, lifespan = None, animated = False) 
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image1 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion_image2 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_orange.png")
explosion_image3 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")
explosion_image4 = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue2.png")



# sound assets purchased from sounddogs.com, please do not redistribute
# .ogg versions of sounds are also available, just replace .mp3 by .ogg
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

def process_sprite_group(canvas, a_group):
    ''' Function to update and draw all the elements in a group. '''
    for element in list(a_group):
        element.draw(canvas)
        
        # Determine if the Sprite is expired, and remove.
        if element.update():
            a_group.discard(element)

def create_explosion(old_sprite):
    ''' Create a new explosion object, which copies most of the 
        object information to a new explosion object. Add the expposion
        object to the explosion_group.'''
    global explosion_group
    # pos, vel, ang, ang_vel, image, info, sound = None):
    # Create an explosion,
    pos = old_sprite.get_pos()
    vel = old_sprite.get_vel()
    ang = old_sprite.get_angle()
    ang_vel = old_sprite.get_angle_vel()
    exp_image = old_sprite.get_explosion_image()
    an_explosion = Sprite(pos, vel, ang, ang_vel, exp_image, explosion_info, explosion_sound)
    explosion_group.add(an_explosion)    
    

def group_collide(group, other_object):
    ''' Determine if a collide has occurred with the object 
        and any items in the group. Remove the element that 
        has collided with the object from the group. 
        Return true if there was a collision.'''
    result = False
    for sprite in list(group):
        if sprite.collision(other_object):
            # print "collision detected!"
            result = True
            group.discard(sprite)
            create_explosion(other_object)
            
    return result        

def group_group_collide(group1, group2):
    '''Determine if a collide has occurred any items in either of 
       the group. Returns the number of elements in first group
       that collided with second group. And also removes the elements
       from the first group.'''
    num = 0
    for sprite in list(group1):
        if group_collide(group2, sprite):
            num +=1
            group1.discard(sprite)
    return num

def restart_game():
    ''' Starts/restarts the game.'''
    global lives, started, score, my_ship, explosion_group 
    score = 0 
    lives = 3
    soundtrack.rewind()
    soundtrack.play()
    explosion_group = set([])
    my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
    

def game_over():
    global rock_group, missile_group, started
    started = False
    rock_group = set([])
    missile_group = set([])   
    soundtrack.pause()
    soundtrack.rewind()
    
    # JKM - Might need to turn off explosion sound.
    
# Ship class
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.explosion_image = explosion_image2
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.image_size[0], self.image_center[1]] , self.image_size,
                              self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size,
                              self.pos, self.image_size, self.angle)
        # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT

        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
            
        self.vel[0] *= .99
        self.vel[1] *= .99

    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
       
    def increment_angle_vel(self):
        self.angle_vel += .05
        
    def decrement_angle_vel(self):
        self.angle_vel -= .05
        
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0], self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0], self.vel[1] + 6 * forward[1]]
        a_missile = Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound, explosion_image4)
        missile_group.add(a_missile)
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def get_explosion_image(self):
        return self.explosion_image
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel
    
    def get_vel(self):
        return self.vel
    
    def get_pos(self):
        return self.pos
    
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None, exp_image = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
        self.explosion_image = exp_image    
                   
    def draw(self, canvas):
        if self.animated:
            # Determine index into animated tiled image.
            # Tiled Image is Horizontally tiled. 0 -> lifespan-1
            if self.age >= self.lifespan:
                # there will be an index issue
                print "ERROR - INDEX into tiled image beyond range"
                print self.age
                return 
            image_center = [self.image_center[0] + self.age * self.image_size[0], self.image_center[1]]
        else:
            # Regular image.
            image_center = self.image_center
        
        # Draw the object
        canvas.draw_image(self.image, image_center, self.image_size,
                          self.pos, self.image_size, self.angle)

    def update(self):
        # update angle
        self.angle += self.angle_vel
        
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # update age and check if need to destroy this sprite
        self.age +=1
        return self.age >= self.lifespan
 
    def get_explosion_image(self):
        return self.explosion_image
    
    def get_angle(self):
        return self.angle
    
    def get_angle_vel(self):
        return self.angle_vel
    
    def get_vel(self):
        return self.vel
    
    def get_pos(self):
        return self.pos
    
    def get_radius(self):
        return self.radius 

    def collision(self, other_object, min_distance = 0):
        ''' Determine if another_object has collide with self.
            Returns True if a collision is detected, False otherwise'''
        distance = dist(self.get_pos(), other_object.get_pos())
        sum_of_radius = self.get_radius() + other_object.get_radius()
        
        return (distance) < sum_of_radius + min_distance  
        
    
# key handlers to control ship   
def keydown(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        
def keyup(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        restart_game()

def draw(canvas):
    global time, started, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White")
    canvas.draw_text("Score", [680, 50], 22, "White")
    canvas.draw_text(str(lives), [50, 80], 22, "White")
    canvas.draw_text(str(score), [680, 80], 22, "White")

    # draw ship and update
    my_ship.draw(canvas)
    my_ship.update()

    
    # process sprites
    # a_rock.draw(canvas)
    # a_rock.update()
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)     
    #a_missile.draw(canvas)    
    # a_missile.update()
    
    # Create an explosion
    process_sprite_group(canvas, explosion_group)

    
    # See if any collisions with rocks and the ship.
    if group_collide(rock_group, my_ship):
        lives -= 1    
         
    # See number of rock missile collisions.    
    num_missile_rock = group_group_collide(rock_group, missile_group)
    score += num_missile_rock    

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())

    # Check is game is over.
    if lives <= 0:
        game_over()
        
# timer handler that spawns a rock and does other timer actions
DIFFICULTY = 5
MAX_ROCKS = 12
def timer_actions():
    # global a_rock
    global rock_group, timer, explosion_group
    
    # Small hack to stop music and timer when the frame is closed.
    try:
        if frame.get_canvas_textwidth('Hello world',50) < 10:
            soundtrack.pause()
            timer.stop()
            missile_sound.pause()
            ship_thrust_sound.pause()
            print "Game window closed. Soundtracks and timer stopped"
    except:
        soundtrack.pause()
        timer.stop()
        missile_sound.pause()
        ship_thrust_sound.pause()
        print "Game window closed. Soundtracks and timer stopped"
    
    if not started:
        return
         
    if len(rock_group) >= MAX_ROCKS:
        # Keep the number of rocks to less than the max
        return
    
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    # Increase difficulty (e.g. rock velocity) based on score
    difficulty = 1 + (score / DIFFICULTY)
    rock_vel = [difficulty * rock_vel[0], difficulty * rock_vel[1]]
    rock_avel = random.random() * .2 - .1
    a_rock = Sprite(rock_pos, rock_vel, 0, rock_avel, asteroid_image, asteroid_info, 0, explosion_image4)
    
    # Only allow the rock if it doesn't immediately cause a collision.
    if not a_rock.collision(my_ship, MIN_ROCK_DISTANCE):
        rock_group.add(a_rock)
    else:
        print "Rock creation ignored since too close."

# initialize stuff
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, .1, asteroid_image, asteroid_info)
rock_group = set([])
# a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
missile_group = set([])
explosion_group = set([])


# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

timer = simplegui.create_timer(1000.0, timer_actions)

# get things rolling
timer.start()
frame.start()
