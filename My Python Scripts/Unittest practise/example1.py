# A basic example to show Python's unit test framework

import random
import unittest

class TestSequenceFunctions(unittest.TestCase):
# test suite - a collection of test cases

	def setUp(self):
		self.seq = range(10)
	
	def test_shuffle(self):	# test case: shuffle test
		# make sure the shuffled sequence does not lose any elements
		random.shuffle(self.seq)
		self.seq.sort()		# sort the list

		# assertEqual is a method in unittest.TestCase class
		self.assertEqual(self.seq, range(10))

		# should raise an exception for an immutable sequence
		self.assertRaises(TypeError, random.shuffle, (1, 2, 3))
	
	def test_choice(self):	# test case: choice test
		element = random.choice(self.seq)
		self.assertTrue(element in self.seq)
	
	def test_sample(self):	# test case: sample test
		with self.assertRaises(ValueError):
			random.sample(self.seq, 20)
		for element in random.sample(self.seq, 5):
			self.assertTrue(element in self.seq)

suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)

