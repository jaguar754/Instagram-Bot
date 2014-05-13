#!/usr/bin/python
'''
Jeff Henry's Instagram Bot
* Based of Cracklin's Pycurl Bot

This script simulates image likes on various tags. Gets more attention on your account.

Requirements:
- python > 2.6 but < 3.0
- pycurl library
- web.stagram.com login prior to using the bot [Authentication]

Instructions:
- make sure you have the correct version of Python installed
- make sure you have the pycurl library installed
- log into web.stagram.com with your instagram account and approve the app
- Edit the usernames and passwords in main()
- enjoy!

v1.0 updates:
- added browser agent randomizer
- added optional hashtag limiter
- added a couple extra additions for some people experiencing SSL errors. (thanks Charlie)

v1.1 updates:
- added random sleep time between image likes
- added random tag selection out of list of hashtags
- added multiple account functions
- added rate-limited handling based on single or multiple accounts

v1.2 update:
- Structured into a class for better information organization.
- Statistics output
'''

import os,sys,pycurl,cStringIO,re,random,time,threading

# Keeps track of how many likes failed:
like_failed_counter = 0

# Max Daily likes:
max_daily_likes = 2000

#set a like limit per hashtag. Set value to 0 if you don't want a limit
hashtaglikelimit = 100

#your list of hashtags
hashtags = ["love","instagood","me","cute","photooftheday","tbt","instamood","iphonesia","picoftheday","igers","girl","beautiful","instadaily","tweegram","summer","instagramhub","follow","bestoftheday","iphoneonly","igdaily","happy","picstitch","webstagram","fashion","sky","nofilter","followme","fun","smile","sun","pretty","instagramers","food","like","friends","lol","hair","nature","bored","funny","life","cool","beach","blue","dog","pink","art","hot","my","family","sunset","photo","versagram","instahub","amazing","statigram","girls","cat","awesome","throwbackthursday","repost","clouds","music","black","instalove","night","textgram","followback","igaddict","yummy","white","yum","bestfriend","green","school","likeforlike","eyes","sweet","instago","tagsforlikes","style","2012","foodporn","beauty","boy","nice","halloween","instacollage"]
#hashtags = ['evo','bboy','cars','porsche','nissan','honda','acura','toyota','jdm','bosozoku','gamergirl','girlgamer','model','selfie','girl']
##### NO NEED TO EDIT BELOW THIS LINE

browsers = ["IE ","Mozilla/","Gecko/","Opera/","Chrome/","Safari/"]
operatingsystems = ["Windows","Linux","OS X","compatible","Macintosh","Intel"]
useragent = random.choice(browsers) + str(random.randrange(1,9)) + "." + str(random.randrange(0,50)) + " (" + random.choice(operatingsystems) + "; " + random.choice(operatingsystems) + "; rv:" + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + "." + str(random.randrange(1,9)) + ")"

