#!/usr/bin/python

'''
Cranklin's Instagram Bot v.1.0 
Repaired By: github.com/JeffHenry
Notes from Jeff:
	- Updated Login
	- Updated Like [Webstagram no longer takes POST requests for liking an image.]
	
==============================
Check www.cranklin.com for updates

This bot gets you more likes and followers on your Instagram account.

Requirements:
- python > 2.6 but < 3.0
- pycurl library
- web.stagram.com login prior to using the bot

Instructions:
- make sure you have the correct version of Python installed
- make sure you have the pycurl library installed
- log into web.stagram.com with your instagram account and approve the app
- edit between lines 42 and 52
- from the command line, run "python webstagram.py"
- enjoy!

v1.0 updates:
- added browser agent randomizer
- added optional sleep timer
- added optional hashtag limiter
- added a couple extra additions for some people experiencing SSL errors. (thanks Charlie)
*** thank you Nick, John, Max, Shahar, Charlie for the help
'''

import os
import pycurl
import cStringIO
import re
import random
import time

##### EDIT THESE BELOW

# your instagram username and password
username = "username"
password = "password"

#set a sleep timer between each like. Set value to 0 if you don't want it to sleep at all
sleeptimer = 5

#set a like limit per hashtag. Set value to 0 if you don't want a limit
hashtaglikelimit = 100

#your list of hashtags
hashtags = ["love","instagood","me","cute","photooftheday","tbt","instamood","iphonesia","picoftheday","igers","girl","beautiful","instadaily","tweegram","summer","instagramhub","follow","bestoftheday","iphoneonly","igdaily","happy","picstitch","webstagram","fashion","sky","nofilter","jj","followme","fun","smile","sun","pretty","instagramers","food","like","friends","lol","hair","nature","swag","onedirection","bored","funny","life","cool","beach","blue","dog","pink","art","hot","my","family","sunset","photo","versagram","instahub","amazing","statigram","girls","cat","awesome","throwbackthursday","repost","clouds","baby","red","music","party","black","instalove","night","textgram","followback","all_shots","jj_forum","igaddict","yummy","white","yum","bestfriend","green","school","likeforlike","eyes","sweet","instago","tagsforlikes","style","harrystyles","2012","foodporn","beauty","ignation","niallhoran","i","boy","nice","halloween","instacollage"]

##### NO NEED TO EDIT BELOW THIS LINE

browsers = ["IE ","Mozilla/","Gecko/","Opera/","Chrome/","Safari/"]
operatingsystems = ["Windows","Linux","OS X","compatible","Macintosh","Intel"]
useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"

def login():
	try:
		os.remove("pycookie.txt")
	except:
		pass
	print "[DEBUG]: Removed pycookie.txt"
	
	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, 'https://api.instagram.com/oauth/authorize/?client_id=9d836570317f4c18bca0db6d2ac38e29&redirect_uri=http://web.stagram.com/&response_type=code&scope=comments+relationships+likes')
	c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
	c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
	c.setopt(pycurl.WRITEFUNCTION, buf.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.setopt(pycurl.ENCODING, "")
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	#c.setopt(pycurl.VERBOSE, True)
	c.setopt(pycurl.USERAGENT, useragent)
	c.perform()
	curlData = buf.getvalue()
	buf.close()
		
	clientid = '9d836570317f4c18bca0db6d2ac38e29'
	postaction = re.findall(ur"action=\"([^\"]*)\"",curlData)
	token = re.findall('<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)"/>', curlData)
	postdata = 'csrfmiddlewaretoken='+token[0]+'&username='+username+'&password='+password

	buf = cStringIO.StringIO()
	c = pycurl.Curl()
	c.setopt(pycurl.URL, "https://instagram.com"+postaction[0])
	c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
	c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
	c.setopt(pycurl.WRITEFUNCTION, buf.write)
	c.setopt(pycurl.FOLLOWLOCATION, 1)
	c.setopt(pycurl.ENCODING, "")
	c.setopt(pycurl.SSL_VERIFYPEER, 0)
	c.setopt(pycurl.SSL_VERIFYHOST, 0)
	c.setopt(pycurl.REFERER, "https://instagram.com/accounts/login/?next=/oauth/authorize/%3Fclient_id%3D"+clientid+"%26redirect_uri%3Dhttp%3A//web.stagram.com/%26response_type%3Dcode%26scope%3Dlikes%2Bcomments%2Brelationships")
	c.setopt(pycurl.USERAGENT, useragent)
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS, postdata)
	c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
	#c.setopt(pycurl.VERBOSE, True)
	c.perform()
	curlData = buf.getvalue()
	buf.close()

	if '<a href="/logout">LOG OUT</a>' in curlData:
		print "Logged in"
	else:
		print "Unable to Log in"


