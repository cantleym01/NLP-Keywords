#from newspaper import Article
from rake_nltk import Rake

# parameters are as follows:
# text (string: text to obtain keywords from)
# numOfKeywords (integer: how many keywords to obtain from text)
# title (string: the title of the text if applicable(if left empty it won't be used))
def getKeywords(text, numOfKeywords, title=""):

    # remove words which are not valid keywords or are not useful
    # parameters are as follows:
    # words (list of strings: words to scrub of junk data and irrelevant data)
    def scrubList(words):

        invalidWords = []

        i = 0
        while (i < len(words)):
            # remove everything that's invalid
            # currently it will remove: unicode codes, specified strings in the invalidWords list
            if ('\u' in words[i].encode('raw_unicode_escape') or words[i] in invalidWords):
                del words[i]
            else:  # otherwise increment iteration
                i += 1
        return words

    # clean keywords; some keywords from rake have junk in them
    # parameters are as follows:
    # words (list of strings: words to scrub of junk data and irrelevant data)
    def scrubWord(word):
        word = word.replace(",", "")
        word = word.replace(".", "")

        return word

    rak = Rake()  # english by default

    # extract keywords and store them+their degree in a dictionary
    rak.extract_keywords_from_text(text)
    wordDic = rak.get_word_degrees()

    # use the title if relevant
    if(title != ""):
        # make it a list by splitting on whitespace
        titleWords = title.split()

        # lower everything for accuracy
        for it in range(0, len(titleWords)):
            titleWords[it] = titleWords[it].lower()

        # if a keyword was in the title, double it's weight because it's likely very relevant
        for word in wordDic:
            if(word in titleWords):
                wordDic[word] = wordDic[word]*2

    rankedWords = sorted(wordDic, key=wordDic.get, reverse=True)
    rankedWords = scrubList(rankedWords)
    returnDic = {}

    if (numOfKeywords > len(rankedWords)):
        numOfKeywords = len(rankedWords)

    for it in range(0, numOfKeywords):
        temp = rankedWords[it]
        temp = scrubWord(temp) # scrub the word to be stored without changing it's value in the list

        # add the new, scrubbed word and it's weight
        returnDic[temp.encode('UTF8')] = (wordDic[rankedWords[it]] * (1.0/len(wordDic)))

    return returnDic


#url = 'https://techcrunch.com/2017/10/06/apple-is-looking-into-reports-of-iphone-8-batteries-swelling/'

# newspaper
#art = Article(url, language='en')  # English
#art.download()
#art.parse()

#print(getKeywords(art.text, 10))
#print(getKeywords(art.text, 10, art.title))