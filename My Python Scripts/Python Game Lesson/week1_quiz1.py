"""
The script is to implement question 5 of the week 1 quiz
"""

def f_of_x(x):
	"""
	implement the function: f(x)=-5x^5 + 69x^2 - 47
	"""
	f = -5*(x**5) + 69*(x**2) - 47
	return f
# end of function definition

answer = [f_of_x(0), f_of_x(1), f_of_x(2), f_of_x(3)]

print answer
print max(answer)
