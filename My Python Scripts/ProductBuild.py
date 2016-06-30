# A class to define a software build

# A way to think about modules is they are a specialised dictionary that can store python code so you can get to it with the '.' operator.  Python also has got another construct that serves a similar  purpose called a class.  A class is a way to take a grouping of functions and data and place them inside a container so you can access them with the '.' operator.
import sys

class ProductBuild:
# the ancestor of a class is listed in the parentheses
# python supports multiple inheritance, multiple ancesters can be listed in parentheses
	'define a software build'
	
	def __init__(self, product_name):
		if ('dell' in product_name) or (product_name == 'dpw'):
			self.product_name = 'Dell'
		elif ('enterprise' in product_name) or ('invincea' in product_name):
			self.product_name = 'Enterprise'
		else:
			self.product_name = []
			print 'Invalid product name'
			
