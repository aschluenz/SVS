import re, collections, copy, random
from spellchecker import *
from Ceasar import *

englishLetterFreq = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}

words_len_1 = ['a','i','o']

words_len_2 = ['of', 'to', 'in', 'it', 'is', 'be', 'as', 'at', 'so', 'we', 'he', 'by', 'or', 'on', 'do', 'if', 'me', 'my', 'up',
 'an', 'go', 'no', 'us', 'am']

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'.lower()

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()

alphabet_small = LETTERS.lower()

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
    print ("allwords: ", wordsCount, "found wordscount: ", wordsFoundCounter)
    recWords = float(wordsFoundCounter) / float(wordsCount)*100
    print ('Words recognized: ', recWords, '%')

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

    print ("dict with key from lettercount statistic: ", new_dict)
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
            new_message = new_message.replace(word,new_word)
    return new_message

def correctKey(dictionary, letterA, letterB):
    newKey_Dict = dictionary

    if letterA in LETTERS and letterB in LETTERS:
        print("pair to exchange: ", letterA, letterB)
        try:
            tempKey1 = [key for key in newKey_Dict.items() if key[1] == letterA][0][0]
            tempKey2 = [key for key in newKey_Dict.items() if key[1] == letterB][0][0]
            dictionary[tempKey1] = letterB
            dictionary[tempKey2] = letterA
        except KeyError:
            return dictionary
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
    #liste der woerter mit einem Buchstaben sortiert nach haeufigkeit
    resultList = sorted(word_dict, key=word_dict.get, reverse=True)
    resultList = resultList[:2]
    index = 0
    new_key = dict()
    for e in resultList:
        new_key = correctKey(key,e,words_len_1[index])
        index +=1
    return new_key

def getWordsByLengthTwo(key, message):
    temp_list = words_len_2
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
    #print ("resultlist from two: ", resultList)
    indexA = 0
    new_key = dict()

    list_with_words = []
    list_not_found_words = []

    for e in resultList:
        if e in temp_list:
            list_with_words.append(e)
            list_not_found_words.append(e)

    for item in list_with_words:
        resultList.remove(item)
        temp_list.remove(item)

    for item in resultList:
        itemstart = item[0]
        for b in temp_list:
            found_items = []
            if b.startswith(itemstart):
                found_items.append(b)
                if len(found_items) == 1:
                    temp_list.remove(found_items[0])
                    new_key = correctKey(key, item[1], found_items[0][1])
    return new_key


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
    tempkey = key
    if word != newWord:
        wordLen = len(word)
        counter = 0
        for counter in range(wordLen):
            if word[counter] != newWord[counter]:
                tempkey = correctKey(key, word[counter], newWord[counter])
    return tempkey

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
    key = countAllLetters(cyphertext)

    new_Text = replaceLettersByFrequence(cyphertext, key)
    ##### bis hier alles richtig !!!
    recognizedWordsInPercent(new_Text)

    key = getWordsByLengthOne(key,new_Text)

    new_Text = encrypt(cyphertext,key)

    recognizedWords = recognizedWordsInPercent(new_Text)

    while True:
      if recognizedWords> 40.0:
            print encrypt(cyphertext, key)
            print key 
            break;

      keyTemp = correctKeyBySpellChecker(new_Text, key)

      decriphedTemp = encrypt(cyphertext, keyTemp)
      recognizedWordsTemp = recognizedWordsInPercent(decriphedTemp)

      if recognizedWords < recognizedWordsTemp:
          key = keyTemp
          recognizedWords = recognizedWordsTemp

if __name__ == "__main__":
	main()