def like():
	likecount = 0
	sleepcount = 0
	for tag in hashtags:
		hashtaglikes = 0
		nextpage = "http://web.stagram.com/tag/"+tag+"/?vm=list"
		#print "nextpage: " + nextpage 
		#enter hashtag like loop
		while nextpage != False and (hashtaglikes < 200):
			buf = cStringIO.StringIO()
			c = pycurl.Curl()
			c.setopt(pycurl.URL, nextpage)
			c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
			c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
			c.setopt(pycurl.WRITEFUNCTION, buf.write)
			c.setopt(pycurl.FOLLOWLOCATION, 1)
			c.setopt(pycurl.ENCODING, "")
			c.setopt(pycurl.SSL_VERIFYPEER, 0)
			c.setopt(pycurl.SSL_VERIFYHOST, 0)
			useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
			c.setopt(pycurl.USERAGENT, useragent)
			c.perform()
			curlData = buf.getvalue()
			buf.close()	
			file = open("log.txt","w")
			file.write(curlData)
			
			nextpagelink = re.findall(ur'<li><a href="(.*?)" rel="next"><i class="fa fa-chevron-down"></i> Earlier</a></li>',curlData)
			#print "[DEBUG]: nextpagelink: " + nextpagelink[0]
			if len(nextpagelink)>0:
				nextpage = "http://web.stagram.com"+nextpagelink[0]
			else:
				nextpage = False
				print "[DEBUG]: No next page found."
				
			regex = '<li><button type="button" class="btn btn-default btn-xs likeButton" data-target="(.*?)"><i class="fa fa-heart"></i> Like</button></li>'
			likedata = re.findall(regex,curlData)
			if len(likedata)>0:
				for imageid in likedata:
					if hashtaglikelimit > 0 and hashtaglikes >= hashtaglikelimit:
						break
					repeat = True
					while repeat:
						randomint = random.randint(1000,9999)

						url = 'http://web.stagram.com/api/like/'+imageid
						#print "[DEBUG]: URL: " + url
						#postdata = 'pk='+imageid+'&t='+str(randomint)
						buf = cStringIO.StringIO()
						c = pycurl.Curl()
						c.setopt(pycurl.URL, url)
						c.setopt(pycurl.COOKIEFILE, "pycookie.txt")
						c.setopt(pycurl.COOKIEJAR, "pycookie.txt")
						c.setopt(pycurl.WRITEFUNCTION, buf.write)
						c.setopt(pycurl.FOLLOWLOCATION, 1)
						c.setopt(pycurl.ENCODING, "")
						c.setopt(pycurl.SSL_VERIFYPEER, 0)
						c.setopt(pycurl.SSL_VERIFYHOST, 0)
						useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"
						c.setopt(pycurl.USERAGENT, useragent)
						#c.setopt(pycurl.POST, 1)
						#c.setopt(pycurl.POSTFIELDS, postdata)
						#c.setopt(pycurl.POSTFIELDSIZE, len(postdata))
						#c.setopt(pycurl.VERBOSE, True)
						c.perform()
						postData = buf.getvalue()
						buf.close()
						if postData == '''{"status":"OK","message":"LIKED"}''':
							likecount += 1
							hashtaglikes += 1
							print "You liked #"+tag+" image "+imageid+"! Like count: "+str(likecount)
							repeat = False
							sleepcount = 0
							if sleeptimer > 0:
								time.sleep(sleeptimer)
						else:
							sleepcount += 1
							print "Your account has been rate limited. Sleeping on "+tag+" for "+str(sleepcount)+" minute(s). Liked "+str(likecount)+" photo(s)..."
							time.sleep(60)	
							
def main():
    login()
    like()

if __name__ == "__main__":
    main()
