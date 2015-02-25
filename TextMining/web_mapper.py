from pattern.web import *

def get_cleaned_urls(seed_link):
	"""
	This function takes a link to a webpage, and tries to extract any links on that page to other website.  
	"""
	list_of_clean_url = []
	try:
		web_page_text = URL(seed_link).download()
		web_links = find_urls(web_page_text)
		for link in web_links:
			new_url = clean_url(link)
			if new_url != -1:
				list_of_clean_url.append(clean_url(link))
		return list_of_clean_url
	except:
		return -1
def clean_url(link):
	"""
	Takes a link, and either returns -1 if not a valid link, or a normalized link in the form:
	www.[URL].[com/gov/edu/org]
	Possibly may decouple the top level domain into an input arguement, but that is to be considered later.

	>>> clean_url('reddit.com')
	'http://www.reddit.com'
	>>> clean_url('asfa')
	-1
	>>> clean_url('http')
	-1
	>>> clean_url('http://www.reddit.com')
	'http://www.reddit.com'
	"""
	allowed_domain = ['.com','.gov','.edu','.org']
	if any(domain in link for domain in allowed_domain):
		if 'http' in link:
			return link
		else:
			if 'www.' in link:
				return 'http://' + link
			else:
				return 'http://www.' + link
	else:
		return -1

def web_crawl(seed_link, degrees):
	"""
	Notes to self:
	Need to reorganize this so that I can eliminate dead links. 
	How to make this faster.... -> maybe ignore that stuff about domains... 
	"""
	n = 0
	to_do = []
	current_links = []
	links_to_parse = [seed_link]
	link_map = {}
	while n < degrees:
		print 'initial links'
		print links_to_parse
		if len(links_to_parse)!=0:
			for link in links_to_parse:
				list_of_urls = get_cleaned_urls(link)
				if list_of_urls == -1:
					pass
				else:
					if link_map.has_key(link):
						pass
					else:
						link_map[link] = n
						to_do.extend(get_cleaned_urls(link))
		

		links_to_parse = list(to_do)	
		to_do = []
		n+=1
		print n

	return link_map


if __name__ == '__main__':
    import doctest
    doctest.testmod()