class Team(object):

	def __init__(self, name=None, logo=None, members=0):
		self.name = name
		self.logo = logo
		self.members = members
	
	def ShowName(self):
		print self.name
	
	def ShowLogo(self):
		print self.logo
	
	def ShowMembers(self):
		print self.members

