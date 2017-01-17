import struct
"""
XTEA implementation CFB Mode
sources:
    http://jhafranco.com/2013/06/07/validation-of-an-aes-cfb-implementation-in-python/
    http://code.activestate.com/recipes/496737-python-xtea-encryption/
    https://en.wikipedia.org/wiki/XTEA
    http://code.activestate.com/recipes/496737-python-xtea-encryption/
"""
BLOCKSIZE = 8
DELTA = 0x9E3779B9L
MASK = 0xFFFFFFFFL
ROUNDS = 32

def xteaCfbEncrypt(data, key, rounds=ROUNDS, iv='\00\00\00\00\00\00\00\00'):
    cipherText = ''
    data = map(ord,data)

    for i in range(0,len(data)):
        xtea = encipher(iv,key,rounds)
        byte = chr(ord(xtea[0]) ^ data[i])
        iv = iv[1:] + byte
        cipherText += byte

    return cipherText

def xteaCfbDecrypt(data, key, rounds=ROUNDS, iv='\00\00\00\00\00\00\00\00'):
    plainText = ''
    data = map(ord,data)

    for i in range(0, len(data)):
        xtea = encipher(iv,key,rounds)
        byte = chr(ord(xtea[0]) ^ data[i])
        iv = iv[1:] + chr(data[i])
        plainText += byte

    return plainText

def encipher(data,key, rounds):

    v0,v1 = struct.unpack('!2L', data)
    k = struct.unpack('!4L', key)
    sum_ = 0

    for i in xrange(0,rounds):
        v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (sum_ + k[sum_ >> 11 & 3]))) & MASK
        sum_ = (sum_ - DELTA) & MASK
        v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (sum_ + k[sum_ & 3]))) & MASK

    return struct.pack('!2L', v0, v1)
