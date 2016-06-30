"""
This script is for question 9 of week 1 quiz
"""
import math

def project_to_distance(pointX, pointY, distance):
	dist_to_origin = math.sqrt(pointX**2 + pointY**2)
	scale = distance / dist_to_origin

	print pointX * scale, pointY * scale

project_to_distance(2, 7, 4)

