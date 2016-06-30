# The file modifies the MySQL script moreError.sql
# moreError.sql is used to populate the errors table in the IMS database

import datetime
import os
import time

# remove an old file
if os.path.exists('moreError.sql'):
	os.remove('moreError.sql')

def get_timestamp():
# returns a timestamp string in Year Month Day, hour minute second format
	ts = time.time()
	return datetime.datetime.fromtimestamp(ts).strftime('%Y %b %d %H:%M:%S')

my_script_file = open('moreError.sql', 'w')

best_lines = ['It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife.  Jane Austen: Pride and Prejudice (1813)',
		'All happy families are alike; each unhappy family is unhappy in its own way.  Leo Tolstoy:  Anna Karenina (1878)',
		'It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair, we had everything before us, we has nothing before us, we were all going direct to Heaven, we were all going direct the other way.  Charles Dickens: A Tale of Two Cities (1859)',
		'It was a bright cold day in April, and the clocks were striking thirteen.  George Orwell:  Nineteen Eighty-Four (1949)',
		'It was a queer, sultry summer, the summer they electrocuted the Rosenbergs, and I didn\'t know what I was doing in New York.  Sylvia Plath:  The Bell Jar (1963)',
		'You don\'t know about me without you have read a book by the name of \'The Adventures of Tom Sawyer\'; but that ain\'t no matter.  That book was made by a Mr Mark Twain, and he told the truth, mainly.  Mark Twain:  The Adventures of Huckleberry Finn (1884)',
		'If you really want to hear about it, the first thing you\'ll probably want to know is where I was born, and what my lousy childhood was like, and how my parents were occupied and all before they had me, and all that David Copperfield kind of crap, but I don\'t feel like going into it, if you want to know the truth.  J.D Salinger:  The Catcher in The Rye (1951)',
		'They say when trouble comes close ranks, and so the white people did.  Jean Rhys:  Wide Sargasso Sea (1966)',
		'In my younger and more vulnerable years my father gave me some advice that I\'ve been turning over in my mind ever since.  Whenever you feel like criticising any one, he told me, just remember that all the people in this world haven\'t had the advantages that you\'ve had.  F. Scott Fitzgerald:  The Great Gatsby (1925)',
		'The past is a foreign country:  they do things differently there.  L.P. Hartley:  The Go-Between (1953)',
		'As Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his bed into a monstrous vermin.  Franz Kafka:  Metamorphosis (1915)',
		'Call me Ishmael.  Herman Melville:  Moby-Dick (1851)',
		'The sun shone, having no alternative, on the nothing new.  Samuel Beckett:  Murphy (1938)',
		'It was love at first sight.  The first time Yossarian saw the chaplain he fell madly in love with him.  Joseph Heller:  Catch-22 (1961)',
		'Miss Brooke had that kind of beauty which seems to be thrown into relief by poor dress.  George Eliot:  Middlemarch (1871)',
		'All children, except one, grow up.  J.M. Barrie:  Peter Pan (1911)',
		'Under certain circumstance there are few hours in life more agreeable than the hour dedicated to the ceremony known as afternoon tea.  Henry James:  The Portrait of a Lady (1880)',
		'Lolita, light of my life, fire of my loins.  My sin, my soul.  Lo-lee-ta: the tip of the tongue taking a trip of three steps down the palate to tap, at three, on the teeth.  Lo. Lee. Ta.  Vladimir Nabokov:  Lolita (1955)',
		'It was inevitable: the scent of bitter almonds always reminded him of the fate of unrequited love.  Gabriel Garcia Marquez:  Love in the Time of Cholera (1985)',
		'They\'re out there.  Black boys in white suits up before me to commit sex acts in the hall and get it mopped up before I can catch them.  Ken Kesey:  One Flew Over the Cuckoo\'s Nest (1962)',
		'I am a camera with its shutter open, quite passive, recording, not thinking.  Christopher Isherwood:  Goodbye to Berlin (1939)',
		'Elmer Gantry was drunk.  He was eloquently drunk, lovingly and pugnaciously drunk.  Sinclair Lewis:  Elmer Gantry (1926)',
		'A green hunting cap squeezed the top of a fleshy balloon of a head.  John Kennedy Toole: A Confederacy of Dunces (1980)',
		'The cold passed reluctantly from the earth, and the retiring fogs revealed an army stretched out on the hills, resting.  Stephen Crane: The Red Badge of Courage (1895)',
		'It was the day my grandmother exploded.  Iain Banks:  The Crow Roads (1992)',
		'The schoolmaster was leaving the village, and everybody seemed sorry.  Thomas Hardy:  Jude the Obscure (1895)',
		'There was no possibility of taking a walk that day.  Charlotte Bronte:  Jane Eyre (1847)',
		'Mother died today.  Or maybe, yesterday; I can\'t be sure.  Albert Camus:  The Stranger (1946)',
		'He was an old man who fished alone in a skiff in the Gulf Stream and he had gone eighty-four days now without taking a fish.  Ernest Hemingway:  The Old Man and The Sea (1952)',
		'All this happened, more or less.  Kurt Vonnegut:  Slaughterhouse Five (1969)']

command = 'INSERT INTO errors (date, method, path, message) VALUES '
idx = 0		# index

for msg in best_lines:
	#time.sleep(15)
	my_values = '(\'' + get_timestamp() + '\', '

	if (idx % 2) == 0:
		my_values += "\'GET\', "
	else:
		my_values += "\'POST\', "
	
	if idx < 16:
		my_values += "\'/ims2/DukeofWellington\', "
	else:
		my_values += "\'/ims2/WinstonChurchil\', "
	
	my_values += "\'" + msg + "\');" + '\n'
	
	my_script_file.write(command + my_values)
	idx += 1

my_script_file.close()

