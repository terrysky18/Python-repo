import glob
import re

directory = '\\\\beaver\\Builds'	#product build location

#search pattern
product1 = 'InvinceaEnterprise_*'
p = glob.glob(directory + '\\' + product1 + '*.exe')

i = 0
while (i < 100):
	version = re.findall(r'\d+', p[i])
	print version
	i +=1
