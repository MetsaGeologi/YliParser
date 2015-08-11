# Library imports
from urllib.request import urlopen, FancyURLopener, Request
from lxml import etree, html
from lxml.html.clean import clean_html
from bs4 import BeautifulSoup
import re
import subprocess

# Commands
cmds = ["!exit", "!info"]
cmd_current = 0
cmd_executed = 0
cmd_info = "YliBot v0.1 :D Written in Python 3.2 :Dd, Running on RaspberryPI :Dddd"

# UrlOpener class
class UrlOpener(FancyURLopener):
	version = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36"
	targeturl = "http://ylilauta.org/satunnainen/39569996"
	posturl = "http://ylilauta.org/scripts/post.php"
url_opener = UrlOpener()

# Cleanhtml tags method
def cleanhtml(raw_html):
	cleaner = re.compile("<p id=.*?>.*?</p>")
	cleantext = re.findall(cleaner, raw_html)
	cleaner = re.compile("<a href.*?>.*?</a>")
	cleantext = re.sub(cleaner, "", "\n".join(cleantext))
	soup = BeautifulSoup(cleantext)
	cleantext = "".join(soup.findAll(text=True))
	return cleantext

# Send a message to the board
def sendmsg(message):
	request = url_opener.open(url_opener.posturl, None)
	return request

# Main function
def main():
	# Global variables
	global url_opener
	global cmd_executed
	global cmd_current
	# Our UrlOpener instance
	url_opener.addheader("Connection", "keep-alive")
	url_opener.addheader("Accept", "text/html;q=0.9")
	url_opener.addheader("Accept-encoding", "")
	url_opener.addheader("Accept-language", "fi-FI,fi;q=0.8,en-US;q=0.6,en;q=0.4")
	while True:
		# Open the target
		page = url_opener.open(url_opener.targeturl, None)
		# Format the output
		parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
		tree = etree.parse(page, parser)
		doc_format = etree.tostring(tree.getroot(), pretty_print=True, encoding="utf-8")
		doc_string = doc_format.decode("utf-8")
		# Iterate over the html document
		output = ""
		div_post = 'div class=\"post\">'
		in_post = False
		for line in doc_string.splitlines():
			if in_post == True:
				if div_post in line:
					in_post = False
				else:
					output += line
					continue
			if div_post in line and in_post == False:
				in_post = True
				output += "\n" + line.split(div_post, 1)[1]	
		# Create another tree and remove all html
		output_nohtml = cleanhtml(output)
		# Parse through each post
		cmd = ""
		cmd_current = 0
		for line in output_nohtml.splitlines():
			if any(x in line for x in cmds):
				cmd_current += 1
				print("current: ", cmd_current, " executed: ", cmd_executed)
				if cmd_current <= cmd_executed or cmd != "":
					continue
				cmd = line
		# Execute command
		if cmd != "":
			print("CMD Executed!")
			cmd_executed += 1
		if cmd == cmds[0]:
			print("!exit Command requested!")
		elif cmd == cmds[1]:
			print(sendmsg(cmd_info))
	
	# Save output to file
	file = open("output.html", "w")
	file.write(output_nohtml)
	file.close()

# Function hooks
if __name__ == "__main__":
	main()
