Instagram-Bot v 1.1
'''
Cranklin's Instagram Bot v.1.0
Repaired By: Jeff Henry
Repairs:
- Updated Login Request
- Updated Like Requests
- Updated Next Page Search
=================================================================================
FOR MULTIPLE ACCOUNTS, ADD USERNAME AND PASSWORDS TO THE ARRAYS BELOW. MAKE SURE
THE APPROPRIATE PASSWORD GOES WITH THE SAME INDEX AS THE USERNAME.
=================================================================================

This bot gets you more likes and followers on your Instagram account.

Requirements:
- python > 2.6 but < 3.0
- pycurl library
- web.stagram.com login prior to using the bot

Instructions:
- make sure you have the correct version of Python installed
- make sure you have the pycurl library installed
- log into web.stagram.com with your instagram account and approve the app
- edit between lines 52 and 62
- from the command line, run "python InstaBot.py"
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
'''
