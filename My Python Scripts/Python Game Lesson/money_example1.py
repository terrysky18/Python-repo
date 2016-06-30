# Handle single quantity
def convert_units(val, name):
	result = str(val) + " " + name
	if val > 1:
		result = result + "s"
	return result
        
# convert xx.yy to xx pounds and yy pences
def convert(val):
	# Split into dollars and cents
	pound = int(val)
	pence = int(round(100 * (val - pound)))

	# Convert to strings
	pound_string = convert_units(pound, "pound")
	pence_string = convert_units(pence, "pence")

	# return composite string
	if pound == 0 and pence == 0:
		return "Broke!"
	elif pound == 0:
		return pence_string
	elif pence == 0:
		return pound_string
	else:
		return pound_string + " and " + pence_string
    
    
# Tests
print convert(11.23)
print convert(11.20) 
print convert(1.12)
print convert(12.01)
print convert(1.01)
print convert(0.01)
print convert(1.00)
print convert(0)
