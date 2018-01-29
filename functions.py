import requests
from bs4 import BeautifulSoup as bs
from regexes import forumsRegex, threadsRegex, emailRegex, otherPages
pages = set()
forbiddenLinks = ["/?", "/register", "/login"]

forums = ["/nairaland", "/politics", "/crime", "/romance", "/jobs", "/career",
 "/business", "/investment", "/nysc", "/education",
  "/autos", "/cartalk", "/properties","/health", "/travel", "/family"
  , "/culture", "/religion", "/food", "/diaries", "/ads", "/pets", "/agriculture"]

threadLinks = set()
allLinks = []
startingUrl = "http://www.nairaland.com"

def getEmails(soup):
	if soup is not None:
		groups = emailRegex.findall(str(soup))
		return groups
	return

def getSoupFromLink(pageUrl):
	r = requests.get(startingUrl + getRelativeUrl(pageUrl))
	element = "Error"
	if r.status_code == 200:
		element = bs(r.content, "lxml")
	else:
		print("Error")
		return None
	return element


def getForumLinks(soup):
	global forbiddenLinks
	forumLinks = []
	for link in soup.findAll("a", href=forumsRegex):
		if link.attrs['href'] is not None:
			if (link.attrs['href'] not in forumLinks) and (link.attrs['href'] not in forbiddenLinks):
				forumLinks.append(link['href'])

	return forumLinks


def getInternalLinks(soup):
	# this get links of threads
	# /somedigits/somealphadash
	# global threadLinks
	internalLinks = []
	for link in soup.findAll("a", href=threadsRegex):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in internalLinks:
				internalLinks.append(link.attrs['href'])

	# return threadLinks
	return internalLinks


def PaginatedLinks(start, soup, startingUrl):
	global allLinks
	internalLinks = getInternalLinks(soup)
	parts = splitRelativeUrl(start)
	for i in internalLinks:
		if isLinkAChildOfThread(start, i):
			if not otherPages.match(i):
				allLinks.append(i)

	return allLinks

def expandOnLink(start,soup, startingUrl):
	global allLinks
	initialLinks = PaginatedLinks(start, soup, startingUrl)
	maxTest = []
	for l in initialLinks:
		l = l.replace(start, "")
		if l is not '':
			maxTest.append(int(l))
		else:
			maxTest.append(0)

	lastLink = max(maxTest)
	for i in range(1, lastLink+1):
		allLinks.append("{}{}".format(start, i))

	return allLinks


def getRelativeUrl(fullUrl):
	relativeUrl = fullUrl.replace("http://www.nairaland.com", "")
	return relativeUrl

def splitRelativeUrl(relativeUrl):
	# url of thread i.e /dddd/sss-sssss will return 2 + parts
	addressParts = relativeUrl.split("/")
	return addressParts


def isLinkAChildOfThread(url, link):
	# link is a relative link?
	# url will always be a relative link
	if(link.lower().startswith(url.lower())):
		return True
	return False

def getLinks(pageUrl):
	bsObj = None
	global pages
	try:
		html =  requests.get("http://www.nairaland.com")
		if html.status_code == 200:
			bsObj = bs(html.content, "lxml")
	except Exception as e:
		print("[-] Error occured: {}".format(e))
	
	if bsObj is not None:
		for link in bsObj.findAll("a", href=forumsRegex):
			if 'href' in link.attrs:
				if link.attrs['href'] not in pages:
					newPage = link.attrs['href']
					pages.add(newPage)
					getLinks(newPage)

	return pages

def writeToFile(content, filename):
	# open file for writing
	with open(filename, "w") as f:
		for e in content:
			f.writelines(e)
			f.write("\n")
	print("File {} written".format(filename))


def getAllLinks(soup):
	allLinks = []

	for link in soup.findAll("a"):
		if 'href' in link.attrs:
			if link.attrs['href'] not in allLinks:
				allLinks.append(link.attrs['href'])

	return allLinks