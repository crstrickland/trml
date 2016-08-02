#!/usr/bin/python
#filename: trml.py
from __future__ import division
import shelve
from textblob import TextBlob
from spacy.en import English
import re as normies
import string

print "ready"

nlp =  English()

def removepunct(s):
    lets = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    sl = ''.join(ch for ch in s if ch in lets)
    return sl

def getSubject(sentence):
    parse = nlp(sentence)
    for token in parse:
        if token.dep_ == 'nsubj':
            return token.text

def s_unicode(obj):
    try:
        return unicode(obj)
    except:
        text = str(obj).encode('string_escape')
        return unicode(text)

def talnlp(sentence):
    sentence = str(normies.sub('[^A-Za-z0-9 ]+', '', sentence))
    print sentence
    #sentence = sentence.translate(string.maketrans("",""), string.punctuation)

    sentence_u = s_unicode(sentence)
    print sentence_u

    rating = getRating(sentence_u)
    subject = getSubject(sentence_u)

    subrate = getSub(subject)

    if(subrate != 'MISSING'):
        rating = (rating + subrate) / 2

    subject = str(normies.sub('[^A-Za-z0-9 ]+', '', str(subject)))
    #subject = subject.translate(string.maketrans("", ""), string.punctuation)

    modSub(subject, rating)

    return rating

def getRating(sentence):
    rating = TextBlob(sentence)
    ratingraw = 2000.0 * ((rating.sentiment.polarity + 1.0) * rating.sentiment.subjectivity)
    #talrobot is very subjective
    tal_rating = (int(ratingraw) % 200) - 100
    return tal_rating

#adds subject to database, or changes its rating
def modSub(subject, rating, fn='trbdict'):

    db = shelve.open(fn, flag = 'c', protocol = 2, writeback = False)

    db[subject] = rating
    db.close()

#returns rating of subject, or 'MISSING' if subject not in database
def getSub(subject, fn='trbdict'):

    db = shelve.open(fn, flag = 'c', protocol =2, writeback= False)

    try:
        rating = db[subject]
    except:
        return 'MISSING'

    db.close()

    return rating

#makes a new database
def makeDB(fn='trbdict'):
   d = shelve.open(fn, flag = 'c', protocol = 2, writeback = False)


makeDB()

x = raw_input()

while(x != 'STOP'):
    x = raw_input()
    print talnlp(x)