from pattern.web import *
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt 

def get_links(seed_link):
	"""
	This function gets all the links associated with a specific link. It uses clean_url as a helper function to clean the seed_link, and then clean all new_links
	The same error handling is also present, where if the download() fails, then it just throws a -1.
	"""
	seed_link = clean_url(seed_link)
	try:
		#creates a fresh list or urls.
		list_of_urls = []
		#parses the html for links
		web_page_text = URL(seed_link).download()
		web_links = find_urls(web_page_text)
		#normalizes the links so that its all lowercase
		web_links = [x.lower() for x in web_links]
		#adds all the links to list_of_urls after cleaning.
		for link in web_links:
			new_url = clean_url(link)
			#if valid, add to the list.
			if new_url != -1:
				list_of_urls.append(new_url)
		unique_links = []
		#goes through the list of links, and add only if not present already.
		for link in list_of_urls:
			if link not in unique_links:
				unique_links.append(link)
			else:
				pass
		#returns the links. 
		return unique_links
	except:
		return -1
def clean_url(seed_link):
	"""
	This function cleans a seed_link so that it will be usable for the pattern URL download api.
	This will be based on the allowed domains listed below.
	If no domains are present, then it just returns -1.
	>>> clean_url('google.com')
	u'http://www.google.com'
	>>> clean_url('asfa')
	-1
	>>> clean_url('google.edu')
	u'http://www.google.edu'
	>>> clean_url('google.au')
	-1
	""" 
	#Tokenizes based on . and /
	parts_of_url = re.split(r'[./]+',seed_link)
	#list of allowed domains. Add more if you want more coverage. There will be problems with other countries most likely....
	allowed_domain = ['com','gov','edu','org', '']
	#iterates through the choices above
	for domain in allowed_domain:
		#If an allowed domain is present, and the length of the tokenized string is greater than one, then we proceed to essentially reassemble the string
		#in a standardized way
		if domain in parts_of_url and len(parts_of_url)>1:
			index_of_domain = parts_of_url.index(domain)
			return u'http://www.' + parts_of_url[index_of_domain-1] + u'.'+ domain
		#If not, we just skip it.
		else:
			pass
	#if no allowed domain was found... we just return -1
	return -1


def web_crawl(seed_link, degrees):
	"""
	Basically, this function takes a website and degrees, and tells you what websites are n degrees away given the criteria listed under graph_network().
	It should probably be better optimized, but still gets through 6 degrees for at least http://google.com in about 2-3 minutes or so. 
	"""
	list_of_sites = [(seed_link,0,seed_link)]
	work_list = [seed_link]

	#Now I start the process
	for n in range(1,degrees+1):
		to_do = []
		# This iterates over the different links that originate from n-1 degree ( initially 0)
		for work_url in work_list:
			#This represents the list of new urls to add, this resets it for each level
			addition_list = [] 
			#This gets all the links from the work_url		
			new_links_from_work_url = get_links(work_url)
			#This skips the link if the link is invalid -> not an actual website. 
			if new_links_from_work_url == -1:
				continue
			#Creates a working copy of the new_links so that we can edit it.
			new_links_from_work_url_copy = list(new_links_from_work_url)
			#This will find all the sites that are unique by iteration
			for listed_sites in list_of_sites:
				#Looks toward each of the links from above.
				for new_addition_url in new_links_from_work_url:
					#If the new_addition_url already exists in the listed_sites, we remove it for the new sites to be registered.
					if(new_addition_url == listed_sites[0]):
						new_links_from_work_url_copy.remove(new_addition_url)
			#For all the links that need to be registered, we iterate through to add em.
			for link_to_add in new_links_from_work_url_copy:
				list_of_sites.append((link_to_add,n,work_url))
				#We also add them to a to_do list for our new working list
				to_do.append(link_to_add)
		#Sets the work_list to the new stuff.
		work_list = to_do[:]

	#Goes through, and makes sure that each site is actually a valid website.
	for listed_site in list_of_sites:
		try: 
			URL(listed_site[0]).download()
		except:
			#If not valid, we remove it.
			list_of_sites.remove(listed_site)

	return list_of_sites

def graph_network(website_link, degrees):
	"""
	Current implementation is very slow, start with degrees = 1 
	for whatever website you start with and work your way up in degrees
	This particular function is used to find all the unique websites that can be accessed from the front page of each website.
	Essentially, you would find all websites that are accesible from website_link's homepage and then go to their homepages and see
	Which websites are accesible from their and so on. This will continue until you get degrees clicks away. 

	"""
	#Generates the list of sites. see above ^
	site_list = web_crawl(website_link, degrees)
	print site_list
	#Maps the value of the degrees here.
	val_map = dict()
	#Create a directed graph
	G = nx.DiGraph()
	#Adds all the origin of the nodes in site_list
	histo = dict()
	for element in site_list:
		#Just strips out extraenous text 
		val_map[element[0][11:]] = element[1]
		histo[element[1]] = histo.get(element[1],0) + 1
		G.add_edges_from([(element[0][11:], element[2][11:])])
	values = [val_map.get(node, 0.25) for node in G.nodes()]

	print histo
	nx.draw_spring(G,with_labels=True, node_color = values)
	plt.show(G)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    graph_network('http://www.google.com', 3)