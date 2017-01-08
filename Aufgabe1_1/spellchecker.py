import re, collections

alphabet_small = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()


#################################
#Start Spell-Checker from http://norvig.com/spell-correct.html
#################################

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

def correctWord(word, key):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    newWord = max(candidates, key=NWORDS.get)
    if word != newWord:
        print ("word to correct: ", word , newWord)
        wordLen = len(word)
        counter = 0

        for counter in range(wordLen):
            if word[counter] != newWord[counter]:
                print("substitution: ", word[counter], newWord[counter])
                key = correctKey(key, word[counter], newWord[counter])
                return key
    return False

# def correctKey(dictionary, letterA, letterB):
#     newKey_Dict = dictionary
#     if letterA in alphabet_small and letterB in alphabet_small:
#         print("Pair to swap: ", letterA," with ", letterB)
#         try:
#             tempKey1 = [key for key in newKey_Dict.items() if key[1] == letterA][0][0]
#             tempKey2 = [key for key in newKey_Dict.items() if key[1] == letterB][0][0]
#             dictionary[tempKey1] = letterB
#             dictionary[tempKey2] = letterA
#         except KeyError:
#             return dictionary
#     return dictionary

def correctKey(dictionary, letterOne, letterTwo):
    new_dict = dict(zip(dictionary.values(), dictionary.keys()))
    try:
        tempOne = new_dict[letterOne]
        tempTwo = new_dict[letterTwo]
        dictionary[tempOne] = letterTwo
        dictionary[tempTwo] = letterOne
    except KeyError:
        return dictionary
    return dictionary