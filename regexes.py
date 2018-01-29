import re


emailRegex = re.compile(r'''([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})''', re.VERBOSE)
# forumsRegex = re.compile(r"^/[a-z-](?!login)+")
forumsRegex = re.compile(r"((?!^/(login|register)$).)*")
threadsRegex = re.compile(r"^((http://www.nairaland.com)?/\d+)")
paginationLinks = re.compile(r'^/links(/d+)?')

# can't use this because other threads will be matched
otherPages = re.compile(r'^(/\d+/).*/\d+(#\d+)$')