import re, collections, copy, random

englishLetterFreq = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}

words_len_1 = ['a','i','o']

words_len_2 = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up',
 'an', 'go', 'no', 'us', 'am']

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'.lower()

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()

alphabet_small = LETTERS.lower()

#################################
#Start Spell-Checker from http://norvig.com/spell-correct.html
#################################


def encrypt(text, keyDict):
    newtext = ''
    for c in text:
        try:
            newtext += keyDict[c]
        except KeyError:
            newtext += c
    return newtext

def words(text):
    return re.findall('[a-z]+', text.lower())

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

NWORDS = train(words(file('dictionary.txt').read()))

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet_small if b]
    return set(transposes + replaces)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    return max(candidates, key=NWORDS.get)

#################################
#End Spell-Checker
#################################

def getDictWords():
    file = open('dictionary.txt', 'r')
    text = file.read().lower()
    list = text.split()
    return list

def recognizedWordsInPercent(text):
    wordsCount = 0
    wordsFoundCounter = 0
    words = text.split()
    wordsDict = getDictWords()
    for word in words:
        wordsCount += 1
        if word in wordsDict:
            wordsFoundCounter += 1
            #print("found: ", word)
    return wordsFoundCounter/wordsCount*100

def countAllLetters(message):
    letterCount = {}
    for c in alphabet_small:
        letterCount[c] = 0
    all_Letters = 0
    for letter in message:
        if letter in alphabet_small:
            letterCount[letter] += 1
            all_Letters += 1
    # sortiert buchstaben nach haeufigkeit...haeufigster zu erst
    print ("lettercounted: ", letterCount)
    sortedList = sorted(letterCount, key=letterCount.get, reverse=True)
    print ("sorted list: " , sortedList)

    new_dict = dict(zip(sortedList,ETAOIN))

    print ("dict with key from lettercount statistic: ",new_dict)
    return new_dict

def generateDecryptKey(freq_Dict):
    decrypt_Dict = dict(zip(freq_Dict, englishLetterFreq))
    return decrypt_Dict

def replaceLettersByFrequence(message,decryptKeyDict):
    replaced_Message =''
    for symbol in message:
        if symbol in LETTERS:
            replaced_Message = replaced_Message + decryptKeyDict[symbol]
        else:
            replaced_Message = replaced_Message + symbol
    return replaced_Message

def findWords(message):
    new_message = message
    #all words from string as list
    wordlist = re.sub("[^\w]", " ",  message).split()
    #dictionary for corrected words
    word_correction = {}
    #loop through all words, find correction and replace them in the string
    for word in wordlist:
        new_word = correct(word)
        if new_word != word:
            word_correction[word] = new_word
            #exchange words in string
            new_message = new_message.replace(word,new_word)
    return new_message

def correctKey(dictionary, Key, Value):
    newKey_Dict = dictionary
    try:
         tempOne = newKey_Dict[Key] # value an stelle letterOne 
         temp_key = newKey_Dict.keys()[newKey_Dict.values().index(tempOne)]

         #tempTwo = newKey_Dict[tempOne] # value an stelle lettertwo
         dictionary[tempOne] = Value 
         dictionary[temp_key] = Key  



    except KeyError:
        return dictionary
    print ("key after corerction: ", dictionary)    
    return dictionary

def getWordsByLengthOne(key,message):
    # all words as list
    word_dict = dict()
    wordlist = re.sub("[^a-zA-Z]", " ",  message).split()
    for word in wordlist:
        if len(word) == 1:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    resultList = sorted(word_dict, key=word_dict.get, reverse=True)
    print ("words length 1:" ,resultList)
    resultList = resultList[:3]
    index = 0
    for e in resultList:
        print ("e: ", e)
        print ("words_index: ", words_len_1[index])
        correctKey(key,e,words_len_1[index])
        index +=1

def getWordsByLengthTwo(key, message):
    word_dict = dict()
    wordlist = re.sub("[^a-zA-Z]", " ",  message).split()
    for word in wordlist:
        if len(word) == 2:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1
    resultList = sorted(word_dict, key=word_dict.get, reverse=True)
    resultList = resultList[:24]
    indexA = 0
    for e in resultList:
        indexB = 0
        for char in words_len_2[indexA]:
            correctKey(key,e[indexB], char)
            indexB +=1
        indexA += 1

def correctKeyBySpellChecker(text, key):
    keyTemp = copy.deepcopy(key)

    words = text.split()
    random.shuffle(words)

    for word in words:
        newKey = correctWord(word, keyTemp)
        if newKey != False:
            return newKey
    return keyTemp

def correctWord(word, key):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    newWord = max(candidates, key=NWORDS.get)

    if word != newWord:
        wordLen = len(word)
        counter = 0
        for counter in range(wordLen):
            key = correctKey(key, word[counter], newWord[counter])
            return key
    return False

def initKey():
    key_dict = dict.fromkeys(ETAOIN)
    print ("init key: ", key_dict)
    return key_dict

def readFile(fileName):
    file = open(fileName, 'r')
    text = file.read().lower()
    return text

def main():

    cyphertext = readFile('alice_encrypt.txt')
    # init Key with "None" values ordered by ETAOIN
    #key = initKey()

    key = countAllLetters(cyphertext)

    new_Text = replaceLettersByFrequence(cyphertext, key)
    ##### bis hier alles richtig !!!
    #print(new_Text)
    getWordsByLengthOne(key,new_Text)

    #getWordsByLengthTwo(key,new_Text)

    #decypherText = encrypt(cyphertext, key)

    #recognizedWords = recognizedWordsInPercent(decypherText)

    #while True:
    #    print ('Words recognized: ', recognizedWords, '%')
    #    if recognizedWords> 60:
    #        break;
    
    #    keyTemp = correctKeyBySpellChecker(decypherText, key)
    
    #    decriphedTemp = encrypt(cyphertext, keyTemp)
    #    recognizedWordsTemp = recognizedWordsInPercent(decriphedTemp)
    
     #   if recognizedWords < recognizedWordsTemp:
     #       key = keyTemp
     #       recognizedWords = recognizedWordsTemp



if __name__ == "__main__":
	main()
