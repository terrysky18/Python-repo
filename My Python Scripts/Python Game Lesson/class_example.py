# an overtly simple example of defining and using class in python

class Character:	# class name is always capitalised in Python
	def __init__(self, name, initial_health):
	# the initialiser of the class
		self.name = name
		self.health = initial_health
		self.inventory = []
	
	def __str__(self):
		text_str = "Name: " + self.name
		text_str = " Health: " + str(self.health)
		text_str = " Inventory: " + str(self.inventory)
		return text_str
	
	def grab(self, item):
	# member function of the class
		self.inventory.append(item)
	
	def get_health(self):
	# member function of the class
		return self.health

def example():
# an example of using the type Character
	me = Character("Bob", 20)
	print str(me)		# using string cast to print the object me
	me.grab("pencil")
	me.grab("paper")
	print str(me)
	print "Health: ", me.get_health()

example()
