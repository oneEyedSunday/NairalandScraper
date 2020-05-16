import sys
from core.functions import *
import time

# turn this to optparse or argparse


startingUrl = 'https://www.nairaland.com'


def main():
    # holds all links to be scraped,
    # so we don't scrape twice
    # holds all links to be visited, so we don't visit twice
    links_to_scrape = []
    emails = []

    if len(sys.argv) > 1:
        # forum given, start from forum
        if str(sys.argv[1]):
            start = sys.argv[1]
            # normalise url
            normalized_url = getRelativeUrl(start)
            x = splitRelativeUrl(normalized_url)
            x = x[:3]
            normalized_url = "/".join(x)
            if len(sys.argv) > 2:
                filename = str(sys.argv[2])

            else:
                filename = "{}.txt".format(normalized_url)

            if checkFile(filename):
                # scraped before or filename exists
                print("File exists already, this could mean the thread has been scraped before.\n")
                # open file and find out thread that was scraped
                name = getLinkFromFile(filename)
                print("File contains results of scraping {}\n".format(name))
                print("Do you want to scrape thread again?\n")
                again = input("> ")
                if str(again.lower()) in ("yes", "y"):
                    # scrape again
                    pass
                else:
                    sys.exit("Thank you\n")
            try:
                links_to_scrape.append(normalized_url)
                html = requests.get(startingUrl + normalized_url)
                # get all paginated links
                if html.status_code == 200:
                    bs_obj = bs(html.content, "lxml")
                    links = expandOnLink(normalized_url, bs_obj, startingUrl)
                    for l in links:
                        if l not in links_to_scrape:
                            links_to_scrape.extend(links)
                else:
                    print("[-] Error couldn't connect to {}".format(startingUrl))
            except Exception as e:
                print("[-] Error: {}\n".format(e))

            finally:
                for l in links_to_scrape:
                    try:
                        print("Parsing {}".format(l))
                        emails.extend(getEmails(getSoupFromLink(l)))
                        time.sleep(5)
                    except Exception as e:
                        print("[-] Error : {}".format(e))

                # indicate link that was scraped
                writeToFile(normalized_url, emails, filename)
    else:
        # ask for link
        print("You did not specify a link.")
        print("Usage: python main_thread.py 'thread link' 'savefilename --optional'")
        sys.exit(1)


if __name__ == "__main__":
    main()
