# Author: Ansh Chandnani
# June 9th, 2020
# Python program to use the Twitter Search API and prepare some basic statistics

import sys
from twython import Twython
from datetime import datetime, date

def countNumOfTweets(allTweets):
    numOfTweets = 0
    for tweet in allTweets['statuses']:
        numOfTweets += 1
    return numOfTweets


def countNumOfTweetsLang(allTweets, isoLangCode):
    numOfTweets = 0
    for tweet in allTweets['statuses']:
        if tweet['lang'] == isoLangCode:
            numOfTweets += 1
    return numOfTweets

def getAvgFollowers(allTweets):
    totalNumOfFollowers = 0
    for tweet in allTweets['statuses']:
        totalNumOfFollowers += tweet['user']['followers_count']
    return (totalNumOfFollowers / countNumOfTweets(allTweets))

def countUserRetweets(allTweets):
    retweets = {}
    for tweet in allTweets['statuses']:
        if tweet['retweet_count'] > 0:
            user = tweet['user']['screen_name']
            numOfRetweets = tweet['retweet_count']
            if user in retweets:
                retweets[user] += numOfRetweets
            else:
                retweets.update({user: numOfRetweets})
    return retweets


def getHashtags(allTweets):
    hashtags = {}
    for tweet in allTweets['statuses']:
        for item in tweet['entities']['hashtags']:
            hashtag = item['text']
            if hashtag in hashtags:
                hashtags[hashtag] += 1
            else:
                hashtags.update({hashtag: 1})
    return hashtags


if __name__ == '__main__':

    CONSUMER_KEY = '''ENTER YOUR CONSUMER KEY'''
    CONSUMER_SECRET = '''ENTER YOUR CONSUMER SECRET'''
    ACCESS_TOKEN = '''ENTER YOUR ACCESS TOKEN'''
    ACCESS_SECRET = '''ENTER YOUR ACCESS SECRET'''

    # Creating link to Twitter Search
    twitterLink = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

    print('Python progam to analyze twitter search results for hashtags, retweets, followers, etc.')

    # user input search query
    searchQuery = input('Enter Twitter Search Query: ')
    # user input number of tweets to analyze
    try:
        numOfTweets = int(input('Enter the number of tweets to analyze: '))
    except:
        print('Invalid Input! Proceeding with 100 tweets...')
        numOfTweets = 100

    # tweets variable stores json data of tweets collected
    tweets = twitterLink.search(q=searchQuery, count=numOfTweets)
    # print(tweets)

    # Getting date and time for log
    today = date.today()
    now = datetime.now()
    currentTime = now.strftime('%H:%M:%S')

    # Writing statistics to file
    fileStream = open('TwitterStats.txt', 'a+')
    fileStream.write(str(today) + ' ' + str(currentTime) + '\n')
    fileStream.write('Total number of tweets analyzed: ' + str(countNumOfTweets(tweets)))
    fileStream.write('\nTotal number of tweets in English: ' + str(countNumOfTweetsLang(tweets, 'en')))
    fileStream.write('\nMean number of followers observed: ' + str(getAvgFollowers(tweets)))
    fileStream.write('\n\nUser Statistics:\n\n')
    retweets = countUserRetweets(tweets)
    fileStream.write('USER \t RETWEETS RECEIVED\n')
    for user in retweets:
        fileStream.write(user + '\t\t' + str(retweets[user]) + '\n')
    hashtags = getHashtags(tweets)
    fileStream.write('\nHASHTAG \t FREQUENCY\n')
    for hashtag in hashtags:
        fileStream.write(hashtag + '\t\t' + str(hashtags[hashtag]) + '\n')
    fileStream.write('\n--------------------------------------------------------\n')

    # Final message
    print('Total number of tweets analyzed:', countNumOfTweets(tweets))
    print('Statistics are saved in TwitterStats.txt')
