import string 
import re

# Keys can not be mutable -> keys should not change.
# Keys work by basically being hashed into something
# Hash is hashed yo. 
#
#
#

def get_word_list(file_name):
	f = open(file_name,'r')
	punctuation = string.punctuation
	lines = f.readlines()
	curr_line = 0
	word_dict = dict()
	while lines[curr_line].find('START OF THIS PROJECT GUTENBERG EBOOK') == -1:
 	    curr_line += 1
	lines = lines[curr_line+1:]
	for single_line in lines:
		line_of_text = string.lower(single_line)
		list_of_words = re.split('[?., ![{}^\n%&*(\)@;:\"\r-]', line_of_text)
		for word in list_of_words:
			if len(word) == 0:
				pass
			else:
				word_dict[word] = word_dict.get(word, 0) + 1
	return word_dict

def get_top_n_words(D,n):
	word_counts = []
	ordered_by_frequency = sorted(D, key=D.get, reverse=True)
	for x in range(0, n):
		word_counts.append((ordered_by_frequency[x], D[ordered_by_frequency[x]]))

	return word_counts

file_name = "pg1400.txt"
dictionary = get_word_list(file_name)

print get_top_n_words(dictionary, 1000)