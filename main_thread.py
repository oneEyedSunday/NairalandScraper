import sys, datetime, random
from bs4 import BeautifulSoup as bs
import requests
from functions import *
import time
import regexes
# turn this to optparse or argparse


startingUrl = 'https://www.nairaland.com'

def main():
	# get options
	# start url, etc, forums to search in

	# holds all links to be scraped,
	# so we dont scrape twice
	# holds all links to be viisted, so we don't visit twice
	linksToScrape = []
	emails = []

	if len(sys.argv) > 1 :
		# forum given, start from forum
		if str(sys.argv[1]):
			try:
				# scrape thread
				start = sys.argv[1]
				# normalise
				normalisedUrl = getRelativeUrl(start)
				linksToScrape.append(normalisedUrl)
				# print(normalisedUrl)
				html = requests.get(startingUrl + normalisedUrl)
				# thread
				# get all paginated links
				if html.status_code == 200:
					bsObj = bs(html.content, "lxml")
					links  = expandOnLink(normalisedUrl, bsObj, startingUrl)
					linksToScrape.extend(links)
				else:
					print("[-] Error")
			except Exception as e:
				raise e

			finally:
				for l in linksToScrape:
					try:
						print("Parsing {}".format(l))
						emails.extend(getEmails(getSoupFromLink(l)))
						# time.sleep(5)
					except Exception as e:
						print("[-] Error : {}".format(e))	

				if len(sys.argv) > 2:
					filename = str(sys.argv[2])
				else:
					filename = splitRelativeUrl(str(sys.argv[1]))[2] + ".txt"
				writeToFile(emails, filename)
	else:
		# start from home
		try:
			html = requests.get(startingUrl)
			bsObj = bs(html.content, "lxml")
			print(getInternalLinks(bsObj))
		except Exception as e:
			raise e


if __name__ == "__main__":
	main()