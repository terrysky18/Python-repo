from sys import argv
script, product_name = argv

if ('dell' in product_name) or (product_name == 'dpw'):
	product = 'Dell'
elif ('enterprise' in product_name) or ('invincea' in product_name):
	product = 'Enterprise'
else:
	product = []
	print 'Invalid product name'
	exit(0)

print product
