from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data
import nltk
import ssl
try:
   _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
   pass
else:
   ssl._create_default_https_context = _create_unverified_https_context

#nltk.download('punkt')

## SI 206 - HW
## COMMENT WITH:
## Your section day/time: Monday 4-5:30
## Any names of people you worked with on this assignment: N/A

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:
#Code for Part 3:Caching
#Finish parts 1 and 2 and then come back to this
CACHE_FNAME = 'twitter_cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, parameters, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION, indent=4)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]


#Code for Part 1:Get Tweets

baseurl = "https://api.twitter.com/1.1/statuses/user_timeline.json"
parameters = {}
parameters["screen_name"] = username
parameters["count"] = num_tweets
response_obj = make_request_using_cache(baseurl, parameters)

print("===")


response_file = "tweet.json"
fileref = open(response_file, "w")
fileref.write(json.dumps(response_obj, indent=4))   


print("USER: " + username)
print("TWEETS ANALYZED: " + num_tweets)



#Code for Part 2:Analyze Tweets

all_tokens = []
for elem in response_obj:
    tokens = nltk.word_tokenize(elem["text"])
    all_tokens.extend(tokens)

clean_tokens = [] 
for item in all_tokens:
    if item[0].isalpha(): # is the first letter in the item an alphabetical character?
        if item == "http" or item == "https" or item == "RT": # is the item "http", "https", or "RT"?
            pass
        else:
            clean_tokens.append(item)
    else:
        pass

fdist = nltk.FreqDist(clean_tokens)
fdist_clean_mostcommon = fdist.most_common(5)
print("5 MOST FREQUENT WORDS: ", end="") 
for tu in fdist_clean_mostcommon:
    word = tu[0]
    freq = tu[1]
    print("{}({})".format(word, freq), end=" ")
print("") #for formatting only
print("===") #for formatting only



if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
