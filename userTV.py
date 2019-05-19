import requests
import json

# Make a request to the pushshift API for the top authors on comment
# score
endpoint = 'https://api.pushshift.io/reddit/'
queryType = 'comment'
subreddit = 'habs'
aggs = 'author:score:sum'
aggSize = 500
after = '2019-01-20'

response = requests.get(endpoint + queryType + '/search/' + \
                                              '?aggs=' + aggs + \
                                              '&after=' + after + \
                                              '&min_doc_count=1&size=0' + \
                                              '&agg_size=' + str(aggSize) + \
                                              '&subreddit=' + subreddit)

# Append the username, number of comments, and total score as a list
# to the list of all users
userList = []
for entry in response.json()['aggs']['author:score']:
   userList.append([entry['key'],entry['doc_count'],entry['score']])

# Calculate the mean of the comments
meanComments = 0
meanCommentScore = 0
for user in userList:
   meanComments += user[1]
   meanCommentScore += user[2]
meanComments /= len(userList)
meanCommentScore /= len(userList)

# Calculate the standard deviation of the comments
stdevComments = 0
stdevCommentScore = 0
for user in userList:
   stdevComments += (user[1]-meanComments)**2
   stdevCommentScore += (user[2]-meanCommentScore)**2
stdevComments /= len(userList)
stdevCommentScore /= len(userList)
from math import sqrt
stdevComments = sqrt(stdevComments)
stdevCommentScore = sqrt(stdevCommentScore)

# Find the number of standard deviations each user is
# from the mean for each category and sum them together
# to get the user's score
for user in userList:
   user.append(((user[1]-meanComments)/stdevComments)+
               ((user[2]-meanCommentScore)/stdevCommentScore))
