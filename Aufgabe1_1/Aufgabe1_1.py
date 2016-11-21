import re, collections

englishLetterFreq = {'e': 12.70, 't': 9.06, 'a': 8.17, 'o': 7.51, 'i': 6.97, 'n': 6.75, 's': 6.33, 'h': 6.09, 'r': 5.99, 'd': 4.25, 'l': 4.03, 'c': 2.78,
 'u': 2.76, 'm': 2.41, 'w': 2.36, 'f': 2.23, 'g': 2.02, 'y': 1.97, 'p': 1.93, 'b': 1.29, 'v': 0.98, 'k': 0.77, 'j': 0.15, 'x': 0.15, 'q': 0.10, 'z': 0.07}

ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()

alphabet_small = LETTERS.lower()

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
#alphabet = LETTERS.lower()

def edits1(word):
    s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    #deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet_small if b]
    #inserts    = [a + c + b     for a, b in s for c in alphabet_small]
    #return set(deletes + transposes + replaces + inserts)
    return set(transposes + replaces)


def known_edits2(word):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

def known(words):
    return set(w for w in words if w in NWORDS)

def correct(word):
    candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
    #print (word, candidates)
    return max(candidates, key=NWORDS.get)


#################################
#End Spell-Checker
#################################

def countAllLetters(message):

    letterCount = {}
    for c in alphabet_small:
        letterCount[c] = 0

    all_Letters = 0

    for letter in message:
        if letter in alphabet_small:
            letterCount[letter] += 1
            all_Letters += 1

    for letter in letterCount:
        #calculate Percent
        valueInPercent = (letterCount[letter] * 100) / all_Letters
        letterCount[letter] = valueInPercent
    return sorted(letterCount, key=letterCount.get, reverse=True)

def generateDecryptKey(freq_Dict):
    decrypt_Dict = dict(zip(freq_Dict, englishLetterFreq))
    #decrypt_Dict = dict(zip(englishLetterFreq,freq_Dict))
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


def main():
    cyphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd.""".lower()
    print('Original Cyphertext: ')
    print(cyphertext)
    LetterDictByFrequence = countAllLetters(cyphertext)

    decrypt_key = generateDecryptKey(LetterDictByFrequence)
    print('Key with letter statistic: ')
    print(decrypt_key)

    new_Text = replaceLettersByFrequence(cyphertext, decrypt_key)
    print('Text after letter replacement: ')
    print(new_Text)

    Text_after_spell_checker = findWords(new_Text.lower())
    print('Text after Spell-Checker:')
    print(Text_after_spell_checker)

if __name__ == "__main__":
	main()
