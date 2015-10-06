import time
import requests
import string
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import re
def is_in_arr(lis,s):
	result=False
	for item in lis:
		if item==s:
			result=True
	return result
def deleteDuplicates(lis):
	newLis=[]
	for item in lis:
		if item not in newLis:
			newLis.append(item)
	return newLis

def getGoodLink(url):
	k = url.rfind("/")
	return url[:k+1]
def crawl(url,pages):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "microsoft" not in href_test and "facebook" not in href_test and "twitter" not in href_test:
					if href_test.startswith("http"):
						pages.append(str(href))
					else:
						lin=getGoodLink(url)
						pages.append(lin+str(href))

	except:
		print "Error at: "+str(url)
def crawlTitle(url):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('span'):
			try:
				href=link.get('title')
				if href != "Loading icon" and href != None:
					arr.append(href)
				
			except:
				pass
		new = deleteDuplicates(arr)
		return new[0]


	except:
		print "Error at: "+str(url)
#print crawlTitle("https://www.youtube.com/watch?v=ek9fUnnzAhk")
def getPartial(answer,title):
	points=0
	answers = answer.split(" ")
	for item in answers:
		if str(item) in title:
			points= points + 2
	if points > 10:
		return 10		
	return points

def GradeYouQuiz(answer, title):
	points=0
	answer = str(answer).lower()
	title = "https://www.youtube.com/watch?v="+str(title)
	title = crawlTitle(title)
	title = str(title).lower()
	answerStripped = answer.strip()
	titleStripped = title.strip()
	if answerStripped == titleStripped:
		points = 10
	else:
		points = getPartial(answer,title)
	return points
def getVideoSearchUser(name):
	search = name.replace(" ","+")
	a=[]
	url="https://www.youtube.com/results?search_query="+str(search)+"&lclk=channel&filters=channel"
	crawl(url,a)
	b=[]
	for item in a:
		if "/user" in item:
			b.append(item)
	new = deleteDuplicates(b)
	try:
		return str(new[0]+"/videos")
	except:
		print "Bad"
def getVidsFromUser(name):
	url=getVideoSearchUser(name)
	a=[]
	crawl(url,a)
	b=[]
	c=[]
	for item in a:
		if "/watch" in item:
			b.append(item)
	for item in b:
		testW = str(item[52:])
		if len(testW)>5:
			c.append(testW)
	new=deleteDuplicates(c)
	return new

def getVideoSearch(link):
	search=link.replace(" ","+")
	a=[]
	url="https://www.youtube.com/results?search_query="+str(search)
	crawl(url,a)
	b=[]
	c=[]
	for item in a:
		if "/watch" in item:
			b.append(item)
	for item in b:
		testW=str(item[33:])
		if len(testW)>5:
			c.append(testW)
	new=deleteDuplicates(c)
	return new