class Account(object):
	def __init__(self,username,password):
		super(Account, self).__init__()
		self.username = username
		self.password = password
		self.overall_likes = 0
		self.times_failed = 0
		self.tags_visited = 0
		self.login_fails = 0
		self.rate_limit_counter = 0
	
	#--- Login to Webstagram service.
	def login(self):
		try:
			os.remove("pycookie.txt")
		except:
			pass
			
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
		c.setopt(pycurl.USERAGENT, useragent)
		c.perform()
		curlData = buf.getvalue()
		buf.close()
	
		#--- Handle failed web page retrieval:
		if '<body class="p-dialog oauth-login">' not in curlData:
			print "Error getting login page."
			sys.exit(0)
		
		clientid = '9d836570317f4c18bca0db6d2ac38e29'
		postaction = re.findall(ur"action=\"([^\"]*)\"",curlData)
		token = re.findall('<input type="hidden" name="csrfmiddlewaretoken" value="(.*?)"/>', curlData)
		postdata = 'csrfmiddlewaretoken='+token[0]+'&username='+self.username+'&password='+self.password
	
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
		c.perform()
		curlData = buf.getvalue()
		buf.close()

		#--- Login Confirmation:
		if '<a href="/logout">LOG OUT</a>' in curlData:
			print "Logged into " + self.username
		elif(self.login_fails < 3):
			print "Unable to log into " + self.username + ". Attempting again."
			self.login_fails += 1
			time.sleep(5)
			self.login()
		elif(self.login_fails >= 3):
			print "3 login attempts failed for " + self.username + ". Program Ending."
			sys.exit(0)
		#--- Self Authorization attempt. Unsure if functional yet.
		elif '<input class="button confirm button-green" type="submit" value="Authorize" name="allow">' in curlData:
			print "Attempting to authorize Web.Stagram Services..."
			
			postdata = 'csrfmiddlewaretoken='+token[0]+'&allow=Authorize'
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
			c.perform()
			curlData = buf.getvalue()
			buf.close()

	#--- Like images!
	def like(self):
		likecount = 0
		tag_like_fail = 0
		global like_failed_counter
		global max_dialy_likes
		
		while(True):
			#--- Check if we reached today's cap.
			if self.overall_likes == max_daily_likes:
				print "Max Daily Likes reached. Best to stop in order to not get banned or rate-limited"
				sys.exit(0)
				
			#--- Generate a random tag from the list:
			current_tag = random.randrange(0,len(hashtags))
			print '---------------------------------------------'
			print 'Visiting #' + hashtags[current_tag]
			print '---------------------------------------------'
			self.tags_visited += 1
			hashtag_likes = 0
			
			#--- Visit the current tag:
			nextpage = "http://web.stagram.com/tag/"+hashtags[current_tag]+"/?vm=list"
			while nextpage != False and (hashtaglikelimit == 0 or (hashtaglikelimit > 0 and hashtag_likes < hashtaglikelimit)):
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
				c.setopt(pycurl.USERAGENT, useragent)
				c.perform()
				curlData = buf.getvalue()
				buf.close()	
			
				#--- Grab the next page link:
				nextpagelink = re.findall(ur'<li><a href="(.*?)" rel="next"><i class="fa fa-chevron-down"></i> Earlier</a></li>',curlData)
				if len(nextpagelink)>0:
					nextpage = "http://web.stagram.com"+nextpagelink[0]
				else:
					nextpage = False
					break;
				
				#--- Find all the like buttons:
				regex = '<li><button type="button" class="btn btn-default btn-xs likeButton" data-target="(.*?)"><i class="fa fa-heart"></i> Like</button></li>'
				likedata = re.findall(regex,curlData)
			
				#--- If found un-liked images:
				if len(likedata)>0:
					for imageid in likedata:
						if hashtaglikelimit > 0 and hashtag_likes >= hashtaglikelimit:
							break
						
						#--- Print statistics every 50 likes:
						if(likecount%50 == 0 and likecount >1):
							self.print_statistics()
						repeat = True
						
						#--- Like the image:
						while repeat:
							url = 'http://web.stagram.com/api/like/'+imageid
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
							c.setopt(pycurl.USERAGENT, useragent)
							c.perform()
							postData = buf.getvalue()
							buf.close()
						
							#--- Check for successful like:
							if postData == '''{"status":"OK","message":"LIKED"}''':
								likecount += 1
								self.overall_likes += 1
								hashtag_likes += 1
								print "Liked an image with #"+str(hashtags[current_tag])+" \t Like count: "+str(likecount)
								repeat = False
								time.sleep(random.randrange(5,25))
							#--- Failed: 
							else:
								self.times_failed += 1
								like_failed_counter += 1
								tag_like_fail +=1
								#--- Check if rate-limited:
								if(like_failed_counter >= 20):
									like_failed_counter = 0
									self.print_statistics()
									print self.username+" rate-limited. Sleeping for 10 minutes."
									time.sleep(600)
									self.like()
								else:
									repeat = False
								
	def print_statistics(self): 
		print "------------------------------------------------------------------------"
		print "                         S T A T I S T I C S                            "
		print "------------------------------------------------------------------------"
		print " Account:\t\t" + self.username
		print " Total Tags Visited:\t" + str(self.tags_visited)
		print " Overall Likes: \t" + str(self.overall_likes)
		print " Total Tag Fails: \t" + str(self.times_failed)
		print "------------------------------------------------------------------------"
	
	def run(self):
		self.login()
		self.like()
		
if __name__ == "__main__":
	bot = Account("username","password")
	bot.run()
