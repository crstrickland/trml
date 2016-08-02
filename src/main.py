
import shelve
from textblob import TextBlob
from spacy.en import English

nlp =  English()


def getsubject(sentence):
    parse = nlp(sentence)
    for token in parse:
        if word.dep_ == 'nsubj':
            return word.text

def s_unicode(str):
    try:
        return unicode(str)
    except:
        text = str(obj).encode('string_escape')
        return unicode(text)

def getRating(sentence):
    sentence = s_unicode(sentence)



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

