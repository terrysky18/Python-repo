import re
import requests

def readTextFile(filename):
	"""
	Read the text file specified by filename,
	return the file content in a string
	param:  filename - exact directory to the file
	return:  string - file content
	"""
	try:
		content = ""
		with open(filename, "r") as myfile:
			content = myfile.read()
		return content
	except (FileNotFoundError):
		print("File not found")

def processFileContent(content):
	"""
	Take a file content as a string and extract the information then return it as a dictionary
	Assuming the file content in follow pattern:

	Users: user1; user2, user3; user4 ...
	Admins: admin1, admin2; admin3 ...
	Partners: partner1, partner2; partner3 ...

	param:  content - file content as a string
	return:  {"Users":[...], "Admins":[...], "Partners":[...]}
	"""
	result = {}
	result["Users"] = []
	result["Admins"] = []
	result["Partners"] = []

	lines = content.splitlines()
	for line in lines:
		words = re.findall(r"(\w+)", line)
		if words[0] == "Users":
			for word in words[1:]:
				result["Users"].append(word)

		elif words[0] == "Admins":
			for word in words[1:]:
				result["Admins"].append(word)

		elif words[0] == "Partners":
			for word in words[1:]:
				result["Partners"].append(word)
	return result

def launchURL(test_url, username):
	"""
	Use the requests module to access the url and return the API response as a json
	param:  test_url - the URL for testing, e.g. "www.example.com/login/"
	param:  username - the username for testing
	return:  json object
	"""
	test_url += username
	test_request = requests.get(test_url)
	return test_request.json()

def testUsers(test_url, usernames, user_type):
	"""
	Test the url with urser parameters and the return API response as a list of dictionary
	param:  test_url - the URL for testing, e.g. "www.example.com/login/"
	param:  usernames - username dictionary
	param:  user_type - specify the type user used for testing; i.e. User, Admin, Partner
	return:  list of dictionary
	"""
	response = {}
	for username in usernames[user_type]:
		response[username] = launchURL(test_url, username)
	return response


if __name__ == "__main__":
	filepath = r"C:\Users\user\Documents\test.txt"
	my_info = readTextFile(filepath)
	my_content = processFileContent(my_info)
	url = "www.example.com/login/"
	user_resp = testUsers(url, my_content, "Users")
	admin_resp = testUsers(url, my_content, "Admins")
	partner_resp = testUsers(url, my_content, "Partners")
