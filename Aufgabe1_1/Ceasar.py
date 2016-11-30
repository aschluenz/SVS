import sys,random

def getRandomKey():
    abc = getAlphabetAsList()
    random.shuffle(abc)
    return abc

def getAlphabetAsList():
    return list(map(chr, range(ord('a'),ord('z')+1)))

def encrypt(text, keyDict):
    newtext = ''
    for c in text:
        try:
            newtext += keyDict[c]
        except KeyError:
            newtext += c
    return newtext

key = getRandomKey()
abc = getAlphabetAsList()
print ("key", key)
print ("abc", abc)

encryptKey = dict(zip(abc,key))
print encryptKey

file = open('alice.txt', 'r')
text = file.read().lower()

cyphertext = encrypt(text,encryptKey)

new_file = open('alice_encrypt.txt', 'w')
new_file.write(cyphertext)
new_file.close()
